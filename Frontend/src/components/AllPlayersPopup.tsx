import React, { useEffect } from 'react';
import type { Team } from '../types';
import './AllPlayersPopup.css';

interface AllPlayersPopupProps {
  teams: Team[];
  onClose: () => void;
}

const AllPlayersPopup: React.FC<AllPlayersPopupProps> = ({ teams, onClose }) => {
  // Get all players from all teams
  const allPlayers = teams.flatMap(team => 
    team.players.map(player => ({
      ...player,
      teamName: team.name,
      teamOwner: team.owner
    }))
  );

  // Group players by team
  const playersByTeam = teams.reduce((acc, team) => {
    acc[team.name] = team.players;
    return acc;
  }, {} as Record<string, any[]>);

  // Handle escape key to close popup
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  // Handle click outside to close popup
  const handleOverlayClick = (event: React.MouseEvent) => {
    if (event.target === event.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="all-players-popup-overlay" onClick={handleOverlayClick}>
      <div className="all-players-popup">
        <div className="popup-header">
          <h2>All Players Across Teams</h2>
        </div>
        
        <div className="popup-content">
          {allPlayers.length === 0 ? (
            <div className="no-players">
              <p>No players have been sold yet.</p>
            </div>
          ) : (
            <div className="teams-summary">
              <div className="summary-stats">
                <div className="stat-item">
                  <span className="stat-label">Total Players:</span>
                  <span className="stat-value">{allPlayers.length}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Teams with Players:</span>
                  <span className="stat-value">
                    {Object.keys(playersByTeam).filter(teamName => playersByTeam[teamName].length > 0).length}
                  </span>
                </div>
              </div>
              
              <div className="teams-list">
                {teams.map(team => (
                  <div key={team.id} className="team-section">
                    <div className="team-header">
                      <h3>{team.name}</h3>
                      <span className="owner">Owner: {team.owner}</span>
                      <span className="player-count">
                        {team.players.length} player{team.players.length !== 1 ? 's' : ''}
                      </span>
                    </div>
                    
                    {team.players.length > 0 ? (
                      <div className="players-grid">
                        {team.players.map(player => (
                          <div key={player.id} className="player-card">
                            <div className="player-photo">
                              <img src={player.photo} alt={player.name} />
                            </div>
                            <div className="player-info">
                              <h4>{player.name}</h4>
                              <p className="player-position">{player.type}</p>
                              <span className={`category-badge ${player.category.toLowerCase()}`}>
                                {player.category}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="no-team-players">No players yet</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AllPlayersPopup; 