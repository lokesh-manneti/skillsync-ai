import axios from 'axios';

// Create an axios instance pointing to our proxy
const apiClient = axios.create({
  baseURL: '/api', // NO trailing slash
});

// This interceptor (from geminicli) automatically attaches the token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const registerUser = (email, password) => {
  return apiClient.post('/auth/register', { email, password });
};

export const loginUser = (email, password) => {
  const data = {
    username: email,
    password: password
  };
  return apiClient.post('/auth/login', data, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
};

export const uploadResume = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/resume/upload', formData);
};

export const getResumeHistory = () => {
  return apiClient.get('/resume/history');
};

export const getSkillGapAnalysis = (resumeId, roleName, learningPreference) => {
  return apiClient.post('/skill-gap/analyze', {
    resume_id: resumeId,
    role_name: roleName,
    learning_preference: learningPreference,
  });
};

export const getOptimizedResume = (resumeId, roleName) => {
  return apiClient.post('/resume/optimize', {
    resume_id: resumeId,
    role_name: roleName,
  });
};

export default apiClient;