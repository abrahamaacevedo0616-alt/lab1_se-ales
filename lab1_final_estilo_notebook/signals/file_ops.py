from __future__ import annotations

from math import gcd

import numpy as np


def _load_txt_values(file_storage) -> np.ndarray:
    if file_storage is None or not file_storage.filename:
        raise ValueError('Debes cargar ambos archivos .txt.')

    raw = file_storage.read()

    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        text = raw.decode('latin-1')

    rows = []
    text = text.replace(',', ' ').replace(';', ' ')

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        try:
            nums = [float(value) for value in line.split()]
        except ValueError:
            continue

        rows.append(nums)

    if len(rows) == 0:
        raise ValueError(f'El archivo {file_storage.filename} no contiene datos numéricos válidos.')

    arr = np.array(rows, dtype=float)

    if arr.ndim == 1:
        values = arr
    elif arr.shape[1] == 1:
        values = arr[:, 0]
    else:
        values = arr[:, -1]

    if len(values) < 2:
        raise ValueError('Cada archivo debe tener al menos dos muestras.')

    return values.astype(float)



def _interpolate_to_common(x: np.ndarray, up_factor: int, mode: str = 'linear') -> np.ndarray:
    if up_factor == 1:
        return x.copy()

    n = np.arange(len(x), dtype=float)
    n_new = np.arange(0, len(x) - 1 + 1 / up_factor, 1 / up_factor)

    if mode == 'zero':
        y = np.zeros_like(n_new)
        idx = np.round(n * up_factor).astype(int)
        y[idx] = x
        return y

    if mode == 'step':
        y = np.zeros_like(n_new)
        for i, k in enumerate(n_new):
            left = int(np.floor(k))
            left = min(left, len(x) - 1)
            y[i] = x[left]
        return y

    return np.interp(n_new, n, x)



def process_sampled_files(file1, file2, fs1: int = 2000, fs2: int = 2200, mode: str = 'linear') -> dict:
    x1 = _load_txt_values(file1)
    x2 = _load_txt_values(file2)

    fs_common = fs1 * fs2 // gcd(fs1, fs2)
    L1 = fs_common // fs1
    L2 = fs_common // fs2

    y1 = _interpolate_to_common(x1, L1, mode=mode)
    y2 = _interpolate_to_common(x2, L2, mode=mode)

    N = min(len(y1), len(y2))
    y1 = y1[:N]
    y2 = y2[:N]
    y_sum = y1 + y2

    t1 = np.arange(len(x1)) / fs1
    t2 = np.arange(len(x2)) / fs2
    t_common = np.arange(N) / fs_common

    return {
        'fs1': fs1,
        'fs2': fs2,
        'fs_common': fs_common,
        'L1': int(L1),
        'L2': int(L2),
        'mode': mode,
        'note': f'Se usa f_c = mcm({fs1}, {fs2}) = {fs_common} Hz. La señal 1 se sobremuestrea por {L1} y la señal 2 por {L2}. Para poder sumarlas, se recortan ambas al soporte temporal común más corto.',
        'original_1': {
            'title': f'Señal 1 original ({fs1} Hz)',
            'domain': 'continuous',
            't': t1.tolist(),
            'x': x1.tolist(),
        },
        'original_2': {
            'title': f'Señal 2 original ({fs2} Hz)',
            'domain': 'continuous',
            't': t2.tolist(),
            'x': x2.tolist(),
        },
        'oversampled_1': {
            'title': f'Señal 1 sobremuestreada ({fs_common} Hz)',
            'domain': 'continuous',
            't': t_common.tolist(),
            'x': y1.tolist(),
        },
        'oversampled_2': {
            'title': f'Señal 2 sobremuestreada ({fs_common} Hz)',
            'domain': 'continuous',
            't': t_common.tolist(),
            'x': y2.tolist(),
        },
        'sum_signal': {
            'title': 'Suma de señales sobremuestreadas',
            'domain': 'continuous',
            't': t_common.tolist(),
            'x': y_sum.tolist(),
        },
    }
