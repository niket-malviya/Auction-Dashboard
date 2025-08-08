import React, { useState } from 'react';
import './BidInput.css';

interface BidInputProps {
  bidAmount: number;
  setBidAmount: (amount: number) => void;
  teamList: { id: string; name: string }[] | undefined;
  selectedTeam: string;
  setSelectedTeam: (team: string) => void;
  onSubmit: () => void;
  onUnsold: () => void;
  disabled?: boolean;
}

const BidInput: React.FC<BidInputProps> = ({
  bidAmount,
  setBidAmount,
  teamList,
  selectedTeam,
  setSelectedTeam,
  onSubmit,
  onUnsold,
  disabled = false
}) => {
  const [inputValue, setInputValue] = useState(bidAmount.toString());
  const [showError, setShowError] = useState(false);

  // Sync inputValue with bidAmount when it changes externally
  React.useEffect(() => {
    setInputValue(bidAmount.toString());
    setShowError(false);
  }, [bidAmount]);

  const handleIncrease = () => {
    if (!disabled) {
      setBidAmount(bidAmount + 10);
      setInputValue((bidAmount + 10).toString());
      setShowError(false);
    }
  };

  const handleDecrease = () => {
    if (!disabled && bidAmount > 10) {
      setBidAmount(bidAmount - 10);
      setInputValue((bidAmount - 10).toString());
      setShowError(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!disabled) {
      const value = e.target.value;
      setInputValue(value);
      
      const numericValue = Number(value);
      
      if (value === '') {
        setShowError(false);
      } else if (isNaN(numericValue)) {
        setShowError(true);
      } else if (numericValue < 10) {
        setShowError(true);
      } else {
        setBidAmount(numericValue);
        setShowError(false);
      }
    }
  };

  const handleInputBlur = () => {
    if (!disabled) {
      const numericValue = Number(inputValue);
      
      if (inputValue === '' || isNaN(numericValue) || numericValue < 10) {
        setBidAmount(10);
        setInputValue('10');
        setShowError(false);
      }
    }
  };

  const handleSubmit = () => {
    if (!disabled && selectedTeam) {
      const numericValue = Number(inputValue);
      if (numericValue >= 10) {
        onSubmit();
      }
    }
  };

  // Check if submit button should be disabled
  const isSubmitDisabled = disabled || !selectedTeam || Number(inputValue) < 10 || isNaN(Number(inputValue));

  return (
    <div className="bid-input">
      <div className="bid-controls">
        <button 
          type="button" 
          onClick={handleDecrease}
          disabled={disabled || bidAmount <= 10}
          className={disabled ? 'disabled' : ''}
        >
          -
        </button>
                 <div className="input-container">
           <input
             type="number"
             value={inputValue}
             onChange={handleInputChange}
             onBlur={handleInputBlur}
             min="10"
             disabled={disabled}
             className={`${disabled ? 'disabled' : ''} ${showError ? 'error' : ''}`}
           />
           {showError && (
             <div className="error-message">Min bid: $10</div>
           )}
         </div>
        <button 
          type="button" 
          onClick={handleIncrease}
          disabled={disabled}
          className={disabled ? 'disabled' : ''}
        >
          +
        </button>
      </div>
      
      <select
        value={selectedTeam}
        onChange={(e) => !disabled && setSelectedTeam(e.target.value)}
        disabled={disabled}
        className={disabled ? 'disabled' : ''}
      >
        <option value="">Select Team</option>
        {teamList.map(team => (
          <option key={team.id} value={team.id}>
            {team.name}
          </option>
        ))}
      </select>
      
             <div className="bid-buttons">
         <button
           type="button"
           onClick={onUnsold}
           disabled={disabled}
           className={disabled ? 'disabled' : ''}
         >
           Unsold
         </button>
         <button
           type="button"
           onClick={handleSubmit}
           disabled={isSubmitDisabled}
           className={isSubmitDisabled ? 'disabled' : ''}
         >
           Sold
         </button>
       </div>
    </div>
  );
};

export default BidInput;