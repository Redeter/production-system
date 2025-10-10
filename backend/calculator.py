import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import random

# ----------------------------- ДЕФОЛТНЫЕ КОЭФФИЦИЕНТЫ -----------------------------
def make_default_coeffs():
    return {
        "k1": 0.1, "k5": 0.05, "k8": 0.05, "k11": 0.05, "k15": 0.05,
        "k18": 0.05, "k23": 0.02, "k24": 0.05, "k25": 0.05, "k26": 0.05,
        "k28": 0.02, "k29": 0.02, "k35": 0.05,
        "a2": 1.0, "a3": 1.0, "a4": 1.0, "a9": 1.0, "a10": 1.0,
        "a13": 1.0, "a14": 1.0,
        "c6": 1.0, "c12": 1.0, "c16": 1.0, "c17": 1.0,
        "c19": 1.0, "c20": 1.0, "c21": 1.0, "c22": 1.0,
        "c27": 1.0, "c30": 1.0, "c31": 1.0, "c32": 1.0,
        "c33": 1.0, "c34": 1.0, "c36": 1.0,
        "Nplan": 100.0,
        "dUstar": 1.0, "dIstar": 1.0, "dTstar": 1.0, "dPGstar": 1.0, "dPVstar": 1.0
    }

# ----------------------------- ФУНКЦИИ f1..f36 -----------------------------
def make_f_functions(coeffs):
    def f1(X3):
        return math.exp(-coeffs.get("k1", 0.1) * X3)

    def f2(X11):
        a2 = coeffs.get("a2", 1.0); dUstar = coeffs.get("dUstar", 0.0)
        return 1.0 / (1.0 + a2 * (X11 - dUstar) ** 2)

    def f3(X12):
        a3 = coeffs.get("a3", 1.0); dIstar = coeffs.get("dIstar", 0.0)
        return 1.0 / (1.0 + a3 * (X12 - dIstar) ** 2)

    def f4(X13):
        a4 = coeffs.get("a4", 1.0); dTstar = coeffs.get("dTstar", 0.0)
        return 1.0 / (1.0 + a4 * (X13 - dTstar) ** 2)

    def f5(X2):
        return 1.0 - math.exp(-coeffs.get("k5", 0.05) * X2)

    def f6(X8):
        c6 = coeffs.get("c6", 1.0)
        return X8 / (X8 + c6) if (X8 + c6) != 0 else 0.0

    def f7(X17):
        Nplan = coeffs.get("Nplan", 100.0)
        return min(1.0, X17 / Nplan) if Nplan != 0 else 1.0

    def f8(X10):
        return math.exp(-coeffs.get("k8", 0.05) * X10)

    def f9(X15):
        a9 = coeffs.get("a9", 1.0); dPGstar = coeffs.get("dPGstar", 0.0)
        return 1.0 / (1.0 + a9 * (X15 - dPGstar) ** 2)

    def f10(X16):
        a10 = coeffs.get("a10", 1.0); dPVstar = coeffs.get("dPVstar", 0.0)
        return 1.0 / (1.0 + a10 * (X16 - dPVstar) ** 2)

    def f11(X2):
        return math.exp(-coeffs.get("k11", 0.05) * X2)

    def f12(X17):
        c12 = coeffs.get("c12", 1.0)
        return X17 / (X17 + c12) if (X17 + c12) != 0 else 0.0

    def f13(X15):
        a13 = coeffs.get("a13", 1.0); dPGstar = coeffs.get("dPGstar", 0.0)
        return 1.0 / (1.0 + a13 * (X15 - dPGstar) ** 2)

    def f14(X16):
        a14 = coeffs.get("a14", 1.0); dPVstar = coeffs.get("dPVstar", 0.0)
        return 1.0 / (1.0 + a14 * (X16 - dPVstar) ** 2)

    def f15(X2):
        return math.exp(-coeffs.get("k15", 0.05) * X2)

    def f16(X6):
        c16 = coeffs.get("c16", 1.0)
        return X6 / (X6 + c16) if (X6 + c16) != 0 else 0.0

    def f17(X7):
        c17 = coeffs.get("c17", 1.0)
        return X7 / (X7 + c17) if (X7 + c17) != 0 else 0.0

    def f18(X10):
        return math.exp(-coeffs.get("k18", 0.05) * X10)

    def f19(X17):
        c19 = coeffs.get("c19", 1.0)
        return X17 / (X17 + c19) if (X17 + c19) != 0 else 0.0

    def f20(X17):
        c20 = coeffs.get("c20", 1.0)
        return X17 / (X17 + c20) if (X17 + c20) != 0 else 0.0

    def f21(X17):
        c21 = coeffs.get("c21", 1.0)
        return X17 / (X17 + c21) if (X17 + c21) != 0 else 0.0

    def f22(X17):
        c22 = coeffs.get("c22", 1.0)
        return X17 / (X17 + c22) if (X17 + c22) != 0 else 0.0

    def f23(X17):
        return math.exp(-coeffs.get("k23", 0.02) * X17)

    def f24(X5):
        return math.exp(-coeffs.get("k24", 0.05) * X5)

    def f25(X5):
        return math.exp(-coeffs.get("k25", 0.05) * X5)

    def f26(X5):
        return math.exp(-coeffs.get("k26", 0.05) * X5)

    def f27(X9):
        c27 = coeffs.get("c27", 1.0)
        return X9 / (X9 + c27) if (X9 + c27) != 0 else 0.0

    def f28(X17):
        return math.exp(-coeffs.get("k28", 0.02) * X17)

    def f29(X17):
        return math.exp(-coeffs.get("k29", 0.02) * X17)

    def f30(X9):
        c30 = coeffs.get("c30", 1.0)
        return X9 / (X9 + c30) if (X9 + c30) != 0 else 0.0

    def f31(X6):
        c31 = coeffs.get("c31", 1.0)
        return X6 / (X6 + c31) if (X6 + c31) != 0 else 0.0

    def f32(X7):
        c32 = coeffs.get("c32", 1.0)
        return X7 / (X7 + c32) if (X7 + c32) != 0 else 0.0

    def f33(X8):
        c33 = coeffs.get("c33", 1.0)
        return X8 / (X8 + c33) if (X8 + c33) != 0 else 0.0

    def f34(X14):
        c34 = coeffs.get("c34", 1.0)
        return X14 / (X14 + c34) if (X14 + c34) != 0 else 0.0

    def f35(X4):
        return math.exp(-coeffs.get("k35", 0.05) * X4)

    def f36(X18):
        c36 = coeffs.get("c36", 1.0)
        return X18 / (X18 + c36) if (X18 + c36) != 0 else 0.0

    return {
        'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4, 'f5': f5, 'f6': f6, 'f7': f7,
        'f8': f8, 'f9': f9, 'f10': f10, 'f11': f11, 'f12': f12, 'f13': f13,
        'f14': f14, 'f15': f15, 'f16': f16, 'f17': f17, 'f18': f18, 'f19': f19,
        'f20': f20, 'f21': f21, 'f22': f22, 'f23': f23, 'f24': f24, 'f25': f25,
        'f26': f26, 'f27': f27, 'f28': f28, 'f29': f29, 'f30': f30, 'f31': f31,
        'f32': f32, 'f33': f33, 'f34': f34, 'f35': f35, 'f36': f36
    }

