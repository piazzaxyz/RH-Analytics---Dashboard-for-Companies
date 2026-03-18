import api from './api';

export async function fetchDashboardOverview() {
  const response = await api.get('/dashboard/overview');
  return response.data;
}

export async function fetchPayrollEvolution() {
  const response = await api.get('/dashboard/payroll-evolution');
  return response.data;
}

export async function fetchHeadcountByDepartment() {
  const response = await api.get('/dashboard/headcount-by-department');
  return response.data;
}

export async function fetchOvertimeByDepartment() {
  const response = await api.get('/dashboard/overtime-by-department');
  return response.data;
}
