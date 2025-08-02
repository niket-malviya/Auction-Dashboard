import React, { useState } from 'react';
import TeamCard from '../components/TeamCard';
import TeamPlayerListPopup from '../components/TeamPlayerListPopup';

const Teams: React.FC = () => {
  const [showTeamPopup, setShowTeamPopup] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState<any>(null);

  // Mock data for 8 teams
  const teams = [
    {
      id: '1',
      name: 'Mumbai Indians',
      owner: 'Mukesh Ambani',
      ownerPhoto: 'https://via.placeholder.com/48x48/FF6B6B/FFFFFF?text=MA',
      players: [],
      goldCount: 0,
      silverCount: 0,
      bronzeCount: 0,
      maxGold: 3,
      maxSilver: 3,
      maxBronze: 2,
      totalPlayers: 0,
      maxPlayers: 8,
      budget: 1000000,
      remaining: 1000000
    },
    {
      id: '2',
      name: 'Chennai Super Kings',
      owner: 'N Srinivasan',
      ownerPhoto: 'https://via.placeholder.com/48x48/4ECDC4/FFFFFF?text=NS',
      players: [],
      goldCount: 0,
      silverCount: 0,
      bronzeCount: 0,
      maxGold: 3,
      maxSilver: 3,
      maxBronze: 2,
      totalPlayers: 0,
      maxPlayers: 8,
      budget: 1000000,
      remaining: 1000000
    },
    {
      id: '3',
      name: 'Royal Challengers Bangalore',
      owner: 'Vijay Mallya',
      ownerPhoto: 'https://via.placeholder.com/48x48/FFE66D/000000?text=VM',
      players: [],
      goldCount: 0,
      silverCount: 0,
      bronzeCount: 0,
      maxGold: 3,
      maxSilver: 3,
      maxBronze: 2,
      totalPlayers: 0,
      maxPlayers: 8,
      budget: 1000000,
      remaining: 1000000
    },
    {
      id: '4',
      name: 'Kolkata Knight Riders',
      owner: 'Shah Rukh Khan',
      ownerPhoto: 'https://via.placeholder.com/48x48/95E1D3/000000?text=SRK',
      players: [],
      goldCount: 0,
      silverCount: 0,
      bronzeCount: 0,
      maxGold: 3,
      maxSilver: 3,
      maxBronze: 2,
      totalPlayers: 0,
      maxPlayers: 8,
      budget: 1000000,
      remaining: 1000000
    },
    {
      id: '5',
      name: 'Delhi Capitals',
      owner: 'Parth Jindal',
      ownerPhoto: 'https://via.placeholder.com/48x48/F38181/FFFFFF?text=PJ',
      players: [],
      goldCount: 0,
      silverCount: 0,
      bronzeCount: 0,
      maxGold: 3,
      maxSilver: 3,
      maxBronze: 2,
      totalPlayers: 0,
      maxPlayers: 8,
      budget: 1000000,
      remaining: 1000000
    },
    {
      id: '6',
      name: 'Punjab Kings',
      owner: 'Preity Zinta',
      ownerPhoto: 'https://via.placeholder.com/48x48/A8E6CF/000000?text=PZ',
      players: [],
      goldCount: 0,
      silverCount: 0,
      bronzeCount: 0,
      maxGold: 3,
      maxSilver: 3,
      maxBronze: 2,
      totalPlayers: 0,
      maxPlayers: 8,
      budget: 1000000,
      remaining: 1000000
    },
    {
      id: '7',
      name: 'Rajasthan Royals',
      owner: 'Manoj Badale',
      ownerPhoto: 'https://via.placeholder.com/48x48/FFB6C1/000000?text=MB',
      players: [],
      goldCount: 0,
      silverCount: 0,
      bronzeCount: 0,
      maxGold: 3,
      maxSilver: 3,
      maxBronze: 2,
      totalPlayers: 0,
      maxPlayers: 8,
      budget: 1000000,
      remaining: 1000000
    },
    {
      id: '8',
      name: 'Sunrisers Hyderabad',
      owner: 'Kalanithi Maran',
      ownerPhoto: 'https://via.placeholder.com/48x48/FFA07A/000000?text=KM',
      players: [],
      goldCount: 0,
      silverCount: 0,
      bronzeCount: 0,
      maxGold: 3,
      maxSilver: 3,
      maxBronze: 2,
      totalPlayers: 0,
      maxPlayers: 8,
      budget: 1000000,
      remaining: 1000000
    }
  ];

  const handleTeamClick = (team: any) => {
    setSelectedTeam(team);
    setShowTeamPopup(true);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Teams</h2>
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', 
        gap: '2rem',
        marginTop: '2rem'
      }}>
        {teams.map(team => (
          <div key={team.id} onClick={() => handleTeamClick(team)} style={{ cursor: 'pointer' }}>
            <TeamCard team={team} />
          </div>
        ))}
      </div>

      {showTeamPopup && selectedTeam && (
        <TeamPlayerListPopup
          team={selectedTeam}
          onClose={() => setShowTeamPopup(false)}
        />
      )}
    </div>
  );
};

export default Teams;