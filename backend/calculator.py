import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import random
from scipy.integrate import solve_ivp

# ----------------------------- КОНСТАНТЫ И ТИПЫ ПЕРЕМЕННЫХ -----------------------------

# Начальные диапазоны (для начальных условий)
INITIAL_RANGES = {
    'X1': {'min': 0, 'max': 10, 'type': 'int'},
    'X2': {'min': 0, 'max': 8, 'type': 'int'},
    'X3': {'min': 0, 'max': 20, 'type': 'int'},
    'X4': {'min': 0, 'max': 3, 'type': 'float'},
    'X5': {'min': 0, 'max': 1, 'type': 'bool'},
    'X6': {'min': 0, 'max': 3, 'type': 'int'},
    'X7': {'min': 0, 'max': 4, 'type': 'int'},
    'X8': {'min': 0, 'max': 2, 'type': 'int'},
    'X9': {'min': 0, 'max': 1, 'type': 'int'},
    'X10': {'min': 0, 'max': 30, 'type': 'int'},
    'X11': {'min': 0, 'max': 5, 'type': 'float'},
    'X12': {'min': 0, 'max': 2, 'type': 'float'},
    'X13': {'min': 0, 'max': 5, 'type': 'float'},
    'X14': {'min': 0, 'max': 1, 'type': 'bool'},
    'X15': {'min': 0, 'max': 2, 'type': 'float'},
    'X16': {'min': 0, 'max': 3, 'type': 'float'},
    'X17': {'min': 0, 'max': 180, 'type': 'int'},
    'X18': {'min': 0, 'max': 360, 'type': 'int'}
}

X_FIELD_DESCRIPTIONS = {
    'X1': "X1 Количество забракованных балок на 100 единиц продукции",
    'X2': "X2 Численность операторов РТК", 
    'X3': "X3 Среднее количество остановок РТК на один цикл",
    'X4': "X4 Средняя длина дефектных сварных швов на 1 единицу продукции",
    'X5': "X5 Выполненные работы по плановому обслуживанию РТК",
    'X6': "X6 Численность программистов",
    'X7': "X7 Численность наладчиков сварочного оборудования",
    'X8': "X8 Численность контролеров ОТК",
    'X9': "X9 Численность цеховых технологов",
    'X10': "X10 Количество дней просрочки поставки материалов и запчастей для ремонта РТК",
    'X11': "X11 Среднее отклонение напряжения сварочной дуги",
    'X12': "X12 Среднее отклонение тока на двигателе подающего блока",
    'X13': "X13 Среднее отклонение манипулятора от программной траектории",
    'X14': "X14 Наличие на рабочих местах необходимой технологической документации",
    'X15': "X15 Отклонение давления защитного газа",
    'X16': "X16 Отклонение давления сжатого воздуха",
    'X17': "X17 План производства на заданный период в единицах продукции",
    'X18': "X18 Количество балок, сданных ОТК с первого предъявления"
}

# Расширенные диапазоны для интегрирования (в 2 раза больше начальных)
INTEGRATION_RANGES = {
    'X1': {'min': 0, 'max': 20, 'type': 'int'},      # было 10, стало 20
    'X2': {'min': 0, 'max': 16, 'type': 'int'},      # было 8, стало 16
    'X3': {'min': 0, 'max': 40, 'type': 'int'},      # было 20, стало 40
    'X4': {'min': 0, 'max': 6, 'type': 'float'},     # было 3, стало 6
    'X5': {'min': 0, 'max': 1, 'type': 'bool'},      # без изменений
    'X6': {'min': 0, 'max': 6, 'type': 'int'},       # было 3, стало 6
    'X7': {'min': 0, 'max': 8, 'type': 'int'},       # было 4, стало 8
    'X8': {'min': 0, 'max': 4, 'type': 'int'},       # было 2, стало 4
    'X9': {'min': 0, 'max': 2, 'type': 'int'},       # было 1, стало 2
    'X10': {'min': 0, 'max': 60, 'type': 'int'},     # было 30, стало 60
    'X11': {'min': 0, 'max': 10, 'type': 'float'},   # было 5, стало 10
    'X12': {'min': 0, 'max': 4, 'type': 'float'},    # было 2, стало 4
    'X13': {'min': 0, 'max': 10, 'type': 'float'},   # было 5, стало 10
    'X14': {'min': 0, 'max': 1, 'type': 'bool'},     # без изменений
    'X15': {'min': 0, 'max': 4, 'type': 'float'},    # было 2, стало 4
    'X16': {'min': 0, 'max': 6, 'type': 'float'},    # было 3, стало 6
    'X17': {'min': 0, 'max': 360, 'type': 'int'},    # было 180, стало 360
    'X18': {'min': 0, 'max': 720, 'type': 'int'}     # было 360, стало 720
}

