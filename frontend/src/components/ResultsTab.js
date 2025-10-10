import React from 'react';

const ResultsTab = ({ results }) => {
  if (!results) return <div>Нет данных для отображения</div>;

  return (
    <div>
      <div className="row mb-4">
        <div className="col-md-8">
          <h5>Графики переменных системы</h5>
          {results.plots?.graphs && (
            <img 
              src={`data:image/png;base64,${results.plots.graphs}`} 
              alt="Графики системы"
              className="img-fluid border rounded"
            />
          )}
        </div>
        <div className="col-md-4">
          <h5>Лепестковая диаграмма</h5>
          {results.plots?.radar && (
            <img 
              src={`data:image/png;base64,${results.plots.radar}`} 
              alt="Лепестковая диаграмма"
              className="img-fluid border rounded"
            />
          )}
        </div>
      </div>

      <div className="row">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h6 className="mb-0">Результаты расчета</h6>
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
          <div className="card">
            <div className="card-header">
              <h6 className="mb-0">Статистика расчета</h6>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-6">
                  <div className="border rounded p-2 text-center bg-light">
                    <div className="text-muted small">Максимальное |Δ|</div>
                    <div className="h5 text-primary mb-0">
                      {results.statistics?.maxAbsDelta?.toFixed(6)}
                    </div>
                  </div>
                </div>
                <div className="col-6">
                  <div className="border rounded p-2 text-center bg-light">
                    <div className="text-muted small">Среднее |Δ|</div>
                    <div className="h5 text-info mb-0">
                      {results.statistics?.meanAbsDelta?.toFixed(6)}
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-3">
                <div className="d-flex justify-content-between border-bottom py-1">
                  <span className="text-muted">Шагов интегрирования:</span>
                  <strong>{results.statistics?.steps}</strong>
                </div>
                <div className="d-flex justify-content-between border-bottom py-1">
                  <span className="text-muted">Время расчета (T):</span>
                  <strong>{results.times?.[results.times.length - 1]?.toFixed(1)}</strong>
                </div>
                <div className="d-flex justify-content-between py-1">
                  <span className="text-muted">Шаг интегрирования (dt):</span>
                  <strong>0.5</strong>
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