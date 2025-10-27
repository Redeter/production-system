import React, { useState, useEffect } from 'react';
import ParametersTab from './components/ParametersTab';
import ResultsTab from './components/ResultsTab';
import './App.css';

// Базовый URL для API
const API_BASE_URL = process.env.REACT_APP_API_URL;

function App() {
  const [activeTab, setActiveTab] = useState('parameters');
  const [initialValues, setInitialValues] = useState({});
  const [parameters, setParameters] = useState({});
  const [functions, setFunctions] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [backendStatus, setBackendStatus] = useState('unknown');

  useEffect(() => {
    checkBackendConnection();
    initializeDefaultValues();
    initializeDefaultFunctions();
  }, []);

  

  const initializeDefaultValues = () => {
    const defaultInitialValues = {};
    for (let i = 1; i <= 18; i++) {
      defaultInitialValues[`X${i}`] = '';
    }
    setInitialValues(defaultInitialValues);

    const defaultParameters = {
      T: 50, 
      dt: 0.5,
      O0: 10, 
      dU: 0, dI: 0, dT: 0, dPG: 0, dPV: 0,
      dUstar: 1, dIstar: 1, dTstar: 1, dPGstar: 1, dPVstar: 1
    };
    
    const paramNames = [
      'Nw','Ns','O0','Oin','Oout','Sm','Rw','Nst','Sstar','Ld','Lstar',
      'Mf','Mp','P0','Pin','Pout','R0','Rin','Rout','C0','Cin','Cout',
      'T0','Tin','Tout','Nr','Df','Dp','dU','dUstar','dI','dIstar',
      'dT','dTstar','Tdf','Tdp','dPG','dPGstar','dPV','dPVstar','NTP',
      'Nd','Ab','T','dt'
    ];
    
    paramNames.forEach(p => { 
      if (!defaultParameters[p]) defaultParameters[p] = ''; 
    });
    setParameters(defaultParameters);
  };

  const initializeDefaultFunctions = () => {
    const defaultFunctions = {};
    for (let i = 1; i <= 36; i++) {
      defaultFunctions[`f${i}`] = {
        a: '', b: '', c: '', d: ''
      };
    }
    setFunctions(defaultFunctions);
  };

  const apiRequest = async (endpoint, options = {}) => {
    try {
      const url = `${API_BASE_URL}${endpoint}`;
      console.log(`🔄 API Request: ${url}`, options);
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      console.log(`📨 API Response: ${response.status} ${response.statusText}`);

      // Проверяем Content-Type перед парсингом
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('❌ Non-JSON response:', text.substring(0, 200));
        throw new Error(`Сервер вернул не JSON ответ: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`❌ API ошибка (${endpoint}):`, error);
      throw error;
    }
  };

  const handleGenerateValues = async () => {
    try {
      setLoading(true); 
      setError(''); 
      setSuccess('');
      
      if (backendStatus !== 'connected') {
        setError('Бэкенд недоступен. Запустите Flask сервер на localhost:5000');
        return;
      }

      const data = await apiRequest('/api/generate-values');
      
      if (data.success) {
        const newInitialValues = {};
        const newParameters = { ...parameters };
        const newFunctions = { ...functions };

        // Разделяем полученные данные на начальные значения, параметры и функции
        Object.keys(data.data).forEach(key => {
          if (key.startsWith('X')) {
            newInitialValues[key] = data.data[key];
          } else if (key.startsWith('f') && key.length <= 3) {
            newFunctions[key] = data.data[key];
          } else {
            newParameters[key] = data.data[key];
          }
        });

        setInitialValues(newInitialValues);
        setParameters(newParameters);
        setFunctions(newFunctions);

        setSuccess('Начальные значения, параметры и функции успешно сгенерированы!');
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError(data.error || 'Ошибка при генерации значений');
      }
    } catch (err) {
      setError('Ошибка подключения к бэкенду: ' + (err.message || ''));
      setBackendStatus('disconnected');
    } finally { 
      setLoading(false); 
    }
  };

  const handleLoadTestValues = async () => {
    try {
      setLoading(true);
      setError('');
      setSuccess('');

      if (backendStatus !== 'connected') {
        setError('Бэкенд недоступен. Запустите Flask сервер на localhost:5000');
        return;
      }

      const data = await apiRequest('/api/test-values');

      if (data.success) {
        const testData = data.data;
        
        // Устанавливаем тестовые значения
        setInitialValues(testData.initialValues);
        setParameters(testData.parameters);
        setFunctions(testData.functions);

        setSuccess('Тестовые значения успешно загружены!');
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError(data.error || 'Ошибка при загрузке тестовых значений');
      }
    } catch (err) {
      setError('Ошибка подключения к бэкенду: ' + (err.message || ''));
      setBackendStatus('disconnected');
    } finally {
      setLoading(false);
    }
  };

  const handleCalculate = async () => {
    try {
      setLoading(true); 
      setError(''); 
      setSuccess('');

      console.log("📤 Отправка данных на бэкенд:", {
        initialValues,
        parameters, 
        functions
      });

      // Проверка заполнения начальных значений
      const missing = [];
      for (let i = 1; i <= 18; i++) {
        const val = initialValues[`X${i}`];
        if (val === undefined || val === '' || isNaN(val)) missing.push(`X${i}`);
      }
      if (missing.length) { 
        setError(`Не заданы значения для: ${missing.join(', ')}`); 
        return; 
      }

      const requestData = { 
        initialValues, 
        parameters, 
        functions 
      };
      
      const data = await apiRequest('/api/calculate', {
        method: 'POST',
        body: JSON.stringify(requestData)
      });

      if (data.success) {
        setResults(data);
        setActiveTab('results');
        setSuccess('Расчет успешно завершен!');
        setBackendStatus('connected');
      } else {
        setError(data.error || 'Ошибка при расчете');
      }
    } catch (err) {
      setError('Ошибка расчета: ' + (err.message || ''));
      setBackendStatus('disconnected');
    } finally { 
      setLoading(false); 
    }
  };

  const handleInitialValueChange = (key, value) => {
    setInitialValues(prev => ({ ...prev, [key]: value }));
  };

  const handleParameterChange = (key, value) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const handleFunctionChange = (funcName, coeff, value) => {
    setFunctions(prev => ({
      ...prev,
      [funcName]: {
        ...prev[funcName],
        [coeff]: value === '' ? '' : parseFloat(value) || 0
      }
    }));
  };

  const handleRetryConnection = () => {
    setBackendStatus('checking');
    checkBackendConnection();
  };

  const getStatusAlert = () => {
    switch (backendStatus) {
      case 'connected':
        return (
          <div className="alert alert-success alert-dismissible fade show" role="alert">
            <strong>✅ Подключено:</strong> Бэкенд доступен на {API_BASE_URL}
            <button type="button" className="btn-close" onClick={() => setBackendStatus('connected')}></button>
          </div>
        );
      case 'disconnected':
        return (
          <div className="alert alert-warning alert-dismissible fade show" role="alert">
            <strong>❌ Не подключено:</strong> Бэкенд недоступен. Запустите Flask сервер на localhost:5000
            <button type="button" className="btn-close" onClick={() => setBackendStatus('disconnected')}></button>
            <div className="mt-2">
              <button className="btn btn-sm btn-outline-secondary" onClick={handleRetryConnection}>
                Повторить подключение
              </button>
            </div>
          </div>
        );
      case 'checking':
        return (
          <div className="alert alert-info alert-dismissible fade show" role="alert">
            <strong>🔍 Проверка подключения...</strong>
            <div className="spinner-border spinner-border-sm ms-2" role="status"></div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="container-fluid py-3">
      <div className="row">
        <div className="col-12">

          

          {/* Основная карточка приложения */}
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
                  functions={functions}
                  onInitialValueChange={handleInitialValueChange}
                  onParameterChange={handleParameterChange}
                  onFunctionChange={handleFunctionChange}
                />
              )}
              {activeTab === 'results' && results && (
                <ResultsTab results={results} />
              )}
            </div>

            <div className="card-footer bg-dark">
              <div className="d-flex gap-2 justify-content-between flex-wrap">
                <div className="d-flex gap-2 flex-wrap">
                  <button 
                    className="btn btn-light border-dark" 
                    onClick={handleGenerateValues} 
                    disabled={loading || backendStatus !== 'connected'}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2 text-dark"></span>
                        Генерация...
                      </>
                    ) : (
                      'Сгенерировать случайные значения'
                    )}
                  </button>
                  <button 
                    className="btn btn-outline-light" 
                    onClick={handleLoadTestValues} 
                    disabled={loading || backendStatus !== 'connected'}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2"></span>
                        Загрузка...
                      </>
                    ) : (
                      'Загрузить тестовые значения'
                    )}
                  </button>
                </div>
                <button 
                  className="btn btn-success" 
                  onClick={handleCalculate} 
                  disabled={loading || backendStatus !== 'connected'}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Расчет...
                    </>
                  ) : (
                    'Рассчитать'
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Инструкция по запуску */}
          {backendStatus === 'disconnected' && (
            <div className="card mt-3 border-warning">
              <div className="card-header bg-warning text-dark">
                <strong>Инструкция по запуску</strong>
              </div>
              <div className="card-body">
                <p>Для работы приложения необходимо:</p>
                <ol>
                  <li>Запустить Flask сервер: <code>python app.py</code></li>
                  <li>Убедиться, что сервер работает на <code>http://localhost:5000</code></li>
                  <li>Обновить страницу или нажать "Повторить подключение"</li>
                </ol>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;