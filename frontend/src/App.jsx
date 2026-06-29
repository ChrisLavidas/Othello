import React, { useState } from 'react';
import Setup from './components/Setup';
import Game from './components/Game';
import { setupGame, resetGame } from './api';

export default function App() {
  const [screen, setScreen] = useState('setup'); // 'setup' | 'game'
  const [humanColor, setHumanColor] = useState('B');

  async function handleStart(color, depth) {
    try {
      await setupGame(color, depth);
      setHumanColor(color);
      setScreen('game');
    } catch (e) {
      alert(
        'Δεν μπόρεσα να συνδεθώ με τον server.\n' +
        'Σιγουρέψου ότι τρέχει το backend:\n\n' +
        'cd backend\nuvicorn server:app --reload --port 8000\n\n' +
        e.message
      );
    }
  }

  async function handleReset() {
    await resetGame();
    setScreen('setup');
  }

  if (screen === 'game') {
    return <Game humanColor={humanColor} onReset={handleReset} />;
  }

  return <Setup onStart={handleStart} />;
}
