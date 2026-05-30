import matplotlib.pyplot as plt
import numpy as np

nb_of_sensors = 80

categories = ['Silvanet n°1', 'Silvanet n°2', 'New prototype']
production = [102.21, 102.21, 65.41]
distribution = [4.07, 4.07, 4.07]
use_phase = [4.12, 4.12, 4.12]
energy_source = [43.35, 64.31, 20.19]

production = [val / nb_of_sensors for val in production]
distribution = [val / nb_of_sensors for val in distribution]
use_phase = [val / nb_of_sensors for val in use_phase]
energy_source = [val / nb_of_sensors for val in energy_source]

for i in range(len(categories)):
    print(f"{categories[i]}: {production[i]:.2f} kg CO2 eq. (Sensor production), {distribution[i]:.2f} kg CO2 eq. (Distribution), {use_phase[i]:.2f} kg CO2 eq. (Use phase), {energy_source[i]:.2f} kg CO2 eq. (Energy source)")

bar_width = 0.5
x = np.arange(len(categories))

colors = {
    'Sensor production': "#5893F1",
    'Distribution': "#80E0F8F1",
    'Use phase': "#FBCB8F",
    'Energy source': "#F67A3B"
}

fig, ax = plt.subplots()
ax.bar(x, production, bar_width, label='Sensor production', color=colors['Sensor production'])
ax.bar(x, distribution, bar_width, bottom=production, label='Distribution', color=colors['Distribution'])
ax.bar(x, use_phase, bar_width, bottom=np.array(distribution)+np.array(production), label='Use phase', color=colors['Use phase'])
ax.bar(x, energy_source, bar_width, bottom=np.array(distribution)+np.array(production)+np.array(use_phase), label='Energy source', color=colors['Energy source'])

ax.set_ylabel(r'GWP [kg CO$_2$ eq.]', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)
ax.legend(loc='upper right')
ax.set_ylim(0, 2.8)

for i in range(len(categories)):
    total = production[i] + distribution[i] + use_phase[i] + energy_source[i]
    total = round(total, 2)
    ax.text(i, total+0.05, str(total), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()