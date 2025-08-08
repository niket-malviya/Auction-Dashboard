import React, { useEffect, useState } from 'react';
import BidInput from '../components/BidInput';
import SoldPopup from '../components/SoldPopup';
import TeamPlayerListPopup from '../components/TeamPlayerListPopup';
import AllPlayersPopup from '../components/AllPlayersPopup';
import AuctionProgress from '../components/AuctionProgress';
import { EyeIcon } from '@heroicons/react/24/outline';
import './Dashboard.css';
import Sold from '../components/Sold';
import Unsold from '../components/Unsold';
import Resell from '../components/Resell';
import { fetchPlayers } from '../api/players';
import type { Player as BackendPlayer } from '../api/players';

import { fetchTeams } from '../api/teamsApi';
import { assignPlayerToTeam } from '../api/soldPlayer';
// import TeamCard from '../components/TeamCard';
import type { Team, Player, PlayerCategory, PlayerStatus } from '../types';


// Define types for our mock data
export interface MockPlayer {
  id: string;
  name: string;
  lastName: string;
  flatNo: string;
  age: number;
  mobileNumber: string;
  imgUrl: string | null;
  bowlerType: 'left' | 'right' | null;
  batterType: 'left' | 'right' | null;
  category: 'gold' | 'silver' | 'bronze' | null;
  tournamentId: string;

  status?: 'available' | 'sold' | 'unsold';
  wasUnsold?: boolean;
}




