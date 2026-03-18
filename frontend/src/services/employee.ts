import api from './api';

export async function fetchEmployees(params?: { skip?: number; limit?: number; search?: string }) {
  const response = await api.get('/employees/', { params });
  return response.data;
}

export async function createEmployee(data: any) {
  const response = await api.post('/employees/', data);
  return response.data;
}
