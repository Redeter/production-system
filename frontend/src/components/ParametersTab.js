import React, { useState } from 'react';

const ParametersTab = ({ 
  initialValues, 
  parameters,
  functions,
  onInitialValueChange,
  onParameterChange,
  onFunctionChange
}) => {
  const [activeSection, setActiveSection] = useState('initial');

  const xFieldNames = {
    X1: "X1 Количество забракованных балок на 100 единиц продукции",
    X2: "X2 Численность операторов РТК", 
    X3: "X3 Среднее количество остановок РТК на один цикл",
    X4: "X4 Средняя длина дефектных сварных швов на 1 единицу продукции",
    X5: "X5 Выполненные работы по плановому обслуживанию РТК",
    X6: "X6 Численность программистов",
    X7: "X7 Численность наладчиков сварочного оборудования",
    X8: "X8 Численность контролеров ОТК",
    X9: "X9 Численность цеховых технологов",
    X10: "X10 Количество дней просрочки поставки материалов и запчастей для ремонта РТК",
    X11: "X11 Среднее отклонение напряжения сварочной дуги",
    X12: "X12 Среднее отклонение тока на двигателе подающего блока",
    X13: "X13 Среднее отклонение манипулятора от программной траектории",
    X14: "X14 Наличие на рабочих местах необходимой технологической документации",
    X15: "X15 Отклонение давления защитного газа",
    X16: "X16 Отклонение давления сжатого воздуха",
    X17: "X17 План производства на заданный период в единицах продукции",
    X18: "X18 Количество балок, сданных ОТК с первого предъявления"
  };

  // Описания функций с переменными
  const functionDescriptions = {
    f1: "f1(X3)",
    f2: "f2(X11)", 
    f3: "f3(X12)",
    f4: "f4(X13)",
    f5: "f5(X2)",
    f6: "f6(X8)",
    f7: "f7(X17)",
    f8: "f8(X10)",
    f9: "f9(X15)",
    f10: "f10(X16)",
    f11: "f11(X2)",
    f12: "f12(X17)",
    f13: "f13(X15)",
    f14: "f14(X16)",
    f15: "f15(X2)",
    f16: "f16(X6)",
    f17: "f17(X7)",
    f18: "f18(X10)",
    f19: "f19(X17)",
    f20: "f20(X17)",
    f21: "f21(X17)",
    f22: "f22(X17)",
    f23: "f23(X17)",
    f24: "f24(X5)",
    f25: "f25(X5)",
    f26: "f26(X5)",
    f27: "f27(X9)",
    f28: "f28(X17)",
    f29: "f29(X17)",
    f30: "f30(X9)",
    f31: "f31(X6)",
    f32: "f32(X7)",
    f33: "f33(X8)",
    f34: "f34(X14)",
    f35: "f35(X4)",
    f36: "f36(X18)"
  };

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

  const renderInitialValues = () => (
    <div className="row">
      {[...Array(18)].map((_, i) => {
        const fieldKey = `X${i + 1}`;
        return (
          <div key={fieldKey} className="col-md-4 col-sm-6 mb-2">
            <label className="form-label small mb-1">
              {xFieldNames[fieldKey]}
            </label>
            <input
              type="number"
              step="0.001"
              className="form-control form-control-sm"
              value={initialValues[fieldKey] || ''}
              onChange={(e) => onInitialValueChange(fieldKey, parseFloat(e.target.value))}
            />
          </div>
        );
      })}
    </div>
  );

  const renderParameters = () => {
    const paramGroups = [
      {
        title: 'Основные параметры',
        params: ['Nw', 'Ns', 'O0', 'Oin', 'Oout', 'Sm', 'Rw', 'Nst', 'Sstar', 'Ld', 'Lstar']
      },
      {
        title: 'Производственные параметры', 
        params: ['Mf', 'Mp', 'P0', 'Pin', 'Pout', 'R0', 'Rin', 'Rout', 'C0', 'Cin', 'Cout']
      },
      {
        title: 'Технические параметры',
        params: ['T0', 'Tin', 'Tout', 'Nr', 'Df', 'Dp', 'Tdf', 'Tdp', 'NTP', 'Nd', 'Ab']
      },
      {
        title: 'Допуски и отклонения',
        params: ['dU', 'dUstar', 'dI', 'dIstar', 'dT', 'dTstar', 'dPG', 'dPGstar', 'dPV', 'dPVstar']
      },
      {
        title: 'Параметры интегрирования',
        params: ['T', 'dt']
      }
    ];

    return (
      <div>
        {paramGroups.map((group, groupIndex) => (
          <div key={groupIndex} className="mb-4">
            <h6 className="border-bottom pb-1">{group.title}</h6>
            <div className="row">
              {group.params.map((param) => (
                <div key={param} className="col-md-3 col-sm-4 mb-2">
                  <label className="form-label small mb-1">{param}</label>
                  <input
                    type="number"
                    step="0.001"
                    className="form-control form-control-sm"
                    value={parameters[param] || ''}
                    onChange={(e) => onParameterChange(param, parseFloat(e.target.value))}
                  />
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderFunctionInput = (funcName) => {
    const currentFunc = functions[funcName] || { a: 0, b: 0, c: 0, d: 0 };

    return (
      <div className="card mb-3 border-0 bg-light">
        <div className="card-body p-3">
          <div className="row align-items-center">
            <div className="col-md-2 col-sm-12 mb-2 mb-md-0">
              <h6 className="mb-0 fw-bold text-dark">{functionDescriptions[funcName]} =</h6>
            </div>
            <div className="col-md-10 col-sm-12">
              <div className="row g-2 align-items-center">
                {/* Коэффициент a */}
                <div className="col-auto">
                  <input
                    type="number"
                    step="0.001"
                    className="form-control form-control-sm text-center"
                    style={{ width: '80px' }}
                    value={currentFunc.a || ''}
                    onChange={(e) => onFunctionChange(funcName, 'a', e.target.value)}
                    placeholder="0.00"
                  />
                </div>
                <div className="col-auto">
                  <span className="fw-bold">·k³</span>
                </div>
                <div className="col-auto">
                  <span className="fw-bold">+</span>
                </div>

                {/* Коэффициент b */}
                <div className="col-auto">
                  <input
                    type="number"
                    step="0.001"
                    className="form-control form-control-sm text-center"
                    style={{ width: '80px' }}
                    value={currentFunc.b || ''}
                    onChange={(e) => onFunctionChange(funcName, 'b', e.target.value)}
                    placeholder="0.00"
                  />
                </div>
                <div className="col-auto">
                  <span className="fw-bold">·k²</span>
                </div>
                <div className="col-auto">
                  <span className="fw-bold">+</span>
                </div>

                {/* Коэффициент c */}
                <div className="col-auto">
                  <input
                    type="number"
                    step="0.001"
                    className="form-control form-control-sm text-center"
                    style={{ width: '80px' }}
                    value={currentFunc.c || ''}
                    onChange={(e) => onFunctionChange(funcName, 'c', e.target.value)}
                    placeholder="0.00"
                  />
                </div>
                <div className="col-auto">
                  <span className="fw-bold">·k</span>
                </div>
                <div className="col-auto">
                  <span className="fw-bold">+</span>
                </div>

                {/* Коэффициент d */}
                <div className="col-auto">
                  <input
                    type="number"
                    step="0.001"
                    className="form-control form-control-sm text-center"
                    style={{ width: '80px' }}
                    value={currentFunc.d || ''}
                    onChange={(e) => onFunctionChange(funcName, 'd', e.target.value)}
                    placeholder="0.00"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderFunctions = () => {
    return (
      <div>
        {functionGroups.map((group, groupIndex) => (
          <div key={groupIndex} className="mb-4">
            <h6 className="border-bottom pb-2 mb-3 text-dark">{group.title}</h6>
            <div className="row">
              {group.functions.map((func) => (
                <div key={func} className="col-lg-6 col-xl-4 mb-3">
                  {renderFunctionInput(func)}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div>
      <ul className="nav nav-pills mb-3">
        <li className="nav-item">
          <button
            className={`nav-link ${activeSection === 'initial' ? 'active' : ''}`}
            onClick={() => setActiveSection('initial')}
          >
            Начальные значения
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeSection === 'parameters' ? 'active' : ''}`}
            onClick={() => setActiveSection('parameters')}
          >
            Параметры системы
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeSection === 'functions' ? 'active' : ''}`}
            onClick={() => setActiveSection('functions')}
          >
            Функции системы
          </button>
        </li>
      </ul>

      <div className="tab-content">
        {activeSection === 'initial' && renderInitialValues()}
        {activeSection === 'parameters' && renderParameters()}
        {activeSection === 'functions' && renderFunctions()}
      </div>
    </div>
  );
};

export default ParametersTab;