const Dashboard: React.FC = () => {
  // const [teams, setTeams] = useState<Team[]>([]);
  const MIN = 10; // Minimum bid amount
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0);
  const [bidAmount, setBidAmount] = useState(10);
  const [selectedTeam, setSelectedTeam] = useState('');
  const [showSoldPopup, setShowSoldPopup] = useState(false);
  const [showTeamPopup, setShowTeamPopup] = useState(false);
  const [showAllPlayersPopup, setShowAllPlayersPopup] = useState(false);
  const [showUnsoldConfirm, setShowUnsoldConfirm] = useState(false);
  const [selectedTeamForPopup, setSelectedTeamForPopup] = useState<Team | null>(null);
  const [teamData, setTeamData] = useState<Team[]>([]);
  const [players, setPlayers] = useState<BackendPlayer[]>([]);
  const [showReavailableNotification, setShowReavailableNotification] = useState(false);

  useEffect(() => {
    const loadTeams = async () => {
      try {
        const data = await fetchTeams();
        setTeamData(data);
      } catch (error) {
        console.error('Failed to fetch teams:', error);
      }
    };

    loadTeams();
  },[]);

  useEffect(()=>{
    const loadPlayers = async ()=>{
      try {
        const data = await fetchPlayers();
        setPlayers(data);
      } catch (error) {
        console.error('Failed to fetch players:', error);
      }
    };
    loadPlayers();

  },[]);

  const handleViewPlayers = (team: Team) => {
    // Optional: Implement navigation or modal for showing players
    console.log('View players for:', team.name);
  };

  // Sort players: available first, then sold, then unsold at the end
  // But if all available players are sold, make unsold players available again
  const availablePlayers = players.filter((player: BackendPlayer) => player.status === 'available');
  //const soldPlayers = players.filter(player => player.status === 'sold');
  const unsoldPlayers = players.filter((player: BackendPlayer) => player.status === 'unsold');
  
  // If no available players left, make unsold players available
  const shouldMakeUnsoldAvailable = availablePlayers.length === 0 && unsoldPlayers.length > 0;
  
  // Show all players for navigation, but sort them properly
  let filteredPlayers = [...players];
  
  const sortedPlayers = filteredPlayers.sort((a: BackendPlayer, b: BackendPlayer) => {
    // First sort by status: available first, then unsold, then sold
    const statusOrder = { 'available': 1, 'unsold': 2, 'sold': 3 };
    const statusA = statusOrder[a.status as keyof typeof statusOrder] || 0;
    const statusB = statusOrder[b.status as keyof typeof statusOrder] || 0;
    
    if (statusA !== statusB) {
      return statusA - statusB;
    }
    
    // Then sort by category priority: gold, silver, bronze
    const categoryOrder = { 'gold': 1, 'silver': 2, 'bronze': 3 };
    return (categoryOrder[(a.category?.toLowerCase?.() ?? a.category) as keyof typeof categoryOrder] || 0) - 
           (categoryOrder[(b.category?.toLowerCase?.() ?? b.category) as keyof typeof categoryOrder] || 0);
  });
  
  // Calculate category counts from sold players
  const soldPlayersData = sortedPlayers.filter((player: BackendPlayer) => player.status === 'sold');
  
  const goldSelected = soldPlayersData.filter((player: BackendPlayer) => player.category === 'gold').length;
  const silverSelected = soldPlayersData.filter((player: BackendPlayer) => player.category === 'silver').length;
  const bronzeSelected = soldPlayersData.filter((player: BackendPlayer) => player.category === 'bronze').length;

  const currentPlayer = sortedPlayers[currentPlayerIndex] || sortedPlayers[0];
  const teamList = teamData?.map((team: Team) => ({ id: team.id, name: team.name }));
  const isCurrentPlayerSold = currentPlayer?.status === 'sold';
  const isCurrentPlayerUnsold = currentPlayer?.status === 'unsold';
  
  // Allow bidding on available players and unsold players when they become available
  const isCurrentPlayerActuallyAvailable = 
    (currentPlayer?.status === 'available') || 
    (shouldMakeUnsoldAvailable && currentPlayer?.status === 'unsold');

  // Function to check if a team can bid on the current player
  function canTeamBidOnPlayer(team: Team, currentBidAmount: number = bidAmount) {
    // If no current player, can't bid
    if (!currentPlayer) return false;
    
    // Check category limits
    let canBidByCategory = false;
    if (currentPlayer && currentPlayer.category && currentPlayer.category.toLowerCase() === 'gold') {
      canBidByCategory = team.goldCount < team.maxGold;
    } else if (currentPlayer && currentPlayer.category && currentPlayer.category.toLowerCase() === 'silver') {
      canBidByCategory = team.silverCount < team.maxSilver;
    } else if (currentPlayer && currentPlayer.category && currentPlayer.category.toLowerCase() === 'bronze') {
      canBidByCategory = team.bronzeCount < team.maxBronze;
    }
    
    if (!canBidByCategory) return false;
    
    // Check budget limits
    const maxBidForTeam = Math.max(0, team.remaining - (MIN * (team.maxPlayers - team.totalPlayers)));
    return currentBidAmount <= maxBidForTeam;
  }

  // Clear selected team if it can't bid on current player
  React.useEffect(() => {
    if (selectedTeam) {
      const selectedTeamData = teamData?.find((team: Team) => team.id === selectedTeam);
      if (selectedTeamData && !canTeamBidOnPlayer(selectedTeamData, bidAmount)) {
        setSelectedTeam('');
      }
    }
  }, [currentPlayerIndex, teamData, selectedTeam, bidAmount]);

  const handleNextPlayer = () => {
    setCurrentPlayerIndex((prev: number) => (prev + 1) % sortedPlayers.length);
  };

  const handlePrevPlayer = () => {
    setCurrentPlayerIndex((prev: number) => (prev - 1 + sortedPlayers.length) % sortedPlayers.length);
  };

  // Update current player index when sorting changes
  React.useEffect(() => {
    // If we're currently viewing a player that's no longer at the same index due to sorting changes
    // Reset to first available player
    if (currentPlayerIndex >= sortedPlayers.length) {
      setCurrentPlayerIndex(0);
    }
  }, [sortedPlayers.length, currentPlayerIndex]);

  // Handle re-available notification auto-dismiss
  React.useEffect(() => {
    if (shouldMakeUnsoldAvailable && !showReavailableNotification) {
      setShowReavailableNotification(true);
      
      // Auto-dismiss after 5 seconds
      const timer = setTimeout(() => {
        setShowReavailableNotification(false);
      }, 5000);
      
      return () => clearTimeout(timer);
    } else if (!shouldMakeUnsoldAvailable) {
      setShowReavailableNotification(false);
    }
  }, [shouldMakeUnsoldAvailable, showReavailableNotification]);