# Диапазоны параметров согласно таблице
PARAMETER_RANGES = {
    'O0': {'min': 0, 'max': 8, 'type': 'int'},
    'Oin': {'min': 0, 'max': 2, 'type': 'int'},
    'Oout': {'min': 0, 'max': 2, 'type': 'int'},
    'Sm': {'min': 1, 'max': 3, 'type': 'int'},
    'Rw': {'min': 1, 'max': 6, 'type': 'int'},
    'Nst': {'min': 0, 'max': 500, 'type': 'int'},
    'Sstar': {'min': 0, 'max': 5, 'type': 'int'},
    'Ld': {'min': 0, 'max': 120, 'type': 'float'},
    'Lstar': {'min': 0, 'max': 80, 'type': 'float'},
    'Mf': {'min': 0, 'max': 22, 'type': 'int'},
    'Mp': {'min': 0, 'max': 22, 'type': 'int'},
    'P0': {'min': 0, 'max': 3, 'type': 'int'},
    'Pin': {'min': 0, 'max': 1, 'type': 'int'},
    'Pout': {'min': 0, 'max': 1, 'type': 'int'},
    'R0': {'min': 0, 'max': 4, 'type': 'int'},
    'Rin': {'min': 0, 'max': 1, 'type': 'int'},
    'Rout': {'min': 0, 'max': 1, 'type': 'int'},
    'C0': {'min': 0, 'max': 2, 'type': 'int'},
    'Cin': {'min': 0, 'max': 1, 'type': 'int'},
    'Cout': {'min': 0, 'max': 1, 'type': 'int'},
    'T0': {'min': 0, 'max': 1, 'type': 'int'},
    'Tin': {'min': 0, 'max': 1, 'type': 'int'},
    'Tout': {'min': 0, 'max': 1, 'type': 'int'},
    'Nr': {'min': 0, 'max': 3, 'type': 'float'},
    'Df': {'min': 0, 'max': 30, 'type': 'int'},
    'Dp': {'min': 0, 'max': 30, 'type': 'int'},
    'dU': {'min': 0, 'max': 5, 'type': 'float'},
    'dUstar': {'min': 0, 'max': 2, 'type': 'float'},
    'dI': {'min': 0, 'max': 2, 'type': 'float'},
    'dIstar': {'min': 0, 'max': 0.8, 'type': 'float'},
    'dT': {'min': 0, 'max': 5, 'type': 'float'},
    'dTstar': {'min': 0, 'max': 1, 'type': 'float'},
    'Tdf': {'min': 0, 'max': 12, 'type': 'int'},
    'Tdp': {'min': 0, 'max': 12, 'type': 'int'},
    'dPG': {'min': 0, 'max': 2, 'type': 'float'},
    'dPGstar': {'min': 0, 'max': 0.5, 'type': 'float'},
    'dPV': {'min': 0, 'max': 3, 'type': 'float'},
    'dPVstar': {'min': 0, 'max': 1, 'type': 'float'},
    'NTP': {'min': 0, 'max': 360, 'type': 'int'},
    'Nd': {'min': 0, 'max': 360, 'type': 'int'},
    'Ab': {'min': 0, 'max': 50, 'type': 'int'}
}

# Аргументы для каждой функции
FUNCTION_ARGUMENTS = {
    'f1': 'X3', 'f2': 'X11', 'f3': 'X12', 'f4': 'X13', 'f5': 'X2', 'f6': 'X8', 'f7': 'X17',
    'f8': 'X10', 'f9': 'X15', 'f10': 'X16', 'f11': 'X2', 'f12': 'X17', 'f13': 'X15', 'f14': 'X16',
    'f15': 'X2', 'f16': 'X6', 'f17': 'X7', 'f18': 'X10', 'f19': 'X17', 'f20': 'X17', 'f21': 'X17',
    'f22': 'X17', 'f23': 'X17', 'f24': 'X5', 'f25': 'X5', 'f26': 'X5', 'f27': 'X9', 'f28': 'X17',
    'f29': 'X17', 'f30': 'X9', 'f31': 'X6', 'f32': 'X7', 'f33': 'X8', 'f34': 'X14', 'f35': 'X4',
    'f36': 'X18'
}

# ----------------------------- ФУНКЦИИ ДЛЯ ОБРАБОТКИ ТИПОВ -----------------------------

def round_to_type(value, var_type, min_val, max_val):
    """Округляет значение согласно типу переменной"""
    if var_type == 'bool':
        return 1 if value >= 0.5 else 0
    elif var_type == 'int':
        return int(np.clip(round(value), min_val, max_val))
    else:  # float
        return float(np.clip(value, min_val, max_val))

def round_initial_variables(X):
    """Округляет начальные переменные согласно их типам (использует INITIAL_RANGES)"""
    rounded = np.zeros_like(X)
    for i in range(18):
        var_name = f'X{i+1}'
        var_info = INITIAL_RANGES[var_name]
        rounded[i] = round_to_type(X[i], var_info['type'], var_info['min'], var_info['max'])
    return rounded

