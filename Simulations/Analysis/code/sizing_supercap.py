H = 118 #kWh/m²  from Vincent
length = 42e-3 # m
width = 23e-3 # m

A_mod = length * width # m²
print(f"Area per module: {A_mod:.4f} m²")
eta_n = 0.25
FF = 0.759 

E_mod = 1000*H * A_mod * eta_n * FF
print(f"Energy per module: {E_mod:.2f} mWh")

P_mod = E_mod / 24  # mW
print(f"Power per module: {P_mod:.2f} mW")

P_avg = 0.200 #mW
eta_SC = 0.95  # efficiency of supercapacitor
eta_conv = 0.75

# longuest night = 16h
E = P_avg * 16  # mWh
print(f"Energy needed for the longest night: {E:.2f} mWh")

E_joule = E*3600 /1000  # convert mWh to J
print(f"Energy needed for the longest night: {E_joule:.2f} J")

V_OVCH = 4.5
V_OVDIS = 3.6
C_batt = 2*E_joule / ((V_OVCH**2 - V_OVDIS**2)*eta_SC*eta_conv)  # F
print(f"Capacitance needed: {C_batt:.2f} F")