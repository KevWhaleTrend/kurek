/* ═══════════════════════════════════════════════════════════════
   VOIDYACHT — shared.js
   Loader, navbar highlight, scroll-reveal, page-transition
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── 1. LOADER ── */
  document.body.classList.add('vy-loading');
  const lc = document.getElementById('vy-loader-content');
  const ll = document.getElementById('vy-loader-line');

  setTimeout(() => {
    if (lc) lc.style.opacity = '1';
    setTimeout(() => {
      if (ll) ll.style.width = '100%';
      setTimeout(() => {
        document.body.classList.remove('vy-loading');
        document.body.classList.add('vy-loaded');
        setTimeout(() => {
          const el = document.getElementById('vy-loader');
          if (el) el.style.display = 'none';
        }, 800);
      }, 600);
    }, 200);
  }, 50);

  /* ── 2. ACTIVE NAV LINK ── */
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.vy-nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === current || (current === '' && href === 'index.html')) {
      a.classList.add('nav-active');
    }
  });

  /* ── 3. SCROLL-REVEAL ── */
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('vy-visible'), i * 80);
        revealObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.vy-reveal').forEach(el => revealObs.observe(el));

  /* ── 4. PAGE TRANSITION ── */
  document.querySelectorAll('a[href]').forEach(a => {
    a.addEventListener('click', e => {
      try {
        const tgt = new URL(a.href, window.location.href);
        if (
          tgt.hostname === window.location.hostname &&
          tgt.pathname !== window.location.pathname &&
          !a.hasAttribute('target') &&
          !a.href.includes('#')
        ) {
          e.preventDefault();
          document.body.classList.remove('vy-loaded');
          document.body.classList.add('vy-navigating');
          setTimeout(() => { window.location.href = a.href; }, 700);
        }
      } catch (_) { }
    });
  });



})();
