
from __future__ import annotations

from fractions import Fraction
import numpy as np

from signals.base_signals import Delta, continuous_support, evaluate_continuous_signal, get_signal_by_key

ALLOWED_A = [2, 3, 4, 5, 1 / 2, 1 / 3, 1 / 4, 1 / 5]
ALLOWED_T0 = [1, 2, 3, 4, 5, 6]
ALLOWED_M = [2, 3, 4, 1 / 2, 1 / 3, 1 / 4, 1 / 5]
ALLOWED_N0 = [1, 2, 3, 4, 5, 6]
INTERP_METHODS = ['zero', 'step', 'linear']


def _validate_sign(sign: str) -> None:
    if sign not in ('+', '-'):
        raise ValueError("El signo debe ser '+' o '-'.")


def _sign(sign: str) -> int:
    return 1 if sign == '+' else -1


def _to_list(a):
    return np.array(a, dtype=float).tolist()


# ============================================================
# TRANSFORMACIONES CONTINUAS TIPO NOTEBOOK
# ============================================================

def _continuous_by_argument(signal_key: str, alpha: float, beta: float):
    p = continuous_support(signal_key)
    nuevos_p = []
    for i in range(len(p)):
        nuevos_p.append((p[i] - beta) / alpha)

    if alpha < 0:
        nuevos_p = nuevos_p[::-1]

    t1 = np.arange(nuevos_p[0], nuevos_p[1], Delta)
    t2 = np.arange(nuevos_p[1], nuevos_p[2], Delta)
    t3 = np.arange(nuevos_p[2], nuevos_p[3], Delta)
    t4 = np.arange(nuevos_p[3], nuevos_p[4] + Delta, Delta)

    t = np.concatenate((t1, t2, t3, t4))
    x = evaluate_continuous_signal(signal_key, alpha * t + beta)
    return t, x, nuevos_p


def transform_continuous(signal_key: str, a_mag: float, a_sign: str, t0: int, shift_sign: str, method: str) -> dict:
    _validate_sign(a_sign)
    _validate_sign(shift_sign)

    if a_mag not in ALLOWED_A:
        raise ValueError('Valor de |a| no permitido.')
    if t0 not in ALLOWED_T0:
        raise ValueError('Valor de t0 no permitido.')
    if method not in ('method_1', 'method_2'):
        raise ValueError('Método no permitido.')

    signal = get_signal_by_key(signal_key)
    if signal['domain'] != 'continuous':
        raise ValueError('La señal seleccionada no es continua.')

    a = _sign(a_sign) * float(a_mag)
    b = _sign(shift_sign) * float(t0)

    # Método 1 del notebook: desplazamiento y luego escalamiento
    if method == 'method_1':
        p = continuous_support(signal_key)

        nuevos_p = []
        for i in range(len(p)):
            nuevos_p.append(p[i] - b)

        t1 = np.arange(nuevos_p[0], nuevos_p[1], Delta)
        t2 = np.arange(nuevos_p[1], nuevos_p[2], Delta)
        t3 = np.arange(nuevos_p[2], nuevos_p[3], Delta)
        t4 = np.arange(nuevos_p[3], nuevos_p[4] + Delta, Delta)

        t_step1 = np.concatenate((t1, t2, t3, t4))
        x_step1 = evaluate_continuous_signal(signal_key, t_step1 + b)

        for i in range(len(nuevos_p)):
            nuevos_p[i] = nuevos_p[i] * (1 / a)

        if a < 0:
            nuevos_p = nuevos_p[::-1]

        t1 = np.arange(nuevos_p[0], nuevos_p[1], Delta)
        t2 = np.arange(nuevos_p[1], nuevos_p[2], Delta)
        t3 = np.arange(nuevos_p[2], nuevos_p[3], Delta)
        t4 = np.arange(nuevos_p[3], nuevos_p[4] + Delta, Delta)

        t_final = np.concatenate((t1, t2, t3, t4))
        x_final = evaluate_continuous_signal(signal_key, a * t_final + b)

        steps = [
            {
                'title': 'Paso 1 — Desplazamiento',
                'expression': f'v(t) = x(t {"+" if b >= 0 else "-"} {abs(b):g})',
                'domain': 'continuous',
                't': _to_list(t_step1),
                'x': _to_list(x_step1),
            },
            {
                'title': 'Paso 2 — Escalamiento',
                'expression': f'y(t) = v({a:g}t)',
                'domain': 'continuous',
                't': _to_list(t_final),
                'x': _to_list(x_final),
            },
        ]

    else:
        p = continuous_support(signal_key)

        nuevos_p = []
        for i in range(len(p)):
            nuevos_p.append(p[i] * (1 / a))

        if a < 0:
            nuevos_p = nuevos_p[::-1]

        t1 = np.arange(nuevos_p[0], nuevos_p[1], Delta)
        t2 = np.arange(nuevos_p[1], nuevos_p[2], Delta)
        t3 = np.arange(nuevos_p[2], nuevos_p[3], Delta)
        t4 = np.arange(nuevos_p[3], nuevos_p[4] + Delta, Delta)

        t_step1 = np.concatenate((t1, t2, t3, t4))
        x_step1 = evaluate_continuous_signal(signal_key, a * t_step1)

        for i in range(len(nuevos_p)):
            nuevos_p[i] = nuevos_p[i] - (b / a)

        t1 = np.arange(nuevos_p[0], nuevos_p[1], Delta)
        t2 = np.arange(nuevos_p[1], nuevos_p[2], Delta)
        t3 = np.arange(nuevos_p[2], nuevos_p[3], Delta)
        t4 = np.arange(nuevos_p[3], nuevos_p[4] + Delta, Delta)

        t_final = np.concatenate((t1, t2, t3, t4))
        x_final = evaluate_continuous_signal(signal_key, a * t_final + b)

        steps = [
            {
                'title': 'Paso 1 — Escalamiento',
                'expression': f'v(t) = x({a:g}t)',
                'domain': 'continuous',
                't': _to_list(t_step1),
                'x': _to_list(x_step1),
            },
            {
                'title': 'Paso 2 — Desplazamiento',
                'expression': f'y(t) = v(t {"+" if b / a >= 0 else "-"} {abs(b / a):g})',
                'domain': 'continuous',
                't': _to_list(t_final),
                'x': _to_list(x_final),
            },
        ]

    return {
        'signal_key': signal_key,
        'domain': 'continuous',
        'method': method,
        'final_expression': f'y(t) = x({a:g}t {"+" if b >= 0 else "-"} {abs(b):g})',
        'steps': steps,
        'final_signal': {
            'title': 'Señal transformada',
            'domain': 'continuous',
            't': _to_list(t_final),
            'x': _to_list(x_final),
        },
        'note': 'Transformación continua escrita con puntos de quiebre, tramos y concatenación, como en el notebook de clase.',
    }


