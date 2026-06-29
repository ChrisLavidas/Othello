import React, { useState } from 'react';
import { playSound, unlockAudio } from '../audio';
import './Setup.css';

export default function Setup({ onStart }) {
  const [color, setColor] = useState('B');
  const [depth, setDepth] = useState(3);
  const [loading, setLoading] = useState(false);

  async function handleStart() {
    setLoading(true);
    await unlockAudio();
    playSound('start');

    try {
      await onStart(color, depth);
    } finally {
      setLoading(false);
    }
  }

  const depthLabels = ['', 'Very Easy', 'Easy', 'Medium', 'Hard', 'Very Hard', 'Expert'];

  return (
    <div className="setup-wrapper">
      <header className="setup-header">
        <h1>OTHELLO</h1>
        <p>Reversi — Minimax AI with Alpha-Beta Pruning</p>
        <p style={{fontSize: '12px', color: '#888', marginTop: '4px'}}>Game by Chris Lavidas</p>
      </header>

      <div className="setup-card">
        <div className="setup-title">Game Settings</div>

        <div className="setup-row">
          <label>Your Color:</label>
          <div className="color-btns">
            <button
              className={`color-btn ${color === 'B' ? 'active' : ''}`}
              onClick={() => setColor('B')}
            >
              ⚫ Black
            </button>
            <button
              className={`color-btn ${color === 'W' ? 'active' : ''}`}
              onClick={() => setColor('W')}
            >
              ⚪ White
            </button>
          </div>
          <p className="color-hint">Black always plays first</p>
        </div>

        <div className="setup-row">
          <label>
            AI Depth: <strong>{depth}</strong>
            <span className="depth-label-text"> — {depthLabels[depth]}</span>
          </label>
          <input
            type="range"
            min={1}
            max={6}
            value={depth}
            onChange={e => setDepth(Number(e.target.value))}
            className="depth-slider"
          />
          <div className="depth-labels">
            <span>1 — Easy</span>
            <span>6 — Expert</span>
          </div>
        </div>

        <button className="start-btn" onClick={handleStart} disabled={loading}>
          {loading ? 'Loading...' : '▶ Start Game'}
        </button>
      </div>
    </div>
  );
}
