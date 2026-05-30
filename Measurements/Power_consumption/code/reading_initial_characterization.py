import pandas as pd
import matplotlib.pyplot as plt

path = "C:/Users/Home/Desktop/dschrobiltgen_Forest_FireDetection/ForestFireDetection/Measurements/Power_consumption/data/initial prototype/initial/"

save_loc = path
freq = 4
fichier_csv1 = path + f"initial_prototype_1V8_{freq}MHz.csv"
fichier_csv2 = path + f"initial_prototype_3V3_{freq}MHz.csv"

df1 = pd.read_csv(fichier_csv1, sep=",", skiprows=7)
df2 = pd.read_csv(fichier_csv2, sep=",", skiprows=7)

###################### PARAMETERS ######################
save = False
shifting = True
margin = 0.1 
delta = 1

t0_1 = 15.597
t0_2 = 17.634
space = 0.02
sending_DUR = 0.063
radio_DUR = 0.048

OSR_HUM = 8
OSR_PRES = 8
OSR_TEMP = 8
HEATR_DUR = 50 # [ms]
#######################################################

wake_up_DUR = 1  # [ms]
SW_duration = 0.477  # [ms]

T_DUR = wake_up_DUR + OSR_TEMP * 1.963 + SW_duration  # [ms]
P_DUR = OSR_PRES * 1.963 + SW_duration  # [ms]
H_DUR = OSR_HUM * 1.963 + SW_duration  # [ms]
G_DUR = HEATR_DUR*(1+margin) + 5 * 0.477 + SW_duration  # [ms]

Total_DUR = T_DUR + P_DUR + H_DUR + G_DUR  # [ms]


print("Total duration of the measurement: ", Total_DUR, "ms")

colonne_courant1 = 1000*df1.iloc[:, 1]
colonne_courant2 = 1000*df2.iloc[:, 1]

df1["DateTime"] = pd.to_datetime(
     df1["Time"], format="%H:%M:%S"
) + pd.to_timedelta(df1["Fractional Seconds"], unit="s")

df1["Relative Time (s)"] = (df1["DateTime"] - df1["DateTime"].iloc[0]).dt.total_seconds()
colonne_temps1 = df1["Relative Time (s)"]

df2["DateTime"] = pd.to_datetime(
        df2["Time"], format="%H:%M:%S"
    ) + pd.to_timedelta(df2["Fractional Seconds"], unit="s")

df2["Relative Time (s)"] = (df2["DateTime"] - df2["DateTime"].iloc[0]).dt.total_seconds()
colonne_temps2 = df2["Relative Time (s)"]

colonne_temps1 *= 1000
colonne_temps2 *= 1000
t0_1 *= 1000
t0_2 *= 1000
sending_DUR *= 1000
radio_DUR *= 1000
space *= 1000


plt.figure(figsize=(12, 6))

if shifting:
    plt.plot(
        colonne_temps1[(colonne_temps1 > t0_1 - space) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR + space)] - t0_1 + space,
        1.9 * colonne_courant1[(colonne_temps1 > t0_1 - space) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR + space)],
        label=f"Supply voltage = 1.8V",
    )

    plt.plot(
        colonne_temps2[(colonne_temps2 > t0_2 - space) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR + space)] - t0_2 + space,
        3.3 * colonne_courant2[(colonne_temps2 > t0_2 - space) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR + space)],
        label=f"Supply voltage = 3.3V",
    )
else:
    plt.plot(
        colonne_temps1,
        1.9 * colonne_courant1,
        label=f"Supply voltage = 1.8V",
    )

    plt.plot(
        colonne_temps2,
        3.3 * colonne_courant2,
        label=f"Supply voltage = 3.3V",
    )
t0 = space
plt.axvspan(t0, t0 + Total_DUR, color='green', alpha=0.15, label= "Data acquisition")
plt.axvspan(t0 + Total_DUR, t0 + Total_DUR + sending_DUR - radio_DUR, color='blue', alpha=0.15, label="Packetizing")
plt.axvspan(t0 + Total_DUR + sending_DUR - radio_DUR, t0 + Total_DUR + sending_DUR, color='red', alpha=0.15, label="Radio transmission")

