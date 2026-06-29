import React from 'react';
import './ScoreBoard.css';

export default function ScoreBoard({ scores, humanColor, status, isAiTurn }) {
  return (
    <div className="scoreboard">
      <div className={`score-card ${humanColor === 'B' ? 'active-turn' : ''}`}>
        <div className="disc-dot black" />
        <div className="score-info">
          <div className="score-label">
            Black&nbsp;
            {humanColor === 'B'
              ? <span className="badge you">You</span>
              : <span className="badge ai">AI</span>
            }
          </div>
          <div className="score-num">{scores.B}</div>
        </div>
      </div>

      <div className="status-center">
        {isAiTurn
          ? <span className="thinking">⏳</span>
          : <span>VS</span>
        }
      </div>

      <div className={`score-card ${humanColor === 'W' ? 'active-turn' : ''}`}>
        <div className="disc-dot white" />
        <div className="score-info">
          <div className="score-label">
            White&nbsp;
            {humanColor === 'W'
              ? <span className="badge you">You</span>
              : <span className="badge ai">AI</span>
            }
          </div>
          <div className="score-num">{scores.W}</div>
        </div>
      </div>
    </div>
  );
}
