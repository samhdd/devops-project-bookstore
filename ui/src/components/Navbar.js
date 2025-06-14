// src/components/Navbar.js
import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';
import '../assets/styles/Navbar.css';

function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const profileMenuRef = useRef(null);
  
  // Close profile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setProfileMenuOpen(false);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    logout();
    setProfileMenuOpen(false);
  };
  
  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/">
          <span className="logo-text">Prepare.sh Book Shop</span>
        </Link>
      </div>
      
      <div className="mobile-menu-button" onClick={() => setMenuOpen(!menuOpen)}>
        <span>☰</span>
      </div>
      
      <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
        <Link to="/category/classics" onClick={() => setMenuOpen(false)}>Classics</Link>
        <Link to="/category/modern" onClick={() => setMenuOpen(false)}>Modern</Link>
        <Link to="/category/poetry" onClick={() => setMenuOpen(false)}>Poetry</Link>
        <Link to="/category/fiction" onClick={() => setMenuOpen(false)}>Fiction</Link>
      </div>
      
      <div className="nav-right">
        <div className="cart-icon">
          <Link to="/cart">
            <span className="material-icons">shopping_cart</span>
          </Link>
        </div>
        
        {isAuthenticated() ? (
          <div className="profile-dropdown" ref={profileMenuRef}>
            <div 
              className="profile-avatar" 
              onClick={() => setProfileMenuOpen(!profileMenuOpen)}
            >
              {user?.email?.charAt(0).toUpperCase() || "U"}
            </div>
            
            {profileMenuOpen && (
              <div className="profile-menu">
                <div className="profile-menu-header">
                  <p className="profile-menu-name">{user?.firstName || "User"}</p>
                  <p className="profile-menu-email">{user?.email}</p>
                </div>
                <div className="profile-menu-items">
                  <Link to="/profile" onClick={() => setProfileMenuOpen(false)}>My Profile</Link>
                  {user?.role === 'admin' && (
                    <Link to="/admin" onClick={() => setProfileMenuOpen(false)}>Admin Dashboard</Link>
                  )}
                  <button onClick={handleLogout}>Logout</button>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="auth-links">
            <Link to="/login" className="login-button">Login</Link>
            <Link to="/register" className="register-button">Register</Link>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;