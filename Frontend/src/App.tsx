import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuctionProvider } from './context/AuctionContext';
import Header from './components/Header';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import PlayerList from './pages/PlayerList';
import AuctionInfo from './pages/AuctionInfo';
import Teams from './pages/Teams';
import './App.css';

const AppContent: React.FC = () => {
  const location = useLocation();
  const hideHeaderRoutes = ["/login", "/register"];

  return (
    <>
      {!hideHeaderRoutes.includes(location.pathname) && <Header />}
      <div className="main-content">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/players" element={<PlayerList />} />
          <Route path="/auction-info" element={<AuctionInfo />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    </>
  );
};

const App: React.FC = () => {
  return (
    <AuctionProvider>
      <Router>
        <AppContent />
      </Router>
    </AuctionProvider>
  );
};

export default App;
