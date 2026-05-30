/*
 * my_sensor.c
 *
 *  Created on: Apr 23, 2025
 *      Author: Dorian
 */


#include "my_sensor.h"
#include "bme69x.h"
#include "main.h"



/* Variables */
struct bme69x_dev bme690_dev;
I2C_HandleTypeDef *my_hi2c;
static uint8_t dev_addr;
struct bme69x_conf conf;
struct bme69x_heatr_conf heatr_conf;
struct bme69x_data data;
uint8_t n_fields;


/**************************/
/*** INTERFACE FUNCTIONS***/
/**************************/
BME69X_INTF_RET_TYPE bme69x_i2c_read(uint8_t reg_addr, uint8_t *reg_data, uint32_t len, void *intf_ptr)
{
	if(HAL_I2C_Mem_Read(my_hi2c, *((uint16_t *)intf_ptr), reg_addr, 1, (uint8_t *) reg_data, len, HAL_MAX_DELAY) == HAL_OK) {return BME69X_OK;}
	else {return BME69X_E_COM_FAIL;}
}

BME69X_INTF_RET_TYPE bme69x_i2c_write(uint8_t reg_addr, const uint8_t *reg_data, uint32_t len, void *intf_ptr)
{
	if(HAL_I2C_Mem_Write(my_hi2c, *((uint16_t *)intf_ptr), reg_addr, 1, (uint8_t *) reg_data, len, HAL_MAX_DELAY) == HAL_OK) {return BME69X_OK;}
	else {return BME69X_E_COM_FAIL;}
}

void bme69x_delay_us(uint32_t period, void *intf_ptr)
{
	HAL_Delay(period/1000); 
}

static int8_t bme69x_interface_init(struct bme69x_dev *bme)
{
    int8_t rslt = BME69X_OK;
    if (bme != NULL) {
    	dev_addr = BME69X_I2C_ADDR_LOW<<1;
    	bme->read = &bme69x_i2c_read;
    	bme->write = &bme69x_i2c_write;
    	bme->intf = BME69X_I2C_INTF;
    	bme->delay_us = &bme69x_delay_us;
    	bme->intf_ptr = &dev_addr;
    	bme->amb_temp = 20; /* The ambient temperature in deg C is used for defining the heater temperature */
    }
    else{
        rslt = BME69X_E_NULL_PTR;
    }
    return rslt;
}
/**************************/


/*** Utilitary function to print error code ***/
void bme69x_check_rslt(const char* api_name, int8_t rslt)
{
#if(VERBOSE)
//	debug_print(api_name);
    switch (rslt)
    {
        case BME69X_OK:
        	debug_print(" : Success\r\n");
            break;
        case BME69X_E_NULL_PTR:
            debug_print(" : Null pointer\r\n");
            break;
        case BME69X_E_COM_FAIL:
        	debug_print(" : Communication failure\r\n");
            break;
        case BME69X_E_INVALID_LENGTH:
        	debug_print(" : Incorrect length parameter\r\n");
            break;
        case BME69X_E_DEV_NOT_FOUND:
        	debug_print(" : Device not found\r\n");
            break;
        case BME69X_E_SELF_TEST:
        	debug_print(" : Self test error\r\n");
            break;
        case BME69X_W_NO_NEW_DATA:
        	debug_print(" : No new data found\r\n");
            break;
        default:
        	debug_print(" : Unknown error code\r\n");
            break;
    }
#endif
}

void my_sensor_init(I2C_HandleTypeDef *hi2c, uint8_t perform_selftest)
{
	my_hi2c = hi2c;

	int8_t rslt;

	rslt = bme69x_interface_init(&bme690_dev);
	bme69x_check_rslt("BME690 interface init", rslt);

	rslt = bme69x_init(&bme690_dev);
	bme69x_check_rslt("BME690 init", rslt);

	if(perform_selftest) {
		//debug_print("BME690 selftest check begin...\r\n");
		rslt = bme69x_selftest_check(&bme690_dev);
		bme69x_check_rslt("BME690 selftest check", rslt);
	}

	conf.filter = FILTER;
	conf.odr = ODR;
	conf.os_hum  = OS_HUM;
	conf.os_pres = OS_PRES;
	conf.os_temp = OS_TEMP;
	rslt = bme69x_set_conf(&conf, &bme690_dev);
	bme69x_check_rslt("bme69x_set_conf", rslt);

#if(SENSE_GAS)
	heatr_conf.enable = BME69X_ENABLE;
	heatr_conf.heatr_temp = HEATR_TEMP;   // heater T° set to 300 °C
	heatr_conf.heatr_dur = HEATR_DUR;
	rslt = bme69x_set_heatr_conf(BME69X_FORCED_MODE, &heatr_conf, &bme690_dev);
	bme69x_check_rslt("bme69x_set_heatr_conf", rslt);
#else
	heatr_conf.enable = BME69X_DISABLE;
	rslt = bme69x_set_heatr_conf(BME69X_FORCED_MODE, &heatr_conf, &bme690_dev);1
	bme69x_check_rslt("bme69x_set_heatr_conf", rslt);
#endif

	rslt = bme69x_set_op_mode(BME69X_SLEEP_MODE, &bme690_dev);
	bme69x_check_rslt("bme69x_set_op_mode", rslt);
}

void print_data_bme(uint8_t n_fields){

	if (n_fields) {
#ifdef BME69X_USE_FPU
		APP_PRINTF("T [C*100]=%10.2f\tP [Pa]=%10.2f\tH [%%*1000]=%10.2f\tGasR [ohm]=%10.2f\tStatus=0x%02X\r\n",
		           data.temperature,
		           data.pressure,
		           data.humidity,
		           data.gas_resistance,
		           data.status);

#else
	    APP_PRINTF("T[C*100]=%d\tP[Pa]=%u\tH[%%*1000]=%u\tGasR[ohm]=%u\tStatus=0x%02X\r\n",
	               data.temperature,
	               data.pressure,
	               data.humidity,
	               data.gas_resistance,
	               data.status);
#endif
	}

}

struct bme69x_data *get_BME_data()
{
	int8_t rslt;
	uint32_t del_period;

	// activate the supply
	HAL_GPIO_WritePin(EN_LV_GPIO_Port, EN_LV_Pin, GPIO_PIN_SET);

	rslt = bme69x_set_op_mode(BME69X_FORCED_MODE, &bme690_dev);
	bme69x_check_rslt("bme69x_set_op_mode", rslt);

	/* Calculate delay period in microseconds */
#if(SENSE_GAS)
	del_period = bme69x_get_meas_dur(BME69X_FORCED_MODE, &conf, &bme690_dev) + (heatr_conf.heatr_dur * 1000);
#else
	del_period = bme69x_get_meas_dur(BME69X_FORCED_MODE, &conf, &bme690_dev);
#endif

	bme690_dev.delay_us(del_period, bme690_dev.intf_ptr);

	rslt = bme69x_get_data(BME69X_FORCED_MODE, &data, &n_fields, &bme690_dev);

	// deactivate the supply
	HAL_GPIO_WritePin(EN_LV_GPIO_Port, EN_LV_Pin, GPIO_PIN_RESET);

#if(VERBOSE)
	print_data_bme(n_fields);
#endif

	return &data;
}
