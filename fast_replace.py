"""
Applies to all 3 HTML pages:
1. Fixes loader logo ghost: hides #loader entirely after animation + removes stray `}` from index.html
2. Replaces side-drawer with full-page overlay menu
3. Hamburger only in navbar (no visible nav-links on desktop either, clean look)
4. Mobile-responsive via existing CSS + overlay
"""

import re

# ─── Shared snippets ───────────────────────────────────────────────────────────

OVERLAY_CSS = """
    /* ── FULL PAGE NAV OVERLAY ── */
    .hamburger-btn {
      display: flex !important;
      flex-direction: column;
      gap: 6px;
      background: none;
      border: none;
      cursor: pointer;
      z-index: 3000;
      padding: 10px;
      position: relative;
    }
    .hamburger-btn span {
      display: block;
      width: 26px;
      height: 1.5px;
      background: var(--text-main, #F0EDE6);
      transition: transform 0.4s ease, opacity 0.4s ease, width 0.4s ease;
      transform-origin: center;
    }
    .hamburger-btn.open span:nth-child(1) { transform: translateY(7.5px) rotate(45deg); }
    .hamburger-btn.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
    .hamburger-btn.open span:nth-child(3) { transform: translateY(-7.5px) rotate(-45deg); }

    .fullnav-overlay {
      position: fixed;
      inset: 0;
      z-index: 2500;
      background: var(--bg, #061A24);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      padding: 0 8vw;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.5s cubic-bezier(0.16,1,0.3,1), visibility 0.5s;
      overflow: hidden;
    }
    .fullnav-overlay.open {
      opacity: 1;
      visibility: visible;
    }
    .fullnav-overlay .nav-item {
      font-family: 'Editorial New', 'Fraunces', serif;
      font-size: clamp(2.5rem, 7vw, 6rem);
      font-weight: 300;
      color: var(--text-main, #F0EDE6);
      text-decoration: none;
      line-height: 1.15;
      letter-spacing: -0.02em;
      opacity: 0;
      transform: translateY(30px);
      transition: opacity 0.5s ease, transform 0.5s ease, color 0.3s ease;
      display: block;
    }
    .fullnav-overlay.open .nav-item {
      opacity: 1;
      transform: translateY(0);
    }
    .fullnav-overlay.open .nav-item:nth-child(1) { transition-delay: 0.10s; }
    .fullnav-overlay.open .nav-item:nth-child(2) { transition-delay: 0.17s; }
    .fullnav-overlay.open .nav-item:nth-child(3) { transition-delay: 0.24s; }
    .fullnav-overlay.open .nav-item:nth-child(4) { transition-delay: 0.31s; }
    .fullnav-overlay.open .nav-item:nth-child(5) { transition-delay: 0.38s; }
    .fullnav-overlay .nav-item:hover { color: var(--accent, #00C4A1); }

    .fullnav-bottom {
      position: absolute;
      bottom: 40px;
      left: 8vw;
      right: 8vw;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border, rgba(255,255,255,0.06));
      padding-top: 20px;
      opacity: 0;
      transition: opacity 0.5s ease 0.4s;
    }
    .fullnav-overlay.open .fullnav-bottom { opacity: 1; }
    .fullnav-bottom .fn-theme {
      background: none; border: 1px solid var(--border, rgba(255,255,255,0.06));
      color: var(--text-muted, rgba(240,237,230,0.6)); padding: 8px 20px;
      border-radius: 40px; cursor: pointer; font-size: 0.85rem;
      font-family: 'DM Sans', sans-serif; transition: all 0.3s;
    }
    .fullnav-bottom .fn-theme:hover { background: var(--text-main, #F0EDE6); color: var(--bg, #061A24); }
    .fullnav-bottom .fn-copy { font-size: 0.8rem; color: var(--text-muted, rgba(240,237,230,0.6)); }

    /* Loader: hide entirely after animation */
    body.loaded #loader { pointer-events: none; }
    body.loaded #loader-top,
    body.loaded #loader-bottom { transition-delay: 0s; }
"""

