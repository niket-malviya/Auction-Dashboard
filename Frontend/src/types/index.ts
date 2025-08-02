// Types
export type PlayerType = 'Batter' | 'Bowler' | 'Allrounder';
export type PlayerCategory = 'Gold' | 'Silver' | 'Bronze';

export interface Player {
  id: string;
  name: string;
  age: number;
  photo: string;
  type: PlayerType;
  category: PlayerCategory;
}

export interface Team {
  id: string;
  name: string;
  owner: string;
  ownerPhoto: string;
  players: Player[];
  goldCount: number;
  silverCount: number;
  bronzeCount: number;
  maxGold: number;
  maxSilver: number;
  maxBronze: number;
  totalPlayers: number;
  maxPlayers: number;
  budget: number;
  remaining: number;
} 