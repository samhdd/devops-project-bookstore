import React, { useState, useEffect } from 'react';
import { useAuth } from '../utils/AuthContext';
import { Navigate } from 'react-router-dom';
import '../assets/styles/Profile.css';

const Profile = () => {
  const { isAuthenticated, user, getProfile, logout } = useAuth();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState('');
  
  useEffect(() => {
    const fetchProfile = async () => {
      if (isAuthenticated()) {
        try {
          const result = await getProfile();
          if (result.success) {
            setProfile(result.user);
          } else {
            setError('Failed to load profile data');
          }
        } catch (err) {
          setError('An error occurred while loading your profile');
          console.error('Profile loading error:', err);
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };
    
    fetchProfile();
  }, [getProfile, isAuthenticated]);
  
  // Redirect to login if not authenticated
  if (!isAuthenticated() && !loading) {
    return <Navigate to="/login" replace />;
  }
  
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };
  
  const handleLogout = () => {
    logout();
  };
  
  if (loading) {
    return (
      <div className="profile-container">
        <div className="profile-card">
          <h2>Loading profile...</h2>
        </div>
      </div>
    );
  }
  
  return (
    <div className="profile-container">
      <div className="profile-card">
        <h2>My Profile</h2>
        
        {error && <div className="profile-error">{error}</div>}
        
        {profile && (
          <div className="profile-details">
            <div className="profile-header">
              <div className="profile-avatar">
                {profile.firstName && profile.lastName
                  ? `${profile.firstName.charAt(0)}${profile.lastName.charAt(0)}`
                  : profile.email.charAt(0).toUpperCase()}
              </div>
              <div className="profile-name">
                <h3>{profile.firstName} {profile.lastName}</h3>
                <p className="profile-email">{profile.email}</p>
                <p className="profile-role">Role: {profile.role}</p>
              </div>
            </div>
            
            <div className="profile-info">
              <div className="profile-info-item">
                <span className="profile-label">Account Created:</span>
                <span className="profile-value">{formatDate(profile.createdAt)}</span>
              </div>
              <div className="profile-info-item">
                <span className="profile-label">Last Login:</span>
                <span className="profile-value">{formatDate(profile.lastLogin)}</span>
              </div>
            </div>
            
            <div className="profile-actions">
              <button className="profile-button edit">Edit Profile</button>
              <button className="profile-button logout" onClick={handleLogout}>
                Log Out
              </button>
            </div>
            
            <div className="profile-sections">
              <div className="profile-section">
                <h4>Order History</h4>
                <p className="profile-placeholder">No orders yet.</p>
              </div>
              
              <div className="profile-section">
                <h4>Saved Addresses</h4>
                <p className="profile-placeholder">No addresses saved.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
