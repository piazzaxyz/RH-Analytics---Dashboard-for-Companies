import React, { useState, useEffect } from 'react';
import { fetchEmployees } from '../services/employee';
import Button from './ui/Button';
import './EmployeeForm.css';

interface LoanFormProps {
  onSubmit: (data: any) => void;
}

const LoanForm: React.FC<LoanFormProps> = ({ onSubmit }) => {
  const [employees, setEmployees] = useState<{ id: number; full_name: string }[]>([]);
  const [form, setForm] = useState({
    employee_id: 0,
    total_amount: 5000,
    installments_count: 12,
    reason: '',
    start_month: new Date().toISOString().slice(0, 7),
  });

  useEffect(() => {
    fetchEmployees({ limit: 500 }).then((data: any) => {
      const list = Array.isArray(data) ? data : [];
      setEmployees(list);
      if (list.length) setForm(prev => ({ ...prev, employee_id: list[0].id }));
    });
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    let val: any = value;
    if (name === 'total_amount') val = parseFloat(value) || 0;
    else if (name === 'installments_count') val = parseInt(value) || 1;
    else if (name === 'employee_id') val = parseInt(value) || 0;
    setForm(prev => ({ ...prev, [name]: val }));
  };

  const monthlyDiscount = form.installments_count > 0
    ? (form.total_amount / form.installments_count).toFixed(2)
    : '0.00';

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      ...form,
      monthly_discount: parseFloat(monthlyDiscount),
      status: 'ativo',
    });
  };

  return (
    <form onSubmit={handleSubmit} className="employee-form">
      <div className="form-field">
        <label>Colaborador</label>
        <select name="employee_id" value={form.employee_id} onChange={handleChange} required>
          {employees.map(emp => (
            <option key={emp.id} value={emp.id}>{emp.full_name}</option>
          ))}
        </select>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>Valor Total (R$)</label>
          <input
            name="total_amount"
            type="number"
            min={0}
            step={0.01}
            value={form.total_amount}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-field">
          <label>Nº de Parcelas</label>
          <input
            name="installments_count"
            type="number"
            min={1}
            max={60}
            value={form.installments_count}
            onChange={handleChange}
            required
          />
        </div>
      </div>
      <div className="form-field">
        <label>Parcela Mensal</label>
        <input
          type="text"
          value={`R$ ${parseFloat(monthlyDiscount).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
          readOnly
          style={{ background: 'var(--content-bg)', cursor: 'not-allowed' }}
        />
      </div>
      <div className="form-field">
        <label>Mês Início</label>
        <input
          name="start_month"
          type="month"
          value={form.start_month}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-field">
        <label>Motivo</label>
        <input
          name="reason"
          value={form.reason}
          onChange={handleChange}
          placeholder="Ex: Aquisição de imóvel, emergência médica..."
          required
        />
      </div>
      <div className="form-actions">
        <Button type="submit">Salvar Empréstimo</Button>
      </div>
    </form>
  );
};

export default LoanForm;
