import numpy as np
import matplotlib.pyplot as plt

E_Active = 5.790  # [mJ]

def E_inactive(lambda_):
    return 0.01551 * (lambda_ - 1.01)  # [mJ]

lambda_vals = np.logspace(np.log10(30), np.log10(7200), 500)  # [s]
P_avg = (E_Active + E_inactive(lambda_vals)) / lambda_vals  # [mW]

lambda_ticks = np.array([30, 60, 300, 600, 1800, 3600, 7200])
lambda_tick_labels = ['30 s', '1 min', '5 min', '10 min', '30 min', '1 h', '2 h']

y_ticks = [200, 100, 50, 30, 20]
y_tick_labels = [str(val) for val in y_ticks]

special_lambdas = np.array([60, 600, 3600])  # [s] = 1 min, 10 min, 30 min
special_P_avg = 1000*(E_Active + E_inactive(special_lambdas)) / special_lambdas

fig, ax = plt.subplots()
plt.loglog(lambda_vals, 1000*P_avg, label='P_avg(λ)')
ax.scatter(special_lambdas, special_P_avg, color='red', marker='o', s=50, label='Points clés')

for x, y in zip(special_lambdas, special_P_avg):
    ax.plot([0, x], [y, y], color='red', linestyle='--', linewidth=0.6)
    ax.plot([x, x], [y, min(P_avg)], color='red', linestyle='--', linewidth=0.6)
    ax.text(-0.01, y, f'{y:.1f}', transform=ax.get_yaxis_transform(),
            color='red', ha='right', va='center', fontsize=10, clip_on=False)


plt.xticks(lambda_ticks, lambda_tick_labels, fontsize=12)
plt.yticks(y_ticks, y_tick_labels, fontsize=12)
plt.ylim(13, 290)
plt.xlabel('λ', fontsize=13)
plt.ylabel(r'$P_{avg, \lambda}$ [$\mu$W]', fontsize=13)
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.tight_layout()
plt.show()