import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';

// Component to protect routes that require authentication
export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // If still checking authentication status, show nothing or a spinner
  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  // If not authenticated, redirect to login with return path
  if (!isAuthenticated()) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If authenticated, render children or outlet
  return children ? children : <Outlet />;
};

// Component to protect routes that require admin role
export const AdminRoute = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();
  const location = useLocation();

  // If still checking authentication status, show nothing or a spinner
  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  // If not authenticated or not admin, redirect
  if (!isAuthenticated()) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  if (!isAdmin()) {
    return <Navigate to="/" replace />;
  }

  // If authenticated and admin, render children or outlet
  return children ? children : <Outlet />;
};

export default ProtectedRoute;
