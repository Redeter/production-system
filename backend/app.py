from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import numpy as np
import sys
import traceback

# Добавляем текущую директорию в путь для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Подключение калькулятора
try:
    import calculator
    print("✓ Calculator module imported successfully")
except ImportError as e:
    print(f"✗ Error importing calculator: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Files in directory: {os.listdir(current_dir)}")
    # Создаем заглушку если модуль не найден
    class CalculatorStub:
        def generate_suitable_values(self):
            return {"X1": 1.0, "X2": 1.0}
        def get_test_values(self):
            return {
                'initialValues': {"X1": 2, "X2": 4},
                'parameters': {"T": 50, "dt": 0.5},
                'functions': {"f1": {"a": 0.001, "b": -0.02, "c": 0.15, "d": 0.1}}
            }
        def integrate(self, *args, **kwargs):
            return [0, 1, 2], [[1.0]*18, [1.1]*18, [1.2]*18], [1.0]*18, [1.0]*18, [1.0]*18, [1.0]*18
        def create_plots(self, *args, **kwargs):
            return "stub_plot"
        def create_all_radar_plots(self, *args, **kwargs):
            return {
                'initial': 'stub_radar0',
                'quarter1': 'stub_radar1',
                'quarter2': 'stub_radar2', 
                'quarter3': 'stub_radar3',
                'final': 'stub_radar4'
            }
    
    calculator = CalculatorStub()

app = Flask(__name__, static_folder='static')
CORS(app)

# -------------------
# API маршруты
# -------------------
@app.route('/api/generate-values', methods=['GET', 'OPTIONS'])
def generate_values():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        print("=== GENERATE VALUES ENDPOINT CALLED ===")
        values = calculator.generate_suitable_values()
        print("✓ Values generated successfully")
        return jsonify({'success': True, 'data': values})
    except Exception as e:
        print(f"✗ Error in generate_values: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test-values', methods=['GET', 'OPTIONS'])
def get_test_values():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        print("=== TEST VALUES ENDPOINT CALLED ===")
        test_values = calculator.get_test_values()
        print("✓ Test values retrieved successfully")
        return jsonify({'success': True, 'data': test_values})
    except Exception as e:
        print(f"✗ Error in get_test_values: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        print("=== CALCULATE ENDPOINT CALLED ===")
        
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400
        
        # Проверяем структуру данных
        print(f"Data keys: {list(data.keys())}")
        
        # Извлекаем начальные значения
        initial_values = data.get('initialValues', {})
        print(f"Initial values keys: {list(initial_values.keys())}")
        
        # Создаем X0 с значениями по умолчанию
        X0 = []
        for i in range(18):
            key = f'X{i+1}'
            value = initial_values.get(key, 0.1)
            # Преобразуем в float, обрабатывая пустые строки
            if value == '':
                value = 0.1
            try:
                X0.append(float(value))
            except (ValueError, TypeError):
                X0.append(0.1)
        
        params = data.get('parameters', {})
        functions_data = data.get('functions', {})
        
        print(f"X0: {X0}")
        print(f"Parameters count: {len(params)}")
        print(f"Functions data count: {len(functions_data)}")
        
        # Детальная информация о функциях
        if functions_data:
            print("=== FUNCTIONS DATA ===")
            for i in range(1, min(6, 37)):  # Первые 5 функций
                func_name = f'f{i}'
                if func_name in functions_data:
                    coeffs = functions_data[func_name]
                    print(f"{func_name}: a={coeffs.get('a')}, b={coeffs.get('b')}, c={coeffs.get('c')}, d={coeffs.get('d')}")
        else:
            print("WARNING: No functions data received!")
        
        T = params.get('T', 50.0)
        dt = params.get('dt', 0.5)
        
        # Преобразуем T и dt в float
        try:
            T = float(T) if T != '' else 50.0
            dt = float(dt) if dt != '' else 0.5
        except (ValueError, TypeError):
            T = 50.0
            dt = 0.5
        
        if dt <= 0 or T <= 0:
            return jsonify({'success': False, 'error': 'T и dt должны быть положительными'}), 400

        # Преобразуем функции в формат для калькулятора
        functions_coeffs = {}
        for func_name, coeffs in functions_data.items():
            functions_coeffs[func_name] = {
                'a': float(coeffs.get('a', 0.0) or 0.0),
                'b': float(coeffs.get('b', 0.0) or 0.0),
                'c': float(coeffs.get('c', 0.0) or 0.0),
                'd': float(coeffs.get('d', 0.0) or 0.0)
            }
        
        # Добавляем функции по умолчанию для отсутствующих
        for i in range(1, 37):
            func_name = f'f{i}'
            if func_name not in functions_coeffs:
                functions_coeffs[func_name] = {'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0}
        
        print(f"Processed functions: {len(functions_coeffs)}")
        if 'f1' in functions_coeffs:
            print(f"f1 coefficients: {functions_coeffs['f1']}")

        print("=== STARTING INTEGRATION ===")
        times, Xs, X_quarter1, X_quarter2, X_quarter3, X_final = calculator.integrate(
            calculator.derivatives,
            X0, 0.0, float(T), float(dt),
            params, functions_coeffs
        )

        Xfinal = Xs[-1, :].tolist()
        deltas = (Xs[-1, :] - X0).tolist()

        plot_image = calculator.create_plots(times, Xs)
        radar_images = calculator.create_all_radar_plots(X_quarter1, X_quarter2, X_quarter3, X_final, X0)

        max_abs_delta = float(np.max(np.abs(deltas)))
        mean_abs_delta = float(np.mean(np.abs(deltas)))

        print(f"=== CALCULATION COMPLETED ===")
        print(f"Final values: {[f'{x:.4f}' for x in Xfinal]}")
        print(f"Deltas: {[f'{d:.4f}' for d in deltas]}")
        print("=" * 50)

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
                'radar': radar_images
            }
        })
    except Exception as e:
        print(f"!!! ERROR IN CALCULATE: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'calculator': 'loaded'})

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
    print("Starting Flask server...")
    print(f"Python path: {sys.path}")
    print(f"Working directory: {current_dir}")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)