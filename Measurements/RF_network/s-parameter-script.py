import skrf as rf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

path = "C:/Users/Home/Desktop/dschrobiltgen_Forest_FireDetection/ForestFireDetection/Measurements/RF_network/data/"

Dut_cap_v2 = rf.Network(path + 'v2_meas.s1p')
Dut_cap_v1 = rf.Network(path + 'v1_meas.s1p')
data_v1 = np.loadtxt(path + 'v1_meas.s1p',comments='!', skiprows=24)
data_v2= np.loadtxt(path + 'v2_meas.s1p',comments='!', skiprows=24)
Thru_v1 = np.loadtxt(path + 'v1_thru.s2p',comments='!', skiprows=24)
Thru_v2 = np.loadtxt(path + 'v2_thru.s2p',comments='!', skiprows=24)
Z0 = 50
Y0 = 1/Z0
target_freq = 868e6

idx_v1 = np.argmin(np.abs(Dut_cap_v1.f - target_freq))
idx_v2 = np.argmin(np.abs(Dut_cap_v2.f - target_freq))
s11_v1 = Dut_cap_v1.s[idx_v1, 0, 0]
s11_v2 = Dut_cap_v2.s[idx_v2, 0, 0]
z_v1 = Dut_cap_v1.z[idx_v1, 0, 0]
z_v2 = Dut_cap_v2.z[idx_v2, 0, 0]

z_str_v1 = f"{z_v1.real:.1f} {'+' if z_v1.imag >= 0 else '-'} j{abs(z_v1.imag):.1f} Ω"
z_str_v2 = f"{z_v2.real:.1f} {'+' if z_v2.imag >= 0 else '-'} j{abs(z_v2.imag):.1f} Ω"

fig, ax = plt.subplots()
Dut_cap_v1.plot_s_smith(ax=ax, label='PCB V1')
ax.plot(s11_v1.real, s11_v1.imag, 'rx', markersize=15, label= z_str_v1 + ' at 868 MHz (V1)', color='green')
Dut_cap_v2.plot_s_smith(ax=ax, label='PCB V2')
ax.plot(s11_v2.real, s11_v2.imag, 'rx', markersize=15, label= z_str_v2 + ' at 868 MHz (V2)', color='red')

plt.legend(loc='upper left', bbox_to_anchor=(-0.3, 1.0))
plt.show()


freq_v1 = data_v1[:,0]
freq_v2 = data_v2[:,0]

S11_real_v1 = data_v1[:,1]
S11_imag_v1 = data_v1[:,2]
S11_real_v2 = data_v2[:,1]
S11_imag_v2 = data_v2[:,2]

S11_data_v1 = S11_real_v1 + 1j*S11_imag_v1
S11_data_v2 = S11_real_v2 + 1j*S11_imag_v2

carrier_freq = 868
BW = 0.125

plt.figure()
plt.axvspan(carrier_freq - BW/2, carrier_freq + BW/2, color='gray', alpha=0.5, label='Frequency band \nused')
plt.plot(1000*freq_v1, 20*np.log10(np.abs(S11_data_v1)), label='PCB V1')
plt.plot(1000*freq_v2, 20*np.log10(np.abs(S11_data_v2)), label='PCB V2')
plt.xlabel('Frequency [MHz]')
plt.ylabel('S11 [dB]')
plt.xlim(800, 1000)
plt.legend()
plt.grid()


Thru_real_v1 = Thru_v1[:,3]
Thru_imag_v1 = Thru_v1[:,4]
Thru_real_v2 = Thru_v2[:,3]
Thru_imag_v2 = Thru_v2[:,4]

Thru_data_v1 = Thru_real_v1 + 1j*Thru_imag_v1
Thru_data_v2 = Thru_real_v2 + 1j*Thru_imag_v2
carrier_freq = 868
BW = 0.125

