import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

frequencies_mhz = np.array([0.1, 0.2, 0.4, 0.8, 1, 2, 4, 8, 16, 24, 32, 48])
currents_ua = np.array([0.6, 0.8, 1.2, 1.9, 4.7, 6.5, 11, 18.5, 62, 85, 110, 155])
currents_max = np.array([1, 1.2, 1.7, 2.5, 6, 9, 15, 25, 80, 110, 130, 190])
frequencies_labels = np.delete(frequencies_mhz, [3, 9])

plt.figure()
plt.plot(frequencies_mhz, currents_ua, marker='o', linestyle='-', label='Typical')
plt.plot(frequencies_mhz, currents_max, marker='o', linestyle='-', label='Maximum')

plt.xscale('log')
plt.yscale('log')

xtick_labels = [str(int(f)) if f.is_integer() else str(f) for f in frequencies_labels]
plt.xticks(frequencies_labels, labels=xtick_labels, fontsize=12)
plt.yticks([1, 10, 100], labels=['1', '10', '100'], fontsize=12)
plt.gca().yaxis.set_major_formatter(ScalarFormatter())

plt.xlabel('Frequency [MHz]', fontsize=13)
plt.ylabel('Current consumption [µA]', fontsize=13)
plt.legend(fontsize=12)
plt.grid(True, which="major", linestyle="--", linewidth=0.5)
plt.show()