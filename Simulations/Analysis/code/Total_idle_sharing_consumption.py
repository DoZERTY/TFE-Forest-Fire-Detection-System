import matplotlib.pyplot as plt
import numpy as np

categories = ['Typical', 'Maximum', 'Measured']
rf_switch = [100, 180, 0]
cpu = [1, 2.8, 0]
sensor = [0.15, 1, 0]
radio = [0.14, 0.14, 0]
clock_source = [0.36, 0.36, 0]
meas = [0, 0, 113]

bar_width = 0.5
x = np.arange(len(categories))
colors = {
    'CPU': '#6BAED6',
    'RF switch': '#FD8D3C',
    'Sensor': '#74C476',
    'Radio': '#F08080',
    'Clock source': '#D2A679',
}

fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 0.2]})

pos1 = ax_top.get_position()
pos2 = ax_bottom.get_position()

ax_top.set_position([pos1.x0, pos1.y0 + 0.012, pos1.width, pos1.height])
ax_bottom.set_position([pos2.x0, pos2.y0 - 0.02, pos2.width, pos2.height])

ax_top.set_ylim(90, 200)
ax_bottom.set_ylim(0, 27) 
ax_bottom.set_yticks([0, 20])

for ax in (ax_top, ax_bottom):
    ax.bar(x, rf_switch, bar_width, label='RF switch', color=colors['RF switch'])
    ax.bar(x, cpu, bar_width, bottom=rf_switch, label='CPU', color=colors['CPU'])
    ax.bar(x, sensor, bar_width, bottom=np.array(cpu)+np.array(rf_switch), label='BME680', color=colors['Sensor'])
    ax.bar(x, radio, bar_width, bottom=np.array(cpu)+np.array(rf_switch)+np.array(sensor), label='Radio', color=colors['Radio'])
    ax.bar(x, clock_source, bar_width, bottom=np.array(cpu)+np.array(rf_switch)+np.array(sensor)+np.array(radio), label='Clock sources', color=colors['Clock source'])
    ax.bar(x, meas, bar_width, color='lightgray', zorder=3)

ax_top.spines['bottom'].set_visible(False)
ax_bottom.spines['top'].set_visible(False)
ax_top.tick_params(labeltop=False)
ax_top.tick_params(axis='x', which='both', bottom=False, top=False)
ax_bottom.xaxis.tick_bottom()

d = .02
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False, linewidth=1.5)
ax.plot([-d, +d], [1.12, 1.22], **kwargs)
ax.plot([-d, +d], [0.95, 1.05], **kwargs)
ax.plot([1-d, 1+d], [1.12, 1.22], **kwargs)
ax.plot([1-d, 1+d], [0.95, 1.05], **kwargs)

ax_top.set_ylabel(r'Current consumption [$\mu$A]', fontsize=12)
ax_bottom.set_xticks(x)
ax_bottom.set_xticklabels(categories, fontsize=12)
ax_top.legend(loc='upper left')
plt.tight_layout()

for i in range(len(categories)):
    total = rf_switch[i] + cpu[i] + sensor[i] + radio[i] + clock_source[i] + meas[i]
    total = round(total, 2)   # round to 2 decimal places
    ax_top.text(i, total + 2, str(total) + r" $\mu$A", ha='center', va='bottom', fontsize=10)
plt.show()





# Final cosnumption
categories = ['Typical', 'Maximum', 'Measured']
rf_switch = [0, 0, 0]
cpu = [1, 2.8, 0]
sensor = [0.11, 0.14, 0]
radio = [0.14, 0.14, 0]
clock_source = [0.36, 0.36, 0]
meas = [0, 0, 4.7]

bar_width = 0.5
x = np.arange(len(categories))
colors = {
    'CPU': '#6BAED6',
    'RF switch': '#FD8D3C',
    'Sensor': '#74C476',
    'Radio': '#F08080',
    'Clock source': '#D2A679',
}

fig, ax = plt.subplots()

ax.bar(x, rf_switch, bar_width, label='RF switch', color=colors['RF switch'])
ax.bar(x, cpu, bar_width, bottom=rf_switch, label='CPU', color=colors['CPU'])
ax.bar(x, sensor, bar_width, bottom=np.array(cpu)+np.array(rf_switch), label='BME690', color=colors['Sensor'])
ax.bar(x, radio, bar_width, bottom=np.array(cpu)+np.array(rf_switch)+np.array(sensor), label='Radio', color=colors['Radio'])
ax.bar(x, clock_source, bar_width, bottom=np.array(cpu)+np.array(rf_switch)+np.array(sensor)+np.array(radio), label='Clock sources', color=colors['Clock source'])
ax.bar(x, meas, bar_width, color='lightgray', zorder=3)

ax.set_ylabel(r'Current consumption [$\mu$A]', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)
ax.legend(loc='upper left')
ax.set_ylim(0, 6)

for i in range(len(categories)):
    total = rf_switch[i] + cpu[i] + sensor[i] + radio[i] + clock_source[i] + meas[i]
    total = round(total, 2)
    ax.text(i, total+0.05, str(total) + r" $\mu$A", ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()