# ----------------------------- ПРАВЫЕ ЧАСТИ СИСТЕМЫ -----------------------------
def derivatives(X, params, coeffs):
    f = make_f_functions(coeffs)
    X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16, X17, X18 = X
    
    # Извлечение параметров с значениями по умолчанию
    Nw = params.get('Nw', 1.0); Ns = params.get('Ns', 1.0)
    O0 = params.get('O0', 10.0); Oin = params.get('Oin', 0.0); Oout = params.get('Oout', 0.0)
    Sm = params.get('Sm', 1.0); Rw = params.get('Rw', 1.0)
    Nst = params.get('Nst', 1.0); Sstar = params.get('Sstar', 1.0)
    Ld = params.get('Ld', 1.0); Lstar = params.get('Lstar', 1.0)
    Mf = params.get('Mf', 1.0); Mp = params.get('Mp', 1.0)
    P0 = params.get('P0', 1.0); Pin = params.get('Pin', 0.0); Pout = params.get('Pout', 0.0)
    R0 = params.get('R0', 1.0); Rin = params.get('Rin', 0.0); Rout = params.get('Rout', 0.0)
    C0 = params.get('C0', 1.0); Cin = params.get('Cin', 0.0); Cout = params.get('Cout', 0.0)
    T0 = params.get('T0', 1.0); Tin = params.get('Tin', 0.0); Tout = params.get('Tout', 0.0)
    Nr = params.get('Nr', 1.0); Df = params.get('Df', 1.0); Dp = params.get('Dp', 1.0)
    dU = params.get('dU', 0.0); dUstar = params.get('dUstar', 0.0)
    dI = params.get('dI', 0.0); dIstar = params.get('dIstar', 0.0)
    dT = params.get('dT', 0.0); dTstar = params.get('dTstar', 0.0)
    Tdf = params.get('Tdf', 1.0); Tdp = params.get('Tdp', 1.0)
    dPG = params.get('dPG', 0.0); dPGstar = params.get('dPGstar', 0.0)
    dPV = params.get('dPV', 0.0); dPVstar = params.get('dPVstar', 0.0)
    NTP = params.get('NTP', 1.0)
    Nd = params.get('Nd', 1.0); Ab = params.get('Ab', 0.0)

    local_coeffs = coeffs.copy()
    local_coeffs.setdefault('dUstar', dUstar)
    local_coeffs.setdefault('dIstar', dIstar)
    local_coeffs.setdefault('dTstar', dTstar)
    local_coeffs.setdefault('dPGstar', dPGstar)
    local_coeffs.setdefault('dPVstar', dPVstar)

    f = make_f_functions(local_coeffs)

    dX = [0.0] * 18
    dX[0] = Nw * f['f1'](X3) * f['f2'](X11) * f['f3'](X12) * f['f4'](X13) - Ns * f['f5'](X2) * f['f6'](X8) * f['f7'](X17)
    dX[1] = (O0 + Oin) * f['f12'](X17) - (Sm + Rw + Oout)
    dX[2] = (Nw / max(1e-9, Nst)) * f['f8'](X10) * f['f9'](X15) * f['f10'](X16) - Sstar * f['f11'](X2)
    dX[3] = Ld * f['f13'](X15) * f['f14'](X16) - Lstar * f['f15'](X2)
    dX[4] = Mf * f['f16'](X6) * f['f17'](X7) - Mp * f['f18'](X10)
    dX[5] = (P0 + Pin) * f['f19'](X17) - (Sm + Rw + Pout)
    dX[6] = (R0 + Rin) * f['f20'](X17) - (Sm + Rw + Rout)
    dX[7] = (C0 + Cin) * f['f21'](X17) - (Sm + Rw + Cout)
    dX[8] = (T0 + Tin) * f['f22'](X17) - Tout
    dX[9] = (Nr + Df) * f['f23'](X17) - Dp
    dX[10] = dU - dUstar * f['f24'](X5)
    dX[11] = dI - dIstar * f['f25'](X5)
    dX[12] = dT - dTstar * f['f26'](X5)
    dX[13] = Tdf * f['f27'](X9) - Tdp
    dX[14] = dPG - dPGstar * f['f28'](X17)
    dX[15] = dPV - dPVstar * f['f29'](X17)
    dX[16] = NTP * f['f30'](X9) - Nw
    dX[17] = Nd * f['f31'](X6) * f['f32'](X7) * f['f33'](X8) * f['f34'](X14) - (Ab + Ld * f['f35'](X1) * f['f36'](X4))
    
    return np.array(dX, dtype=float)