plt.figure()
plt.axvspan(carrier_freq - BW/2, carrier_freq + BW/2, color='gray', alpha=0.5, label='Frequency band \nused')
plt.plot(1000*Thru_v1[:,0], 20*np.log10(np.abs(Thru_data_v1)), label='PCB V1')
plt.plot(1000*Thru_v2[:,0], 20*np.log10(np.abs(Thru_data_v2)), label='PCB V2')

plt.xlabel('Frequency [MHz]')
plt.ylabel('S21 [dB]')
plt.xlim(800, 1000)
plt.legend()
plt.grid()
plt.show()




#########  V2  #########
print("\n\n      V2: \n")
beta_SMA = 26.344  # en rad/m
beta_line = 33.38  # en rad/m

L_SMA = 0.007  # SMA length
L_line = 0.06  # length line

alpha_SMA_db = 0.029
alpha_line_db = 0.174

alpha_SMA_db_per_m = alpha_SMA_db / L_SMA  # conversion dB/m
alpha_line_db_per_m = alpha_line_db / L_line  # conversion dB/m

# Conversion of coefficients to Neper/m
alpha_SMA = alpha_SMA_db_per_m / 8.686
alpha_line = alpha_line_db_per_m / 8.686


def compute_ZL(Zin, Z0, gamma, L):
    tanh_gammaL = np.tanh(gamma * L)
    num = (Zin - Z0 * tanh_gammaL)
    den = (Z0 - Zin * tanh_gammaL)
    ZL = Z0 * (num / den)
    return ZL

Z_in = 160.6 + 1j * 12.7
Z_int = compute_ZL(Z_in, Z0, alpha_SMA + 1j*beta_SMA, L_SMA)
Z_A_1C = compute_ZL(Z_int, Z0, alpha_line + 1j*beta_line, L_line)



#########  V1  #########
print("\n\n      V1: \n")
L_line = 0.075  # length line

alpha_SMA_db = 0.029
alpha_line_db = 0.2173

alpha_SMA_db_per_m = alpha_SMA_db / L_SMA  # conversion dB/m
alpha_line_db_per_m = alpha_line_db / L_line  # conversion dB/m

alpha_SMA = alpha_SMA_db_per_m / 8.686
alpha_line = alpha_line_db_per_m / 8.686



Z_in = 38.2 - 1j * 44
Z_int = compute_ZL(Z_in, Z0, alpha_SMA + 1j*beta_SMA, L_SMA)
Z_A_1C = compute_ZL(Z_int, Z0, alpha_line + 1j*beta_line, L_line)




#############################################   Towards generator    #########################################################
def compute_ZG(ZL, Z0, gamma, L):
    tanh_gammaL = np.tanh(gamma * L)
    num = (ZL + Z0 * tanh_gammaL)
    den = (Z0 + ZL * tanh_gammaL)
    ZG = Z0 * (num / den)
    return ZG

initial_prot = 42.48 + 1j * 64.87
new_prot = 33.25 - 1j * 98.58

Z_G_inital = compute_ZG(initial_prot, Z0, alpha_SMA + 1j*beta_SMA, L_SMA)
Z_G_new = compute_ZG(new_prot, Z0, alpha_SMA + 1j*beta_SMA, L_SMA)

print("\n\n      Towards generator: \n")
print(f"Z_G_inital: {Z_G_inital:.3f}")
print(f"Z_G_new: {Z_G_new:.3f}")



def compute_Gamma(Zin, Z0):
    return (Zin - Z0) / (Zin + Z0)

def compute_losses(Gamma):
    ML = -10* np.log10(1- np.abs(Gamma)**2)
    return ML


Gamma_initial = compute_Gamma(Z_G_inital, Z0)
Gamma_new = compute_Gamma(Z_G_new, Z0)
print("\n\n      Gamma: \n")
print(f"Gamma_initial: {np.abs(Gamma_initial):.3f}")
print(f"Gamma_new: {np.abs(Gamma_new):.3f} \n")

ML_initial = compute_losses(Gamma_initial)
ML_new = compute_losses(Gamma_new)
print(f"ML_initial: {ML_initial:.3f} dB")
print(f"ML_new: {ML_new:.3f} dB")