import React from 'react';
import type { Team } from '../types';
import './TeamPlayerListPopup.css';

interface TeamPlayerListPopupProps {
  team: Team;
  onClose: () => void;
}

const TeamPlayerListPopup: React.FC<TeamPlayerListPopupProps> = ({ team, onClose }) => {
  return (
    <div className="team-player-popup-overlay">
      <div className="team-player-popup">
        <button className="close-btn" onClick={onClose}>&times;</button>
        <h2>{team.name} Players</h2>
        <ul className="player-list">
          {team.players.length === 0 && <li>No players yet.</li>}
          {team.players.map(player => (
            <li key={player.id} className="player-list-item">
              <img src={player.photo} alt={player.name} className="player-photo" />
              <span>{player.name}</span>
              <span className="player-type">{player.type}</span>
              <span className={`category-badge ${player.category.toLowerCase()}`}>{player.category}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default TeamPlayerListPopup;