


import React, { useEffect, useState } from 'react';
import { fetchTeamPlayersAndOwner } from '../api/teamPlayer';
import './TeamPlayerListPopup.css';

interface Player {
  id: number;
  name: string;
  imgUrl?: string;
  category?: string;
  type?: string;
  bidAmount?: number;
}

interface TeamPlayerListPopupProps {
  teamId: string;
  teamName: string;
  onClose: () => void;
}

const TeamPlayerListPopup: React.FC<TeamPlayerListPopupProps> = ({ teamId, teamName, onClose }) => {
  const [players, setPlayers] = useState<Player[]>([]);
  const [ownerName, setOwnerName] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getPlayers = async () => {
      setLoading(true);
      try {
        const data = await fetchTeamPlayersAndOwner(teamId);

        // Ensure players is always an array and IDs are numbers
        const formattedPlayers: Player[] = Array.isArray(data.players)
          ? data.players.map((p: any) => ({
              id: Number(p.id),
              name: p.name || '',
              imgUrl: p.imgUrl || p.img_url || '',
              category: p.category || '',
              type: p.type || '',
              bidAmount: p.bidAmount || 0
            }))
          : [];

        setPlayers(formattedPlayers);
        setOwnerName(data.ownerName || '');
      } catch (error) {
        console.error('Error fetching team players:', error);
        setPlayers([]);
        setOwnerName('');
      } finally {
        setLoading(false);
      }
    };

    getPlayers();
  }, [teamId]);

  return (
    <div
      className="team-player-popup-overlay"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="team-player-popup">
        <button className="close-btn" onClick={onClose}>
          &times;
        </button>
        <h2>{teamName} Players</h2>
        {ownerName && <p><strong>Owner:</strong> {ownerName}</p>}

        {loading ? (
          <div>Loading...</div>
        ) : (
          <ul className="player-list">
            {players.length === 0 && <li>No players yet.</li>}
            {players.map((player) => (
              <li key={player.id} className="player-list-item">
                {player.imgUrl && (
                  <img
                    src={player.imgUrl}
                    alt={player.name}
                    className="player-photo"
                  />
                )}
                <span>{player.name}</span>
                <span className="player-type">{player.type}</span>
                <span
                  className={`category-badge ${player.category?.toLowerCase()}`}
                >
                  {player.category}
                </span>
                <span className="bid-amount">Bid: ₹{player.bidAmount}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default TeamPlayerListPopup;
