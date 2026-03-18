import React, { useState, useEffect } from 'react';
import { fetchEmployees } from '../services/employee';
import Button from './ui/Button';
import './EmployeeForm.css';

const EVALUATION_TYPES = [
  { value: 'comportamental', label: 'Comportamental' },
  { value: 'profissional', label: 'Profissional' },
  { value: 'academica', label: 'Acadêmica' },
  { value: 'tecnica', label: 'Técnica' },
  { value: 'outro', label: 'Outro' },
];

interface EvaluationFormProps {
  onSubmit: (data: any) => void;
}

const EvaluationForm: React.FC<EvaluationFormProps> = ({ onSubmit }) => {
  const [employees, setEmployees] = useState<{ id: number; full_name: string }[]>([]);
  const [form, setForm] = useState({
    employee_id: 0,
    evaluation_type: 'comportamental',
    reference_month: new Date().toISOString().slice(0, 7),
    technical_score: 7,
    behavioral_score: 7,
    notes: '',
    action_plan: '',
  });

  useEffect(() => {
    fetchEmployees({ limit: 500 }).then((data: any) => {
      const list = Array.isArray(data) ? data : [];
      setEmployees(list);
      if (list.length) setForm(prev => ({ ...prev, employee_id: list[0].id }));
    });
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    let val: any = value;
    if (name === 'technical_score' || name === 'behavioral_score') val = Math.min(10, Math.max(0, parseInt(value) || 0));
    else if (name === 'employee_id') val = parseInt(value) || 0;
    setForm(prev => ({ ...prev, [name]: val }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const score = Math.round((form.technical_score + form.behavioral_score) / 2);
    onSubmit({
      ...form,
      score,
      status: 'pendente',
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
      <div className="form-field">
        <label>Tipo de Avaliação</label>
        <select name="evaluation_type" value={form.evaluation_type} onChange={handleChange}>
          {EVALUATION_TYPES.map(t => (
            <option key={t.value} value={t.value}>{t.label}</option>
          ))}
        </select>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>Mês de Referência</label>
          <input
            name="reference_month"
            type="month"
            value={form.reference_month}
            onChange={handleChange}
            required
          />
        </div>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>Nota Técnica (0-10)</label>
          <input
            name="technical_score"
            type="number"
            min={0}
            max={10}
            value={form.technical_score}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-field">
          <label>Nota Comportamental (0-10)</label>
          <input
            name="behavioral_score"
            type="number"
            min={0}
            max={10}
            value={form.behavioral_score}
            onChange={handleChange}
            required
          />
        </div>
      </div>
      <div className="form-field">
        <label>Observações</label>
        <textarea
          name="notes"
          value={form.notes}
          onChange={handleChange}
          rows={3}
          style={{ padding: '10px 14px', borderRadius: 8, border: '1px solid var(--card-border)', fontFamily: 'inherit' }}
        />
      </div>
      <div className="form-field">
        <label>Plano de Ação</label>
        <textarea
          name="action_plan"
          value={form.action_plan}
          onChange={handleChange}
          rows={2}
          style={{ padding: '10px 14px', borderRadius: 8, border: '1px solid var(--card-border)', fontFamily: 'inherit' }}
        />
      </div>
      <div className="form-actions">
        <Button type="submit">Salvar Avaliação</Button>
      </div>
    </form>
  );
};

export default EvaluationForm;
