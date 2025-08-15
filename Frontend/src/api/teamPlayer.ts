import axios from "axios";

interface PlayerInfo {
  id: string;
  name: string;
  category: string;
  bidAmount: number;
}

interface TeamData {
  teamId: string;
  ownerName: string;
  players: PlayerInfo[];
}

export const fetchTeamPlayersAndOwner = async (teamId: string): Promise<TeamData> => {
  try {
    // 1️⃣ Get team_player entries
    const { data: teamPlayers } = await axios.get(`/team_players/team/${teamId}`);

    // 2️⃣ Get team details (for owner name)
    const { data: teamDetails } = await axios.get(`/teams/${teamId}`);

    const ownerName = teamDetails?.owner_name || "Unknown Owner";

    // 3️⃣ Fetch player details for each player_id
    const players = await Promise.all(
      teamPlayers.map(async (tp: any) => {
        const { data: playerDetails } = await axios.get(`/players/${tp.player_id}`);

        return {
          id: playerDetails.id,
          name: playerDetails.name,
          category: playerDetails.category,
          bidAmount: tp.bid_amount,
        };
      })
    );

    return {
      teamId,
      ownerName,
      players,
    };
  } catch (error) {
    console.error("Error fetching team + players:", error);
    throw error;
  }
};
