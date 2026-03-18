import React, { useState, useEffect } from 'react';
import { fetchDepartments } from '../services/departments';
import { fetchPositions } from '../services/positions';
import Button from './ui/Button';
import './EmployeeForm.css';

interface EmployeeFormProps {
  onSubmit: (data: any) => void;
}

const EmployeeForm: React.FC<EmployeeFormProps> = ({ onSubmit }) => {
  const [departments, setDepartments] = useState<{ id: number; name: string }[]>([]);
  const [positions, setPositions] = useState<{ id: number; title: string }[]>([]);
  const [form, setForm] = useState({
    full_name: '',
    cpf: '',
    rg: '',
    birth_date: '',
    address: '',
    phone: '',
    email: '',
    work_card_number: '',
    work_card_series: '1234',
    admission_date: new Date().toISOString().slice(0, 10),
    status: 'ativo',
    department_id: 1,
    position_id: 1,
    salary: 4000,
    pis_pasep: '',
    bank_name: 'Banco do Brasil',
    bank_agency: '',
    bank_account: '',
    bank_account_type: 'corrente',
  });

  useEffect(() => {
    Promise.all([fetchDepartments(), fetchPositions()]).then(([d, p]) => {
      const depts = Array.isArray(d) ? d : [];
      const pos = Array.isArray(p) ? p : [];
      setDepartments(depts);
      setPositions(pos);
      if (depts.length || pos.length) {
        setForm(prev => ({
          ...prev,
          ...(depts.length && { department_id: depts[0].id }),
          ...(pos.length && { position_id: pos[0].id }),
        }));
      }
    });
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    let val: any = value;
    if (name === 'salary') val = parseFloat(value) || 0;
    else if (name === 'department_id' || name === 'position_id') val = parseInt(value) || 1;
    setForm(prev => ({ ...prev, [name]: val }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} className="employee-form">
      <div className="form-row">
        <div className="form-field">
          <label>Nome completo</label>
          <input name="full_name" value={form.full_name} onChange={handleChange} required />
        </div>
        <div className="form-field">
          <label>CPF</label>
          <input name="cpf" value={form.cpf} onChange={handleChange} required />
        </div>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>RG</label>
          <input name="rg" value={form.rg} onChange={handleChange} required />
        </div>
        <div className="form-field">
          <label>Data Nascimento</label>
          <input name="birth_date" type="date" value={form.birth_date} onChange={handleChange} required />
        </div>
      </div>
      <div className="form-field">
        <label>Endereço</label>
        <input name="address" value={form.address} onChange={handleChange} required />
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>Telefone</label>
          <input name="phone" value={form.phone} onChange={handleChange} required />
        </div>
        <div className="form-field">
          <label>E-mail</label>
          <input name="email" type="email" value={form.email} onChange={handleChange} required />
        </div>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>CTPS Número</label>
          <input name="work_card_number" value={form.work_card_number} onChange={handleChange} required />
        </div>
        <div className="form-field">
          <label>CTPS Série</label>
          <input name="work_card_series" value={form.work_card_series} onChange={handleChange} />
        </div>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>Data Admissão</label>
          <input name="admission_date" type="date" value={form.admission_date} onChange={handleChange} required />
        </div>
        <div className="form-field">
          <label>Status</label>
          <select name="status" value={form.status} onChange={handleChange}>
            <option value="ativo">Ativo</option>
            <option value="inativo">Inativo</option>
          </select>
        </div>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>Departamento</label>
          <select name="department_id" value={form.department_id} onChange={handleChange} required>
            {departments.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
          </select>
        </div>
        <div className="form-field">
          <label>Cargo</label>
          <select name="position_id" value={form.position_id} onChange={handleChange} required>
            {positions.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
          </select>
        </div>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>Salário</label>
          <input name="salary" type="number" value={form.salary} onChange={handleChange} required />
        </div>
        <div className="form-field">
          <label>PIS/PASEP</label>
          <input name="pis_pasep" value={form.pis_pasep} onChange={handleChange} required />
        </div>
      </div>
      <div className="form-row">
        <div className="form-field">
          <label>Banco</label>
          <input name="bank_name" value={form.bank_name} onChange={handleChange} />
        </div>
        <div className="form-field">
          <label>Agência</label>
          <input name="bank_agency" value={form.bank_agency} onChange={handleChange} required />
        </div>
        <div className="form-field">
          <label>Conta</label>
          <input name="bank_account" value={form.bank_account} onChange={handleChange} required />
        </div>
        <div className="form-field">
          <label>Tipo</label>
          <select name="bank_account_type" value={form.bank_account_type} onChange={handleChange}>
            <option value="corrente">Corrente</option>
            <option value="poupanca">Poupança</option>
          </select>
        </div>
      </div>
      <div className="form-actions">
        <Button type="submit">Salvar</Button>
      </div>
    </form>
  );
};

export default EmployeeForm;
