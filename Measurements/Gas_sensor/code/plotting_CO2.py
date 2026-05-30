import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt


path = "C:/Users/Home/Desktop/dschrobiltgen_Forest_FireDetection/ForestFireDetection/Measurements/Gas_Sensor/"
FILENAME = path + "data/CO2_measurements.txt"
SAMPLE_INTERVAL = 20
PHASE_DURATION = 1800

temperature = []
humidity = []
gas_resistance = []

with open(FILENAME, 'r') as f:
    for line in f:
        try:
            parts = line.strip().split('\t')

            temp = int(parts[0].split('=')[1])         # C*100
            hum = int(parts[2].split('=')[1])          # %*1000
            gas = float(parts[3].split('=')[1])        # ohms

            temperature.append(temp / 100.0)           # °C
            humidity.append(hum / 1000.0)              # %
            gas_resistance.append(gas / 1000.0)        # kOhms
            
        except (IndexError, ValueError) as e:
            continue

time_sec = [i * SAMPLE_INTERVAL for i in range(len(temperature))]


########################################################## first plot ################################################################
fig, ax1 = plt.subplots()

# Gas resistance
color1 = 'tab:green'
ax1.set_xlabel('Time [s]', fontsize=12)
ax1.xaxis.set_tick_params(labelsize=12)
ax1.set_ylabel(r'$R_{gas}$ [kΩ]', color=color1, fontsize=12)
ax1.plot(time_sec, gas_resistance, color=color1)
ax1.tick_params(axis='y', labelcolor=color1, labelsize=12)
ax1.set_ylim(100, 150)

# Humidity
ax2 = ax1.twinx()
color2 = 'tab:blue'
ax2.spines.right.set_position(("axes", 1.05))
ax2.set_ylabel('Humidity [%]', color=color2, fontsize=12)
ax2.plot(time_sec, humidity, color=color2, label='Humidity')
ax2.tick_params(axis='y', labelcolor=color2, labelsize=12)
ax2.set_ylim(36, 46)

# Temperature
ax3 = ax1.twinx()
color3 = 'tab:red'
ax3.spines.right.set_position(("axes", 1.12))
ax3.set_ylabel('Temperature [°C]', color=color3, fontsize=12)
ax3.plot(time_sec, temperature, color=color3, label='Temperature')
ax3.tick_params(axis='y', labelcolor=color3, labelsize=12)
ax3.set_ylim(22, 26)

# CO2
co2_concentration_phases = [0, 800, 0, 2000, 0, 2000, 0]
co2_concentration = []
for conc in co2_concentration_phases:
    steps = PHASE_DURATION // SAMPLE_INTERVAL
    co2_concentration.extend([conc] * steps)

co2_concentration = co2_concentration[:len(time_sec)]
time_sec1 = time_sec[:len(co2_concentration)]
ax4 = ax1.twinx()
color4 = 'tab:purple'
ax4.spines.left.set_position(("axes", -0.1))
ax4.yaxis.set_label_position("left")
ax4.yaxis.set_ticks_position("left")
ax4.set_ylabel('CO2 concentration [ppm]', color=color4, fontsize=12)
ax4.plot(time_sec1, co2_concentration, color=color4, linewidth=1.9, label='CO2 concentration')
ax4.tick_params(axis='y', labelcolor=color4, labelsize=12)
ax4.set_ylim(-100, 2500)

# Measurement phases
phases = [
    ("Stabilization", 'lightgray'),
    ("CO2 800 ppm", 'lightcoral'),
    ("Recovery (0 ppm)", 'lightgray'),
    ("CO2 2000 ppm", 'lightsalmon'),
    ("Recovery (0 ppm)", 'lightgray'),
    ("CO2 2000 ppm", 'lightsalmon'),
    ("Recovery (0 ppm)", 'lightgray'),
]

ylim = ax1.get_ylim()
y_levels = [0.08, 0.03]
for i, (label, color) in enumerate(phases):
    start = i * PHASE_DURATION
    end = (i + 1) * PHASE_DURATION
    ax1.axvspan(start, end, color=color, alpha=0.3)
    y_fraction = y_levels[i % len(y_levels)]
    y_text = ylim[0] + (ylim[1] - ylim[0]) * y_fraction

    ax1.text(
        (start + end) / 2, y_text,
        label,
        ha='center',
        va='bottom',
        fontsize=8,
        color='black',
        fontweight='bold',
        rotation=45,
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round,pad=0.2')
    )