const handleSubmitBid = async () => {
  if (isCurrentPlayerActuallyAvailable && selectedTeam) {
    const selectedTeamData = teamData?.find((team: Team) => team.id === selectedTeam);
    if (!selectedTeamData) return;

    let canBid = false;
    if (currentPlayer && currentPlayer.category?.toLowerCase() === 'gold' && selectedTeamData.goldCount < selectedTeamData.maxGold) {
      canBid = true;
    } else if (currentPlayer?.category?.toLowerCase() === 'silver' && selectedTeamData.silverCount < selectedTeamData.maxSilver) {
      canBid = true;
    } else if (currentPlayer?.category?.toLowerCase() === 'bronze' && selectedTeamData.bronzeCount < selectedTeamData.maxBronze) {
      canBid = true;
    }

    if (!canBid) {
      alert(`Team ${selectedTeamData.name} cannot bid on ${currentPlayer.category} players. They have reached their limit.`);
      return;
    }

    try {
      await assignPlayerToTeam(
        currentPlayer.id,
        currentPlayer.tournamentId,
        selectedTeam,
        bidAmount
      );

      setPlayers((prevPlayers: BackendPlayer[]) => 
        prevPlayers.map((player: BackendPlayer) => 
          player.id === currentPlayer.id 
            ? { ...player, status: 'sold' as const }
            : player
        )
      );

      // 🟢 Fetch latest team data from backend
      const updatedTeams = await fetchTeams();
      setTeamData(updatedTeams);

      setShowSoldPopup(true);
      setBidAmount(10);
      setSelectedTeam('');

    } catch (error) {
      console.error("Failed to assign player:", error);
      alert("Something went wrong while assigning player. Please try again.");
    }
  }
};

  const handleTeamClick = (team: Team) => {
    setSelectedTeamForPopup(team);
    setShowTeamPopup(true);
  };

  const handleUnsold = () => {
    setShowUnsoldConfirm(true);
  };

  const handleUnsoldConfirm = () => {
    // Mark player as unsold
    setPlayers((prevPlayers: BackendPlayer[]) => 
      prevPlayers.map((player: BackendPlayer) => 
        player.id === currentPlayer.id 
          ? { ...player, status: 'unsold' as const, wasUnsold: true }
          : player
      )
    );
    
    // Reset bid amount
    setBidAmount(10);
    
    // Reset team selection
    setSelectedTeam('');
    
    // Close confirmation popup
    setShowUnsoldConfirm(false);
    
    // Move to next player
    handleNextPlayer();
  };

  const handleUnsoldCancel = () => {
    setShowUnsoldConfirm(false);
  };

  return (
    <div className="dashboard-main">
      {/* Auction Progress Section */}
      <AuctionProgress
        currentPlayer={currentPlayerIndex + 1}
        totalPlayers={sortedPlayers.length}
        goldSelected={goldSelected}
        maxGold={2}
        silverSelected={silverSelected}
        maxSilver={4}
        bronzeSelected={bronzeSelected}
        maxBronze={6}
        onViewAllPlayers={() => setShowAllPlayersPopup(true)}
      />
      
      {/* Show notification when unsold players become available */}
      {showReavailableNotification && (
        <div className="reavailable-notification">
          <div className="notification-content">
            <span className="notification-icon">🔄</span>
            <span className="notification-text">
              All available players have been sold! You can now bid on unsold players.
            </span>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="dashboard-content">
        {/* Left Panel - Combined Player and Bidding Card */}
        <div className="player-panel">
          {/* Combined Card with Player Card on top and Bidding below */}
          <div className={`combined-card ${currentPlayer?.category?.toLowerCase() || ''} ${isCurrentPlayerUnsold && !shouldMakeUnsoldAvailable ? 'unsold' : ''} ${isCurrentPlayerUnsold && shouldMakeUnsoldAvailable ? 'resell' : ''}`}>
            {/* Player Card Section (Top) */}
            <div className="player-card-section">
              {isCurrentPlayerSold && (
                <div className="sold-out-badge">Sold Out</div>
              )}
              <div className="player-photo-section">
                <img src={currentPlayer?.imgUrl || '/default-player.png'} alt={currentPlayer?.name} className="player-photo-large" />
              </div>
              <h4 className="player-name">
                {currentPlayer ? `${currentPlayer.name} ${currentPlayer.lastName}` : ''}
              </h4>
              <div className="player-stats">
                <div className="info-row">
                  <div className="info-item">
                    <span className="info-label">Age</span>
                    <span className="info-value">{currentPlayer?.age || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Bowling Style</span>
                    <span className="info-value">{currentPlayer?.bowlerType || 'N/A'}</span>
                  </div>
                </div>
                <div className="info-row">
                  <div className="info-item">
                    <span className="info-label">Flat No.</span>
                    <span className="info-value">{currentPlayer?.flatNo || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Batting Style</span>
                    <span className="info-value">{currentPlayer?.batterType || 'N/A'}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Bidding Section (Bottom) */}
            <div className="bidding-section">
          
              
              {isCurrentPlayerSold && (
                <Sold isAnimationNeeded={false} />
              )}
              {isCurrentPlayerUnsold && !shouldMakeUnsoldAvailable && (
                <Unsold isAnimationNeeded={false} />
              )}
              {isCurrentPlayerUnsold && shouldMakeUnsoldAvailable && (
                <Resell isAnimationNeeded={false} />
              )}
              
              <div className="current-bid-section">
                <p className="bid-label">Current Highest Bid</p>
                <div className="bid-amount">${bidAmount.toLocaleString()}</div>
              </div>

              {/* Bid Input Section */}
              <div className="bid-input-section">
                <BidInput
                  bidAmount={bidAmount}
                  setBidAmount={setBidAmount}
                  teamList={teamList}
                  selectedTeam={selectedTeam}
                  setSelectedTeam={setSelectedTeam}
                  onSubmit={handleSubmitBid}
                  onUnsold={handleUnsold}
                  disabled={!isCurrentPlayerActuallyAvailable}
                />
              </div>

              {/* Player Navigation */}
              <div className="player-navigation">
                <button onClick={handlePrevPlayer} className="nav-btn arrow-btn">
                  <span className="arrow-icon">&lt;</span>
                </button>
                <button onClick={handleNextPlayer} className="nav-btn arrow-btn">
                  <span className="arrow-icon">&gt;</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel - Team Cards */}
        <div className="teams-panel">
          <div className="teams-grid">
            {teamData?.map((team: Team) => {
              const canBid = canTeamBidOnPlayer(team, bidAmount);
              const isFull = team.totalPlayers >= team.maxPlayers;

              // Determine which limit is hit
              let limitHitLabel = '';
              if (team.totalPlayers >= team.maxPlayers) {
                limitHitLabel = 'Max Players Hit';
              } else if (currentPlayer?.category?.toLowerCase() === 'gold' && team.goldCount >= team.maxGold) {
                limitHitLabel = 'Max Gold Hit';
              } else if (currentPlayer?.category?.toLowerCase() === 'silver' && team.silverCount >= team.maxSilver) {
                limitHitLabel = 'Max Silver Hit';
              } else if (currentPlayer?.category?.toLowerCase() === 'bronze' && team.bronzeCount >= team.maxBronze) {
                limitHitLabel = 'Max Bronze Hit';
              }

              return (
                <div 
                  key={team.id} 
                  className={`team-card-enhanced ${!canBid || isFull ? 'disabled-team' : ''}`}
                >
                  <div className="team-header">
                    <img src={team.img_url} alt={team.owner} className="owner-photo" />
                    <div className="team-info">
                      <h4>{team.name}</h4>
                      <span className="owner-name">{team.owner}</span>
                    </div>
                    <button 
                      className="view-players-btn" 
                      onClick={(e) => {
                        e.stopPropagation();
                        handleTeamClick(team);
                      }}
                      title="View team players"
                    >
                      <EyeIcon className="view-players-icon" />
                      <span className="sr-only">View players</span>
                    </button>
                  </div>
                  <div className="team-details">
                    <div className="budget-info">Budget: ${team.remaining.toLocaleString()}/${team.budget.toLocaleString()}</div>
                    <div className="players-info">Players: {team.totalPlayers}/{team.maxPlayers}</div>
                    <div className="max-bid-info">Max Bid: ${Math.max(0, team.remaining - (MIN * (team.maxPlayers - team.totalPlayers))).toLocaleString()}</div>
                    <div className="category-info">
                      <span className={`gold ${team.goldCount >= team.maxGold ? 'limit-reached' : ''}`}>
                        Gold: {team.goldCount}/{team.maxGold}
                      </span>
                      <span className={`silver ${team.silverCount >= team.maxSilver ? 'limit-reached' : ''}`}>
                        Silver: {team.silverCount}/{team.maxSilver}
                      </span>
                      <span className={`bronze ${team.bronzeCount >= team.maxBronze ? 'limit-reached' : ''}`}>
                        Bronze: {team.bronzeCount}/{team.maxBronze}
                      </span>
                    </div>
                 
                                         {!canBid && (
                       <div className="disabled-message">
                         {(() => {
                           // Check category limits first
                           let canBidByCategory = false;
                           if (currentPlayer && currentPlayer.category && currentPlayer.category.toLowerCase() === 'gold') {
                             canBidByCategory = team.goldCount < team.maxGold;
                           } else if (currentPlayer && currentPlayer.category && currentPlayer.category.toLowerCase() === 'silver') {
                             canBidByCategory = team.silverCount < team.maxSilver;
                           } else if (currentPlayer && currentPlayer.category && currentPlayer.category.toLowerCase() === 'bronze') {
                             canBidByCategory = team.bronzeCount < team.maxBronze;
                           }
                           
                           if (!canBidByCategory) {
                             return `Cannot bid on ${currentPlayer?.category} players`;
                           } else {
                             const maxBidForTeam = Math.max(0, team.remaining - (MIN * (team.maxPlayers - team.totalPlayers)));
                             return `Bid exceeds max ($${maxBidForTeam.toLocaleString()})`;
                           }
                         })()}
                       </div>
                     )}
                  </div>
                  {/* Add this just inside the team-card-enhanced div */}
                  {limitHitLabel && (
        <div className="limit-hit-tab">
          {limitHitLabel}
        </div>
      )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {showSoldPopup && (
        <SoldPopup
          player={currentPlayer as any}
          team={teamData?.find(t => t.id === selectedTeam) as any || teamData?.[0] as any}
          onClose={() => setShowSoldPopup(false)}
        />
      )}

      {showTeamPopup && selectedTeamForPopup && (
        <TeamPlayerListPopup
          team={selectedTeamForPopup as any}
          onClose={() => setShowTeamPopup(false)}
        />
      )}

      {showAllPlayersPopup && (
        <AllPlayersPopup
          teams={teamData as any}
          onClose={() => setShowAllPlayersPopup(false)}
        />
      )}

      {showUnsoldConfirm && (
        <div className="confirmation-overlay">
          <div className="confirmation-popup">
            <h3>Mark Player as Unsold</h3>
            <p>Are you sure you want to mark this player as unsold?</p>
            <div className="confirmation-buttons">
              <button onClick={handleUnsoldConfirm} className="confirm-btn">
                Yes, Mark as Unsold
              </button>
              <button onClick={handleUnsoldCancel} className="cancel-btn">
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;