LOADER_FIX_JS = """
      // Hide loader entirely after animation completes
      setTimeout(() => {
        const loaderEl = document.getElementById('loader');
        if (loaderEl) { loaderEl.style.visibility = 'hidden'; loaderEl.style.display = 'none'; }
      }, 1500);
"""

OVERLAY_JS_INDEX = """
    // Full-page Nav Overlay
    const burgerAll = document.querySelectorAll('.hamburger-btn');
    const overlay = document.getElementById('fullnav-overlay');
    function toggleOverlay() {
      const isOpen = overlay.classList.toggle('open');
      document.querySelectorAll('.hamburger-btn').forEach(b => b.classList.toggle('open', isOpen));
      document.body.style.overflow = isOpen ? 'hidden' : '';
    }
    burgerAll.forEach(b => b.addEventListener('click', toggleOverlay));
    // Theme toggle inside overlay
    const fnThemeBtn = document.getElementById('fn-theme-btn');
    if (fnThemeBtn) {
      fnThemeBtn.addEventListener('click', () => {
        const root = document.documentElement;
        root.getAttribute('data-theme') === 'light' ? root.removeAttribute('data-theme') : root.setAttribute('data-theme', 'light');
      });
    }
"""

# ── INDEX.HTML ──────────────────────────────────────────────────────────────────
def patch_index(content):
    # Remove stray `}` at end
    content = re.sub(r'\}\s*$', '', content.strip()) + '\n</html>\n'

    # Inject overlay CSS before closing </style> of loader block
    if 'FULL PAGE NAV OVERLAY' not in content:
        content = content.replace(
            'body.navigating>*:not(#loader) {\n      opacity: 0 !important;\n      transform: translateY(12px);\n      transition: opacity 0.4s ease, transform 0.4s ease;\n    }',
            'body.navigating>*:not(#loader) {\n      opacity: 0 !important;\n      transform: translateY(12px);\n      transition: opacity 0.4s ease, transform 0.4s ease;\n    }\n' + OVERLAY_CSS
        )

    # Replace nav + side-drawer with hamburger-only nav + fullnav overlay
    old_nav = '''  <nav>
    <a href="#" class="logo">VoidYacht</a>
    <ul class="nav-links">
      <li><a href="#how-it-works">Protocol</a></li>
      <li><a href="#fleet">Fleet</a></li>
      <li><a href="#tokenomics">Economics</a></li>
      <li><a href="simulation.html">Simulation</a></li>
      <li><a href="litepaper.html">Litepaper</a></li>
    </ul>
    <div style="display:flex; align-items:center;">
      <button class="theme-toggle" id="theme-btn-idx">Light / Dark</button>
      <button class="hamburger-btn" id="burger-btn-idx"><span></span><span></span><span></span></button>
    </div>
  </nav>

  <div class="side-drawer" id="side-drawer-idx">
    <a href="index.html">Home</a>
    <a href="#fleet">Fleet</a>
    <a href="simulation.html">Simulation</a>
    <a href="litepaper.html">Litepaper</a>
    <a href="#" id="theme-btn-mobile"
      style="margin-top:20px; font-size: 1rem; color: var(--text-muted); font-family: 'DM Sans', sans-serif;">Toggle
      Theme</a>
  </div>'''

    new_nav = '''  <nav>
    <a href="index.html" class="logo">VoidYacht</a>
    <button class="hamburger-btn" id="burger-btn-idx" aria-label="Menu"><span></span><span></span><span></span></button>
  </nav>

  <!-- Full-Page Nav Overlay -->
  <div class="fullnav-overlay" id="fullnav-overlay">
    <a href="index.html" class="nav-item">Home</a>
    <a href="simulation.html" class="nav-item">Simulation</a>
    <a href="litepaper.html" class="nav-item">Litepaper</a>
    <a href="#fleet" class="nav-item">Fleet</a>
    <a href="#tokenomics" class="nav-item">Economics</a>
    <div class="fullnav-bottom">
      <button class="fn-theme" id="fn-theme-btn">Light / Dark</button>
      <span class="fn-copy">© 2025 VoidYacht Protocol</span>
    </div>
  </div>'''

    if 'fullnav-overlay' not in content:
        content = content.replace(old_nav, new_nav)

    # Inject overlay JS after renderSteps()
    if 'Full-page Nav Overlay' not in content:
        content = content.replace(
            '    renderSteps();\n\n    // Theme & Hamburger',
            '    renderSteps();\n' + OVERLAY_JS_INDEX + '\n    // Theme & Hamburger (legacy refs removed)'
        )

    # Remove old theme/drawer JS since overlay handles it now
    old_theme_js = """    // Theme & Hamburger (legacy refs removed)
    const tBtn = document.getElementById('theme-btn-idx');
    const tBtnMob = document.getElementById('theme-btn-mobile');
    const bBtn = document.getElementById('burger-btn-idx');
    const drawer = document.getElementById('side-drawer-idx');

    function toggleTheme(e) {
      if (e) e.preventDefault();
      const root = document.documentElement;
      if (root.getAttribute('data-theme') === 'light') {
        root.removeAttribute('data-theme');
      } else {
        root.setAttribute('data-theme', 'light');
      }
    }

    tBtn.addEventListener('click', toggleTheme);
    tBtnMob.addEventListener('click', toggleTheme);

    bBtn.addEventListener('click', () => { drawer.classList.toggle('open'); });
    document.addEventListener('click', (e) => {
      if (!drawer.contains(e.target) && !bBtn.contains(e.target)) drawer.classList.remove('open');
    });"""
    # only remove if overlay JS was injected
    if 'Full-page Nav Overlay' in content and old_theme_js in content:
        content = content.replace(old_theme_js, '    // Theme handled by overlay fn-theme-btn')

    # Loader hide fix
    if 'Hide loader entirely' not in content:
        content = content.replace(
            "          document.body.classList.remove(\"loading\");\n          document.body.classList.add(\"loaded\");\n        }, 600);",
            "          document.body.classList.remove(\"loading\");\n          document.body.classList.add(\"loaded\");\n" + LOADER_FIX_JS + "        }, 600);"
        )

    return content


