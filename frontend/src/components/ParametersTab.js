import React from 'react';

const ParametersTab = ({ 
  initialValues, 
  parameters,
  functions,
  onInitialValueChange,
  onParameterChange,
  onFunctionChange
}) => {
  // Метаданные для всех параметров с названиями
  const paramMeta = {
    X1: { min: 0, max: 10, type: 'int', name: 'Количество забракованных балок на 100 ед. продукции' },
    X2: { min: 0, max: 8, type: 'int', name: 'Численность операторов РТК' },
    X3: { min: 0, max: 20, type: 'int', name: 'Среднее количество остановок РТК на цикл' },
    X4: { min: 0, max: 3, type: 'float', name: 'Средняя длина дефектных швов на 1 ед. продукции' },
    X5: { type: 'bool', name: 'Выполненные работы по плановому обслуживанию РТК' },
    X6: { min: 0, max: 3, type: 'int', name: 'Численность программистов' },
    X7: { min: 0, max: 4, type: 'int', name: 'Численность наладчиков сварочного оборудования' },
    X8: { min: 0, max: 2, type: 'int', name: 'Численность контролеров ОТК' },
    X9: { min: 0, max: 1, type: 'int', name: 'Численность цеховых технологов' },
    X10: { min: 0, max: 30, type: 'int', name: 'Количество дней просрочки поставки материалов' },
    X11: { min: 0, max: 5, type: 'float', name: 'Среднее отклонение напряжения сварочной дуги' },
    X12: { min: 0, max: 2, type: 'float', name: 'Среднее отклонение тока на двигателе подающего блока' },
    X13: { min: 0, max: 5, type: 'float', name: 'Среднее отклонение манипулятора от траектории' },
    X14: { type: 'bool', name: 'Наличие технологической документации на рабочих местах' },
    X15: { min: 0, max: 2, type: 'float', name: 'Отклонение давления защитного газа' },
    X16: { min: 0, max: 3, type: 'float', name: 'Отклонение давления сжатого воздуха' },
    X17: { min: 0, max: 180, type: 'int', name: 'План производства на период (ед. продукции)' },
    X18: { min: 0, max: 360, type: 'int', name: 'Количество балков, сданных ОТК с 1-го предъявления' },
    
    O0: { min:0,max:8,type:'int', name: 'Численность операторов РТК на начало периода' },
    Oin: { min:0,max:2,type:'int', name: 'Численность принятых операторов РТК за период' },
    Oout: { min:0,max:2,type:'int', name: 'Численность уволенных операторов РТК за период' },
    Sm: { min:1,max:3,type:'int', name: 'Сменность работы производства' },
    Rw: { min:1,max:6,type:'int', name: 'Количество РТК в производственном процессе' },
    Nst: { min:0,max:500,type:'int', name: 'Количество остановок РТК за период' },
    Sstar: { min:0,max:5,type:'int', name: 'Допустимое количество остановок РТК за цикл' },
    Ld: { min:0,max:120,type:'float', name: 'Общая длина дефектных швов за период' },
    Lstar: { min:0,max:80,type:'float', name: 'Расчетная длина дефектных швов за период' },
    Mf: { min:0,max:22,type:'int', name: 'Количество выполненных мероприятий ППР' },
    Mp: { min:0,max:22,type:'int', name: 'Количество запланированных мероприятий ППР' },
    
    P0: { min:0,max:3,type:'int', name: 'Численность программистов на начало периода' },
    Pin: { min:0,max:1,type:'int', name: 'Численность принятых программистов за период' },
    Pout: { min:0,max:1,type:'int', name: 'Численность уволенных программистов за период' },
    
    R0: { min:0,max:4,type:'int', name: 'Численность наладчиков на начало периода' },
    Rin: { min:0,max:1,type:'int', name: 'Численность принятых наладчиков за период' },
    Rout: { min:0,max:1,type:'int', name: 'Численность уволенных наладчиков за период' },
    
    C0: { min:0,max:2,type:'int', name: 'Численность контролеров ОТК на начало периода' },
    Cin: { min:0,max:1,type:'int', name: 'Численность принятых контролеров за период' },
    Cout: { min:0,max:1,type:'int', name: 'Численность уволенных контролеров за период' },
    
    T0: { min:0,max:1,type:'int', name: 'Численность технологов на начало периода' },
    Tin: { min:0,max:1,type:'int', name: 'Численность принятых технологов за период' },
    Tout: { min:0,max:1,type:'int', name: 'Численность уволенных технологов за период' },
    
    Nr: { min:0,max:3,type:'float', name: 'Длительность ремонта РТК (дни)' },
    Df: { min:0,max:30,type:'int', name: 'Фактический срок поставки запчастей' },
    Dp: { min:0,max:30,type:'int', name: 'Плановый срок поставки запчастей' },
    
    dU: { min:0,max:5,type:'float', name: 'Среднее отклонение напряжения от номинала' },
    dUstar: { min:0,max:2,type:'float', name: 'Допустимое отклонение напряжения' },
    dI: { min:0,max:2,type:'float', name: 'Среднее отклонение тока от номинала' },
    dIstar: { min:0,max:0.8,type:'float', name: 'Допустимое отклонение тока' },
    dT: { min:0,max:5,type:'float', name: 'Среднее отклонение манипулятора от траектории' },
    dTstar: { min:0,max:1,type:'float', name: 'Допустимое отклонение манипулятора' },
    
    Tdf: { min:0,max:12,type:'int', name: 'Фактическое количество технологических документов' },
    Tdp: { min:0,max:12,type:'int', name: 'Необходимое количество технологических документов' },
    
    dPG: { min:0,max:2,type:'float', name: 'Среднее отклонение давления защитного газа' },
    dPGstar: { min:0,max:0.5,type:'float', name: 'Допустимое отклонение давления защитного газа' },
    dPV: { min:0,max:3,type:'float', name: 'Среднее отклонение давления сжатого воздуха' },
    dPVstar: { min:0,max:1,type:'float', name: 'Допустимое отклонение давления сжатого воздуха' },
    
    NTP: { min:0,max:360,type:'int', name: 'Количество балков по технологическому процессу' },
    Nd: { min:0,max:360,type:'int', name: 'Количество балков, сданных с 1-го предъявления' },
    Ab: { min:0,max:50,type:'int', name: 'Количество актов о несоответствующей продукции' },
    
    Nw: { min:1,max:10,type:'int', name: 'Количество рабочих недель' },
    Ns: { min:1,max:10,type:'int', name: 'Количество смен' },
    T: { min:1,max:100,type:'float', name: 'Время интегрирования' },
    dt: { min:0.1,max:1,type:'float', name: 'Шаг времени' }
  };

  // Аргументы для каждой функции
  const functionArguments = {
    f1: 'X3', f2: 'X11', f3: 'X12', f4: 'X13', f5: 'X2', f6: 'X8', f7: 'X17',
    f8: 'X10', f9: 'X15', f10: 'X16', f11: 'X2', f12: 'X17', f13: 'X15', f14: 'X16',
    f15: 'X2', f16: 'X6', f17: 'X7', f18: 'X10', f19: 'X17', f20: 'X17', f21: 'X17',
    f22: 'X17', f23: 'X17', f24: 'X5', f25: 'X5', f26: 'X5', f27: 'X9', f28: 'X17',
    f29: 'X17', f30: 'X9', f31: 'X6', f32: 'X7', f33: 'X8', f34: 'X14', f35: 'X4',
    f36: 'X18'
  };

  const handleInputChange = (key, value, type, isFunc = false, coeff = null) => {
    let val = value;
    
    // Для float заменяем запятую на точку
    if (typeof value === 'string' && type === 'float') {
      val = value.replace(',', '.');
    }
    
    if (!isFunc) {
      if (key.startsWith('X')) {
        onInitialValueChange(key, val);
      } else {
        onParameterChange(key, val);
      }
    } else {
      onFunctionChange(key, coeff, val);
    }
  };

  const handleNumberChange = (key, value, type, isFunc = false, coeff = null) => {
    // Преобразуем в число только при потере фокуса
    let numValue;
    if (type === 'int') {
      numValue = parseInt(value) || 0;
    } else if (type === 'float') {
      numValue = parseFloat(value.replace(',', '.')) || 0;
    } else if (type === 'bool') {
      numValue = parseInt(value) || 0;
    } else {
      numValue = value;
    }
    
    handleInputChange(key, numValue, type, isFunc, coeff);
  };

  // Рендер одной функции в компактном формате
  const renderFunction = (func) => {
    const currentFunc = functions[func] || { a: '', b: '', c: '', d: '' };
    const arg = functionArguments[func];

    return (
      <div className="card mb-3 p-3 bg-light border-0">
        <div className="d-flex align-items-center flex-wrap gap-2">
          <strong className="fs-6 me-2" style={{ minWidth: '80px' }}>
            {func}({arg}) =
          </strong>
          
          {/* Коэффициент a (x³) */}
          <div className="d-flex align-items-center gap-1">
            <input 
              type="number" 
              step="0.001"
              className="form-control form-control-sm text-center" 
              style={{width: '80px', fontSize: '0.85rem'}}
              value={currentFunc.a || ''}
              onChange={(e) => handleInputChange(func, e.target.value, 'float', true, 'a')}
              onBlur={(e) => handleNumberChange(func, e.target.value, 'float', true, 'a')}
              placeholder="a"
            />
            <span className="fs-6 mx-1">·x³</span>
          </div>
          
          <span className="fs-6 mx-1">+</span>
          
          {/* Коэффициент b (x²) */}
          <div className="d-flex align-items-center gap-1">
            <input 
              type="number" 
              step="0.001"
              className="form-control form-control-sm text-center" 
              style={{width: '80px', fontSize: '0.85rem'}}
              value={currentFunc.b || ''}
              onChange={(e) => handleInputChange(func, e.target.value, 'float', true, 'b')}
              onBlur={(e) => handleNumberChange(func, e.target.value, 'float', true, 'b')}
              placeholder="b"
            />
            <span className="fs-6 mx-1">·x²</span>
          </div>
          
          <span className="fs-6 mx-1">+</span>
          
          {/* Коэффициент c (x) */}
          <div className="d-flex align-items-center gap-1">
            <input 
              type="number" 
              step="0.001"
              className="form-control form-control-sm text-center" 
              style={{width: '80px', fontSize: '0.85rem'}}
              value={currentFunc.c || ''}
              onChange={(e) => handleInputChange(func, e.target.value, 'float', true, 'c')}
              onBlur={(e) => handleNumberChange(func, e.target.value, 'float', true, 'c')}
              placeholder="c"
            />
            <span className="fs-6 mx-1">·x</span>
          </div>
          
          <span className="fs-6 mx-1">+</span>
          
          {/* Коэффициент d (константа) */}
          <div className="d-flex align-items-center gap-1">
            <input 
              type="number" 
              step="0.001"
              className="form-control form-control-sm text-center" 
              style={{width: '80px', fontSize: '0.85rem'}}
              value={currentFunc.d || ''}
              onChange={(e) => handleInputChange(func, e.target.value, 'float', true, 'd')}
              onBlur={(e) => handleNumberChange(func, e.target.value, 'float', true, 'd')}
              placeholder="d"
            />
          </div>
        </div>
      </div>
    );
  };

  // Рендер одного параметра/начального значения
  const renderParameter = (param) => {
    const meta = paramMeta[param];
    const value = initialValues[param] !== undefined ? initialValues[param] : parameters[param];
    
    return (
      <div key={param} className="card mb-2 p-2 border-0 bg-light">
        <div className="d-flex align-items-center justify-content-between">
          <div className="flex-grow-1 me-3" style={{minWidth: 0}}>
            <div className="mb-0" style={{fontSize: '0.85rem', lineHeight: '1.2', fontWeight: 'normal'}}>
              {meta.name}
            </div>
          </div>
          <div className="d-flex align-items-center gap-2 flex-shrink-0">
            {meta.type === 'bool' ? (
              <select 
                className="form-select form-select-sm"
                style={{width: '70px', fontSize: '0.85rem'}}
                value={value || 0}
                onChange={(e) => handleInputChange(param, e.target.value, meta.type)}
              >
                <option value="0">0</option>
                <option value="1">1</option>
              </select>
            ) : (
              <input 
                type="number" 
                step={meta.type === 'float' ? '0.001' : '1'}
                min={meta.min} 
                max={meta.max}
                className="form-control form-control-sm text-center" 
                style={{width: '70px', fontSize: '0.85rem'}}
                value={value || ''} 
                onChange={(e) => handleInputChange(param, e.target.value, meta.type)}
                onBlur={(e) => handleNumberChange(param, e.target.value, meta.type)}
              />
            )}
            {meta.min !== undefined && meta.max !== undefined && 
              <small className="text-muted nowrap" style={{fontSize: '0.65rem', minWidth: '45px'}}>
                [{meta.min}-{meta.max}]
              </small>
            }
          </div>
        </div>
      </div>
    );
  };

  // Группировка функций для организации
  const functionGroups = [
    {
      title: 'Функции качества (f1-f4)',
      functions: ['f1', 'f2', 'f3', 'f4']
    },
    {
      title: 'Функции персонала (f5-f11)',
      functions: ['f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11']
    },
    {
      title: 'Функции производства (f12-f22)',
      functions: ['f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22']
    },
    {
      title: 'Функции обслуживания (f23-f29)',
      functions: ['f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29']
    },
    {
      title: 'Функции эффективности (f30-f36)',
      functions: ['f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36']
    }
  ];

  // Разделение параметров на группы для лучшей организации
  const parameterGroups = {
    'Начальные значения (X1-X18)': Object.keys(paramMeta).filter(key => key.startsWith('X')),
    'Основные параметры': ['Nw', 'Ns', 'O0', 'Oin', 'Oout', 'Sm', 'Rw', 'Nst', 'Sstar', 'Ld', 'Lstar'],
    'Производственные параметры': ['Mf', 'Mp', 'P0', 'Pin', 'Pout', 'R0', 'Rin', 'Rout', 'C0', 'Cin', 'Cout'],
    'Технические параметры': ['T0', 'Tin', 'Tout', 'Nr', 'Df', 'Dp', 'Tdf', 'Tdp', 'NTP', 'Nd', 'Ab'],
    'Допуски и отклонения': ['dU', 'dUstar', 'dI', 'dIstar', 'dT', 'dTstar', 'dPG', 'dPGstar', 'dPV', 'dPVstar'],
    'Параметры интегрирования': ['T', 'dt']
  };

  return (
    <div className="row">
      {/* Левая колонка: функции */}
      <div className="col-md-6">
        <h5 className="mb-3 text-dark">Функции системы</h5>
        <div style={{maxHeight: '70vh', overflowY: 'auto', paddingRight: '10px'}}>
          {functionGroups.map(group => (
            <div key={group.title} className="mb-4">
              <h6 className="border-bottom pb-2 mb-3 text-dark">{group.title}</h6>
              {group.functions.map(func => (
                <div key={func}>
                  {renderFunction(func)}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* Правая колонка: начальные условия и параметры */}
      <div className="col-md-6">
        <h5 className="mb-3 text-dark">Начальные условия и параметры системы</h5>
        <div style={{maxHeight: '70vh', overflowY: 'auto'}}>
          {Object.entries(parameterGroups).map(([groupTitle, params]) => (
            <div key={groupTitle} className="mb-4">
              <h6 className="border-bottom pb-2 mb-3 text-dark">{groupTitle}</h6>
              {params.map(param => paramMeta[param] && renderParameter(param))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ParametersTab;