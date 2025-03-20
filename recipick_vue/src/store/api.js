import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export function setAuthToken(token) {
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;
  } else {
    delete apiClient.defaults.headers.common['Authorization'];
  }
}

export default apiClient;
