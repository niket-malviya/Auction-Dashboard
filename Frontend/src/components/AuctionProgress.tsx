import React from 'react';
import './AuctionProgress.css';

interface AuctionProgressProps {
  currentPlayer: number;
  totalPlayers: number;
  goldSelected: number;
  maxGold: number;
  silverSelected: number;
  maxSilver: number;
  bronzeSelected: number;
  maxBronze: number;
}

const AuctionProgress: React.FC<AuctionProgressProps> = ({
  currentPlayer,
  totalPlayers,
  goldSelected,
  maxGold,
  silverSelected,
  maxSilver,
  bronzeSelected,
  maxBronze
}) => {
  const overallProgress = (currentPlayer / totalPlayers) * 100;
  const goldProgress = (goldSelected / maxGold) * 100;
  const silverProgress = (silverSelected / maxSilver) * 100;
  const bronzeProgress = (bronzeSelected / maxBronze) * 100;

  return (
    <div className="auction-progress-section">
      <div className="combined-progress">
        <div className="progress-item">
          <div className="progress-label">
            <span>Auction</span>
            <span className="progress-count">Player {currentPlayer} of {totalPlayers}</span>
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${overallProgress}%` }}></div>
          </div>
        </div>
        
        <div className="progress-item">
          <div className="progress-label">
            <span className="category-icon gold">●</span>
            <span>Gold</span>
            <span className="progress-count">{goldSelected}/{maxGold}</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill gold-fill" 
              style={{ width: `${goldProgress}%` }}
            ></div>
          </div>
        </div>
        
        <div className="progress-item">
          <div className="progress-label">
            <span className="category-icon silver">●</span>
            <span>Silver</span>
            <span className="progress-count">{silverSelected}/{maxSilver}</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill silver-fill" 
              style={{ width: `${silverProgress}%` }}
            ></div>
          </div>
        </div>
        
        <div className="progress-item">
          <div className="progress-label">
            <span className="category-icon bronze">●</span>
            <span>Bronze</span>
            <span className="progress-count">{bronzeSelected}/{maxBronze}</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill bronze-fill" 
              style={{ width: `${bronzeProgress}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuctionProgress; 