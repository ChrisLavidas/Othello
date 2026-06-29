const BASE = process.env.REACT_APP_API_URL || '';

async function readError(res, fallback) {
  const text = await res.text();

  try {
    const data = JSON.parse(text);
    return data.detail || fallback;
  } catch {
    return text || fallback;
  }
}

export async function setupGame(humanColor, depth) {
  const res = await fetch(`${BASE}/setup_game/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ human_color: humanColor, depth }),
  });
  if (!res.ok) throw new Error(await readError(res, 'Σφάλμα σύνδεσης με τον server'));
  return res.json();
}

export async function getState() {
  const res = await fetch(`${BASE}/state`);
  if (!res.ok) throw new Error(await readError(res, 'Σφάλμα ανάκτησης κατάστασης'));
  return res.json();
}

export async function makeMove(row, col) {
  const res = await fetch(`${BASE}/make_move/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ row, col }),
  });
  if (!res.ok) {
    throw new Error(await readError(res, 'Σφάλμα κίνησης'));
  }
  return res.json();
}

export async function aiTurn() {
  const res = await fetch(`${BASE}/ai_turn/`, { method: 'POST' });
  if (!res.ok) {
    throw new Error(await readError(res, 'Σφάλμα AI'));
  }
  return res.json();
}

export async function resetGame() {
  const res = await fetch(`${BASE}/reset`, { method: 'POST' });
  if (!res.ok) throw new Error(await readError(res, 'Σφάλμα επανεκκίνησης'));
  return res.json();
}
