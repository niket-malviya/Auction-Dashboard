import React from 'react';
import './Unsold.css';

interface UnsoldProps {
  isAnimationNeeded?: boolean;
}

const Unsold: React.FC<UnsoldProps> = ({ isAnimationNeeded = false }) => {
  return (
    <div className={`unsold-badge ${isAnimationNeeded ? 'animated' : ''}`}>
      UNSOLD
    </div>
  );
};

export default Unsold; 