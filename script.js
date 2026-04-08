/* ============================================================
   CHAINSCAN — Onchain Wallet Intelligence | Main Script
   ============================================================ */

gsap.registerPlugin(ScrollTrigger, TextPlugin);

// ── HEX GRID BACKGROUND ─────────────────────────────────────
(function initHexBackground() {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H, hexes = [];
  const R = 30;
  const HH = R * Math.sqrt(3);
  const CW = R * 1.5;

  function buildGrid() {
    hexes = [];
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
    const cols = Math.ceil(W / CW) + 3;
    const rows = Math.ceil(H / HH) + 3;
    for (let c = -1; c < cols; c++) {
      for (let r = -1; r < rows; r++) {
        hexes.push({
          x: c * CW,
          y: r * HH + (c % 2 === 0 ? 0 : HH / 2),
          glow: 0,
          timer: Math.random() * 300,
        });
      }
    }
  }
  buildGrid();
  window.addEventListener('resize', buildGrid);

  function drawHex(cx, cy, r, opacity, fill) {
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const a = (Math.PI / 3) * i - Math.PI / 6;
      const px = cx + r * Math.cos(a);
      const py = cy + r * Math.sin(a);
      i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
    }
    ctx.closePath();
    if (fill) {
      ctx.fillStyle = `rgba(255,107,0,${opacity * 0.15})`;
      ctx.fill();
    }
    ctx.strokeStyle = `rgba(255,107,0,${opacity})`;
    ctx.lineWidth = 0.5;
    ctx.stroke();
  }

  // Subtle star field
  const stars = Array.from({ length: 60 }, () => ({
    x: Math.random(), y: Math.random(),
    r: Math.random() * 1.2 + 0.3,
    a: Math.random() * 0.4 + 0.1,
    flicker: Math.random() * 100,
  }));

  let frame = 0;
  function animate() {
    ctx.clearRect(0, 0, W, H);
    frame++;

    // Stars
    stars.forEach(s => {
      s.flicker += 0.8;
      const alpha = s.a * (0.6 + 0.4 * Math.sin(s.flicker * 0.04));
      ctx.beginPath();
      ctx.arc(s.x * W, s.y * H, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${alpha})`;
      ctx.fill();
    });

    // Hex grid
    hexes.forEach(h => {
      h.timer--;
      if (h.timer <= 0 && h.glow === 0) {
        h.glow = 0.18 + Math.random() * 0.14;
        h.timer = 200 + Math.random() * 400;
      }
      if (h.glow > 0) { h.glow -= 0.005; if (h.glow < 0) h.glow = 0; }
      const base = 0.025 + (Math.sin(frame * 0.003 + h.x * 0.01) * 0.008);
      drawHex(h.x, h.y, R - 1.5, base + h.glow, h.glow > 0.06);
    });

    requestAnimationFrame(animate);
  }
  animate();
})();

// ── CUSTOM CURSOR (sleek black arrow) ────────────────────────
(function initCursor() {
  const cursor  = document.getElementById('cursor-arrow');
  const ring    = document.getElementById('cursor-ring');
  let mx = -100, my = -100, rx = -100, ry = -100;
  let visible = false;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    if (!visible && cursor) { cursor.style.opacity = '1'; visible = true; }
  }, { passive: true });

  document.addEventListener('mouseleave', () => {
    if (cursor) cursor.style.opacity = '0';
    visible = false;
  });

  function loop() {
    if (cursor) {
      cursor.style.transform = `translate(${mx}px,${my}px)`;
    }
    if (ring) {
      rx += (mx - rx) * 0.1;
      ry += (my - ry) * 0.1;
      ring.style.transform = `translate(${rx - 18}px,${ry - 18}px)`;
    }
    requestAnimationFrame(loop);
  }
  loop();

  document.querySelectorAll('a,button,input,[data-step],.step-card,.target-card').forEach(el => {
    el.addEventListener('mouseenter', () => { if (ring) ring.classList.add('hover'); });
    el.addEventListener('mouseleave', () => { if (ring) ring.classList.remove('hover'); });
  });
})();

// ── NAVBAR SCROLL ────────────────────────────────────────────
(function initNav() {
  const nav = document.getElementById('navbar');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 50);
  }, { passive: true });

  const hamburger = document.getElementById('hamburger');
  if (hamburger) hamburger.addEventListener('click', () => {
    const links = nav.querySelector('.nav-links');
    const btn   = nav.querySelector('.btn-nav');
    if (links) {
      const open = links.style.display === 'flex';
      links.style.cssText = open ? '' : 'display:flex;flex-direction:column;position:absolute;top:70px;left:0;right:0;background:rgba(10,10,10,0.98);padding:1.5rem 2rem;border-bottom:1px solid #222;';
      if (btn) btn.style.display = open ? '' : 'block';
    }
  });
})();

// ── SCROLL REVEAL ────────────────────────────────────────────
(function initReveal() {
  const els = document.querySelectorAll('.step-card,.section-label,.section-title,.section-sub,.mockup-ui,.terminal-wrap,.agent-tier-box');
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('visible'), i * 80);
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  els.forEach(el => { el.classList.add('reveal'); io.observe(el); });
})();

// ── GSAP HERO ENTRANCE ───────────────────────────────────────
(function initScrollAnimations() {
  gsap.from('#hero-content', { opacity: 0, y: 50, duration: 1.1, ease: 'power3.out', delay: 0.2 });

  const whaleImg = document.getElementById('whale-img');
  if (whaleImg) {
    whaleImg.style.transition = 'transform 0.3s cubic-bezier(0.2,0.8,0.2,1)';
    let wx = 0, wy = 0;
    document.addEventListener('mousemove', e => {
      const dx = (e.clientX / window.innerWidth - 0.5);
      const dy = (e.clientY / window.innerHeight - 0.5);
      wx = dy * -12; wy = dx * 14;
      whaleImg.style.transform = `perspective(1200px) rotateX(${wx}deg) rotateY(${wy}deg) translateX(${dx*20}px) translateY(${dy*14}px)`;
    }, { passive: true });
    document.addEventListener('mouseleave', () => {
      whaleImg.style.transform = '';
    });

    ScrollTrigger.create({
      trigger: '#hero', start: 'top top', end: 'bottom top', scrub: true,
      onUpdate: self => {
        whaleImg.style.opacity = Math.max(0, 0.72 - self.progress * 1.4);
      }
    });
  }
})();

// ── STEP CARD SPOTLIGHT ──────────────────────────────────────
(function initCardEffects() {
  document.querySelectorAll('.step-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 100;
      const y = ((e.clientY - r.top) / r.height) * 100;
      card.style.background = `radial-gradient(circle at ${x}% ${y}%, #1e1e1e 0%, #161616 60%)`;
    });
    card.addEventListener('mouseleave', () => { card.style.background = ''; });
  });
})();

// ── PAGE FADE IN ─────────────────────────────────────────────
window.addEventListener('load', () => {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.5s ease';
  setTimeout(() => { document.body.style.opacity = '1'; }, 80);
});