plt.tight_layout()
plt.show()




########################################################## second plot ################################################################
fig, ax1 = plt.subplots()

# Gas resistance
color1 = 'tab:green'
ax1.set_xlabel('Time [s]', fontsize=12)
ax1.xaxis.set_tick_params(labelsize=12)
ax1.set_ylabel(r'$R_{gas}$ [kΩ]', color=color1, fontsize=12)
ax1.plot(time_sec, gas_resistance, color=color1)
ax1.tick_params(axis='y', labelcolor=color1, labelsize=12)
ax1.set_ylim(100, 150)

import numpy as np
from scipy.signal import butter, filtfilt

# filtering
fs = 1 / SAMPLE_INTERVAL
cutoff = 0.001
order = 2
b, a = butter(order, cutoff / (0.5 * fs), btype='low', analog=False)
gas_resistance_filtered = filtfilt(b, a, gas_resistance)
dr_gas_resistance_filtered = [0] + [1000 * (gas_resistance_filtered[i] - gas_resistance_filtered[i-1]) / SAMPLE_INTERVAL for i in range(1, len(gas_resistance_filtered))]


# Gas resistance derivative
ax5 = ax1.twinx()
color5 = 'tab:orange'
ax5.spines.right.set_position(("axes", 1))
ax5.set_ylabel(r'$d(R_{gas})/dt$ [Ω/s]', color=color5, fontsize=12)
ax5.plot(time_sec, dr_gas_resistance_filtered, color=color5)

ax5.axhline(y=0, color='tab:gray', linestyle='--', label='0 Ω/s')
ax5.legend(loc='upper left', fontsize=12)
ax5.tick_params(axis='y', labelcolor=color5, labelsize=12)
ax5.set_ylim(-60, 60)

# CO2
co2_concentration_phases = [0, 800, 0, 2000, 0, 2000, 0]
co2_concentration = []
for conc in co2_concentration_phases:
    steps = PHASE_DURATION // SAMPLE_INTERVAL
    co2_concentration.extend([conc] * steps)

co2_concentration = co2_concentration[:len(time_sec)]
time_sec1 = time_sec[:len(co2_concentration)]

ax4 = ax1.twinx()
color4 = 'tab:purple'
ax4.spines.left.set_position(("axes", -0.1))
ax4.yaxis.set_label_position("left")
ax4.yaxis.set_ticks_position("left")
ax4.set_ylabel('CO2 concentration [ppm]', color=color4, fontsize=12)
ax4.plot(time_sec1, co2_concentration, color=color4, linewidth=1.9, label='CO2 concentration')
ax4.tick_params(axis='y', labelcolor=color4, labelsize=12)
ax4.set_ylim(-100, 2500)

# Measurement phases
phases = [
    ("Stabilization", 'lightgray'),
    ("CO2 800 ppm", 'lightcoral'),
    ("Recovery (0 ppm)", 'lightgray'),
    ("CO2 2000 ppm", 'lightsalmon'),
    ("Recovery (0 ppm)", 'lightgray'),
    ("CO2 2000 ppm", 'lightsalmon'),
    ("Recovery (0 ppm)", 'lightgray'),
]
ylim = ax1.get_ylim()
y_levels = [0.08, 0.03]

for i, (label, color) in enumerate(phases):
    start = i * PHASE_DURATION
    end = (i + 1) * PHASE_DURATION
    ax1.axvspan(start, end, color=color, alpha=0.3)

    y_fraction = y_levels[i % len(y_levels)]
    y_text = ylim[0] + (ylim[1] - ylim[0]) * y_fraction

    ax1.text(
        (start + end) / 2, y_text,
        label,
        ha='center',
        va='bottom',
        fontsize=8,
        color='black',
        fontweight='bold',
        rotation=45,
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round,pad=0.2')
    )

plt.tight_layout()
plt.show()