/* ラベンダーの花びら — ロゴ左の花穂をクリックすると花びらが舞って茂みの音が鳴る */
(() => {
  const btn = document.querySelector('.lavender-hotspot');
  if (!btn) return;

  // ロゴの花の紫に合わせた色
  const COLORS = ['#8e7cc3', '#a594d1', '#b9a9e0', '#7b6aa8', '#c9bde6'];
  const PETAL_COUNT = 22;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 花びらを描く透明なレイヤー（ページ全体の上に重ねる）
  let layer = null;
  function getLayer() {
    if (!layer) {
      layer = document.createElement('div');
      layer.className = 'lavender-layer';
      layer.setAttribute('aria-hidden', 'true');
      document.body.appendChild(layer);
    }
    return layer;
  }

  // 音（data-sound に指定したファイル）
  let sound = null;
  if (btn.dataset.sound) {
    sound = new Audio(btn.dataset.sound);
    sound.preload = 'auto';
    sound.volume = 0.4; // 音量 0〜1
  }

  function playSound() {
    if (!sound) return;
    // 連打しても音が重なるように複製して鳴らす
    const s = sound.cloneNode();
    s.volume = sound.volume;
    s.play().catch(() => {});
  }

  function scatter() {
    const r = btn.getBoundingClientRect();
    const box = getLayer();
    const count = reduceMotion ? 6 : PETAL_COUNT;

    for (let i = 0; i < count; i++) {
      const p = document.createElement('span');
      p.className = 'lavender-petal';

      // 花穂のあたり（クリック範囲の上半分）から生まれる
      const x = r.left + r.width * (0.15 + Math.random() * 0.7);
      const y = r.top + r.height * (0.05 + Math.random() * 0.55);
      p.style.left = x + 'px';
      p.style.top = y + 'px';
      p.style.background = COLORS[Math.floor(Math.random() * COLORS.length)];

      // ゆるく右へ流れながら落ちる
      p.style.setProperty('--dx', Math.round(Math.random() * 160 - 40) + 'px');
      p.style.setProperty('--dy', Math.round(180 + Math.random() * 240) + 'px');
      p.style.setProperty('--sway', Math.round(Math.random() * 60 - 30) + 'px');
      p.style.setProperty('--rot', Math.round(Math.random() * 600 - 300) + 'deg');
      p.style.setProperty('--dur', (2 + Math.random() * 1.6).toFixed(2) + 's');
      p.style.setProperty('--delay', (Math.random() * 0.25).toFixed(2) + 's');

      box.appendChild(p);
      p.addEventListener('animationend', () => p.remove());
    }
  }

  btn.addEventListener('click', (e) => {
    e.preventDefault();
    playSound();
    scatter();
  });
})();
