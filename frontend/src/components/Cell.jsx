import React from 'react';
import './Cell.css';

export default function Cell({ value, isHint, isLast, onClick }) {
  return (
    <div
      className={`cell ${isHint ? 'hint' : ''}`}
      onClick={onClick}
      title={isHint ? 'Έγκυρη κίνηση' : ''}
    >
      {value !== 0 && (
        <div className={`disc ${value === 1 ? 'white' : 'black'} ${isLast ? 'last' : ''}`} />
      )}
      {value === 0 && isHint && <div className="hint-dot" />}
    </div>
  );
}