# ── SIMULATION.HTML ──────────────────────────────────────────────────────────────
def patch_simulation(content):
    if 'FULL PAGE NAV OVERLAY' not in content:
        content = content.replace(
            'body.navigating > *:not(#loader) { opacity: 0 !important; transform: translateY(12px); transition: opacity 0.4s ease, transform 0.4s ease; }',
            'body.navigating > *:not(#loader) { opacity: 0 !important; transform: translateY(12px); transition: opacity 0.4s ease, transform 0.4s ease; }\n' + OVERLAY_CSS
        )

    old_nav_sim = """    <!-- Navigation -->
    <nav id="navbar">
        <a href="index.html" class="logo">VoidYacht</a>
        <ul class="nav-links">
            <li><a href="index.html">Home</a></li>
            <li><a href="#fleet">Fleet</a></li>
            <li><a href="litepaper.html">Litepaper</a></li>
        </ul>
        <div style="display:flex; align-items:center; gap:20px;">
            <button class="theme-toggle" id="theme-btn">Light</button>
            <button class="hamburger-btn" id="burger-btn">
                <span></span><span></span><span></span>
            </button>
        </div>
    </nav>
    <div class="side-drawer" id="side-drawer">
        <a href="index.html">Home</a>
        <a href="simulation.html">Simulation</a>
        <a href="litepaper.html">Litepaper</a>
    </div>"""

    new_nav_sim = """    <!-- Navigation -->
    <nav id="navbar">
        <a href="index.html" class="logo">VoidYacht</a>
        <button class="hamburger-btn" id="burger-btn" aria-label="Menu"><span></span><span></span><span></span></button>
    </nav>
    <!-- Full-Page Nav Overlay -->
    <div class="fullnav-overlay" id="fullnav-overlay">
        <a href="index.html" class="nav-item">Home</a>
        <a href="simulation.html" class="nav-item">Simulation</a>
        <a href="litepaper.html" class="nav-item">Litepaper</a>
        <div class="fullnav-bottom">
            <button class="fn-theme" id="fn-theme-btn">Light / Dark</button>
            <span class="fn-copy">© 2025 VoidYacht Protocol</span>
        </div>
    </div>"""

    if 'fullnav-overlay' not in content:
        content = content.replace(old_nav_sim, new_nav_sim)

    # Replace old theme/burger JS in simulation
    old_sim_js = """        /* ──────────────────────────────────────────────────────────────────
           THEME & HAMBURGER
        ──────────────────────────────────────────────────────────────────── */
        const themeBtnSim = document.getElementById('theme-btn');
        const burgerBtnSim = document.getElementById('burger-btn');
        const sideDrawerSim = document.getElementById('side-drawer');
        
        if (themeBtnSim) {
            themeBtnSim.addEventListener('click', () => {
                const root = document.documentElement;
                if (root.getAttribute('data-theme') === 'light') {
                    root.removeAttribute('data-theme');
                    themeBtnSim.textContent = 'Light';
                } else {
                    root.setAttribute('data-theme', 'light');
                    themeBtnSim.textContent = 'Dark';
                }
            });
        }
        
        if (burgerBtnSim && sideDrawerSim) {
            burgerBtnSim.addEventListener('click', () => {
                sideDrawerSim.classList.toggle('open');
            });
            document.addEventListener('click', (e) => {
                if(!sideDrawerSim.contains(e.target) && !burgerBtnSim.contains(e.target)) {
                    sideDrawerSim.classList.remove('open');
                }
            });
        }"""

    new_sim_js = """        /* ── FULL-PAGE NAV OVERLAY ── */
        const _burgerSim = document.getElementById('burger-btn');
        const _overlaySim = document.getElementById('fullnav-overlay');
        const _fnThemeSim = document.getElementById('fn-theme-btn');
        if (_burgerSim && _overlaySim) {
            _burgerSim.addEventListener('click', () => {
                const isOpen = _overlaySim.classList.toggle('open');
                _burgerSim.classList.toggle('open', isOpen);
                document.body.style.overflow = isOpen ? 'hidden' : '';
            });
        }
        if (_fnThemeSim) {
            _fnThemeSim.addEventListener('click', () => {
                const root = document.documentElement;
                root.getAttribute('data-theme') === 'light' ? root.removeAttribute('data-theme') : root.setAttribute('data-theme', 'light');
            });
        }"""

    if 'FULL-PAGE NAV OVERLAY' not in content and old_sim_js in content:
        content = content.replace(old_sim_js, new_sim_js)

    # Loader hide fix
    if 'Hide loader entirely' not in content:
        content = content.replace(
            "                    document.body.classList.remove(\"loading\");\r\n                    document.body.classList.add(\"loaded\");\r\n                }, 600);",
            "                    document.body.classList.remove(\"loading\");\r\n                    document.body.classList.add(\"loaded\");\r\n                    // Hide loader entirely after animation\r\n                    setTimeout(() => { const el = document.getElementById('loader'); if(el){ el.style.visibility='hidden'; el.style.display='none'; } }, 900);\r\n                }, 600);"
        )

    return content


