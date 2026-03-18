import api from './api';

export async function fetchTimesheets(params?: { employee_id?: number; month?: string }) {
  const response = await api.get('/timesheets/', { params });
  return response.data;
}

export async function importTimesheet(file: File, format: string = 'csv') {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post(`/timesheets/import?format=${format}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}
