import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Users, DollarSign, TrendingDown, Activity } from 'lucide-react';
import StatCard from '../components/ui/StatCard';
import DataCard from '../components/ui/DataCard';
import { fetchDashboardOverview, fetchPayrollEvolution, fetchHeadcountByDepartment, fetchOvertimeByDepartment } from '../services/dashboard';
import './DashboardPage.css';

const COLORS = ['#3b82f6', '#22c55e', '#f59e0b', '#8b5cf6', '#ec4899'];

const DashboardPage: React.FC = () => {
  const [overview, setOverview] = useState<any>(null);
  const [evolution, setEvolution] = useState<any>(null);
  const [headcount, setHeadcount] = useState<any[]>([]);
  const [overtime, setOvertime] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetchDashboardOverview(),
      fetchPayrollEvolution(),
      fetchHeadcountByDepartment(),
      fetchOvertimeByDepartment(),
    ])
      .then(([ov, ev, hc, ot]) => {
        setOverview(ov);
        setEvolution(ev);
        setHeadcount(hc);
        setOvertime(ot);
      })
      .catch(() => setError('Erro ao carregar dados'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="page-loading">
        <div className="page-loading__spinner" />
        <p>Carregando dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-error">
        <p>{error}</p>
      </div>
    );
  }

  const evolutionData = evolution?.months?.map((m: string, i: number) => ({
    month: m.slice(-2) + '/' + m.slice(0, 4),
    valor: evolution.values[i] || 0,
  })) || [];

  const headcountData = headcount?.map((h: any) => ({
    name: h.department_name,
    value: h.headcount,
  })) || [];

  return (
    <div className="dashboard-page">
      <header className="page-header">
        <h1>Dashboard</h1>
        <p className="page-subtitle">Visão geral do RH e indicadores</p>
      </header>

      <div className="stats-grid">
        <StatCard
          title="Headcount Ativo"
          value={overview?.headcount ?? 0}
          icon={Users}
          accent="blue"
        />
        <StatCard
          title="Folha Total (R$)"
          value={overview?.total_payroll?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) ?? '0,00'}
          icon={DollarSign}
          accent="green"
        />
        <StatCard
          title="Turnover"
          value={`${((overview?.turnover_rate ?? 0) * 100).toFixed(1)}%`}
          icon={TrendingDown}
          accent="amber"
        />
        <StatCard
          title="Absenteísmo"
          value={`${((overview?.absenteeism_rate ?? 0) * 100).toFixed(1)}%`}
          icon={Activity}
          accent="violet"
        />
      </div>

      <div className="charts-grid">
        <DataCard title="Evolução da Folha (últimos 12 meses)">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={evolutionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `R$${v}`} />
                <Tooltip formatter={(v: number) => [`R$ ${v.toLocaleString('pt-BR')}`, 'Valor']} />
                <Bar dataKey="valor" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </DataCard>

        <DataCard title="Headcount por Departamento">
          <div className="chart-container pie-chart">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={headcountData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  {headcountData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v: number) => [v, 'Colaboradores']} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </DataCard>
      </div>

      <DataCard title="Horas Extras por Departamento">
        <div className="overtime-table">
          {overtime?.length ? (
            overtime.map((o: any) => (
              <div key={o.department_id} className="overtime-row">
                <span className="overtime-dept">{o.department_name}</span>
                <span className="overtime-hours">{o.overtime_hours?.toFixed(1) ?? 0}h</span>
              </div>
            ))
          ) : (
            <p className="empty-state">Nenhum dado de horas extras</p>
          )}
        </div>
      </DataCard>
    </div>
  );
};

export default DashboardPage;
