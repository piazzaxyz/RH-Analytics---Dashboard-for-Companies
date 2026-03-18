import React, { useState, useEffect, useCallback } from 'react';
import { Wallet, Loader2, Plus } from 'lucide-react';
import Button from '../components/ui/Button';
import DataCard from '../components/ui/DataCard';
import LoanForm from '../components/LoanForm';
import { fetchLoans, createLoan } from '../services/loan';
import { fetchEmployees } from '../services/employee';
import './LoansPage.css';

const LoansPage: React.FC = () => {
  const [loans, setLoans] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [employeesMap, setEmployeesMap] = useState<Record<number, string>>({});

  const loadLoans = useCallback(() => {
    setLoading(true);
    fetchLoans()
      .then(setLoans)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadLoans();
    fetchEmployees({ limit: 500 }).then((data: any) => {
      const list = Array.isArray(data) ? data : [];
      const map: Record<number, string> = {};
      list.forEach((e: any) => { map[e.id] = e.full_name; });
      setEmployeesMap(map);
    });
  }, [loadLoans]);

  const handleSubmit = async (data: any) => {
    try {
      await createLoan(data);
      loadLoans();
      setOpen(false);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Erro ao criar empréstimo';
      alert(msg);
    }
  };

  return (
    <div className="loans-page">
      <header className="page-header">
        <div>
          <h1>Empréstimos</h1>
          <p className="page-subtitle">Empréstimos consignados</p>
        </div>
        <Button icon={Plus} onClick={() => setOpen(true)}>
          Novo Empréstimo
        </Button>
      </header>

      <DataCard title="Lista de Empréstimos">
        {loading ? (
          <div className="table-loading">
            <Loader2 size={32} className="spin" />
            <p>Carregando...</p>
          </div>
        ) : (
          <div className="loans-grid">
            {loans.map((loan) => (
              <div key={loan.id} className="loan-card">
                <div className="loan-card__icon">
                  <Wallet size={20} />
                </div>
                <div className="loan-card__content">
                  <span className="loan-card__emp">{employeesMap[loan.employee_id] || `Colaborador #${loan.employee_id}`}</span>
                  <span className="loan-card__amount">
                    R$ {loan.total_amount?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </span>
                  <span className="loan-card__info">
                    {loan.installments_count}x de R$ {loan.monthly_discount?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </span>
                  <span className="loan-card__reason">{loan.reason}</span>
                </div>
                <span className={`status-badge status-${loan.status}`}>{loan.status}</span>
              </div>
            ))}
            {!loans.length && (
              <p className="empty-state">Nenhum empréstimo cadastrado</p>
            )}
          </div>
        )}
      </DataCard>

      {open && (
        <div className="modal-overlay" onClick={() => setOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Novo Empréstimo</h2>
              <button className="modal-close" onClick={() => setOpen(false)}>×</button>
            </div>
            <LoanForm onSubmit={handleSubmit} />
          </div>
        </div>
      )}
    </div>
  );
};

export default LoansPage;