# ----------------------------- RK4 ИНТЕГРАТОР -----------------------------
def rk4_step(fun, X, t, dt, params, coeffs):
    k1 = fun(X, params, coeffs)
    k2 = fun(X + 0.5 * dt * k1, params, coeffs)
    k3 = fun(X + 0.5 * dt * k2, params, coeffs)
    k4 = fun(X + dt * k3, params, coeffs)
    return X + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

def integrate(fun, X0, t0, t1, dt, params, coeffs):
    times = np.arange(t0, t1 + 1e-12, dt)
    n = len(times)
    Xs = np.zeros((n, len(X0)))
    Xs[0, :] = X0
    
    for i in range(1, n):
        Xs[i, :] = rk4_step(fun, Xs[i - 1, :], times[i - 1], dt, params, coeffs)
    
    return times, Xs

# ----------------------------- ГЕНЕРАЦИЯ ПОДХОДЯЩИХ ЗНАЧЕНИЙ -----------------------------
def generate_suitable_values():
    values = {}
    for i in range(18):
        values[f'X{i + 1}'] = round(random.uniform(0.1, 5.0), 3)
    
    param_names = ['Nw', 'Ns', 'O0', 'Oin', 'Oout', 'Sm', 'Rw', 'Nst', 'Sstar', 'Ld', 'Lstar', 
                   'Mf', 'Mp', 'P0', 'Pin', 'Pout', 'R0', 'Rin', 'Rout', 'C0', 'Cin', 'Cout', 
                   'T0', 'Tin', 'Tout', 'Nr', 'Df', 'Dp', 'dU', 'dUstar', 'dI', 'dIstar', 
                   'dT', 'dTstar', 'Tdf', 'Tdp', 'dPG', 'dPGstar', 'dPV', 'dPVstar', 'NTP', 
                   'Nd', 'Ab', 'T', 'dt']
    
    for name in param_names:
        if name == 'O0':
            values[name] = round(random.uniform(5.0, 20.0), 3)
        elif name in ('T', 'dt'):
            values[name] = 50.0 if name == 'T' else 0.5
        elif name in ('dU', 'dI', 'dT', 'dPG', 'dPV'):
            values[name] = round(random.uniform(0.0, 1.0), 3)
        elif name in ('dUstar', 'dIstar', 'dTstar', 'dPGstar', 'dPVstar'):
            values[name] = round(random.uniform(0.5, 2.0), 3)
        else:
            values[name] = round(random.uniform(0.5, 5.0), 3)
    
    return values

# ----------------------------- ВИЗУАЛИЗАЦИЯ -----------------------------
def create_plots(times, Xs):
    fig, axes = plt.subplots(6, 3, figsize=(15, 12))
    axes = axes.flatten()
    
    for i in range(18):
        axes[i].plot(times, Xs[:, i])
        axes[i].set_title(f'X{i + 1}(t)')
        axes[i].grid(True, linestyle='--', alpha=0.4)
        axes[i].tick_params(axis='both', which='major', labelsize=8)
    
    plt.tight_layout()
    
    # Конвертируем в base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return plot_data

def create_radar_plot(Xfinal):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    labels = [f'X{i + 1}' for i in range(18)]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    
    vmax = max(max(Xfinal), abs(min(Xfinal)), 1e-9)
    norm = [v / vmax for v in Xfinal]
    vals = norm + [norm[0]]
    angs = angles + [angles[0]]
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.plot(angs, vals, linewidth=2)
    ax.fill(angs, vals, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles), labels)
    ax.set_ylim(-1.1, 1.1)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    radar_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return radar_data