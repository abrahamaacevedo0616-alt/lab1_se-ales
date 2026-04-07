from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from signals.base_signals import get_signal_by_key, get_signal_catalog
from signals.continuous_ops import continuous_sum_operation
from signals.file_ops import process_sampled_files
from signals.transformations import (
    ALLOWED_A,
    ALLOWED_M,
    ALLOWED_N0,
    ALLOWED_T0,
    INTERP_METHODS,
    interpolate_discrete,
    transform_continuous,
    transform_discrete,
)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        catalog=get_signal_catalog(),
        allowed_a=ALLOWED_A,
        allowed_t0=ALLOWED_T0,
        allowed_m=ALLOWED_M,
        allowed_n0=ALLOWED_N0,
        interp_methods=INTERP_METHODS,
    )


@app.route('/api/signals')
def api_signals():
    return jsonify(get_signal_catalog())


@app.route('/api/signals/<signal_key>')
def api_signal(signal_key: str):
    return jsonify(get_signal_by_key(signal_key))


@app.route('/api/transform', methods=['POST'])
def api_transform():
    payload = request.get_json(force=True)
    signal_key = payload['signal_key']
    method = payload['method']
    domain = payload['domain']

    try:
        if domain == 'continuous':
            result = transform_continuous(
                signal_key=signal_key,
                a_mag=float(payload['scale_mag']),
                a_sign=payload['scale_sign'],
                t0=int(payload['shift_mag']),
                shift_sign=payload['shift_sign'],
                method=method,
            )
        else:
            result = transform_discrete(
                signal_key=signal_key,
                m_mag=float(payload['scale_mag']),
                m_sign=payload['scale_sign'],
                n0=int(payload['shift_mag']),
                shift_sign=payload['shift_sign'],
                method=method,
                interp_mode=payload.get('interp_mode', 'zero'),
            )
        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 400


@app.route('/api/continuous-operation', methods=['POST'])
def api_continuous_operation():
    payload = request.get_json(force=True)
    try:
        result = continuous_sum_operation(signal_key=payload['signal_key'])
        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 400


@app.route('/api/interpolate', methods=['POST'])
def api_interpolate():
    payload = request.get_json(force=True)
    try:
        result = interpolate_discrete(
            signal_key=payload['signal_key'],
            L=int(payload['factor']),
            mode=payload['mode'],
        )
        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 400




@app.route('/api/file-sum', methods=['POST'])
def api_file_sum():
    try:
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        mode = request.form.get('mode', 'linear')
        result = process_sampled_files(file1, file2, fs1=2000, fs2=2200, mode=mode)
        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5001)
