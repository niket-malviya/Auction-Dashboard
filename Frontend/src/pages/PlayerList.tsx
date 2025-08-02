import React from 'react';
import PlayerCard from '../components/PlayerCard';

const PlayerList: React.FC = () => {
  // Mock data for demonstration
  const players = [
    {
      id: '1',
      name: 'Virat Kohli',
      age: 35,
      photo: 'https://via.placeholder.com/80x80/FFD700/000000?text=VK',
      type: 'Batter' as const,
      category: 'Gold' as const
    },
    {
      id: '2',
      name: 'Jasprit Bumrah',
      age: 30,
      photo: 'https://via.placeholder.com/80x80/7EC4CF/000000?text=JB',
      type: 'Bowler' as const,
      category: 'Gold' as const
    },
    {
      id: '3',
      name: 'Rohit Sharma',
      age: 36,
      photo: 'https://via.placeholder.com/80x80/FFD700/000000?text=RS',
      type: 'Batter' as const,
      category: 'Gold' as const
    },
    {
      id: '4',
      name: 'Ravindra Jadeja',
      age: 34,
      photo: 'https://via.placeholder.com/80x80/B6E388/000000?text=RJ',
      type: 'Allrounder' as const,
      category: 'Silver' as const
    },
    {
      id: '5',
      name: 'KL Rahul',
      age: 31,
      photo: 'https://via.placeholder.com/80x80/FFD700/000000?text=KL',
      type: 'Batter' as const,
      category: 'Silver' as const
    },
    {
      id: '6',
      name: 'Mohammed Shami',
      age: 33,
      photo: 'https://via.placeholder.com/80x80/7EC4CF/000000?text=MS',
      type: 'Bowler' as const,
      category: 'Silver' as const
    }
  ];

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Player List</h2>
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
        gap: '2rem',
        marginTop: '2rem'
      }}>
        {players.map(player => (
          <PlayerCard key={player.id} player={player} />
        ))}
      </div>
    </div>
  );
};

export default PlayerList;