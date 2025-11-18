import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../api/authService';

// 1. Create the Auth Context
const AuthContext = createContext();

// 2. Create the Auth Provider component
export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);

  useEffect(() => {
    if (token) {
      // Set token in localStorage
      localStorage.setItem('token', token);
      
      // Set token in axios default headers for all future requests
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      setIsAuthenticated(true);
    } else {
      // Clear token from localStorage
      localStorage.removeItem('token');
      
      // Remove token from axios default headers
      delete apiClient.defaults.headers.common['Authorization'];
      
      setIsAuthenticated(false);
    }
  }, [token]);

  const login = (newToken) => {
    setToken(newToken);
  };

  const logout = () => {
    setToken(null);
  };

  const value = {
    isAuthenticated,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// 3. Create a custom hook to easily use the context
export function useAuth() {
  return useContext(AuthContext);
}