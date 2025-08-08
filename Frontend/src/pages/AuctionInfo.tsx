import React from 'react';

const AuctionInfo: React.FC = () => {
  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h2>Auction Information</h2>
      
      <div style={{ 
        background: 'white', 
        padding: '2rem', 
        borderRadius: '12px', 
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        marginTop: '2rem'
      }}>
        <h3>Auction Rules</h3>
        <ul style={{ lineHeight: '1.8' }}>
          <li>Each team has a budget of $1,000,000</li>
          <li>Teams can bid on players in increments of $10</li>
          <li>Maximum 8 players per team</li>
          <li>Category limits: 3 Gold, 3 Silver, 2 Bronze players</li>
          <li>Bidding continues until no higher bids are placed</li>
          <li>Player goes to the highest bidder</li>
        </ul>

        <h3 style={{ marginTop: '2rem' }}>Player Categories</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
          <div style={{ padding: '1rem', background: '#FFD700', borderRadius: '8px', textAlign: 'center' }}>
            <strong>Gold Players</strong><br/>
            Premium players with high performance
          </div>
          <div style={{ padding: '1rem', background: '#C0C0C0', borderRadius: '8px', textAlign: 'center' }}>
            <strong>Silver Players</strong><br/>
            Good performers with consistent records
          </div>
          <div style={{ padding: '1rem', background: '#CD7F32', borderRadius: '8px', textAlign: 'center', color: 'white' }}>
            <strong>Bronze Players</strong><br/>
            Emerging talents and utility players
          </div>
        </div>

        <h3 style={{ marginTop: '2rem' }}>Player Types</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
          <div style={{ padding: '1rem', background: '#f7c873', borderRadius: '8px', textAlign: 'center' }}>
            <strong>Batters</strong><br/>
            Specialized in batting
          </div>
          <div style={{ padding: '1rem', background: '#7ec4cf', borderRadius: '8px', textAlign: 'center' }}>
            <strong>Bowlers</strong><br/>
            Specialized in bowling
          </div>
          <div style={{ padding: '1rem', background: '#b6e388', borderRadius: '8px', textAlign: 'center' }}>
            <strong>Allrounders</strong><br/>
            Good at both batting and bowling
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuctionInfo;