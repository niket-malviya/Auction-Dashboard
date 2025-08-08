

import { privateApi } from './axios';

export const assignPlayerToTeam = async (
  playerId: string,
  tournamentId: string,
  teamId: string,
  bidAmount: number
) => {
  const response = await privateApi.post('team_players', {
    player_id: playerId,
    tournament_id: tournamentId,
    team_id: teamId,
    bid_amount: bidAmount,
  });
  return response.data;
};
