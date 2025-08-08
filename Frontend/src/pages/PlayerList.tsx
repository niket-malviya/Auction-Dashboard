import React,{useEffect, useState} from 'react';
import PlayerCard from '../components/PlayerCard';
import { fetchPlayers } from '../api/players';

const PlayerList: React.FC = () => {
  const [players, setPlayers] = useState<any[]>([]);
  useEffect(() => {
    const loadPlayers = async () => {
      try {
        const response = await fetchPlayers();
        setPlayers(response);
      } catch (error) {
        console.error('Error fetching players:', error);
      }
    };
    loadPlayers();
  }, []);

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