# ── LITEPAPER.HTML ──────────────────────────────────────────────────────────────
def patch_litepaper(content):
    if 'FULL PAGE NAV OVERLAY' not in content:
        content = content.replace(
            'body.navigating > *:not(#loader) { opacity: 0 !important; transform: translateY(12px); transition: opacity 0.4s ease, transform 0.4s ease; }',
            'body.navigating > *:not(#loader) { opacity: 0 !important; transform: translateY(12px); transition: opacity 0.4s ease, transform 0.4s ease; }\n' + OVERLAY_CSS
        )

    old_nav_lite = """  <nav class="top-nav">
    <a href="index.html" class="logo">VoidYacht</a>
    <div class="nav-links">
      <a href="index.html">Protocol</a>
      <a href="index.html#fleet">Fleet</a>
      <a href="simulation.html">Simulation</a>
      <a href="litepaper.html" class="active">Litepaper</a>
    </div>
    <div class="actions">
      <span class="read-time">~</span>
      <button class="theme-toggle">Light / Dark</button>
      <button class="hamburger-btn" id="burger-btn-lite"><span></span><span></span><span></span></button>
    </div>
  </nav>

  <div class="side-drawer" id="side-drawer-lite">
    <a href="index.html">Home</a>
    <a href="index.html#fleet">Fleet</a>
    <a href="simulation.html">Simulation</a>
    <a href="litepaper.html">Litepaper</a>
    <a href="#" id="theme-btn-lite-mob" style="margin-top:20px; font-size: 1rem; color: var(--text-muted); font-family: 'DM Sans', sans-serif;">Toggle Theme</a>
  </div>"""

    new_nav_lite = """  <nav class="top-nav">
    <a href="index.html" class="logo">VoidYacht</a>
    <button class="hamburger-btn" id="burger-btn-lite" aria-label="Menu"><span></span><span></span><span></span></button>
  </nav>

  <!-- Full-Page Nav Overlay -->
  <div class="fullnav-overlay" id="fullnav-overlay">
    <a href="index.html" class="nav-item">Home</a>
    <a href="simulation.html" class="nav-item">Simulation</a>
    <a href="litepaper.html" class="nav-item">Litepaper</a>
    <div class="fullnav-bottom">
      <button class="fn-theme" id="fn-theme-btn">Light / Dark</button>
      <span class="fn-copy">© 2025 VoidYacht Protocol</span>
    </div>
  </div>"""

    if 'fullnav-overlay' not in content:
        content = content.replace(old_nav_lite, new_nav_lite)

    old_lite_js = """    // ── THEME TOGGLE ──
    const themeBtn = document.querySelector('.theme-toggle');
    const themeBtnMob = document.getElementById('theme-btn-lite-mob');
    
    function toggleThemeLite(e) {
      if(e) e.preventDefault();
      const root = document.documentElement;
      if (root.getAttribute('data-theme') === 'light') root.removeAttribute('data-theme');
      else root.setAttribute('data-theme', 'light');
    }

    themeBtn.addEventListener('click', toggleThemeLite);
    themeBtnMob.addEventListener('click', toggleThemeLite);

    const bBtnLite = document.getElementById('burger-btn-lite');
    const drawerLite = document.getElementById('side-drawer-lite');
    bBtnLite.addEventListener('click', () => { drawerLite.classList.toggle('open'); });
    document.addEventListener('click', (e) => {
      if(!drawerLite.contains(e.target) && !bBtnLite.contains(e.target)) drawerLite.classList.remove('open');
    });"""

    new_lite_js = """    // ── FULLNAV OVERLAY ──
    const _burgerLite = document.getElementById('burger-btn-lite');
    const _overlayLite = document.getElementById('fullnav-overlay');
    const _fnThemeLite = document.getElementById('fn-theme-btn');
    if (_burgerLite && _overlayLite) {
      _burgerLite.addEventListener('click', () => {
        const isOpen = _overlayLite.classList.toggle('open');
        _burgerLite.classList.toggle('open', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
      });
    }
    if (_fnThemeLite) {
      _fnThemeLite.addEventListener('click', () => {
        const root = document.documentElement;
        root.getAttribute('data-theme') === 'light' ? root.removeAttribute('data-theme') : root.setAttribute('data-theme', 'light');
      });
    }"""

    if '── FULLNAV OVERLAY ──' not in content and old_lite_js in content:
        content = content.replace(old_lite_js, new_lite_js)

    # Loader hide fix
    if 'Hide loader entirely' not in content:
        content = content.replace(
            "          document.body.classList.remove(\"loading\");\n          document.body.classList.add(\"loaded\");\n        }, 600);",
            "          document.body.classList.remove(\"loading\");\n          document.body.classList.add(\"loaded\");\n          // Hide loader entirely\n          setTimeout(() => { const el = document.getElementById('loader'); if(el){ el.style.visibility='hidden'; el.style.display='none'; } }, 900);\n        }, 600);"
        )

    return content


FILES = {
    'c:/Users/Ufuk/Desktop/boat/boat/index.html': patch_index,
    'c:/Users/Ufuk/Desktop/boat/boat/simulation.html': patch_simulation,
    'c:/Users/Ufuk/Desktop/boat/boat/litepaper.html': patch_litepaper,
}

for path, patcher in FILES.items():
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = patcher(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Patched: {path}')
