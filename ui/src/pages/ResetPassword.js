import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import '../assets/styles/Auth.css';

const ResetPassword = () => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [validToken, setValidToken] = useState(false);
  const [verifying, setVerifying] = useState(true);
  const { token } = useParams();
  const navigate = useNavigate();
  
  // Verify token on component mount
  useEffect(() => {
    const verifyToken = async () => {
      try {
        const response = await fetch(`/api/auth/reset-password/${token}`);
        const data = await response.json();
        
        if (data.success) {
          setValidToken(true);
        } else {
          setError('This password reset link is invalid or has expired.');
        }
      } catch (err) {
        setError('An error occurred while verifying the token.');
        console.error('Token verification error:', err);
      } finally {
        setVerifying(false);
      }
    };
    
    if (token) {
      verifyToken();
    } else {
      setError('No reset token provided.');
      setVerifying(false);
    }
  }, [token]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }
    
    setLoading(true);
    
    try {
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token, password }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setMessage('Your password has been reset successfully.');
        // Redirect to login after a short delay
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } else {
        setError(data.message || 'An error occurred. Please try again.');
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
      console.error('Reset password error:', err);
    } finally {
      setLoading(false);
    }
  };
  
  if (verifying) {
    return (
      <div className="auth-container">
        <div className="auth-form-container">
          <h2>Reset Password</h2>
          <p>Verifying your reset link...</p>
        </div>
      </div>
    );
  }
  
  if (!validToken) {
    return (
      <div className="auth-container">
        <div className="auth-form-container">
          <h2>Invalid Reset Link</h2>
          <div className="auth-error">{error}</div>
          <div className="auth-links">
            <p>
              <Link to="/forgot-password">Request a new password reset</Link>
            </p>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="auth-container">
      <div className="auth-form-container">
        <h2>Reset Your Password</h2>
        
        {error && <div className="auth-error">{error}</div>}
        {message && <div className="auth-success">{message}</div>}
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="password">New Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter new password"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="confirm-password">Confirm Password</label>
            <input
              type="password"
              id="confirm-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm new password"
              required
            />
          </div>
          
          <button 
            type="submit" 
            className="auth-submit-button"
            disabled={loading}
          >
            {loading ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ResetPassword;