# ============================================================
# INTERPOLACIÓN DISCRETA TIPO NOTEBOOK
# ============================================================

def _interpolacion_discreta_notebook(x, n, M=1):
    n_in = int(n[0])
    n_fin = int(n[-1])

    nI = np.arange(n_in, n_fin * M + 1)
    L_nI = len(nI)
    L_n = len(x)

    x_nI0 = np.zeros(L_nI)
    x_nIEsc = np.zeros(L_nI)
    x_nILin = np.zeros(L_nI)

    for k in range(L_nI):
        if k % M == 0:
            r = int(k / M)
            x_nI0[k] = x[r]
            x_nIEsc[k] = x[r]
            x_nILin[k] = x[r]
        else:
            r = int(k / M)
            x_nI0[k] = 0
            x_nIEsc[k] = x_nIEsc[k - 1]

            if r + 1 < L_n:
                fraccion = (k % M) / M
                x_nILin[k] = x[r] + fraccion * (x[r + 1] - x[r])
            else:
                x_nILin[k] = x[r]

    return nI, x_nI0, x_nIEsc, x_nILin


def interpolate_discrete(signal_key: str, L: int, mode: str) -> dict:
    signal = get_signal_by_key(signal_key)
    if signal['domain'] != 'discrete':
        raise ValueError('La señal seleccionada no es discreta.')
    if L not in [2, 3, 4, 5]:
        raise ValueError('El factor de interpolación permitido es 2, 3, 4 o 5.')
    if mode not in INTERP_METHODS:
        raise ValueError('Método de interpolación no permitido.')

    n = np.array(signal['n'], dtype=int)
    x_n = np.array(signal['x'], dtype=float)

    nI, x0, xEsc, xLin = _interpolacion_discreta_notebook(x_n, n, L)

    if mode == 'zero':
        x_final = x0
        nombre = 'por cero'
        note = f'Se insertan {L-1} muestras nulas entre muestras consecutivas.'
    elif mode == 'step':
        x_final = xEsc
        nombre = 'por escalón'
        note = f'Se insertan {L-1} muestras repitiendo el último valor.'
    else:
        x_final = xLin
        nombre = 'lineal'
        note = f'Se insertan {L-1} muestras usando rectas entre muestras consecutivas.'

    return {
        'domain': 'discrete',
        'signal_key': signal_key,
        'mode': mode,
        'factor': L,
        'final_expression': f'y[n] = x[n/{L}] ({nombre})',
        'note': note,
        'original_signal': {
            'title': 'Señal original',
            'domain': 'discrete',
            'n': n.tolist(),
            'x': x_n.tolist(),
            'n0': 0,
        },
        'final_signal': {
            'title': f'Interpolación {nombre}',
            'domain': 'discrete',
            'n': nI.tolist(),
            'x': x_final.tolist(),
            'n0': 0,
        },
        'steps': [
            {
                'title': 'Paso 1 — Señal original',
                'expression': 'x[n]',
                'domain': 'discrete',
                'n': n.tolist(),
                'x': x_n.tolist(),
            },
            {
                'title': f'Paso 2 — Interpolación {nombre}',
                'expression': f'y[n] = x[n/{L}]',
                'domain': 'discrete',
                'n': nI.tolist(),
                'x': x_final.tolist(),
            }
        ]
    }


