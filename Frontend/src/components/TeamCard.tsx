import React from 'react';
import type { Team } from '../types';
import { EyeIcon } from '@heroicons/react/24/outline';
import './TeamCard.css';

interface TeamCardProps {
  team: Team;
  onViewPlayers?: (team: Team) => void;
}

const TeamCard: React.FC<TeamCardProps> = ({ team, onViewPlayers }) => {
  const handleViewPlayers = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onViewPlayers) {
      onViewPlayers(team);
    }
  };

  return (
    <div className="team-card">
      {/* Team Header Section */}
      <div className="team-header">
        <div className="team-header-content">
          
        <img
  src={team.img_url }
  alt={`${team.name} Logo`}
  className="team-photo"
  onError={(e) => {
    e.currentTarget.onerror = null;
    e.currentTarget.src = '/default-photo.jpg'; // fallback if backend image fails
  }}
/>

          <div className="team-name-section">
            <h4 className="team-name">{team.name}</h4>
            <span className="owner-name">Owner: {team.owner}</span>
          </div>
        </div>
        {onViewPlayers && (
          <button 
            className="view-players-btn" 
            onClick={handleViewPlayers}
            title="View team players"
          >
            <EyeIcon className="eye-icon" />
          </button>
        )}
      </div>

      {/* Team Information Section */}
      <div className="team-info">
        <div className="budget-info">Budget: ${team.remaining}/${team.budget}</div>
        <div className="players-info">Players: {team.totalPlayers}/{team.maxPlayers}</div>
        <div className="max-bid-info">Max Bid: ${Math.max(0, team.remaining - (10 * (team.maxPlayers - team.totalPlayers)))}</div>
        <div className="category-info">
          <span className={`gold ${team.goldCount >= team.maxGold ? 'limit-reached' : ''}`}>
            Gold: {team.goldCount}/{team.maxGold}
          </span>
          <span className={`silver ${team.silverCount >= team.maxSilver ? 'limit-reached' : ''}`}>
            Silver: {team.silverCount}/{team.maxSilver}
          </span>
          {/* <span className={`bronze ${team.bronzeCount >= team.maxBronze ? 'limit-reached' : ''}`}>
            Bronze: {team.bronzeCount}/{team.maxBronze}
          </span> */}
        </div>
      </div>
    </div>
  );
};

export default TeamCard;