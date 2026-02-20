import axios from 'axios';

// Configure axios defaults
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for file uploads
  withCredentials: true, // include cookies for session auth
  // Do not set a default Content-Type here so multipart/form-data uploads
  // will use the correct boundary automatically when FormData is used.
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Mark requests from JS as AJAX so Flask can return JSON errors/responses
    // Use the headers object methods if available, otherwise fall back to plain assignment
    try {
      // @ts-ignore - axios types may differ across versions
      if (config.headers && typeof (config.headers as any).set === 'function') {
        // axios v1 AxiosHeaders
        (config.headers as any).set('X-Requested-With', 'XMLHttpRequest');
      } else if (config.headers) {
        (config.headers as any)['X-Requested-With'] = 'XMLHttpRequest';
      } else {
        config.headers = { 'X-Requested-With': 'XMLHttpRequest' } as any;
      }
    } catch (e) {
      // best-effort - don't block request if header assignment fails
      // @ts-ignore
      config.headers = { ...(config.headers || {}), 'X-Requested-With': 'XMLHttpRequest' };
    }
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.code === 'ECONNREFUSED') {
      console.error('Backend server is not running');
    }
    return Promise.reject(error);
  }
);

export { API_BASE_URL };

export async function authLogin(email: string, password: string) {
  return api.post('/login', { email, password });
}

export async function authRegister(email: string, password: string, display_name?: string) {
  return api.post('/register', { email, password, display_name });
}

export async function authLogout() {
  return api.get('/logout');
}