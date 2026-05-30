import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

current_MCU = 1.01 #mA

T_target  = np.array([200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400])
currentV1_1 = np.array([10.75, 11.14, 11.57, 11.92, 12.235, 12.55, 12.838, 13.12, 13.45, 13.69, 13.94])
required_timeV1_1 = np.array([0.1256, 0.133, 0.137, 0.143, 0.1463, 0.151, 0.156, 0.159, 0.168, 0.169, 0.171])
currentV1_2 = np.array([10.79, 11.17, 11.63, 11.96, 12.275, 12.587, 12.89, 13.15, 13.48, 13.72, 13.97])
required_timeV1_2 = np.array([0.123, 0.131, 0.139, 0.143, 0.145, 0.155, 0.156, 0.164, 0.165, 0.170, 0.174])

average_current = (currentV1_1 + currentV1_2) / 2 - current_MCU
std_current = np.std([currentV1_1, currentV1_2], axis=0)

average_time_required = (required_timeV1_1 + required_timeV1_2) / 2 * 1000  # en ms
std_time = np.std([required_timeV1_1, required_timeV1_2], axis=0) * 1000

plt.figure()
plt.errorbar(T_target, average_current, yerr=std_current, fmt='o-', capsize=5)
plt.xlabel("Target temperature [°C]", fontsize=12)
plt.ylabel("Current [mA]", fontsize=12)
plt.grid()
plt.tight_layout()
plt.show()

plt.figure()
plt.errorbar(T_target, average_time_required, yerr=std_time, fmt='s-', capsize=5)
plt.xlabel("Target temperature [°C]", fontsize=12)
plt.ylabel("Required time [ms]", fontsize=12)
plt.grid()
plt.tight_layout()
plt.show()