from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import numpy as np

# Подключение калькулятора
try:
    from . import calculator
except ImportError:
    import calculator

app = Flask(__name__, static_folder='static')
CORS(app)

# -------------------
# API маршруты
# -------------------
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

# -------------------
# Отдача React фронта
# -------------------
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# -------------------
# Запуск локально
# -------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

