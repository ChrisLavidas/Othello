let audioContext = null;
let masterGain = null;

function getAudioContext() {
  if (typeof window === 'undefined') return null;

  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (!AudioContextClass) return null;

  if (!audioContext) {
    audioContext = new AudioContextClass();
    masterGain = audioContext.createGain();
    masterGain.gain.value = 0.55;
    masterGain.connect(audioContext.destination);
  }

  return audioContext;
}

export async function unlockAudio() {
  const ctx = getAudioContext();
  if (!ctx) return;

  if (ctx.state === 'suspended') {
    await ctx.resume();
  }
}

function playTone(ctx, { frequency, time, duration, type = 'sine', volume = 0.08, endFrequency }) {
  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();
  const start = time;
  const end = time + duration;

  oscillator.type = type;
  oscillator.frequency.setValueAtTime(frequency, start);

  if (endFrequency) {
    oscillator.frequency.exponentialRampToValueAtTime(endFrequency, end);
  }

  gain.gain.setValueAtTime(0.0001, start);
  gain.gain.exponentialRampToValueAtTime(volume, start + 0.012);
  gain.gain.exponentialRampToValueAtTime(0.0001, end);

  oscillator.connect(gain);
  gain.connect(masterGain);
  oscillator.start(start);
  oscillator.stop(end + 0.02);
}

function playNoise(ctx, time, duration, volume) {
  const bufferSize = Math.floor(ctx.sampleRate * duration);
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);

  for (let i = 0; i < bufferSize; i += 1) {
    data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
  }

  const source = ctx.createBufferSource();
  const gain = ctx.createGain();
  const filter = ctx.createBiquadFilter();

  filter.type = 'highpass';
  filter.frequency.value = 900;
  gain.gain.setValueAtTime(volume, time);
  gain.gain.exponentialRampToValueAtTime(0.0001, time + duration);

  source.buffer = buffer;
  source.connect(filter);
  filter.connect(gain);
  gain.connect(masterGain);
  source.start(time);
}

function playSequence(notes) {
  const ctx = getAudioContext();
  if (!ctx) return;

  if (ctx.state === 'suspended') {
    ctx.resume();
  }

  const now = ctx.currentTime + 0.02;
  notes.forEach(note => playTone(ctx, { ...note, time: now + note.delay }));
}

export function playSound(name) {
  const ctx = getAudioContext();
  if (!ctx) return;

  if (name === 'move') {
    const now = ctx.currentTime + 0.01;
    playNoise(ctx, now, 0.045, 0.025);
    playTone(ctx, { frequency: 520, time: now, duration: 0.08, type: 'triangle', volume: 0.08 });
    playTone(ctx, { frequency: 760, time: now + 0.045, duration: 0.09, type: 'sine', volume: 0.045 });
    return;
  }

  if (name === 'aiMove') {
    const now = ctx.currentTime + 0.01;
    playNoise(ctx, now, 0.05, 0.018);
    playTone(ctx, { frequency: 260, time: now, duration: 0.1, type: 'triangle', volume: 0.07 });
    playTone(ctx, { frequency: 390, time: now + 0.055, duration: 0.09, type: 'sine', volume: 0.04 });
    return;
  }

  if (name === 'invalid') {
    playSequence([
      { frequency: 180, delay: 0, duration: 0.08, type: 'sawtooth', volume: 0.045 },
      { frequency: 140, delay: 0.065, duration: 0.09, type: 'sawtooth', volume: 0.035 },
    ]);
    return;
  }

  if (name === 'pass') {
    playSequence([
      { frequency: 330, delay: 0, duration: 0.08, type: 'triangle', volume: 0.04 },
      { frequency: 247, delay: 0.08, duration: 0.12, type: 'triangle', volume: 0.035 },
    ]);
    return;
  }

  if (name === 'start') {
    playSequence([
      { frequency: 392, delay: 0, duration: 0.08, type: 'triangle', volume: 0.05 },
      { frequency: 523.25, delay: 0.07, duration: 0.1, type: 'triangle', volume: 0.06 },
      { frequency: 659.25, delay: 0.15, duration: 0.13, type: 'sine', volume: 0.06 },
    ]);
    return;
  }

  if (name === 'win') {
    playSequence([
      { frequency: 523.25, delay: 0, duration: 0.12, type: 'triangle', volume: 0.07 },
      { frequency: 659.25, delay: 0.1, duration: 0.12, type: 'triangle', volume: 0.075 },
      { frequency: 783.99, delay: 0.2, duration: 0.14, type: 'triangle', volume: 0.08 },
      { frequency: 1046.5, delay: 0.32, duration: 0.24, type: 'sine', volume: 0.07 },
    ]);
    return;
  }

  if (name === 'lose') {
    playSequence([
      { frequency: 392, delay: 0, duration: 0.16, type: 'triangle', volume: 0.065 },
      { frequency: 329.63, delay: 0.14, duration: 0.18, type: 'triangle', volume: 0.055 },
      { frequency: 246.94, delay: 0.3, duration: 0.28, type: 'sine', volume: 0.05 },
    ]);
    return;
  }

  if (name === 'tie') {
    playSequence([
      { frequency: 440, delay: 0, duration: 0.1, type: 'triangle', volume: 0.055 },
      { frequency: 440, delay: 0.12, duration: 0.1, type: 'triangle', volume: 0.055 },
      { frequency: 493.88, delay: 0.25, duration: 0.16, type: 'sine', volume: 0.05 },
    ]);
  }
}
