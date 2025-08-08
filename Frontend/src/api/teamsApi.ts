import api from './axios';
import type { Team } from '../types';

const DEFAULT_MAX_GOLD = 3;
const DEFAULT_MAX_SILVER = 4;
const DEFAULT_MAX_BRONZE = 4;
const DEFAULT_OWNER_PHOTO = 'https://yourcdn.com/default-photo.jpg';

export const fetchTeams = async (): Promise<Team[]> => {
  const response = await api.get('teams');
  return response.data.map((team: any) => ({
    id: team.id,
    name: team.team_name,
    owner: team.owner_name,
    budget: team.total_amount,
    remaining: team.remaining_amount,
    maxPlayers: team.max_players,
    img_url: team.img_url|| DEFAULT_OWNER_PHOTO,

    totalPlayers: team.total_players,
    goldCount: team.gold,
    silverCount: team.silver,
    bronzeCount: team.bronze,
    maxGold: DEFAULT_MAX_GOLD,
    maxSilver: DEFAULT_MAX_SILVER,
    maxBronze: DEFAULT_MAX_BRONZE,
    //ownerPhoto: team.img_url || DEFAULT_OWNER_PHOTO,
  }));
};
