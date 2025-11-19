# Save this as antenna_full_sweep.py and run: python antenna_full_sweep.py
import math, csv, multiprocessing as mp
from scipy import integrate, special, constants
import numpy as np
c = constants.c
Z0 = 50 
def design_patch_params(fr, er, h):
    W = (c / (2 * fr)) * math.sqrt(2 / (er + 1))
    eps_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * (h / W))**-0.5
    Leff = c / (2 * fr * math.sqrt(eps_eff))
    dL = 0.412 * h * ((eps_eff + 0.3) * ((W / h) + 0.264)) / ((eps_eff - 0.258) * ((W / h) + 0.8))
    L = Leff - 2 * dL
    return W, eps_eff, Leff, dL, L

def compute_Gs_for_point(args):
    fr, er, h = args
    W, eps_eff, Leff, dL, L = design_patch_params(fr, er, h)
    # compute G1, G12
    lambda0 = c / fr
    k0 = 2 * math.pi / lambda0
    coef = 1.0 / (120.0 * math.pi**2)
    def integrand_G1(theta):
        cos_t = math.cos(theta)
        X = (k0 * W / 2.0) * cos_t
        ratio = (k0 * W / 2.0) if abs(cos_t) < 1e-12 else math.sin(X)/cos_t
        return (ratio**2) * (math.sin(theta)**3)
    def integrand_G12(theta):
        cos_t = math.cos(theta)
        X = (k0 * W / 2.0) * cos_t
        ratio = (k0 * W / 2.0) if abs(cos_t) < 1e-12 else math.sin(X)/cos_t
        return (ratio**2) * special.j0(k0 * Leff * math.sin(theta)) * (math.sin(theta)**3)
    G1 = coef * integrate.quad(integrand_G1, 0.0, math.pi, epsabs=1e-8, epsrel=1e-6, limit=200)[0]
    G12 = coef * integrate.quad(integrand_G12, 0.0, math.pi, epsabs=1e-8, epsrel=1e-6, limit=200)[0]
    Rin = 1.0 / (2.0 * (G1 + G12))
    # feedline & ground
    A = 50/60.0 * math.sqrt((er+1)/2.0) + (er-1)/(er+1) * (0.23 + 0.11/er)
    Wf = (8.0 * math.exp(A)) / (math.exp(2.0*A)-2.0) * h
    Lf = c / (8 * fr * math.sqrt(eps_eff))
    Lg = L + 6 * h
    Wg = W + 6 * h
    S11 = (Rin - Z0) / (Rin + Z0)
    S11_dB = 20 * np.log10(np.abs(S11) + 1e-12)
    #idx = np.argmin(S11_dB)
    #min_S11_dB = S11_dB[idx]
    return {
        "Frequency_Hz": fr,
        "Frequency_GHz": fr/1e9,
        "Er": er,
        "h_mm": h*1e3,
        "W_mm": W*1e3,
        "L_mm": L*1e3,
        "Leff_mm": Leff*1e3,
        "dL_mm": dL*1e3,
        "eps_eff": eps_eff,
        "G1_S": G1,
        "G12_S": G12,
        "Rin_edge_Ohm": Rin,
        "Feed_W_mm": Wf*1e3,
        "Feed_L_mm": Lf*1e3,
        "Ground_L_mm": Lg*1e3,
        "Ground_W_mm": Wg*1e3,
        "min_S11_dB": S11_dB
    }

if __name__ == "__main__":
    er = 4.4
    h = 1.6e-3
    freqs = [3*1e9 + (i*10e8 / 2) for i in range(101)]  # 1.0 GHz to 6.0 GHz, 10 MHz step
    args_list = [(fr, er, h) for fr in freqs]
    pool = mp.Pool()  # uses all available CPU cores
    results = pool.map(compute_Gs_for_point, args_list)
    pool.close()
    pool.join()
    # write CSV
    fieldnames = list(results[0].keys())
    with open("antenna_dataset_Gs_full.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print("Full dataset saved to antenna_dataset_Gs_full.csv")