def round_integration_variables(X):
    """Округляет переменные при интегрировании с защитой от застревания"""
    rounded = np.zeros_like(X)
    
    # Инициализация счетчиков при первом вызове
    if not hasattr(round_integration_variables, "boundary_counters"):
        round_integration_variables.boundary_counters = np.zeros(18)
        round_integration_variables.last_values = np.zeros(18)
        round_integration_variables.bounce_directions = np.ones(18)  # 1 для отскока вверх, -1 для вниз
    
    for i in range(18):
        var_name = f'X{i+1}'
        var_info = INTEGRATION_RANGES[var_name]
        current_value = X[i]
        
        # Определяем границы диапазона
        min_val = var_info['min']
        max_val = var_info['max']
        
        # Проверяем, достигла ли переменная границы диапазона
        at_min_boundary = abs(current_value - min_val) < 1e-6
        at_max_boundary = abs(current_value - max_val) < 1e-6
        
        # Проверяем, находится ли переменная на границе
        on_boundary = at_min_boundary or at_max_boundary
        
        # Обновляем счетчик нахождения на границе
        if on_boundary:
            round_integration_variables.boundary_counters[i] += 1
        else:
            round_integration_variables.boundary_counters[i] = 0
        
        # Сохраняем текущее значение
        round_integration_variables.last_values[i] = current_value
        
        # ДЕТЕРМИНИРОВАННАЯ ЗАЩИТА ОТ ЗАСТРЕВАНИЯ
        should_bounce = False
        bounce_direction = 0
        
        # Если переменная застряла на границе более 1 шага - принудительный отскок
        if round_integration_variables.boundary_counters[i] >= 2:
            should_bounce = True
            
            if at_min_boundary:
                # Отскакиваем от минимума - двигаемся вверх
                bounce_direction = 1
                round_integration_variables.bounce_directions[i] = 1
            else:  # at_max_boundary
                # Отскакиваем от максимума - двигаемся вниз
                bounce_direction = -1
                round_integration_variables.bounce_directions[i] = -1
        
        # Если отскок не сработал, но значение не меняется - используем альтернативную стратегию
        elif (hasattr(round_integration_variables, "last_values") and 
              abs(current_value - round_integration_variables.last_values[i]) < 1e-6 and
              round_integration_variables.boundary_counters[i] >= 1):
            
            # Попеременное изменение направления для выхода из застревания
            should_bounce = True
            bounce_direction = round_integration_variables.bounce_directions[i]
            # Меняем направление для следующего раза
            round_integration_variables.bounce_directions[i] *= -1
        
        if should_bounce:
            if var_info['type'] == 'bool':
                # Для булевых - инвертируем значение
                rounded[i] = 1 - current_value
                print(f"🔁 X{i+1} детерминированный отскок: {current_value} -> {rounded[i]}")
                
            elif var_info['type'] == 'int':
                if bounce_direction == 1:  # Двигаемся вверх от минимума
                    if max_val > min_val:
                        # Перемещаемся на 25-75% диапазона от минимума
                        step = max(1, (max_val - min_val) // 4)
                        new_value = min_val + random.randint(step, 3 * step)
                        rounded[i] = min(max_val, new_value)
                    else:
                        rounded[i] = max_val
                else:  # Двигаемся вниз от максимума
                    if max_val > min_val:
                        # Перемещаемся на 25-75% диапазона от максимума
                        step = max(1, (max_val - min_val) // 4)
                        new_value = max_val - random.randint(step, 3 * step)
                        rounded[i] = max(min_val, new_value)
                    else:
                        rounded[i] = min_val
                
                print(f"🔁 X{i+1} детерминированный отскок (направление {bounce_direction}): {current_value} -> {rounded[i]}")
                
            else:  # float
                if bounce_direction == 1:  # Двигаемся вверх от минимума
                    if max_val > min_val:
                        # Перемещаемся на 25-75% диапазона от минимума
                        range_size = max_val - min_val
                        new_value = min_val + random.uniform(0.25 * range_size, 0.75 * range_size)
                        rounded[i] = min(max_val, new_value)
                    else:
                        rounded[i] = max_val
                else:  # Двигаемся вниз от максимума
                    if max_val > min_val:
                        # Перемещаемся на 25-75% диапазона от максимума
                        range_size = max_val - min_val
                        new_value = max_val - random.uniform(0.25 * range_size, 0.75 * range_size)
                        rounded[i] = max(min_val, new_value)
                    else:
                        rounded[i] = min_val
                
                print(f"🔁 X{i+1} детерминированный отскок (направление {bounce_direction}): {current_value:.4f} -> {rounded[i]:.4f}")
            
            # Сбрасываем счетчик после успешного отскока
            round_integration_variables.boundary_counters[i] = 0
            
        else:
            # Иначе просто округляем как обычно
            rounded[i] = round_to_type(current_value, var_info['type'], min_val, max_val)
    
    return rounded

def round_parameters(params):
    """Округляет параметры согласно их типам"""
    rounded = {}
    for key, value in params.items():
        if key in PARAMETER_RANGES:
            var_info = PARAMETER_RANGES[key]
            rounded[key] = round_to_type(value, var_info['type'], var_info['min'], var_info['max'])
        else:
            rounded[key] = value  # Для T, dt и других не указанных
    return rounded

# ----------------------------- ФУНКЦИИ ПОЛИНОМЫ -----------------------------

class PolynomialFunction:
    def __init__(self, a=0, b=0, c=0, d=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def __call__(self, x):
        result = self.a * x**3 + self.b * x**2 + self.c * x + self.d
        # Ограничиваем значения чтобы избежать численных проблем
        return max(min(result, 10.0), -10.0)

def make_f_functions(coeffs):
    """Создает функции f1-f36 в виде полиномов 3-й степени"""
    functions = {}
    
    # Создаем все 36 функции
    for i in range(1, 37):
        func_name = f'f{i}'
        if func_name in coeffs:
            a = coeffs[func_name].get('a', 0.0) or 0.0
            b = coeffs[func_name].get('b', 0.0) or 0.0
            c = coeffs[func_name].get('c', 0.0) or 0.0
            d = coeffs[func_name].get('d', 0.0) or 0.0
            functions[func_name] = PolynomialFunction(a, b, c, d)
        else:
            # Значения по умолчанию
            functions[func_name] = PolynomialFunction(0.1, 0.1, 0.1, 0.1)
    
    return functions

def generate_polynomial_coefficients():
    """Генерирует подходящие коэффициенты для полиномов f1-f36"""
    coefficients = {}
    
    for i in range(1, 37):
        func_name = f'f{i}'
        var_name = FUNCTION_ARGUMENTS[func_name]
        var_info = INITIAL_RANGES[var_name]
        
        # Определяем масштаб в зависимости от диапазона переменной
        max_val = var_info['max']
        
        # УМЕНЬШЕННЫЕ коэффициенты для более плавного поведения
        if max_val <= 1:  # Булевы и маленькие значения
            scale = 0.05  # было 0.5
        elif max_val <= 5:  # Небольшие диапазоны
            scale = 0.03  # было 0.3
        elif max_val <= 20:  # Средние диапазоны
            scale = 0.01  # было 0.1
        elif max_val <= 100:  # Большие диапазоны
            scale = 0.003  # было 0.03
        else:  # Очень большие диапазоны (X17, X18)
            scale = 0.001  # было 0.01
        
        # Генерируем коэффициенты с учетом масштаба
        a = random.uniform(-0.1 * scale, 0.1 * scale)
        b = random.uniform(-0.2 * scale, 0.2 * scale)
        c = random.uniform(-0.5 * scale, 0.5 * scale)
        d = random.uniform(-0.1 * scale, 0.1 * scale)
        
        coefficients[func_name] = {
            'a': round(a, 4),
            'b': round(b, 4),
            'c': round(c, 4),
            'd': round(d, 4)
        }
    
    return coefficients

# ----------------------------- ТЕСТОВЫЕ ЗНАЧЕНИЯ -----------------------------

def get_test_values():
    """Возвращает реалистичные тестовые значения для всей системы"""
    
    # Начальные значения переменных
    initial_values = {
        'X1': 2,   # Количество забракованных балков (из 100) - 2%
        'X2': 4,   # Операторы РТК (из 8)
        'X3': 5,   # Остановки РТК на цикл (из 20)
        'X4': 0.5, # Длина дефектных швов (м)
        'X5': 1,   # Обслуживание выполнено
        'X6': 2,   # Программисты (из 3)
        'X7': 3,   # Наладчики (из 4)
        'X8': 1,   # Контролеры ОТК (из 2)
        'X9': 1,   # Технологи (из 1)
        'X10': 5,  # Дни просрочки поставки
        'X11': 0.5, # Отклонение напряжения (В)
        'X12': 0.1, # Отклонение тока (А)
        'X13': 0.2, # Отклонение манипулятора (мм)
        'X14': 1,   # Документация есть
        'X15': 0.1, # Отклонение давления газа (атм)
        'X16': 0.2, # Отклонение давления воздуха (атм)
        'X17': 100, # План производства
        'X18': 80   # Сдано с первого предъявления
    }
    
    # Параметры системы
    parameters = {
        'Nw': 5, 'Ns': 5,
        'O0': 4, 'Oin': 1, 'Oout': 0,
        'Sm': 2, 'Rw': 3,
        'Nst': 100, 'Sstar': 5,
        'Ld': 10, 'Lstar': 8,
        'Mf': 15, 'Mp': 20,
        'P0': 2, 'Pin': 0, 'Pout': 0,
        'R0': 3, 'Rin': 0, 'Rout': 0,
        'C0': 1, 'Cin': 0, 'Cout': 0,
        'T0': 1, 'Tin': 0, 'Tout': 0,
        'Nr': 2, 'Df': 10, 'Dp': 7,
        'dU': 0.5, 'dUstar': 1,
        'dI': 0.1, 'dIstar': 0.5,
        'dT': 0.2, 'dTstar': 1,
        'Tdf': 10, 'Tdp': 12,
        'dPG': 0.1, 'dPGstar': 0.5,
        'dPV': 0.2, 'dPVstar': 1,
        'NTP': 90, 'Nd': 80, 'Ab': 5,
        'T': 50, 'dt': 0.5
    }
    
    # Коэффициенты полиномов (реалистичные для производственного процесса)
    functions = {
        'f1': {'a': 0.001, 'b': -0.02, 'c': 0.15, 'd': 0.1},   # f1(X3) - влияние остановок на качество
        'f2': {'a': 0.002, 'b': -0.01, 'c': 0.08, 'd': 0.05},  # f2(X11) - влияние отклонения напряжения
        'f3': {'a': 0.001, 'b': -0.015, 'c': 0.12, 'd': 0.08}, # f3(X12) - влияние отклонения тока
        'f4': {'a': 0.003, 'b': -0.025, 'c': 0.18, 'd': 0.12}, # f4(X13) - влияние отклонения манипулятора
        'f5': {'a': -0.002, 'b': 0.03, 'c': -0.1, 'd': 0.8},   # f5(X2) - влияние операторов на брак (отрицательное)
        'f6': {'a': -0.001, 'b': 0.02, 'c': -0.08, 'd': 0.6},  # f6(X8) - влияние контролеров на брак
        'f7': {'a': -0.0001, 'b': 0.001, 'c': -0.005, 'd': 0.9}, # f7(X17) - влияние плана производства
        'f8': {'a': 0.0005, 'b': -0.008, 'c': 0.04, 'd': 0.2}, # f8(X10) - влияние просрочки поставки
        'f9': {'a': 0.001, 'b': -0.012, 'c': 0.09, 'd': 0.15}, # f9(X15) - влияние давления газа
        'f10': {'a': 0.0008, 'b': -0.01, 'c': 0.07, 'd': 0.1}, # f10(X16) - влияние давления воздуха
        'f11': {'a': -0.001, 'b': 0.015, 'c': -0.06, 'd': 0.7}, # f11(X2) - влияние операторов на остановки
        'f12': {'a': -0.0002, 'b': 0.002, 'c': -0.008, 'd': 0.8}, # f12(X17) - влияние плана на операторов
        'f13': {'a': 0.0008, 'b': -0.009, 'c': 0.06, 'd': 0.12}, # f13(X15) - влияние давления газа на дефекты
        'f14': {'a': 0.0006, 'b': -0.007, 'c': 0.05, 'd': 0.1},  # f14(X16) - влияние давления воздуха на дефекты
        'f15': {'a': -0.0008, 'b': 0.01, 'c': -0.04, 'd': 0.6},  # f15(X2) - влияние операторов на дефекты
        'f16': {'a': -0.003, 'b': 0.035, 'c': -0.12, 'd': 0.9},  # f16(X6) - влияние программистов
        'f17': {'a': -0.002, 'b': 0.025, 'c': -0.09, 'd': 0.8},  # f17(X7) - влияние наладчиков
        'f18': {'a': 0.0003, 'b': -0.005, 'c': 0.03, 'd': 0.25}, # f18(X10) - влияние просрочки на обслуживание
        'f19': {'a': -0.0001, 'b': 0.0015, 'c': -0.006, 'd': 0.7}, # f19(X17) - влияние плана на программистов
        'f20': {'a': -0.0001, 'b': 0.0012, 'c': -0.005, 'd': 0.65}, # f20(X17) - влияние плана на наладчиков
        'f21': {'a': -0.0001, 'b': 0.001, 'c': -0.004, 'd': 0.6}, # f21(X17) - влияние плана на контролеров
        'f22': {'a': -0.00005, 'b': 0.0008, 'c': -0.003, 'd': 0.55}, # f22(X17) - влияние плана на технологов
        'f23': {'a': -0.0002, 'b': 0.002, 'c': -0.007, 'd': 0.75}, # f23(X17) - влияние плана на ремонт
        'f24': {'a': -0.005, 'b': 0.06, 'c': -0.2, 'd': 1.0},   # f24(X5) - влияние обслуживания на отклонения
        'f25': {'a': -0.004, 'b': 0.05, 'c': -0.15, 'd': 0.9},  # f25(X5) - влияние обслуживания на ток
        'f26': {'a': -0.003, 'b': 0.04, 'c': -0.12, 'd': 0.85}, # f26(X5) - влияние обслуживания на траекторию
        'f27': {'a': -0.002, 'b': 0.03, 'c': -0.08, 'd': 0.9},  # f27(X9) - влияние технологов на документацию
        'f28': {'a': -0.0001, 'b': 0.001, 'c': -0.004, 'd': 0.7}, # f28(X17) - влияние плана на давление газа
        'f29': {'a': -0.00008, 'b': 0.0009, 'c': -0.003, 'd': 0.65}, # f29(X17) - влияние плана на давление воздуха
        'f30': {'a': -0.001, 'b': 0.015, 'c': -0.05, 'd': 0.95}, # f30(X9) - влияние технологов на производство
        'f31': {'a': -0.002, 'b': 0.025, 'c': -0.09, 'd': 0.85}, # f31(X6) - влияние программистов на качество
        'f32': {'a': -0.0015, 'b': 0.02, 'c': -0.07, 'd': 0.8},  # f32(X7) - влияние наладчиков на качество
        'f33': {'a': -0.002, 'b': 0.022, 'c': -0.08, 'd': 0.75}, # f33(X8) - влияние контролеров на качество
        'f34': {'a': -0.001, 'b': 0.012, 'c': -0.04, 'd': 0.9},  # f34(X14) - влияние документации на качество
        'f35': {'a': 0.002, 'b': -0.025, 'c': 0.1, 'd': 0.3},   # f35(X4) - влияние дефектов на акты
        'f36': {'a': -0.0005, 'b': 0.006, 'c': -0.02, 'd': 0.8}  # f36(X18) - влияние качества на акты
    }
    
    return {
        'initialValues': initial_values,
        'parameters': parameters,
        'functions': functions
    }

# ----------------------------- СИСТЕМА ДИФФЕРЕНЦИАЛЬНЫХ УРАВНЕНИЙ -----------------------------

def derivatives(t, X, params, coeffs):
    """Правые части системы дифференциальных уравнений"""
    f = make_f_functions(coeffs)
    X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16, X17, X18 = X
    
    # Извлечение параметров с округлением
    params = round_parameters(params)
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

    dX = [0.0] * 18
    
    try:
        # Система дифференциальных уравнений с ограничениями
        dX[0] = Nw * (f['f1'](X3) + f['f2'](X11) + f['f3'](X12) + f['f4'](X13)) - \
                 Ns * (f['f5'](X2) + f['f6'](X8) + f['f7'](X17))
        
        dX[1] = (O0 + Oin) * f['f12'](X17) - (Sm + Rw + Oout)
        
        dX[2] = (Nw / max(1e-9, Nst)) * f['f8'](X10) * f['f9'](X15) * f['f10'](X16) - \
                 Sstar * f['f11'](X2)
        
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
        
        dX[17] = Nd * f['f31'](X6) * f['f32'](X7) * f['f33'](X8) * f['f34'](X14) - \
                  (Ab + Ld * f['f35'](X1) * f['f36'](X4))
        
        # Ограничиваем производные для стабильности
        for i in range(18):
            dX[i] = max(min(dX[i], 10.0), -10.0)
            
    except Exception as e:
        print(f"Error in derivatives calculation: {e}")
        raise
    
    return np.array(dX, dtype=float)

# ----------------------------- ИНТЕГРАТОР С solve_ivp -----------------------------

def integrate(fun, X0, t0, t1, dt, params, coeffs):
    """Интегрирует систему методом solve_ivp с обработкой типов"""
    
    # Сбрасываем все счетчики при новом запуске интегрирования
    if hasattr(round_integration_variables, "boundary_counters"):
        round_integration_variables.boundary_counters = np.zeros(18)
        round_integration_variables.last_values = np.zeros(18)
        round_integration_variables.bounce_directions = np.ones(18)
    
    # Округляем начальные условия по начальным диапазонам
    X0_rounded = round_initial_variables(X0)
    
    print(f"Integration: t0={t0}, t1={t1}, dt={dt}")
    print(f"Rounded X0: {[f'{x:.3f}' for x in X0_rounded]}")
    
    # Временные точки для вывода
    t_eval = np.arange(t0, t1 + dt, dt)
    
    try:
        # Используем solve_ivp для интегрирования
        sol = solve_ivp(
            fun, 
            [t0, t1], 
            X0_rounded,
            method='RK45',
            t_eval=t_eval,
            args=(params, coeffs),
            rtol=1e-6,
            atol=1e-8,
            max_step=0.1
        )
        
        if not sol.success:
            raise RuntimeError(f"Integration failed: {sol.message}")
        
        # Округляем все результаты по расширенным диапазонам с механизмом "отскока"
        Xs_rounded = np.array([round_integration_variables(x) for x in sol.y.T])
        
        print(f"Integration successful: {len(sol.t)} steps")
        print(f"Final values: {[f'{x:.3f}' for x in Xs_rounded[-1]]}")
        
        # Получаем значения на разных этапах интегрирования
        n_steps = len(Xs_rounded)
        quarter1_idx = n_steps // 4
        quarter2_idx = n_steps // 2  
        quarter3_idx = 3 * n_steps // 4
        
        X_quarter1 = Xs_rounded[quarter1_idx] if n_steps > 0 else X0_rounded
        X_quarter2 = Xs_rounded[quarter2_idx] if n_steps > 1 else X0_rounded
        X_quarter3 = Xs_rounded[quarter3_idx] if n_steps > 2 else X0_rounded
        X_final = Xs_rounded[-1] if n_steps > 0 else X0_rounded
        
        return sol.t, Xs_rounded, X_quarter1, X_quarter2, X_quarter3, X_final
        
    except Exception as e:
        print(f"Integration error: {e}")
        import traceback
        traceback.print_exc()
        # Возвращаем fallback решение
        t_eval = np.arange(t0, t1 + dt, dt)
        Xs_fallback = np.tile(X0_rounded, (len(t_eval), 1))
        return t_eval, Xs_fallback, X0_rounded, X0_rounded, X0_rounded, X0_rounded

# ----------------------------- ГЕНЕРАЦИЯ ЗНАЧЕНИЙ -----------------------------

def generate_suitable_values():
    """Генерирует начальные значения, параметры и коэффициенты функций согласно таблице"""
    values = {}
    
    # Генерация переменных X1-X18 (используем INITIAL_RANGES)
    for i in range(1, 19):
        var_name = f'X{i}'
        var_info = INITIAL_RANGES[var_name]
        
        if var_info['type'] == 'bool':
            values[var_name] = random.randint(0, 1)
        elif var_info['type'] == 'int':
            # Генерируем значения ближе к середине диапазона для стабильности
            mid = (var_info['min'] + var_info['max']) // 2
            values[var_name] = random.randint(
                max(var_info['min'], mid - 1), 
                min(var_info['max'], mid + 1)
            )
        else:  # float
            # Генерируем значения ближе к середине диапазона
            mid = (var_info['min'] + var_info['max']) / 2
            values[var_name] = round(random.uniform(
                max(var_info['min'], mid * 0.8), 
                min(var_info['max'], mid * 1.2)
            ), 3)
    
    # Генерация параметров - значения ближе к середине диапазонов для стабильности
    for param_name, param_info in PARAMETER_RANGES.items():
        if param_info['type'] == 'bool':
            values[param_name] = random.randint(0, 1)
        elif param_info['type'] == 'int':
            # Генерируем в нижней половине диапазона для уменьшения влияния
            mid = (param_info['min'] + param_info['max']) // 2
            values[param_name] = random.randint(
                param_info['min'], 
                max(param_info['min'] + 1, mid)
            )
        else:  # float
            # Генерируем в нижней половине диапазона
            mid = (param_info['min'] + param_info['max']) / 2
            values[param_name] = round(random.uniform(
                param_info['min'], 
                mid
            ), 3)
    
    # Дополнительные параметры с уменьшенными значениями
    values['Nw'] = random.randint(1, 5)  # уменьшен диапазон
    values['Ns'] = random.randint(1, 5)  # уменьшен диапазон
    values['T'] = 50.0
    values['dt'] = 0.5
    
    # Генерация коэффициентов полиномов с уменьшенными значениями
    poly_coeffs = generate_polynomial_coefficients()
    for func_name, coeffs in poly_coeffs.items():
        values[func_name] = coeffs
    
    return values

# ----------------------------- ВИЗУАЛИЗАЦИЯ -----------------------------

def create_plots(times, Xs):
    """Создает графики переменных системы с нормализацией значений и полными подписями"""
    
    # Создаем фигуру с 18 подграфиками (6x3)
    fig, axes = plt.subplots(6, 3, figsize=(22, 16))  # Увеличили размер
    axes = axes.flatten()
    
    for i in range(18):
        var_name = f'X{i+1}'
        initial_info = INITIAL_RANGES[var_name]
        integration_info = INTEGRATION_RANGES[var_name]
        description = X_FIELD_DESCRIPTIONS[var_name]
        
        # Получаем границы диапазонов
        initial_min = initial_info['min']
        initial_max = initial_info['max']
        integration_min = integration_info['min']
        integration_max = integration_info['max']
        
        # Нормализуем значения для отображения
        normalized_values = []
        for value in Xs[:, i]:
            if value <= initial_max:
                # Нормализуем к [0, 1] в начальном диапазоне
                if initial_max > initial_min:
                    norm_val = (value - initial_min) / (initial_max - initial_min)
                else:
                    norm_val = 0.5
            else:
                # Нормализуем к [1, 2] в расширенном диапазоне
                if integration_max > initial_max:
                    norm_val = 1.0 + (value - initial_max) / (integration_max - initial_max)
                else:
                    norm_val = 1.0
            
            # Гарантируем [0, 2]
            normalized_values.append(max(0, min(norm_val, 2.0)))
        
        # Строим график нормализованных значений
        axes[i].plot(times, normalized_values, linewidth=2, color='blue', alpha=0.8)
        
        # Используем полное описание в заголовке
        axes[i].set_title(description, fontsize=10, pad=10, wrap=True)
        
        # Устанавливаем пределы и метки для нормализованных значений
        axes[i].set_ylim(-0.1, 2.1)
        axes[i].set_yticks([0, 1, 2])
        axes[i].set_yticklabels(['0\n(мин)', '1\n(нач. макс)', '2\n(расш. макс)'], fontsize=8)
        
        # Добавляем горизонтальные линии для границ диапазонов
        axes[i].axhline(y=1, color='red', linestyle='--', alpha=0.7, linewidth=1)
        axes[i].axhline(y=2, color='green', linestyle='--', alpha=0.7, linewidth=1)
        axes[i].axhline(y=0, color='orange', linestyle='--', alpha=0.7, linewidth=1)
        
        # Добавляем сетку и настраиваем внешний вид
        axes[i].grid(True, linestyle='--', alpha=0.3)
        axes[i].tick_params(axis='x', which='major', labelsize=8)
        axes[i].tick_params(axis='y', which='major', labelsize=8)
        
        # Добавляем подпись оси X
        if i >= 15:  # Только для нижних графиков
            axes[i].set_xlabel('Время', fontsize=9)
    
    # Добавляем общий заголовок и подписи осей
    plt.suptitle('Динамика переменных системы (нормализованные значения)', fontsize=16, y=0.98)
    fig.text(0.5, 0.02, 'Время', ha='center', fontsize=12)
    fig.text(0.04, 0.5, 'Нормализованное значение', va='center', rotation='vertical', fontsize=12)
    
    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
    
    # Конвертируем в base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return plot_data

def create_radar_plot(X, title='Лепестковая диаграмма'):
    """Создает радиальную диаграмму нормализованных значений с увеличенным размером и короткими подписями"""
    # Увеличиваем размер фигуры для лучшей читаемости
    fig = plt.figure(figsize=(24, 18))
    
    # Создаем полярную систему координат с увеличенной областью для диаграммы
    ax = fig.add_subplot(111, polar=True)
    
    # Используем короткие подписи x1, x2, ..., x18
    labels = [f'x{i + 1}' for i in range(18)]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    
    # Нормализуем значения для отображения в диапазоне [0, 2]
    normalized = []
    for i, value in enumerate(X):
        var_name = f'X{i+1}'
        initial_info = INITIAL_RANGES[var_name]
        integration_info = INTEGRATION_RANGES[var_name]
        
        initial_min = initial_info['min']
        initial_max = initial_info['max']
        integration_max = integration_info['max']
        
        if value <= initial_max:
            # Нормализуем к [0, 1] в начальном диапазоне
            if initial_max > initial_min:
                norm_val = (value - initial_min) / (initial_max - initial_min)
            else:
                norm_val = 0.5
        else:
            # Нормализуем к [1, 2] в расширенном диапазоне
            if integration_max > initial_max:
                norm_val = 1.0 + (value - initial_max) / (integration_max - initial_max)
            else:
                norm_val = 1.0
        
        # Гарантируем [0, 2]
        normalized.append(max(0, min(norm_val, 2.0)))
    
    vals = normalized + [normalized[0]]
    angs = angles + [angles[0]]
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Увеличиваем размеры элементов диаграммы
    ax.plot(angs, vals, 'o-', linewidth=4, markersize=24, label='Нормализованные значения', color='blue')
    ax.fill(angs, vals, alpha=0.25, color='lightblue')
    
    # Увеличиваем шрифт меток и используем короткие подписи
    ax.set_thetagrids(np.degrees(angles), labels, fontsize=24)
    ax.tick_params(axis='x', which='major', pad=30)  # Увеличиваем отступ меток
    
    ax.set_ylim(0, 2.1)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(['0 (мин)', '1 (нач. макс)', '2 (расш. макс)'], fontsize=16)
    
    # Улучшаем сетку
    ax.grid(True, alpha=0.4, linewidth=1.5)
    
    # Добавляем круговые линии для границ диапазонов
    ax.plot(angs, [1] * len(angs), 'r--', alpha=0.6, linewidth=3, label='Начальный максимум')
    ax.plot(angs, [2] * len(angs), 'g--', alpha=0.6, linewidth=3, label='Расширенный максимум')
    
    # Увеличиваем заголовок
    plt.title(title, size=20, pad=40, fontweight='bold')
    
    # Добавляем легенду
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.0), fontsize=16)
    
    # Увеличиваем DPI для лучшего качества
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    radar_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return radar_data

def create_all_radar_plots(X_quarter1, X_quarter2, X_quarter3, X_final, X_initial=None):
    """Создает все лепестковые диаграммы для разных этапов интегрирования"""
    radar_plots = {
        'initial': create_radar_plot(X_initial, 'Начальные значения') if X_initial is not None else create_radar_plot(X_quarter1, 'Начальные значения'),
        'quarter1': create_radar_plot(X_quarter1, 'Лепестковая диаграмма - после первой четверти шагов'),
        'quarter2': create_radar_plot(X_quarter2, 'Лепестковая диаграмма - после второй четверти шагов'),
        'quarter3': create_radar_plot(X_quarter3, 'Лепестковая диаграмма - после третьей четверти шагов'),
        'final': create_radar_plot(X_final, 'Лепестковая диаграмма - финальные значения')
    }
    return radar_plots