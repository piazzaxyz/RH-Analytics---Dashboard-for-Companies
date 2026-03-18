import api from './api';

export async function fetchLoans(params?: { employee_id?: number; status?: string }) {
  const response = await api.get('/loans/', { params });
  return response.data;
}

export async function createLoan(data: any) {
  const response = await api.post('/loans/', data);
  return response.data;
}
