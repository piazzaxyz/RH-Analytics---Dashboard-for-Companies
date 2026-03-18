import axios, { AxiosError } from 'axios';
import { getToken, removeToken } from './auth';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
});

let isRedirecting = false;

api.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => {
    isRedirecting = false;
    return response;
  },
  (error: AxiosError) => {
    isRedirecting = false;
    const status = error.response?.status;
    const url = error.config?.url || '';
    const hadToken = !!error.config?.headers?.Authorization;
    const detail = String(error.response?.data?.detail || '').toLowerCase();

    if (status === 401 && !isRedirecting && error.response) {
      const isLoginRequest = url.includes('/auth/login');
      const isAuthError = detail.includes('token') || detail.includes('autentic') || detail.includes('unauthorized') || detail.includes('não encontrado') || detail.includes('inativo');
      if (!isLoginRequest && hadToken && isAuthError) {
        isRedirecting = true;
        removeToken();
        window.location.replace('/login');
      }
    }
    return Promise.reject(error);
  }
);

export default api;
