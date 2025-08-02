import React from 'react';
import type { Player } from '../types';
import './PlayerCard.css';

interface PlayerCardProps {
  player: Player;
}

const typeColors: Record<Player['type'], string> = {
  Batter: '#f7c873',
  Bowler: '#7ec4cf',
  Allrounder: '#b6e388',
};

const PlayerCard: React.FC<PlayerCardProps> = ({ player }) => {
  return (
    <div className="player-card" style={{ background: typeColors[player.type] }}>
      <div className="player-photo-container">
        <img src={player.photo} alt={player.name} className="player-photo" />
        <span className="player-type-badge">{player.type}</span>
      </div>
      <div className="player-info">
        <h3>{player.name}</h3>
        <p>Age: {player.age}</p>
        <p>Category: {player.category}</p>
        <p>Category: <span className={`category-badge ${player.category.toLowerCase()}`}>{player.category}</span></p>
      </div>
    </div>
  );
};

export default PlayerCard;