plt.text(2, -1, f"{1.8 * (colonne_courant1[(colonne_temps1 > t0_1 - t0) & (colonne_temps1 < t0_1)]).mean():.2f}mW", fontsize=10, color='black')
plt.text(t0 + 0.1*T_DUR, -1, f"{1.8 * (colonne_courant1[(colonne_temps1 > t0_1 + delta) & (colonne_temps1 < t0_1 + T_DUR - delta)]).mean():.2f}mW", fontsize=10, color='black')
plt.text(t0 + T_DUR + 0.1*P_DUR, -1, f"{1.8 * (colonne_courant1[(colonne_temps1 > t0_1 + T_DUR + delta) & (colonne_temps1 < t0_1 + T_DUR + P_DUR - delta)]).mean():.2f}mW", fontsize=10, color='black')
plt.text(t0 + T_DUR + P_DUR + 0.1*H_DUR, -1, f"{1.8 * (colonne_courant1[(colonne_temps1 > t0_1 + T_DUR + P_DUR + delta) & (colonne_temps1 < t0_1 + T_DUR + P_DUR + H_DUR - delta)]).mean():.2f}mW", fontsize=10, color='black')
plt.text(t0 + T_DUR + P_DUR + H_DUR + 0.4*G_DUR, 20, f"{1.8 * (colonne_courant1[(colonne_temps1 > t0_1 + T_DUR + P_DUR + H_DUR + 4*delta) & (colonne_temps1 < t0_1 + T_DUR + P_DUR + H_DUR + G_DUR - 4*delta)]).mean():.2f}mW", fontsize=10, color='black')

# print("\n Values for 1.8V:")
# energy_acquisition = 1.8 * (colonne_courant1[(colonne_temps1 > t0_1 + delta) & (colonne_temps1 < t0_1 + Total_DUR - delta)]).mean() * Total_DUR / 1000
# energy_packetizing = 1.8 * (colonne_courant1[(colonne_temps1 > t0_1 + Total_DUR + delta) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR - radio_DUR - delta)]).mean() * (sending_DUR - radio_DUR) / 1000
# energy_sending = 1.8 * (colonne_courant1[(colonne_temps1 > t0_1 + Total_DUR + sending_DUR - radio_DUR + delta) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR - delta)]).mean() * radio_DUR / 1000
# energy_total = energy_acquisition + energy_packetizing + energy_sending
# print(f"Energy consumption for data acquisition: {energy_acquisition:.2f} mJ")
# print(f"Energy consumption for packetizing: {energy_packetizing:.2f} mJ")
# print(f"Energy consumption for sending: {energy_sending:.2f} mJ")
# print(f"Total energy consumption: {energy_total:.2f} mJ")

# print("\n Values for 3.3V:")
# energy_acquisition = 3.3 * (colonne_courant2[(colonne_temps2 > t0_2 + delta) & (colonne_temps2 < t0_2 + Total_DUR - delta)]).mean() * Total_DUR / 1000
# energy_packetizing = 3.3 * (colonne_courant2[(colonne_temps2 > t0_2 + Total_DUR + delta) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR - radio_DUR - delta)]).mean() * (sending_DUR - radio_DUR) / 1000
# energy_sending = 3.3 * (colonne_courant2[(colonne_temps2 > t0_2 + Total_DUR + sending_DUR - radio_DUR + delta) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR - delta)]).mean() * radio_DUR / 1000
# energy_total = energy_acquisition + energy_packetizing + energy_sending
# print(f"Energy consumption for data acquisition: {energy_acquisition:.2f} mJ")
# print(f"Energy consumption for packetizing: {energy_packetizing:.2f} mJ")
# print(f"Energy consumption for sending: {energy_sending:.2f} mJ")
# print(f"Total energy consumption: {energy_total:.2f} mJ")


plt.text(t0 + Total_DUR + sending_DUR - 0.65*radio_DUR, 75, f"{1.8 * (colonne_courant1[(colonne_temps1 > t0_1 + Total_DUR + sending_DUR - radio_DUR + delta) & (colonne_temps1 < t0_1 + Total_DUR + sending_DUR - delta)]).mean():.2f}mW", fontsize=10, color='black')

