import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './AuthProvider';

function ProtectedRoute() {
  const { isAuthenticated } = useAuth();

  // If authenticated, render the child route (e.g., Dashboard)
  // If not, redirect to the /login page
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}

export default ProtectedRoute;