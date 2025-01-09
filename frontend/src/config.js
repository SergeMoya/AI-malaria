const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Debug log for API URL
console.log('API_URL:', API_URL);

export const endpoints = {
  healthcheck: `${API_URL}/api/healthcheck`,
  analyze: `${API_URL}/api/analyze`,
};

// Debug log for endpoints
console.log('Configured endpoints:', endpoints);

export default endpoints;
