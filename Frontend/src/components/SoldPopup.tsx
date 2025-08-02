import React from 'react';
import type { Player, Team } from '../types';
import './SoldPopup.css';
import Sold from './Sold';

interface SoldPopupProps {
  player: Player;
  team: Team;
  onClose: () => void;
}

const SoldPopup: React.FC<SoldPopupProps> = ({ player, team, onClose }) => {
  return (
    <div className="sold-popup-overlay">
      <div className="sold-popup">
        <button className="close-btn" onClick={onClose}>&times;</button>
        {/* <h2>SOLD!</h2> */}
        <h2><Sold isAnimationNeeded={true} /></h2>
        <div className="sold-info">
          <img src={player.photo} alt={player.name} className="sold-player-photo" />
          <div>
            <h3>{player.name}</h3>
            <p>to</p>
            <div className="sold-team">
              <img src={team.ownerPhoto} alt={team.owner} className="sold-team-owner-photo" />
              <span>{team.name}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SoldPopup;