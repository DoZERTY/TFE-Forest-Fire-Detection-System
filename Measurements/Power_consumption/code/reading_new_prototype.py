import pandas as pd
import matplotlib.pyplot as plt

# Localisation des fichiers CSV
path = "C:/Users/Home/Desktop/dschrobiltgen_Forest_FireDetection/ForestFireDetection/Measurements/Power_consumption/data/new prototype/"
save_loc = path
duration = 150
fichier_csv1 = path + f"Meas_new_prototype_1V8.csv"
fichier_csv2 = path + f"Meas_new_prototype_3V3.csv"

df1 = pd.read_csv(fichier_csv1, sep=",", skiprows=12)
df2 = pd.read_csv(fichier_csv2, sep=",", skiprows=12)

###################### PARAMETERS ######################
save = False
voltage_input1 = 1.8
voltage_input2 = 3.3
shifting = True
margin = 0.1 
delta = 1 # ms

t0_1 = 14.545
t0_2 = 14.512
space = 0.1
sending_DUR = 1.13
radio_DUR = 0.048

t_0_data_acq = 111.5 + space*1000
t_1_data_acq = 304 + space*1000
t_0_packet = 890.5 + space*1000
t_1_packet = 922 + space*1000
t_0_send = 922 + space*1000
t_1_send = 1002.5 + space*1000

OSR_HUM = 8
OSR_PRES = 0
OSR_TEMP = 8
HEATR_DUR = 50 # [ms]
#######################################################

wake_up_DUR = 1  # [ms]
SW_duration = 0.477  # [ms]

T_DUR = wake_up_DUR + OSR_TEMP * 1.963 + SW_duration  # [ms]
H_DUR = OSR_HUM * 1.963 + SW_duration  # [ms]
G_DUR = HEATR_DUR*(1+margin) + 5 * 0.477 + SW_duration  # [ms]

Total_DUR = T_DUR + H_DUR + G_DUR  # [ms]

print("Total duration of the measurement: ", Total_DUR, "ms")

colonne_courant1 = 1000*df1.iloc[:, 0]
colonne_courant2 = 1000*df2.iloc[:, 0]

colonne_temps1 = 1000*df1.iloc[:, 20]  # ms
colonne_temps2 = 1000*df2.iloc[:, 20]  # ms

t0_1 *= 1000
t0_2 *= 1000
sending_DUR *= 1000
radio_DUR *= 1000
space *= 1000

plt.figure(figsize=(12, 6))

if shifting:
    plt.plot(
        colonne_temps1[(colonne_temps1 > t0_1 - space) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR + space)] - t0_1 + space,
        voltage_input1 * colonne_courant1[(colonne_temps1 > t0_1 - space) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR + space)],
        label=f"Supply voltage = 1.8V",
    )

    plt.plot(
        colonne_temps2[(colonne_temps2 > t0_2 - space) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR + space)] - t0_2 + space,
        voltage_input2 * colonne_courant2[(colonne_temps2 > t0_2 - space) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR + space)],
        label=f"Supply voltage = {voltage_input2}V",
    )
else:
    plt.plot(
        colonne_temps1,
        voltage_input1 * colonne_courant1,
        label=f"Supply voltage = 1.8V",
    )

    plt.plot(
        colonne_temps2,
        voltage_input2 * colonne_courant2,
        label=f"Supply voltage = {voltage_input2}V",
    )
t0 = space
plt.axvspan(t_0_data_acq, t_1_data_acq, color='green', alpha=0.15, label= "Data acquisition")
plt.axvspan(t_0_packet, t_1_packet, color='blue', alpha=0.15, label="Packetizing")
plt.axvspan(t_0_send, t_1_send, color='red', alpha=0.15, label="Radio transmission")

plt.xlabel("Time [ms]", fontsize=13)
plt.ylabel("Power [mW]", fontsize=13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
if shifting:
    plt.ylim(-4, 85)
    plt.xlim(0, 1200)
plt.grid(True)
plt.legend(loc='upper left', fontsize=12)
plt.show()


plt.figure(figsize=(12, 6))

if shifting:
    plt.plot(
        colonne_temps1[(colonne_temps1 > t0_1 - space) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR + space)] - t0_1 + space,
        colonne_courant1[(colonne_temps1 > t0_1 - space) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR + space)],
        label=f"Supply voltage = 1.8V",
    )

    plt.plot(
        colonne_temps2[(colonne_temps2 > t0_2 - space) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR + space)] - t0_2 + space,
        colonne_courant2[(colonne_temps2 > t0_2 - space) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR + space)],
        label=f"Supply voltage = {voltage_input2}V",
    )
else:
    plt.plot(
        colonne_temps1,
        colonne_courant1,
        label=f"Supply voltage = 1.8V",
    )

    plt.plot(
        colonne_temps2,
        colonne_courant2,
        label=f"Supply voltage = {voltage_input2}V",
    )
t0 = space
plt.axvspan(t_0_data_acq, t_1_data_acq, color='green', alpha=0.15, label= "Data acquisition")
plt.axvspan(t_0_packet, t_1_packet, color='blue', alpha=0.15, label="Packetizing")
plt.axvspan(t_0_send, t_1_send, color='red', alpha=0.15, label="Radio transmission")

plt.xlabel("Time [ms]", fontsize=13)
plt.ylabel("Current [mA]", fontsize=13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
if shifting:
    plt.ylim(-1, 43)
    plt.xlim(0, 1200)
plt.grid(True)
plt.legend(loc='upper left', fontsize=12)
plt.show()