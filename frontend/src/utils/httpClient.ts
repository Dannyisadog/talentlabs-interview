import type { AxiosRequestConfig, AxiosResponse } from 'axios';
import axios from 'axios';

// Create an axios instance with default config
const httpClient = axios.create({
  baseURL: 'http://localhost:8000/api/v0',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzQ3NDEzNTEyLCJ0eXBlIjoiYWNjZXNzIn0.yVaf46Whnd9D-zKAOtqki2M6tEv2jI7tg_eywiqSeWk',
  },
});

// Request interceptor for setting auth token
httpClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Simple wrapper functions for common HTTP methods
export const get = async <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
  const response = await httpClient.get<T, AxiosResponse<T>>(url, config);
  return response.data;
};

export const post = async <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
  const response = await httpClient.post<T, AxiosResponse<T>>(url, data, config);
  return response.data;
};

export const put = async <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
  const response = await httpClient.put<T, AxiosResponse<T>>(url, data, config);
  return response.data;
};

export const del = async <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
  const response = await httpClient.delete<T, AxiosResponse<T>>(url, config);
  return response.data;
};

export default httpClient; 