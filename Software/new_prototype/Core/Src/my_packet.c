/*
 * my_packet.c
 *
 *  Created on: Apr 28, 2025
 *      Author: Dorian
 */

#include "my_packet.h"
#include "bme69x_defs.h"
#include "radio.h"
#include "main.h"
#include "sys_app.h"

uint8_t packet_buffer[PAYLOAD_MAX_LENGTH];
uint8_t packet_length;
uint32_t mask = 0x000000FF;
uint32_t mask1 = 0x000000F0;
uint32_t mask2 = 0x0000000F;


#if(SEND_SYNC_PACKETS)
uint8_t sync_num = 1;
#endif

void make_packet(struct bme69x_data *bme_data)
{
	packet_length = 0;
	packet_buffer[packet_length++] = (uint8_t) SENDER_ID;

	packet_buffer[packet_length++] = (uint8_t) ((bme_data->temperature >> 8) & mask);
	packet_buffer[packet_length++] = (uint8_t) (bme_data->temperature & mask);
	packet_buffer[packet_length++] = (uint8_t) ((bme_data->humidity >> 12) & mask);
	packet_buffer[packet_length++] = (uint8_t) ((bme_data->humidity >> 4) & mask);
	packet_buffer[packet_length++] = (uint8_t) (((bme_data->humidity & mask2)<<4)|((bme_data->gas_resistance >> 16) & mask2));

#if(SENSE_GAS)
	packet_buffer[packet_length++] = (uint8_t) ((bme_data->gas_resistance >> 8) & mask);
	packet_buffer[packet_length++] = (uint8_t) (bme_data->gas_resistance & mask);
#endif

#if(USE_MAX_LENGTH)
	for(; packet_length < PAYLOAD_MAX_LENGTH;) {
		packet_buffer[packet_length++] = 0;
	}
#endif
}

void send_packet()
{
	APP_PRINTF("Sending %d bytes...\r\n", packet_length);
	if(Radio.Send(packet_buffer, packet_length)) {
//		debug_print("Send packet failed.\r\n");
	}
}

void send_dummy_packet()
{
	for(packet_length = 0; packet_length < PAYLOAD_MAX_LENGTH; ++packet_length) {
		packet_buffer[packet_length] = packet_length;
	}
	send_packet();
}


void decode_print_packet(uint8_t *payload, uint16_t size, int16_t rssi, int8_t LoraSnr_FskCfo)
{
	float rssi_f = -((float)rssi)/2;
	float snr_f = ((float)LoraSnr_FskCfo)/4;
	APP_PRINTF("PACKET RECEIVED --- RSSI = %d (%d.%d dBm)     SNR = %d (%d.%d dB)     SIZE=%d bytes\n                    PAYLOAD=0x",
			rssi,
			(int)(rssi_f),
			((int)(rssi_f*10))%10,
			LoraSnr_FskCfo,
			(int)(snr_f),
			((int)(snr_f*100))%100,
			size);
	for(uint16_t i = 0; i < size; ++i) {
		APP_PRINTF("%02x", payload[i]);
	}
	APP_PRINTF("\r\n");
#if(PRINT_PACKET_DECODED)
	if(size == PACKET_LENGTH) {
		uint8_t id = payload[0];
		uint16_t temp = (uint16_t) ((payload[1] << 8) | payload[2]);
		uint32_t press = (uint32_t) ((payload[3] << 24) | (payload[4] << 16) | (payload[5] << 8) | payload[6]);
		uint32_t hum = (uint32_t) ((payload[7] << 24) | (payload[8] << 16) | (payload[9] << 8) | payload[10]);
		if(SENSE_GAS){
			uint32_t gas = (uint32_t) ((payload[11] << 24) | (payload[12] << 16) | (payload[13] << 8) | payload[14]);
			APP_PRINTF("ID\t\tT [C*100]\t P [Pa]\t H [%%*1000]\t Gas R [ohm]\r\n")
			APP_PRINTF("%u\t\t%d\t\t %u\t\t %u\t\t %u\r\n", id, (int) temp, press, hum, gas);
		} else {
			APP_PRINTF("ID\t\tT [C*100]\t P [Pa]\t H [%%*1000]\r\n");
			APP_PRINTF("%u\t\t%d\t\t %u\t\t %u\r\n", id, (int) temp, press, hum);
		}
	}
#endif
}