# ============================================================
# TRANSFORMACIONES DISCRETAS
# ============================================================

def _mapping_discreto(n, x):
    return {int(n[i]): float(x[i]) for i in range(len(n))}


def _transformacion_discreta_directa(n, x, M, n0, interp_mode='zero'):
    mapping = _mapping_discreto(n, x)

    if abs(M) >= 1:
        M_int = int(M)
        n_final = []
        x_final = []

        for k in range(-100, 101):
            argumento = M_int * k + n0
            if argumento in mapping:
                n_final.append(k)
                x_final.append(mapping[argumento])

        if len(n_final) == 0:
            return np.array([0]), np.array([0.0]), 'No hubo índices válidos dentro del soporte.'

        return np.array(n_final), np.array(x_final), 'Transformación discreta usando coincidencia exacta de índices.'

    frac = Fraction(abs(M)).limit_denominator()
    L = frac.denominator
    nI, x0, xEsc, xLin = _interpolacion_discreta_notebook(x, n, L)

    if interp_mode == 'zero':
        xI = x0
        modo = 'cero'
    elif interp_mode == 'step':
        xI = xEsc
        modo = 'escalón'
    else:
        xI = xLin
        modo = 'lineal'

    if M < 0:
        nI = -nI[::-1]
        xI = xI[::-1]

    n_final = nI - n0
    return n_final, xI, f'Interpolación {modo} con factor L={L} para |M|<1.'


def transform_discrete(signal_key: str, m_mag: float, m_sign: str, n0: int, shift_sign: str, method: str, interp_mode: str = 'zero') -> dict:
    _validate_sign(m_sign)
    _validate_sign(shift_sign)

    if m_mag not in ALLOWED_M:
        raise ValueError('Valor de |M| no permitido.')
    if n0 not in ALLOWED_N0:
        raise ValueError('Valor de n0 no permitido.')
    if method not in ('method_1', 'method_2'):
        raise ValueError('Método no permitido.')

    signal = get_signal_by_key(signal_key)
    if signal['domain'] != 'discrete':
        raise ValueError('La señal seleccionada no es discreta.')

    n = np.array(signal['n'], dtype=int)
    x = np.array(signal['x'], dtype=float)

    M = _sign(m_sign) * float(m_mag)
    b = _sign(shift_sign) * int(n0)

    # Para mostrar paso a paso, se sigue la idea de notebook:
    # primero desplazamiento y luego escalamiento (o al revés),
    # pero el resultado final se deja funcional para la app.
    if method == 'method_1':
        n_step1 = n - b
        x_step1 = x.copy()
        n_final, x_final, note = _transformacion_discreta_directa(n, x, M, b, interp_mode)
        steps = [
            {
                'title': 'Paso 1 — Desplazamiento discreto',
                'expression': f'v[n] = x[n {"+" if b >= 0 else "-"} {abs(b)}]',
                'domain': 'discrete',
                'n': n_step1.tolist(),
                'x': x_step1.tolist(),
            },
            {
                'title': 'Paso 2 — Escalamiento discreto',
                'expression': f'y[n] = v[{M:g}n]',
                'domain': 'discrete',
                'n': n_final.tolist(),
                'x': x_final.tolist(),
            }
        ]
    else:
        n_step1, x_step1, _ = _transformacion_discreta_directa(n, x, M, 0, interp_mode)
        n_final, x_final, note = _transformacion_discreta_directa(n, x, M, b, interp_mode)
        steps = [
            {
                'title': 'Paso 1 — Escalamiento discreto',
                'expression': f'v[n] = x[{M:g}n]',
                'domain': 'discrete',
                'n': n_step1.tolist(),
                'x': x_step1.tolist(),
            },
            {
                'title': 'Paso 2 — Desplazamiento discreto',
                'expression': f'y[n] = v[n {"+" if (b / M if M != 0 else 0) >= 0 else "-"} {abs(b / M) if M != 0 else 0:g}]',
                'domain': 'discrete',
                'n': n_final.tolist(),
                'x': x_final.tolist(),
            }
        ]

    return {
        'signal_key': signal_key,
        'domain': 'discrete',
        'method': method,
        'final_expression': f'y[n] = x[{M:g}n {"+" if b >= 0 else "-"} {abs(b)}]',
        'steps': steps,
        'final_signal': {
            'title': 'Secuencia transformada',
            'domain': 'discrete',
            'n': n_final.tolist(),
            'x': x_final.tolist(),
            'n0': 0,
        },
        'note': note,
    }
