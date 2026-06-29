import React, { useState, useEffect, useCallback } from 'react';
import Cell from './Cell';
import ScoreBoard from './ScoreBoard';
import { getState, makeMove, aiTurn } from '../api';
import { playSound, unlockAudio } from '../audio';
import './Game.css';

export default function Game({ humanColor, onReset }) {
  const [board, setBoard] = useState(
    Array(8).fill(null).map(() => Array(8).fill(0))
  );
  const [availableMoves, setAvailableMoves] = useState([]);
  const [lastMove, setLastMove] = useState(null);
  const [scores, setScores] = useState({ W: 2, B: 2 });
  const [status, setStatus] = useState('Loading...');
  const [gameOver, setGameOver] = useState(false);
  const [gameOverMsg, setGameOverMsg] = useState('');
  const [isAiTurn, setIsAiTurn] = useState(false);

  const countScores = useCallback((b) => {
    let W = 0, B = 0;
    b.forEach(row => row.forEach(v => {
      if (v === 1) W++;
      else if (v === -1) B++;
    }));
    return { W, B };
  }, []);

  function endGame(sc) {
    setGameOver(true);
    setAvailableMoves([]);
    setIsAiTurn(false);
    setScores(sc);
    const humanPieces = humanColor === 'W' ? sc.W : sc.B;
    const aiPieces    = humanColor === 'W' ? sc.B : sc.W;
    if (humanPieces > aiPieces) {
      playSound('win');
      setGameOverMsg(`🎉 You win! ...${humanPieces}–${aiPieces}`);
    } else if (aiPieces > humanPieces) {
      playSound('lose');
      setGameOverMsg(`🤖 AI wins! ${aiPieces}–${humanPieces}`);
    } else {
      playSound('tie');
      setGameOverMsg(`🤝 It's a tie! ${humanPieces}–${aiPieces}`);
    }
    setStatus('Game Over!');
  }

  const triggerAi = useCallback(async () => {
    setIsAiTurn(true);
    setStatus('AI is thinking...');
    try {
      const data = await aiTurn();
      setBoard(data.board);
      if (data.ai_move) setLastMove(data.ai_move);
      setScores(countScores(data.board));

      if (data.scores) {
        endGame(data.scores);
      } else if (data.next_player_is_ai) {
        // Ο άνθρωπος δεν έχει κινήσεις, ο AI παίζει ξανά
        playSound(data.ai_move ? 'aiMove' : 'pass');
        setStatus('You have no moves — AI plays again...');
        setTimeout(triggerAi, 800);
      } else {
        // Σειρά ανθρώπου
        playSound(data.ai_move ? 'aiMove' : 'pass');
        setIsAiTurn(false);
        const state = await getState();
        setAvailableMoves(state.available_moves || []);
        setStatus(humanColor === 'B' ? 'Your turn ⚫' : 'Your turn ⚪');
      }
    } catch (e) {
      setStatus('Error: ' + e.message);
      setIsAiTurn(false);
    }
  
  }, [humanColor, countScores]);

  useEffect(() => {
    async function init() {
      try {
        const state = await getState();
        setBoard(state.board);
        setScores(countScores(state.board));

        // Ο μαύρος παίζει πάντα πρώτος
        if (humanColor === 'B') {
          setAvailableMoves(state.available_moves || []);
          setStatus('Your turn ⚫ — Select a position');
        } else {
          // AI (Μαύρο) παίζει πρώτο
          setTimeout(triggerAi, 500);
        }
      } catch (e) {
        setStatus('Connection error with backend');
      }
    }
    init();
  }, [humanColor, countScores, triggerAi]);

  async function handleCellClick(row, col) {
    if (gameOver || isAiTurn) return;
    await unlockAudio();

    const isValid = availableMoves.some(([r, c]) => r === row && c === col);
    if (!isValid) {
      playSound('invalid');
      return;
    }

    try {
      playSound('move');
      setAvailableMoves([]);
      const data = await makeMove(row, col);
      setBoard(data.board);
      setLastMove([row, col]);
      setScores(countScores(data.board));

      if (data.scores) {
        endGame(data.scores);
      } else if (data.next_player_is_ai) {
        setTimeout(triggerAi, 350);
      } else {
        // Ο AI έκανε πάσο — σειρά ανθρώπου ξανά
        const state = await getState();
        setAvailableMoves(state.available_moves || []);
        setStatus(humanColor === 'B' ? 'Your turn ⚫' : 'Your turn ⚪');
      }
    } catch (e) {
      // Αν η κίνηση απορριφθεί, ανάκτησε διαθέσιμες κινήσεις
      playSound('invalid');
      setStatus('⚠️ ' + e.message);
      try {
        const state = await getState();
        setAvailableMoves(state.available_moves || []);
      } catch (_) {}
    }
  }

  const hintSet = new Set(availableMoves.map(([r, c]) => `${r},${c}`));

  return (
    <div className="game-wrapper">
      <header className="game-header">
        <h1>OTHELLO</h1>
      </header>

      <div className="game-container">
        <ScoreBoard
          scores={scores}
          humanColor={humanColor}
          status={status}
          isAiTurn={isAiTurn}
        />

        <div className="status-bar">{status}</div>

        <div className="board-outer">
          <div className="board-grid">
            {board.map((row, i) =>
              row.map((val, j) => (
                <Cell
                  key={`${i}-${j}`}
                  value={val}
                  isHint={!isAiTurn && !gameOver && hintSet.has(`${i},${j}`)}
                  isLast={lastMove && lastMove[0] === i && lastMove[1] === j}
                  onClick={() => handleCellClick(i, j)}
                />
              ))
            )}
          </div>
        </div>

        {gameOver && (
          <div className="gameover-banner">
            <div className="gameover-msg">{gameOverMsg}</div>
          </div>
        )}

        <div className="game-actions">
          <button
            className="reset-btn"
            onClick={() => {
              playSound('start');
              onReset();
            }}
          >
            ↺ New Game
          </button>
        </div>
      </div>
    </div>
  );
}
