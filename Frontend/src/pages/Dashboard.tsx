import React, { useState } from 'react';
import { useAuction } from '../context/AuctionContext';
import PlayerCard from '../components/PlayerCard';
import TeamCard from '../components/TeamCard';
import BidInput from '../components/BidInput';
import SoldPopup from '../components/SoldPopup';
import TeamPlayerListPopup from '../components/TeamPlayerListPopup';
import AuctionProgress from '../components/AuctionProgress';
import './Dashboard.css';
import Sold from '../components/Sold';

// Define types for our mock data
interface MockPlayer {
  id: string;
  name: string;
  age: number;
  photo: string;
  type: string;
  category: string;
  height: string;
  weight: string;
  stats: {
    ppg: number;
    rpg: number;
    apg: number;
    ftPercent: number;
  };
}

interface MockTeam {
  id: string;
  name: string;
  owner: string;
  ownerPhoto: string;
  players: MockPlayer[];
  goldCount: number;
  silverCount: number;
  bronzeCount: number;
  maxGold: number;
  maxSilver: number;
  maxBronze: number;
  totalPlayers: number;
  maxPlayers: number;
  budget: number;
  remaining: number;
}

// Mock data for demonstration - Basketball theme
const mockPlayers: MockPlayer[] = [
  {
    id: '1',
    name: 'Marcus Johnson',
    age: 24,
    photo: 'https://randomuser.me/api/portraits/men/1.jpg',
    type: 'Point Guard',
    category: 'Gold',
    height: "6'2\"",
    weight: "185 lbs",
    stats: {
      ppg: 18.5,
      rpg: 4.1,
      apg: 7.2,
      ftPercent: 89
    }
  },
  {
    id: '2',
    name: 'David Williams',
    age: 26,
    photo: 'https://randomuser.me/api/portraits/men/2.jpg',
    type: 'Shooting Guard',
    category: 'Gold',
    height: "6'4\"",
    weight: "200 lbs",
    stats: {
      ppg: 22.1,
      rpg: 3.8,
      apg: 4.5,
      ftPercent: 87
    }
  },
  {
    id: '3',
    name: 'Sarah Chen',
    age: 23,
    photo: 'https://randomuser.me/api/portraits/men/3.jpg',
    type: 'Small Forward',
    category: 'Silver',
    height: "6'0\"",
    weight: "170 lbs",
    stats: {
      ppg: 15.2,
      rpg: 5.8,
      apg: 3.1,
      ftPercent: 82
    }
  },
  {
    id: '4',
    name: 'Mike Rodriguez',
    age: 25,
    photo: 'https://randomuser.me/api/portraits/men/4.jpg',
    type: 'Power Forward',
    category: 'Silver',
    height: "6'8\"",
    weight: "220 lbs",
    stats: {
      ppg: 12.8,
      rpg: 8.4,
      apg: 2.2,
      ftPercent: 75
    }
  },
  {
    id: '5',
    name: 'Emma Thompson',
    age: 22,
    photo: 'https://randomuser.me/api/portraits/men/5.jpg',
    type: 'Center',
    category: 'Bronze',
    height: "6'5\"",
    weight: "190 lbs",
    stats: {
      ppg: 8.9,
      rpg: 6.2,
      apg: 1.8,
      ftPercent: 68
    }
  }
];

