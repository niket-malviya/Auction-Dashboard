// Types
export type BattingType = 'left' | 'right' | null;
export type BowlingType = 'left' | 'right' | null;
export type PlayerCategory = 'gold' | 'silver' | 'bronze' | null;
export type PlayerStatus = 'available' | 'sold' | 'unsold';

export interface Player {
  id: string;
  name: string;
  lastName: string;
  flatNo: string;
  age: number;
  mobileNumber: string;
  batterType: BattingType;
  bowlerType: BowlingType;
  category: PlayerCategory;
  tournamentId: string;
  status?: PlayerStatus;
  imgUrl?: string | null;
  // frontend-only field
  type?: 'Batter' | 'Bowler' | 'Allrounder'; // derived on frontend
}


export interface Team {
  id: string;
  name: string;
  owner: string;
  budget: number;
  remaining: number;
  maxPlayers: number;
  img_url?: string;
  // frontend-only fields
  totalPlayers: number;
  goldCount: number;
  silverCount: number;
  bronzeCount: number;
  maxGold: number;
  maxSilver: number;
  maxBronze: number;
  ownerPhoto?: string;
  players?: Player[];
}

