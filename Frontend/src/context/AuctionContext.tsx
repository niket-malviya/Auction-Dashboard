import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { Player, Team } from '../types';

export interface AuctionContextType {
  players: Player[];
  teams: Team[];
  currentUser: string | null;
  setPlayers: React.Dispatch<React.SetStateAction<Player[]>>;
  setTeams: React.Dispatch<React.SetStateAction<Team[]>>;
  setCurrentUser: React.Dispatch<React.SetStateAction<string | null>>;
}

const AuctionContext = createContext<AuctionContextType | undefined>(undefined);

export const AuctionProvider = ({ children }: { children: ReactNode }) => {
  const [players, setPlayers] = useState<Player[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [currentUser, setCurrentUser] = useState<string | null>(null);

  return (
    <AuctionContext.Provider value={{ players, teams, currentUser, setPlayers, setTeams, setCurrentUser }}>
      {children}
    </AuctionContext.Provider>
  );
};

export const useAuction = () => {
  const context = useContext(AuctionContext);
  if (!context) throw new Error('useAuction must be used within AuctionProvider');
  return context;
};