// import React from "react";
// import './Sold.css';

// interface ISold { 
//     isAnimationNeeded: boolean
// }

// const Sold: React.FC<ISold> =  ({isAnimationNeeded = false}) => (
//     <div className={isAnimationNeeded ? 'sold-out-stamp animate' : 'sold-out-stamp'}>SOLD OUT</div>
// )

// export default Sold;

import React from "react";
import './Sold.css';

interface ISold { 
    isAnimationNeeded?: boolean;
    positionClass?: string; // <-- New prop
}

const Sold: React.FC<ISold> = ({ isAnimationNeeded = false, positionClass = "" }) => (
    <div 
        className={`sold-out-stamp ${isAnimationNeeded ? 'animate' : ''} ${positionClass}`}
    >
        SOLD OUT
    </div>
);

export default Sold;
