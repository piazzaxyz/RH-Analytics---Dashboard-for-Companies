import api from './api';

export async function fetchPositions() {
  const response = await api.get('/positions/');
  return response.data;
}
