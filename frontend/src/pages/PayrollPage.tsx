import React, { useState, useEffect } from 'react';
import { DollarSign, Loader2, Calculator } from 'lucide-react';
import Button from '../components/ui/Button';
import DataCard from '../components/ui/DataCard';
import { fetchPayrolls, processPayroll } from '../services/payroll';
import './PayrollPage.css';

const PayrollPage: React.FC = () => {
  const [payrolls, setPayrolls] = useState<any[]>([]);
  const [month, setMonth] = useState(new Date().toISOString().slice(0, 7));
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  const loadPayrolls = () => {
    setLoading(true);
    fetchPayrolls(month)
      .then(setPayrolls)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadPayrolls();
  }, [month]);

  const handleProcess = async () => {
    if (!month) return;
    setProcessing(true);
    try {
      await processPayroll(month);
      loadPayrolls();
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="payroll-page">
      <header className="page-header">
        <div>
          <h1>Folha de Pagamento</h1>
          <p className="page-subtitle">Processamento e consulta de folha</p>
        </div>
        <div className="payroll-actions">
          <input
            type="month"
            value={month}
            onChange={(e) => setMonth(e.target.value)}
            className="month-input"
          />
          <Button
            icon={Calculator}
            onClick={handleProcess}
            loading={processing}
          >
            Processar Folha
          </Button>
        </div>
      </header>

      <DataCard title={`Folhas - ${month}`}>
        {loading ? (
          <div className="table-loading">
            <Loader2 size={32} className="spin" />
            <p>Carregando...</p>
          </div>
        ) : (
          <div className="payroll-grid">
            {payrolls.map((p) => (
              <div key={p.id} className="payroll-card">
                <div className="payroll-card__icon">
                  <DollarSign size={20} />
                </div>
                <div className="payroll-card__content">
                  <span className="payroll-card__month">{p.reference_month}</span>
                  <span className="payroll-card__emp">Colaborador #{p.employee_id}</span>
                  <span className="payroll-card__net">
                    R$ {p.net_salary?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </span>
                </div>
                <span className={`status-badge status-${p.status}`}>{p.status}</span>
              </div>
            ))}
            {!payrolls.length && (
              <p className="empty-state">Nenhuma folha para este mês. Clique em Processar Folha.</p>
            )}
          </div>
        )}
      </DataCard>
    </div>
  );
};

export default PayrollPage;
