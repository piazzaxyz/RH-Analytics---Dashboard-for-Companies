import api from './api';

export async function fetchEvaluations(params?: { employee_id?: number; month?: string }) {
  const response = await api.get('/evaluations/', { params });
  return response.data;
}

export async function createEvaluation(data: any) {
  const response = await api.post('/evaluations/', data);
  return response.data;
}
