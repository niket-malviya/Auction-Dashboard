

import React, { useEffect, useState } from 'react';
import PlayerCard from '../components/PlayerCard';
import { fetchPlayers } from '../api/players';

const PlayerList: React.FC = () => {
  const [players, setPlayers] = useState<any[]>([]);
  const [viewMode, setViewMode] = useState<'card' | 'table'>('card');

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
      {/* Header with Toggle Button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Player List</h2>
        <button
          onClick={() => setViewMode(viewMode === 'card' ? 'table' : 'card')}
          style={{
            padding: '0.5rem 1rem',
            cursor: 'pointer',
            background: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
          }}
        >
          Switch to {viewMode === 'card' ? 'Table View' : 'Card View'}
        </button>
      </div>

      {/* Card View */}
      {viewMode === 'card' ? (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '2rem',
            marginTop: '2rem',
          }}
        >
          {players.map((player) => (
            <PlayerCard key={player.id} player={player} />
          ))}
        </div>
      ) : (
        // Table View
        <table
          style={{
            width: '100%',
            borderCollapse: 'collapse',
            marginTop: '2rem',
          }}
        >
          <thead>
  <tr style={{ background: '#f4f4f4', textAlign: 'left' }}>
    <th style={{ padding: '0.75rem', borderBottom: '1px solid #ddd', textAlign: 'center' }}>Photo</th>
    <th style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>Full Name</th>
    <th style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>Flat No</th>
    <th style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>Batting Style</th>
    <th style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>Bowling Style</th>
    <th style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>Category</th>
  </tr>
</thead>
<tbody>
  {players.map((player) => (
    <tr key={player.id}>
      {/* First column: Image */}
      <td style={{ padding: '0.75rem', borderBottom: '1px solid #ddd', textAlign: 'center' }}>
        <img
          src={player.imgUrl}
          alt={player.name}
          style={{
            width: '50px',
            height: '50px',
            borderRadius: '50%',
            objectFit: 'cover',
          }}
        />
      </td>

      {/* Second column: Full Name */}
      <td style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>
        {player.name} {player.lastName}
      </td>

      {/* Remaining columns */}
      <td style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{player.flatNo}</td>
      <td style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{player.batterType}</td>
      <td style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{player.bowlerType}</td>
      <td style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{player.category}</td>
    </tr>
  ))}
</tbody>

        </table>
      )}
    </div>
  );
};

export default PlayerList;
