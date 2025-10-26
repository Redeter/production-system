import React, { useState } from 'react';

const ParametersTab = ({ 
  initialValues, 
  parameters, 
  coefficients,
  onInitialValueChange,
  onParameterChange,
  onCoefficientsChange
}) => {
  const [activeSection, setActiveSection] = useState('initial');

  // Архив названий для полей X
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

  // ... остальной код без изменений
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

  const renderCoefficients = () => (
    <div>
      <div className="mb-3">
        <small className="text-muted">
          Введите коэффициенты в формате JSON. Оставьте пустым для использования значений по умолчанию.
        </small>
      </div>
      <textarea
        className="form-control font-monospace small"
        rows="8"
        value={coefficients}
        onChange={(e) => onCoefficientsChange(e.target.value)}
        placeholder='{"k1": 0.1, "k5": 0.05, ...}'
      />
    </div>
  );

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
            className={`nav-link ${activeSection === 'coefficients' ? 'active' : ''}`}
            onClick={() => setActiveSection('coefficients')}
          >
            Коэффициенты
          </button>
        </li>
      </ul>

      <div className="tab-content">
        {activeSection === 'initial' && renderInitialValues()}
        {activeSection === 'parameters' && renderParameters()}
        {activeSection === 'coefficients' && renderCoefficients()}
      </div>
    </div>
  );
};

export default ParametersTab;