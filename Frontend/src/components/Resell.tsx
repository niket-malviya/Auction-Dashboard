import React from 'react';
import './Resell.css';

interface ResellProps {
  isAnimationNeeded?: boolean;
}

const Resell: React.FC<ResellProps> = ({ isAnimationNeeded = false }) => {
  return (
    <div className={`resell-badge ${isAnimationNeeded ? 'animated' : ''}`}>
      RESELL
    </div>
  );
};

export default Resell; 