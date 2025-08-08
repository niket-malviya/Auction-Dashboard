import React from 'react';
import './Resold.css';

interface ResoldProps {
  isAnimationNeeded?: boolean;
}

const Resold: React.FC<ResoldProps> = ({ isAnimationNeeded = false }) => {
  return (
    <div className={`resold-badge ${isAnimationNeeded ? 'animated' : ''}`}>
      RESOLD
    </div>
  );
};

export default Resold; 