// 

import React from 'react';
import type { Player } from '../types';
import './PlayerCard.css';

interface PlayerCardProps {
  player: Player;
}

const getPlayerRole = (player: Player): string => {
  if (player.batterType && player.bowlerType) return 'Allrounder';
  if (player.batterType) return 'Batter';
  if (player.bowlerType) return 'Bowler';
  return 'N/A';
};

const PlayerCard: React.FC<PlayerCardProps> = ({ player }) => {
  const role = getPlayerRole(player);
  const categoryClass = player.category?.toLowerCase() || 'default';

  return (
    <div className={`player-card-v2 ${categoryClass}`}>
      <div className="card-header">
        <div className="player-image-wrapper">
          <img
            src={player.imgUrl || '/default-player.png'}
            alt={`${player.name}`}
            className="player-image"
          />
        </div>
        <span className="role-tag">{role}</span>
      </div>

      <div className="card-body">
        <h2 className="player-name">{player.name} {player.lastName}</h2>
        <div className="info-grid">
          <div>
            <span className="label">Age:</span> {player.age}
          </div>
          <div>
            <span className="label">Flat No:</span> {player.flatNo}
          </div>
          <div>
            <span className="label">Batting Style:</span> {player.batterType || 'N/A'}
          </div>
          <div>
            <span className="label">Bowling Style:</span> {player.bowlerType || 'N/A'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlayerCard;
