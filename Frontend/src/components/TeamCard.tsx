import React from 'react';
import type { Team } from '../types';
import './TeamCard.css';

interface TeamCardProps {
  team: Team;
}

const TeamCard: React.FC<TeamCardProps> = ({ team }) => {
  return (
    <div className="team-card">
      <div className="team-header">
        <img src={team.ownerPhoto} alt={team.owner} className="owner-photo" />
        <div>
          <h4>{team.name}</h4>
          <span className="owner-name">Owner: {team.owner}</span>
        </div>
      </div>
      <div className="team-info">
        <div>Players: {team.totalPlayers}/{team.maxPlayers}</div>
        <div className="category-counts">
          <span className="gold">Gold: {team.goldCount}/{team.maxGold}</span>
          <span className="silver">Silver: {team.silverCount}/{team.maxSilver}</span>
          <span className="bronze">Bronze: {team.bronzeCount}/{team.maxBronze}</span>
        </div>
        <div>Budget: ${team.remaining} / ${team.budget}</div>
      </div>
    </div>
  );
};

export default TeamCard;