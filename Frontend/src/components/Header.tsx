import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import './Header.css';

const Header: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <header className="header">
  <nav className="nav-container">
    <div className="tournament-name">Maxx Glory Premier League 2025</div>
    <div className="nav-links-wrapper">
      <ul className="nav-list">
        <li><NavLink to="/dashboard" className={({ isActive }) => isActive ? 'active' : ''}>Dashboard</NavLink></li>
        <li><NavLink to="/players" className={({ isActive }) => isActive ? 'active' : ''}>Player List</NavLink></li>
        <li><NavLink to="/auction-info" className={({ isActive }) => isActive ? 'active' : ''}>Auction Info</NavLink></li>
        <li><NavLink to="/teams" className={({ isActive }) => isActive ? 'active' : ''}>Teams</NavLink></li>
      </ul>
    </div>
    <button onClick={handleLogout} className="logout-button">Logout</button>
  </nav>
</header>

    
  );
};

export default Header;

