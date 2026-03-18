import React, { useState, useEffect, useCallback } from 'react';
import { Award, Loader2, Star, Plus } from 'lucide-react';
import Button from '../components/ui/Button';
import DataCard from '../components/ui/DataCard';
import EvaluationForm from '../components/EvaluationForm';
import { fetchEvaluations, createEvaluation } from '../services/evaluation';
import './EvaluationsPage.css';

const EvaluationsPage: React.FC = () => {
  const [evaluations, setEvaluations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);

  const loadEvaluations = useCallback(() => {
    setLoading(true);
    fetchEvaluations()
      .then(setEvaluations)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadEvaluations();
  }, [loadEvaluations]);

  const handleSubmit = async (data: any) => {
    try {
      await createEvaluation(data);
      loadEvaluations();
      setOpen(false);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Erro ao criar avaliação';
      alert(msg);
    }
  };

  return (
    <div className="evaluations-page">
      <header className="page-header">
        <div>
          <h1>Avaliações</h1>
          <p className="page-subtitle">Avaliações de desempenho</p>
        </div>
        <Button icon={Plus} onClick={() => setOpen(true)}>
          Nova Avaliação
        </Button>
      </header>

      <DataCard title="Lista de Avaliações">
        {loading ? (
          <div className="table-loading">
            <Loader2 size={32} className="spin" />
            <p>Carregando...</p>
          </div>
        ) : (
          <div className="evaluations-table">
            <table>
              <thead>
                <tr>
                  <th>Colaborador</th>
                  <th>Mês Ref.</th>
                  <th>Nota</th>
                  <th>Técnica</th>
                  <th>Comportamental</th>
                  <th>Tipo</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {evaluations.map((ev) => (
                  <tr key={ev.id}>
                    <td>
                      <span className="eval-emp">{ev.employee_name || `#${ev.employee_id}`}</span>
                    </td>
                    <td>{ev.reference_month}</td>
                    <td>
                      <span className="eval-score">
                        <Star size={14} />
                        {ev.score}
                      </span>
                    </td>
                    <td>{ev.technical_score}</td>
                    <td>{ev.behavioral_score}</td>
                    <td>{ev.evaluation_type || '-'}</td>
                    <td>
                      <span className={`status-badge status-${ev.status}`}>
                        {ev.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!evaluations.length && (
              <p className="empty-state">Nenhuma avaliação cadastrada</p>
            )}
          </div>
        )}
      </DataCard>

      {open && (
        <div className="modal-overlay" onClick={() => setOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Nova Avaliação</h2>
              <button className="modal-close" onClick={() => setOpen(false)}>×</button>
            </div>
            <EvaluationForm onSubmit={handleSubmit} />
          </div>
        </div>
      )}
    </div>
  );
};

export default EvaluationsPage;