const mockTeams: MockTeam[] = [
  {
    id: '1',
    name: 'Thunder Bolts',
    owner: 'John Smith',
    ownerPhoto: 'https://randomuser.me/api/portraits/men/6.jpg',
    players: [],
    goldCount: 0,
    silverCount: 0,
    bronzeCount: 0,
    maxGold: 1,
    maxSilver: 2,
    maxBronze: 5,
    totalPlayers: 0,
    maxPlayers: 8,
    budget: 800,
    remaining: 800,
  },
  {
    id: '2',
    name: 'Phoenix Flames',
    owner: 'Mike Johnson',
    ownerPhoto: 'https://randomuser.me/api/portraits/men/7.jpg',
    players: [],
    goldCount: 0,
    silverCount: 0,
    bronzeCount: 0,
    maxGold: 1,
    maxSilver: 2,
    maxBronze: 5,
    totalPlayers: 0,
    maxPlayers: 8,
    budget: 800,
    remaining: 800,
  
  },
  {
    id: '3',
    name: 'Storm Eagles',
    owner: 'Chris Davis',
    ownerPhoto: 'https://randomuser.me/api/portraits/men/8.jpg',
    players: [],
    goldCount: 0,
    silverCount: 0,
    bronzeCount: 0,
    maxGold: 1,
    maxSilver: 2,
    maxBronze: 5,
    totalPlayers: 0,
    maxPlayers: 8,
    budget: 800,
    remaining: 800,
  
  },
  {
    id: '4',
    name: 'Lightning Bolts',
    owner: 'Alex Wilson',
    ownerPhoto: 'https://randomuser.me/api/portraits/men/9.jpg',
    players: [],
    goldCount: 0,
    silverCount: 0,
    bronzeCount: 0,
    maxGold: 1,
    maxSilver: 2,
    maxBronze: 5,
    totalPlayers: 0,
    maxPlayers: 8,
    budget: 800,
    remaining: 800,
  
  },
  {
    id: '5',
    name: 'Fire Dragons',
    owner: 'Ryan Brown',
    ownerPhoto: 'https://randomuser.me/api/portraits/men/10.jpg',
    players: [],
    goldCount: 0,
    silverCount: 0,
    bronzeCount: 0,
    maxGold: 1,
    maxSilver: 2,
    maxBronze: 5,
    totalPlayers: 0,
    maxPlayers: 8,
    budget: 800,
    remaining: 800,
  
  },
  {
    id: '6',
    name: 'Ice Wolves',
    owner: 'Tom Miller',
    ownerPhoto: 'https://randomuser.me/api/portraits/men/11.jpg',
    players: [],
    goldCount: 0,
    silverCount: 0,
    bronzeCount: 0,
    maxGold: 1,
    maxSilver: 2,
    maxBronze: 5,
    totalPlayers: 0,
    maxPlayers: 8,
    budget: 800,
    remaining: 800,
  
  }
];

