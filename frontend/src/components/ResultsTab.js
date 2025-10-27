import React, { useState } from 'react';

const ResultsTab = ({ results }) => {
  const [currentDiagram, setCurrentDiagram] = useState(0);
  
  if (!results) return <div>Нет данных для отображения</div>;

  const radarPlots = results.plots?.radar || {};
  
  // Создаем массив всех доступных диаграмм
  const allDiagrams = [
    { key: 'initial', title: 'Начальные значения' },
    { key: 'quarter1', title: 'После первой четверти шагов интегрирования' },
    { key: 'quarter2', title: 'После второй четверти шагов интегрирования' },
    { key: 'quarter3', title: 'После третьей четверти шагов интегрирования' },
    { key: 'final', title: 'Финальные значения' }
  ].filter(diagram => radarPlots[diagram.key]);

  // Функции для навигации
  const nextDiagram = () => {
    setCurrentDiagram((prev) => (prev + 1) % allDiagrams.length);
  };

  const prevDiagram = () => {
    setCurrentDiagram((prev) => (prev - 1 + allDiagrams.length) % allDiagrams.length);
  };

  const currentDiagramData = allDiagrams[currentDiagram];

  return (
    <div>
      <div className="row mb-4">
        <div className="col-12">
          <h5>Графики переменных системы</h5>
          {results.plots?.graphs && (
            <img 
              src={`data:image/png;base64,${results.plots.graphs}`} 
              alt="Графики системы"
              className="img-fluid border rounded"
            />
          )}
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h4 className="mb-0">Лепестковые диаграммы</h4>
            <div className="d-flex align-items-center">
              <span className="text-muted me-3 fs-5">
                {currentDiagram + 1} из {allDiagrams.length}
              </span>
              <div className="btn-group">
                <button 
                  className="btn btn-outline-primary btn-lg" 
                  onClick={prevDiagram}
                  disabled={allDiagrams.length <= 1}
                >
                  ← Назад
                </button>
                <button 
                  className="btn btn-outline-primary btn-lg" 
                  onClick={nextDiagram}
                  disabled={allDiagrams.length <= 1}
                >
                  Вперед →
                </button>
              </div>
            </div>
          </div>

          {currentDiagramData ? (
            <div className="row justify-content-center">
              <div className="col-12">
                <div className="card shadow-lg">
                  <div className="card-header text-center bg-primary text-white py-3">
                    <h4 className="mb-0 fw-bold">{currentDiagramData.title}</h4>
                  </div>
                  <div className="card-body p-4 d-flex align-items-center justify-content-center">
                    <div style={{ 
                      minHeight: '700px', 
                      width: '100%', 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center'
                    }}>
                      <img 
                        src={`data:image/png;base64,${radarPlots[currentDiagramData.key]}`} 
                        alt={currentDiagramData.title}
                        style={{ 
                          maxWidth: '100%', 
                          maxHeight: '650px', 
                          width: 'auto', 
                          height: 'auto'
                        }}
                        className="img-fluid"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card border-dashed">
              <div className="card-body d-flex align-items-center justify-content-center">
                <div className="text-center text-muted">
                  <div className="fs-4">Нет данных для отображения</div>
                </div>
              </div>
            </div>
          )}
          
          {/* Индикатор прогресса */}
          {allDiagrams.length > 1 && (
            <div className="mt-4">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <small className="text-muted">Прогресс просмотра:</small>
                <small className="text-muted">
                  {currentDiagram + 1} / {allDiagrams.length}
                </small>
              </div>
              <div className="progress" style={{ height: '10px' }}>
                <div 
                  className="progress-bar progress-bar-striped progress-bar-animated" 
                  style={{ 
                    width: `${((currentDiagram + 1) / allDiagrams.length) * 100}%` 
                  }}
                ></div>
              </div>
            </div>
          )}
          
          <div className="alert alert-info mt-4 fs-6">
            <strong>Пояснение:</strong> Лепестковые диаграммы показывают нормализованные значения переменных. 
            Значение 1 соответствует начальному максимуму, значение 2 - расширенному максимуму.
            Красные и зеленые пунктирные линии обозначают границы начального и расширенного диапазонов.
            <br />
            <strong>Навигация:</strong> Используйте кнопки "Назад" и "Вперед" для просмотра всех {allDiagrams.length} диаграмм.
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-md-6">
          <div className="card shadow-sm">
            <div className="card-header bg-light">
              <h6 className="mb-0 fw-bold">Результаты расчета</h6>
            </div>
            <div className="card-body p-0">
              <div className="table-responsive" style={{ maxHeight: '400px' }}>
                <table className="table table-sm table-striped mb-0">
                  <thead className="table-light sticky-top">
                    <tr>
                      <th>Переменная</th>
                      <th>Конечное значение</th>
                      <th>Δ</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.deltas?.map((delta, index) => (
                      <tr key={index}>
                        <td className="fw-bold">X{index + 1}</td>
                        <td>{results.finalValues[index]?.toFixed(4)}</td>
                        <td className={delta >= 0 ? 'text-success' : 'text-danger'}>
                          {delta.toFixed(4)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        
        <div className="col-md-6">
          <div className="card shadow-sm">
            <div className="card-header bg-light">
              <h6 className="mb-0 fw-bold">Статистика расчета</h6>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-6">
                  <div className="border rounded p-3 text-center bg-light">
                    <div className="text-muted small">Максимальное |Δ|</div>
                    <div className="h4 text-primary mb-0 fw-bold">
                      {results.statistics?.maxAbsDelta?.toFixed(6)}
                    </div>
                  </div>
                </div>
                <div className="col-6">
                  <div className="border rounded p-3 text-center bg-light">
                    <div className="text-muted small">Среднее |Δ|</div>
                    <div className="h4 text-info mb-0 fw-bold">
                      {results.statistics?.meanAbsDelta?.toFixed(6)}
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-3">
                <div className="d-flex justify-content-between border-bottom py-2">
                  <span className="text-muted">Шагов интегрирования:</span>
                  <strong className="fs-6">{results.statistics?.steps}</strong>
                </div>
                <div className="d-flex justify-content-between border-bottom py-2">
                  <span className="text-muted">Время расчета (T):</span>
                  <strong className="fs-6">{results.times?.[results.times.length - 1]?.toFixed(1)}</strong>
                </div>
                <div className="d-flex justify-content-between py-2">
                  <span className="text-muted">Шаг интегрирования (dt):</span>
                  <strong className="fs-6">0.5</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsTab;