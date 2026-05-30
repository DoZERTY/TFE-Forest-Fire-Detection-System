import matplotlib.pyplot as plt
import numpy as np

save = False

error = np.loadtxt('error.txt', delimiter=',')

max_error = np.max(error[:,0]) + 2

plt.fill_betweenx([0, max_error], 0, 5, color='green', alpha=0.3, label='Low risk')
plt.fill_betweenx([0, max_error], 5, 10, color='yellow', alpha=0.3, label='Moderate risk')
plt.fill_betweenx([0, max_error], 10, 20, color='orange', alpha=0.3, label='High risk')
plt.fill_betweenx([0, max_error], 20, 30, color='red', alpha=0.3, label='Very high risk')
plt.fill_betweenx([0, max_error], 30, 60, color='purple', alpha=0.3, label='Extreme risk')

plt.legend(fontsize = 13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.plot(error[:,1], error[:,0], 'o')
plt.xlabel('Expected FWI value', fontsize=14)
plt.ylabel('Error', fontsize=14)
plt.ylim(0, 4)
plt.xlim(0, 52)
plt.grid()
if save:
    plt.savefig('../../plot/error_vs_expectedFWI.pdf')
plt.show()



plt.hist(error[:,0], bins=10)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Error', fontsize=14)
plt.ylabel('Nb of occurences', fontsize=14)
plt.grid()
if save:
    plt.savefig('../../plot/error_distribution.pdf')
plt.show()