plt.text(2, 8, f"{3.3 * (colonne_courant2[(colonne_temps2 > t0_2 - t0) & (colonne_temps2 < t0_2)]).mean():.2f}mW", fontsize=10, color='black')
plt.text(t0 + 0.1*T_DUR, 12, f"{3.3 * (colonne_courant2[(colonne_temps2 > t0_2 + delta) & (colonne_temps2 < t0_2 + T_DUR - delta)]).mean():.2f}mW", fontsize=10, color='black')
plt.text(t0 + T_DUR + 0.1*P_DUR, 12, f"{3.3 * (colonne_courant2[(colonne_temps2 > t0_2 + T_DUR + delta) & (colonne_temps2 < t0_2 + T_DUR + P_DUR - delta)]).mean():.2f}mW", fontsize=10, color='black')
plt.text(t0 + T_DUR + P_DUR + 0.1*H_DUR, 12, f"{3.3 * (colonne_courant2[(colonne_temps2 > t0_2 + T_DUR + P_DUR + delta) & (colonne_temps2 < t0_2 + T_DUR + P_DUR + H_DUR - delta)]).mean():.2f}mW", fontsize=10, color='black')
plt.text(t0 + T_DUR + P_DUR + H_DUR + 0.4*G_DUR, 47, f"{3.3 * (colonne_courant2[(colonne_temps2 > t0_2 + T_DUR + P_DUR + H_DUR + 4*delta) & (colonne_temps2 < t0_2 + T_DUR + P_DUR + H_DUR + G_DUR - 4*delta)]).mean():.2f}mW", fontsize=10, color='black')

plt.text(t0 + Total_DUR + sending_DUR - 0.65*radio_DUR, 85, f"{3.3 * (colonne_courant2[(colonne_temps2 > t0_2 + Total_DUR + sending_DUR - radio_DUR + delta) & (colonne_temps2 < t0_2 + Total_DUR + sending_DUR - delta)]).mean():.2f}mW", fontsize=10, color='black')


plt.xlabel("Time [ms]", fontsize=13)
plt.ylabel("Power [mW]", fontsize=13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(-4, 100)
plt.grid(True)
plt.legend(loc='upper left', fontsize=12)


plt.figure(figsize=(12, 6))

if shifting:
    plt.plot(
        colonne_temps1[(colonne_temps1 > t0_1 - space) & (colonne_temps1 < t0_1 + Total_DUR + space)] - t0_1 + space,
        colonne_courant1[(colonne_temps1 > t0_1 - space) & (colonne_temps1 < t0_1 + Total_DUR + space)],
        label=f"Supply voltage = 1.8V",
    )
    plt.plot(
        colonne_temps2[(colonne_temps2 > t0_2 - space) & (colonne_temps2 < t0_2 + Total_DUR + space)] - t0_2 + space,
        colonne_courant2[(colonne_temps2 > t0_2 - space) & (colonne_temps2 < t0_2 + Total_DUR + space)],
        label=f"Supply voltage = 3.3V",
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
        label=f"Supply voltage = 3.3V",
    )
t0 = space + 2
T_DUR *= 1.02
P_DUR *= 1.02
H_DUR *= 1.02
G_DUR = 0.93*G_DUR
plt.axvspan(t0, t0 + T_DUR, color='yellowgreen', alpha=0.25, label= "Temperature")
plt.axvspan(t0 + T_DUR, t0 + T_DUR + P_DUR, color='tomato', alpha=0.25, label="Pressure")
plt.axvspan(t0 + T_DUR + P_DUR, t0 + T_DUR + P_DUR + H_DUR, color='cyan', alpha=0.25, label="Relative humidity")
plt.axvspan(t0 + T_DUR + P_DUR + H_DUR, t0 + T_DUR + P_DUR + H_DUR + G_DUR, color='magenta', alpha=0.25, label="Gas resitance")

plt.xlabel("Time [ms]", fontsize=13)
plt.ylabel("Current [mA]", fontsize=13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlim(right = 135)
plt.ylim(-1, 21)
plt.grid(True)
plt.legend(loc='upper left', fontsize=12)
plt.show()