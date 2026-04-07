
from __future__ import annotations

import numpy as np

from signals.base_signals import continuous_support, evaluate_continuous_signal, get_signal_by_key
from signals.transformations import Delta


def continuous_sum_operation(signal_key: str) -> dict:
    signal = get_signal_by_key(signal_key)
    if signal['domain'] != 'continuous':
        raise ValueError('La señal seleccionada no es continua.')

    # Se sigue la idea del notebook:
    # y(t) = x(t/3 + 2) + x(1 - t/4)
    # primer término -> a = 1/3, t0 = 2
    # segundo término -> a = -1/4, t0 = 1

    p = continuous_support(signal_key)

    # Primer término
    p1 = []
    for i in range(len(p)):
        p1.append((p[i] - 2) / (1 / 3))
    if 1 / 3 < 0:
        p1 = p1[::-1]

    t1a = np.arange(p1[0], p1[1], Delta)
    t1b = np.arange(p1[1], p1[2], Delta)
    t1c = np.arange(p1[2], p1[3], Delta)
    t1d = np.arange(p1[3], p1[4] + Delta, Delta)
    t_v1 = np.concatenate((t1a, t1b, t1c, t1d))
    x_v1 = evaluate_continuous_signal(signal_key, (1 / 3) * t_v1 + 2)

    # Segundo término
    p2 = []
    for i in range(len(p)):
        p2.append((p[i] - 1) / (-1 / 4))
    if -1 / 4 < 0:
        p2 = p2[::-1]

    t2a = np.arange(p2[0], p2[1], Delta)
    t2b = np.arange(p2[1], p2[2], Delta)
    t2c = np.arange(p2[2], p2[3], Delta)
    t2d = np.arange(p2[3], p2[4] + Delta, Delta)
    t_v2 = np.concatenate((t2a, t2b, t2c, t2d))
    x_v2 = evaluate_continuous_signal(signal_key, (-1 / 4) * t_v2 + 1)

    # Malla común para la suma, como en clase
    t_int = np.arange(min(np.min(t_v1), np.min(t_v2)), max(np.max(t_v1), np.max(t_v2)) + Delta, Delta)

    x_v1_int = np.interp(t_int, t_v1, x_v1, left=0.0, right=0.0)
    x_v2_int = np.interp(t_int, t_v2, x_v2, left=0.0, right=0.0)
    x_suma = x_v1_int + x_v2_int

    return {
        'signal_key': signal_key,
        'domain': 'continuous',
        'final_expression': 'y(t) = x(t/3 + 2) + x(1 - t/4)',
        'note': 'Se construyen ambos términos con la lógica del notebook y luego se suman sobre un mismo eje temporal.',
        'base_signal': {
            'title': 'Señal base',
            'domain': 'continuous',
            't': signal['t'],
            'x': signal['x'],
        },
        'steps': [
            {
                'title': 'Paso 1 — Primer término',
                'expression': 'v1(t) = x(t/3 + 2)',
                'domain': 'continuous',
                't': t_v1.tolist(),
                'x': x_v1.tolist(),
            },
            {
                'title': 'Paso 2 — Segundo término',
                'expression': 'v2(t) = x(1 - t/4)',
                'domain': 'continuous',
                't': t_v2.tolist(),
                'x': x_v2.tolist(),
            },
            {
                'title': 'Paso 3 — Suma punto a punto',
                'expression': 'y(t) = v1(t) + v2(t)',
                'domain': 'continuous',
                't': t_int.tolist(),
                'x': x_suma.tolist(),
            },
        ],
        'final_signal': {
            'title': 'Suma final de términos transformados',
            'domain': 'continuous',
            't': t_int.tolist(),
            'x': x_suma.tolist(),
        }
    }
