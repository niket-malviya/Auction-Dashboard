import React, { useState,useEffect } from 'react';
import TeamCard from '../components/TeamCard';
import TeamPlayerListPopup from '../components/TeamPlayerListPopup';
import { fetchTeams } from '../api/teamsApi';
const Teams: React.FC = () => {
  const [teams, setTeams] = useState<any[]>([]);
  const [showTeamPopup, setShowTeamPopup] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState<any>(null);


  useEffect(() => {
    const loadTeams = async () => {
      try {
        const response = await fetchTeams();
        setTeams(response); // Make sure your API returns an array of teams
      } catch (error) {
        console.error('Error fetching teams:', error);
      }
    };

    loadTeams();
  }, []);

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
          <TeamCard 
            key={team.id} 
            team={team} 
            onViewPlayers={handleTeamClick}
          />
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