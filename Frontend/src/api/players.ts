import api, { privateApi } from './axios';

export type Player = {
  id: string;
  name: string;
  lastName: string;
  flatNo: string;
  age: number;
  mobileNumber: string;
  imgUrl: string | null;
  bowlerType: 'left' | 'right' | null;
  batterType: 'left' | 'right' | null;
  category: 'gold' | 'silver' | 'bronze' | null;
  tournamentId: string;
  status:string;
  isOwner: boolean;
};

export const fetchPlayers = async (): Promise<Player[]> => {
  const response = await privateApi.get('players'); // Assumes Flask route is /players
  return response.data.map((player: any) => ({
    id: player.id,
    name: player.name,
    lastName: player.last_name,
    flatNo: player.flat_no,
    age: player.age,
    mobileNumber: player.mobile_number,
    imgUrl: player.img_url,
    bowlerType: player.bowler_type,
    batterType: player.batter_type,
    category: player.category,
    tournamentId: player.tournament_id,
    status:player.status,
    isOwner: player.is_owner,
  }));
};
