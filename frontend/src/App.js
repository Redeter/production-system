import React, { useState, useEffect } from 'react';
import { apiService } from './services/api';
import ParametersTab from './components/ParametersTab';
import ResultsTab from './components/ResultsTab';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('parameters');
  const [initialValues, setInitialValues] = useState({});
  const [parameters, setParameters] = useState({});
  const [coefficients, setCoefficients] = useState('{}');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadDefaultCoefficients();
    initializeDefaultValues();
  }, []);

  const initializeDefaultValues = () => {
    const defaultInitialValues = {};
    for (let i = 1; i <= 18; i++) {
      defaultInitialValues[`X${i}`] = 0.1;
    }
    setInitialValues(defaultInitialValues);

    const defaultParameters = {
      O0: 10, T: 50, dt: 0.5,
      dU: 0, dI: 0, dT: 0, dPG: 0, dPV: 0,
      dUstar: 1, dIstar: 1, dTstar: 1, dPGstar: 1, dPVstar: 1
    };
    
    const paramNames = ['Nw', 'Ns', 'O0', 'Oin', 'Oout', 'Sm', 'Rw', 'Nst', 'Sstar', 'Ld', 'Lstar', 
                       'Mf', 'Mp', 'P0', 'Pin', 'Pout', 'R0', 'Rin', 'Rout', 'C0', 'Cin', 'Cout', 
                       'T0', 'Tin', 'Tout', 'Nr', 'Df', 'Dp', 'dU', 'dUstar', 'dI', 'dIstar', 
                       'dT', 'dTstar', 'Tdf', 'Tdp', 'dPG', 'dPGstar', 'dPV', 'dPVstar', 'NTP', 
                       'Nd', 'Ab', 'T', 'dt'];
    
    paramNames.forEach(param => {
      if (!defaultParameters[param]) {
        defaultParameters[param] = 1.0;
      }
    });
    
    setParameters(defaultParameters);
  };

  const loadDefaultCoefficients = async () => {
    try {
      const response = await apiService.getDefaultCoefficients();
      if (response.data.success) {
        setCoefficients(JSON.stringify(response.data.coefficients, null, 2));
      }
    } catch (err) {
      console.error('Ошибка загрузки коэффициентов:', err);
    }
  };

  const handleGenerateValues = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await apiService.generateValues();
      if (response.data.success) {
        const data = response.data.data;
        
        const newInitialValues = {};
        for (let i = 1; i <= 18; i++) {
          newInitialValues[`X${i}`] = data[`X${i}`];
        }
        setInitialValues(newInitialValues);
        
        const newParameters = { ...parameters };
        Object.keys(data).forEach(key => {
          if (!key.startsWith('X')) {
            newParameters[key] = data[key];
          }
        });
        setParameters(newParameters);
        
        setSuccess('Значения успешно сгенерированы!');
        setTimeout(() => setSuccess(''), 3000);
      }
    } catch (err) {
      setError('Ошибка генерации значений: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleCalculate = async () => {
    try {
      setLoading(true);
      setError('');
      setSuccess('');
      
      let coeffsObj = {};
      if (coefficients.trim()) {
        try {
          coeffsObj = JSON.parse(coefficients);
        } catch (err) {
          setError('Ошибка в формате JSON коэффициентов: ' + err.message);
          return;
        }
      }

      const X0 = [];
      const missingValues = [];
      for (let i = 1; i <= 18; i++) {
        const value = initialValues[`X${i}`];
        if (value === undefined || value === '' || isNaN(value)) {
          missingValues.push(`X${i}`);
        }
        X0.push(parseFloat(value) || 0);
      }

      if (missingValues.length > 0) {
        setError(`Не заданы значения для: ${missingValues.join(', ')}`);
        return;
      }

      const requestData = {
        initialValues,
        parameters,
        coefficients: coeffsObj
      };

      const response = await apiService.calculate(requestData);
      
      if (response.data.success) {
        setResults(response.data);
        setActiveTab('results');
        setSuccess('Расчет успешно завершен!');
      } else {
        setError(response.data.error || 'Ошибка при расчете');
      }
    } catch (err) {
      setError('Ошибка расчета: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleInitialValueChange = (key, value) => {
    setInitialValues(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleParameterChange = (key, value) => {
    setParameters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="container-fluid py-3">
      <div className="row">
        <div className="col-12">
          <h1 className="text-center mb-3">Калькулятор системы Вероятностей ошибок на сварочном производстве</h1>
          
          {error && (
            <div className="alert alert-dark alert-dismissible fade show border" role="alert">
              <strong>Ошибка:</strong> {error}
              <button type="button" className="btn-close" onClick={() => setError('')}></button>
            </div>
          )}
          
          {success && (
            <div className="alert alert-light alert-dismissible fade show border" role="alert">
              <strong>Успех:</strong> {success}
              <button type="button" className="btn-close" onClick={() => setSuccess('')}></button>
            </div>
          )}

          <div className="card border-dark">
            <div className="card-header bg-dark text-white">
              <ul className="nav nav-tabs card-header-tabs border-0">
                <li className="nav-item">
                  <button 
                    className={`nav-link ${activeTab === 'parameters' ? 'active text-dark bg-white' : 'text-white'}`}
                    onClick={() => setActiveTab('parameters')}
                  >
                    Параметры
                  </button>
                </li>
                <li className="nav-item">
                  <button 
                    className={`nav-link ${activeTab === 'results' ? 'active text-dark bg-white' : 'text-white'} ${!results ? 'disabled' : ''}`}
                    onClick={() => setActiveTab('results')}
                    disabled={!results}
                  >
                    Результаты
                  </button>
                </li>
              </ul>
            </div>
            
            <div className="card-body bg-light">
              {activeTab === 'parameters' && (
                <ParametersTab
                  initialValues={initialValues}
                  parameters={parameters}
                  coefficients={coefficients}
                  onInitialValueChange={handleInitialValueChange}
                  onParameterChange={handleParameterChange}
                  onCoefficientsChange={setCoefficients}
                />
              )}

              {activeTab === 'results' && results && (
                <ResultsTab results={results} />
              )}
            </div>

            <div className="card-footer bg-dark">
              <div className="d-flex gap-2 justify-content-between">
                <button 
                  className="btn btn-light border-dark"
                  onClick={handleGenerateValues}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2 text-dark" role="status"></span>
                      Генерация...
                    </>
                  ) : 'Сгенерировать подходящие значения'}
                </button>
                <button 
                  className="btn btn-white border text-dark"
                  onClick={handleCalculate}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2 text-dark" role="status"></span>
                      Расчет...
                    </>
                  ) : 'Рассчитать'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;