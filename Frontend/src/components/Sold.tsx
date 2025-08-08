import React from "react";
import './Sold.css';

interface ISold { 
    isAnimationNeeded: boolean
}

const Sold: React.FC<ISold> =  ({isAnimationNeeded = false}) => (
    <div className={isAnimationNeeded ? 'sold-out-stamp animate' : 'sold-out-stamp'}>SOLD OUT</div>
)

export default Sold;