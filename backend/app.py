from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np


try:
    from . import calculator
except ImportError:
    import calculator

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({
        "message": "Backend is running successfully 🚀",
        "endpoints": [
            "/api/generate-values",
            "/api/calculate",
            "/api/default-coefficients"
        ]
    })

@app.route('/api/generate-values', methods=['GET'])
def generate_values():
    try:
        values = calculator.generate_suitable_values()
        return jsonify({'success': True, 'data': values})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()

        X0 = [data['initialValues'][f'X{i+1}'] for i in range(18)]
        params = data['parameters']
        coeffs = data.get('coefficients', {})

        T = params.get('T', 50.0)
        dt = params.get('dt', 0.5)

        if dt <= 0 or T <= 0:
            return jsonify({'success': False, 'error': 'T и dt должны быть положительными'})

        times, Xs = calculator.integrate(
            calculator.derivatives,
            X0, 0.0, float(T), float(dt),
            params, coeffs
        )

        Xfinal = Xs[-1, :].tolist()
        deltas = (Xs[-1, :] - X0).tolist()

        plot_image = calculator.create_plots(times, Xs)
        radar_image = calculator.create_radar_plot(Xfinal)

        max_abs_delta = float(np.max(np.abs(deltas)))
        mean_abs_delta = float(np.mean(np.abs(deltas)))

        return jsonify({
            'success': True,
            'times': times.tolist(),
            'values': Xs.tolist(),
            'finalValues': Xfinal,
            'deltas': deltas,
            'statistics': {
                'maxAbsDelta': max_abs_delta,
                'meanAbsDelta': mean_abs_delta,
                'steps': len(times)
            },
            'plots': {
                'graphs': plot_image,
                'radar': radar_image
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/default-coefficients', methods=['GET'])
def default_coefficients():
    try:
        coeffs = calculator.make_default_coeffs()
        return jsonify({'success': True, 'coefficients': coeffs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
