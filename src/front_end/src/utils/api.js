import axios from 'axios';

// Cria uma instância centralizada do axios para toda a aplicação
const api = axios.create({
  // O Vite injeta as variáveis do .env através do import.meta.env
  // O fallback para localhost ajuda caso o .env não exista acidentalmente.
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080',
});

// Interceptor de requisições:
// Antes de qualquer chamada HTTP, ele verifica se existe um token no localStorage
// Se existir, injeta automaticamente nos headers de Autenticação.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default api;