const Dashboard: React.FC = () => {
  const MIN = 10; // Minimum bid amount
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0);
  const [bidAmount, setBidAmount] = useState(10);
  const [selectedTeam, setSelectedTeam] = useState('');
  const [showSoldPopup, setShowSoldPopup] = useState(false);
  const [showTeamPopup, setShowTeamPopup] = useState(false);
  const [showUnsoldConfirm, setShowUnsoldConfirm] = useState(false);
  const [selectedTeamForPopup, setSelectedTeamForPopup] = useState<MockTeam | null>(null);
  const [soldPlayers, setSoldPlayers] = useState<Set<string>>(new Set());
  const [teamData, setTeamData] = useState<MockTeam[]>(mockTeams);
  
  // Calculate category counts from sold players
  const soldPlayersList = Array.from(soldPlayers);
  const soldPlayersData = mockPlayers.filter(player => soldPlayersList.includes(player.id));
  
  const goldSelected = soldPlayersData.filter(player => player.category === 'Gold').length;
  const silverSelected = soldPlayersData.filter(player => player.category === 'Silver').length;
  const bronzeSelected = soldPlayersData.filter(player => player.category === 'Bronze').length;

  const currentPlayer = mockPlayers[currentPlayerIndex] || mockPlayers[0];
  const teamList = teamData
    .filter(team => canTeamBidOnPlayer(team, bidAmount))
    .map(team => ({ id: team.id, name: team.name }));
  const isCurrentPlayerSold = soldPlayers.has(currentPlayer.id);

  // Function to check if a team can bid on the current player
  function canTeamBidOnPlayer(team: MockTeam, currentBidAmount: number = bidAmount) {
    // Check category limits
    let canBidByCategory = false;
    if (currentPlayer.category === 'Gold') {
      canBidByCategory = team.goldCount < team.maxGold;
    } else if (currentPlayer.category === 'Silver') {
      canBidByCategory = team.silverCount < team.maxSilver;
    } else if (currentPlayer.category === 'Bronze') {
      canBidByCategory = team.bronzeCount < team.maxBronze;
    }
    
    if (!canBidByCategory) return false;
    
    // Check budget limits
    const maxBidForTeam = Math.max(0, team.remaining - (MIN * (team.maxPlayers - team.totalPlayers)));
    return currentBidAmount <= maxBidForTeam;
  };

  // Clear selected team if it can't bid on current player
  React.useEffect(() => {
    if (selectedTeam) {
      const selectedTeamData = teamData.find(team => team.id === selectedTeam);
      if (selectedTeamData && !canTeamBidOnPlayer(selectedTeamData, bidAmount)) {
        setSelectedTeam('');
      }
    }
  }, [currentPlayerIndex, teamData, selectedTeam, bidAmount]);

  const handleNextPlayer = () => {
    setCurrentPlayerIndex((prev) => (prev + 1) % mockPlayers.length);
  };

  const handlePrevPlayer = () => {
    setCurrentPlayerIndex((prev) => (prev - 1 + mockPlayers.length) % mockPlayers.length);
  };

  const handleSubmitBid = () => {
    if (!isCurrentPlayerSold && selectedTeam) {
      // Check if the selected team can still bid on this player category
      const selectedTeamData = teamData.find(team => team.id === selectedTeam);
      if (!selectedTeamData) return;

      let canBid = false;
      if (currentPlayer.category === 'Gold' && selectedTeamData.goldCount < selectedTeamData.maxGold) {
        canBid = true;
      } else if (currentPlayer.category === 'Silver' && selectedTeamData.silverCount < selectedTeamData.maxSilver) {
        canBid = true;
      } else if (currentPlayer.category === 'Bronze' && selectedTeamData.bronzeCount < selectedTeamData.maxBronze) {
        canBid = true;
      }

      if (!canBid) {
        alert(`Team ${selectedTeamData.name} cannot bid on ${currentPlayer.category} players. They have reached their limit.`);
        return;
      }

      // Mark player as sold
      setSoldPlayers(prev => new Set([...prev, currentPlayer.id]));
      
      // Update team data
      setTeamData(prevTeams => {
        return prevTeams.map(team => {
          if (team.id === selectedTeam) {
            // Add player to team
            const updatedPlayers = [...team.players, currentPlayer];
            
            // Update category counts
            let newGoldCount = team.goldCount;
            let newSilverCount = team.silverCount;
            let newBronzeCount = team.bronzeCount;
            
            if (currentPlayer.category === 'Gold') {
              newGoldCount += 1;
            } else if (currentPlayer.category === 'Silver') {
              newSilverCount += 1;
            } else if (currentPlayer.category === 'Bronze') {
              newBronzeCount += 1;
            }
            
            // Update budget
            const newRemaining = team.remaining - bidAmount;
            
            return {
              ...team,
              players: updatedPlayers,
              goldCount: newGoldCount,
              silverCount: newSilverCount,
              bronzeCount: newBronzeCount,
              totalPlayers: team.totalPlayers + 1,
              remaining: newRemaining,
              
            };
          }
          return team;
        });
      });
      
             setShowSoldPopup(true);
       
       // Reset bid amount to default value after successful bid
       setBidAmount(10);
     }
   };

  const handleTeamClick = (team: MockTeam) => {
    setSelectedTeamForPopup(team);
    setShowTeamPopup(true);
  };

  const handleUnsold = () => {
    setShowUnsoldConfirm(true);
  };

  const handleUnsoldConfirm = () => {
    // Mark player as sold (but not to any team)
    setSoldPlayers(prev => new Set([...prev, currentPlayer.id]));
    
    // Reset bid amount
    setBidAmount(10);
    
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
         totalPlayers={mockPlayers.length}
         goldSelected={goldSelected}
         maxGold={2}
         silverSelected={silverSelected}
         maxSilver={4}
         bronzeSelected={bronzeSelected}
         maxBronze={6}
       />

      {/* Main Content */}
      <div className="dashboard-content">
        {/* Left Panel - Player Card */}
        <div className="player-panel">
          <div className={`player-card-enhanced ${isCurrentPlayerSold ? 'sold' : ''}`}>
            <h3>Player Card</h3>
            <div className="player-photo-section">
              <img src={currentPlayer.photo} alt={currentPlayer.name} className="player-photo-large" />
              <span className="player-number">#23</span>
              {/* {isCurrentPlayerSold && (
                <div className="sold-overlay">
                  <div className="sold-badge">SOLD</div>
                </div>
              )} */}
            </div>
            {isCurrentPlayerSold && (
                <Sold isAnimationNeeded={false} />
              )}
            <h4 className="player-name">{currentPlayer.name}</h4>
            <p className="player-position">{currentPlayer.type}</p>
            <p className="player-category">{currentPlayer.category}</p>
            <p className="player-physical">{currentPlayer.height} • {currentPlayer.weight} • Age {currentPlayer.age}</p>
            
            <div className="player-stats">
              <div className="stat-column">
                <div className="stat-item">
                  <span className="stat-value">{currentPlayer.stats.ppg}</span>
                  <span className="stat-label">PPG</span>
                </div>
                <div className="stat-item">
                  <span className="stat-value">{currentPlayer.stats.rpg}</span>
                  <span className="stat-label">RPG</span>
                </div>
              </div>
              <div className="stat-column">
                <div className="stat-item">
                  <span className="stat-value">{currentPlayer.stats.apg}</span>
                  <span className="stat-label">APG</span>
                </div>
                <div className="stat-item">
                  <span className="stat-value">{currentPlayer.stats.ftPercent}%</span>
                  <span className="stat-label">FT%</span>
                </div>
              </div>
            </div>
            
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
                 disabled={isCurrentPlayerSold}
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

                 {/* Right Panel - Team Cards */}
         <div className="teams-panel">
           <div className="teams-grid">
                           {teamData.map(team => {
                const canBid = canTeamBidOnPlayer(team, bidAmount);
                return (
                 <div 
                   key={team.id} 
                   className={`team-card-enhanced ${!canBid ? 'disabled-team' : ''}`} 
                   onClick={() => handleTeamClick(team)}
                 >
                   <div className="team-header">
                     <img src={team.ownerPhoto} alt={team.owner} className="owner-photo" />
                     <div className="team-info">
                       <h4>{team.name}</h4>
                       <span className="owner-name">{team.owner.split(' ')[0]}</span>
                     </div>
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
                            if (currentPlayer.category === 'Gold') {
                              canBidByCategory = team.goldCount < team.maxGold;
                            } else if (currentPlayer.category === 'Silver') {
                              canBidByCategory = team.silverCount < team.maxSilver;
                            } else if (currentPlayer.category === 'Bronze') {
                              canBidByCategory = team.bronzeCount < team.maxBronze;
                            }
                            
                            if (!canBidByCategory) {
                              return `Cannot bid on ${currentPlayer.category} players`;
                            } else {
                              const maxBidForTeam = Math.max(0, team.remaining - (MIN * (team.maxPlayers - team.totalPlayers)));
                              return `Bid exceeds max ($${maxBidForTeam.toLocaleString()})`;
                            }
                          })()}
                        </div>
                      )}
                   </div>
                 </div>
               );
             })}
           </div>
         </div>
      </div>

      {showSoldPopup && (
        <SoldPopup
          player={currentPlayer as any}
          team={teamData.find(t => t.id === selectedTeam) as any || teamData[0] as any}
          onClose={() => setShowSoldPopup(false)}
        />
      )}

             {showTeamPopup && selectedTeamForPopup && (
         <TeamPlayerListPopup
           team={selectedTeamForPopup as any}
           onClose={() => setShowTeamPopup(false)}
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