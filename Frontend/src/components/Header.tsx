import React from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <nav>
        <ul className="nav-list">
          <li><NavLink to="/dashboard" className={({ isActive }) => isActive ? 'active' : ''}>Dashboard</NavLink></li>
          <li><NavLink to="/players" className={({ isActive }) => isActive ? 'active' : ''}>Player List</NavLink></li>
          <li><NavLink to="/auction-info" className={({ isActive }) => isActive ? 'active' : ''}>Auction Info</NavLink></li>
          <li><NavLink to="/teams" className={({ isActive }) => isActive ? 'active' : ''}>Teams</NavLink></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;