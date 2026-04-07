
from __future__ import annotations

import numpy as np

Delta = 0.01


def _continuous_dict(key: str, title: str, description: str, t: np.ndarray, x: np.ndarray) -> dict:
    return {
        'key': key,
        'title': title,
        'description': description,
        'domain': 'continuous',
        't': t.tolist(),
        'x': x.tolist(),
    }


def _discrete_dict(key: str, title: str, description: str, n: np.ndarray, x: np.ndarray, n0: int = 0) -> dict:
    return {
        'key': key,
        'title': title,
        'description': description,
        'domain': 'discrete',
        'n': n.tolist(),
        'x': x.tolist(),
        'n0': int(n0),
    }


# ============================================================
# DEFINICIONES CONTINUAS ESCRITAS COMO EN EL NOTEBOOK
# ============================================================

def continuous_support(signal_key: str) -> list[float]:
    if signal_key == 'continuous_1':
        return [-2, -1, 1, 3, 4]
    if signal_key == 'continuous_2':
        return [-3, -2, 0, 2, 3]
    raise ValueError('La señal no es continua o no existe.')


def _segment_functions(signal_key: str):
    if signal_key == 'continuous_1':
        x1 = lambda t: 2 * t + 4
        x2 = lambda t: 2 * np.ones(len(np.atleast_1d(t)))
        x3 = lambda t: 3 * np.ones(len(np.atleast_1d(t)))
        x4 = lambda t: 12 - 3 * t
        return [x1, x2, x3, x4]

    if signal_key == 'continuous_2':
        x1 = lambda t: t + 3
        x2 = lambda t: 0.5 * (t + 2) + 2
        x3 = lambda t: -1 * t + 3
        x4 = lambda t: np.ones(len(np.atleast_1d(t)))
        return [x1, x2, x3, x4]

    raise ValueError('La señal no es continua o no existe.')


def _build_continuous_from_points(points: list[float], funcs: list, delta: float = Delta):
    t1 = np.arange(points[0], points[1], delta)
    t2 = np.arange(points[1], points[2], delta)
    t3 = np.arange(points[2], points[3], delta)
    t4 = np.arange(points[3], points[4] + delta, delta)

    x_t = np.concatenate((funcs[0](t1), funcs[1](t2), funcs[2](t3), funcs[3](t4)))
    t = np.concatenate((t1, t2, t3, t4))
    return t, x_t


def evaluate_continuous_signal(signal_key: str, t):
    t = np.array(t, dtype=float)
    x = np.zeros(len(t), dtype=float)
    p = continuous_support(signal_key)
    f = _segment_functions(signal_key)

    # Se replica la lógica por tramos del notebook.
    m1 = (t >= p[0]) & (t < p[1])
    m2 = (t >= p[1]) & (t < p[2])
    m3 = (t >= p[2]) & (t < p[3])
    m4 = (t >= p[3]) & (t <= p[4])

    if np.any(m1):
        x[m1] = np.array(f[0](t[m1]), dtype=float)
    if np.any(m2):
        x[m2] = np.array(f[1](t[m2]), dtype=float)
    if np.any(m3):
        x[m3] = np.array(f[2](t[m3]), dtype=float)
    if np.any(m4):
        x[m4] = np.array(f[3](t[m4]), dtype=float)

    return x


def build_continuous_signal_1(delta: float = Delta) -> dict:
    p_señal_1 = [-2, -1, 1, 3, 4]
    x1_señal_1 = lambda t: 2 * t + 4
    x2_señal_1 = lambda t: 2 * np.ones(len(t))
    x3_señal_1 = lambda t: 3 * np.ones(len(t))
    x4_señal_1 = lambda t: 12 - 3 * t

    t, x_t = _build_continuous_from_points(
        p_señal_1, [x1_señal_1, x2_señal_1, x3_señal_1, x4_señal_1], delta
    )

    return _continuous_dict(
        key='continuous_1',
        title='Señal continua 1',
        description='Señal continua 1 definida por tramos lineales y constantes.',
        t=t,
        x=x_t,
    )


def build_continuous_signal_2(delta: float = Delta) -> dict:
    p_señal_2 = [-3, -2, 0, 2, 3]
    x1_señal_2 = lambda t: t + 3
    x2_señal_2 = lambda t: 0.5 * (t + 2) + 2
    x3_señal_2 = lambda t: -1 * t + 3
    x4_señal_2 = lambda t: np.ones(len(t))

    t, x_t = _build_continuous_from_points(
        p_señal_2, [x1_señal_2, x2_señal_2, x3_señal_2, x4_señal_2], delta
    )

    return _continuous_dict(
        key='continuous_2',
        title='Señal continua 2',
        description='Señal continua 2 definida por tramos, con salto en t=-2 y meseta final.',
        t=t,
        x=x_t,
    )


# ============================================================
# DEFINICIONES DISCRETAS ESCRITAS COMO EN EL NOTEBOOK
# ============================================================

def build_discrete_signal_1() -> dict:
    x_señal_3 = [0, 0, 0, 0, 0, -4, 0, 3, 5, 2, -3, -1, 3, 6, 8, 3, -1, 0, 0, 0, 0, 0]
    n_señal_3 = np.arange(-5, 17)

    return _discrete_dict(
        key='discrete_1',
        title='Secuencia discreta 1',
        description='Secuencia finita definida explícitamente en el laboratorio.',
        n=n_señal_3,
        x=np.array(x_señal_3, dtype=float),
        n0=0,
    )


def build_discrete_signal_2() -> dict:
    x_señal_4 = []
    n_señal_4 = np.arange(-10, 11)

    for n in n_señal_4:
        if -10 <= n <= -6:
            x_señal_4.append(0)
        elif -5 <= n <= 0:
            x_señal_4.append((3 / 4) ** n)
        elif 1 <= n <= 5:
            x_señal_4.append((7 / 4) ** n)
        elif 6 <= n <= 10:
            x_señal_4.append(0)

    return _discrete_dict(
        key='discrete_2',
        title='Secuencia discreta 2',
        description='Secuencia definida por tramos exponenciales.',
        n=n_señal_4,
        x=np.array(x_señal_4, dtype=float),
        n0=0,
    )


def get_signal_catalog() -> dict:
    return {
        'continuous': [build_continuous_signal_1(), build_continuous_signal_2()],
        'discrete': [build_discrete_signal_1(), build_discrete_signal_2()],
    }


def get_signal_by_key(key: str) -> dict:
    signals = [
        build_continuous_signal_1(),
        build_continuous_signal_2(),
        build_discrete_signal_1(),
        build_discrete_signal_2(),
    ]
    for signal in signals:
        if signal['key'] == key:
            return signal
    raise KeyError(f'No existe una señal registrada con la llave: {key}')
