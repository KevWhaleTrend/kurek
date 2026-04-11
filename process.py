import re

def process_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Terminology Replacements
    html = html.replace('BOAT', 'VAOIDYACHT')
    # Use word boundary to avoid replacing inside 'VaoidYacht'
    html = re.sub(r'\bboat\b', 'yacht', html)
    html = re.sub(r'\bBoat\b', 'Yacht', html)
    html = html.replace('NavRace', 'VaoidYacht')
    html = html.replace('NavAgent', 'VaoidAgent')
    html = html.replace('$NAVRCE', '$VAOID')
    html = html.replace('NAVRCE', 'VAOID')

    # 2. SVGs for Step 02 and 03
    step2_svg = '''<div class="step-boat-header">
            <svg class="step-boat-svg" width="180" height="110" viewBox="0 0 180 110" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Checkered background effect -->
              <path d="M 20 20 L 160 20 L 160 90 L 20 90 Z" fill="url(#checkered)" opacity="0.05" />
              <!-- Wake -->
              <ellipse cx="90" cy="80" rx="60" ry="12" fill="rgba(0,196,161,0.15)" />
              <path d="M40 80 Q 20 90 0 100 Q 80 85 180 100 Q 160 90 140 80 Z" fill="rgba(126,238,221,0.1)" />
              <!-- Hull 1 -->
              <path d="M50 55 Q60 70 110 72 Q150 70 155 55 L145 45 Q125 40 105 40 Q85 40 65 45 Z" fill="#00C4A1" />
              <!-- Hull 1 Details -->
              <rect x="95" y="30" width="30" height="15" rx="4" fill="#008c73"/>
              <ellipse cx="140" cy="55" rx="5" ry="5" fill="#7EEEDD"/>
              <text x="110" y="55" font-family="DM Mono" font-size="8" fill="#FFF" font-weight="bold">#1</text>
              <!-- Flags -->
              <line x1="80" y1="40" x2="80" y2="15" stroke="white" stroke-width="2" />
              <path d="M80 15 L 100 22 L 80 30 Z" fill="#FFB347" />
              <line x1="60" y1="45" x2="60" y2="20" stroke="white" stroke-width="2" />
              <path d="M60 20 L 75 25 L 60 30 Z" fill="#FF6B35" />
              <defs>
                 <pattern id="checkered" width="10" height="10" patternUnits="userSpaceOnUse">
                   <rect x="0" y="0" width="5" height="5" fill="#FFF" />
                   <rect x="5" y="5" width="5" height="5" fill="#FFF" />
                 </pattern>
              </defs>
            </svg>
          </div>'''
    
    step3_svg = '''<div class="step-boat-header">
            <svg class="step-boat-svg" width="180" height="110" viewBox="0 0 180 110" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Glow Base -->
              <ellipse cx="90" cy="85" rx="70" ry="15" fill="rgba(123,104,238,0.15)" />
              <ellipse cx="90" cy="85" rx="40" ry="8" fill="rgba(123,104,238,0.25)" />
              <!-- Holographic Hull -->
              <path d="M30 60 Q40 75 90 77 Q140 75 150 60 L140 50 Q115 45 90 45 Q65 45 40 50 Z" stroke="#7B68EE" stroke-width="2" fill="rgba(123,104,238,0.2)" />
              <!-- Circuit Lines -->
              <path d="M90 77 L 90 90 L 110 95" stroke="#7EEEDD" stroke-width="2" fill="none" stroke-dasharray="2 2" />
              <path d="M40 60 L 20 70" stroke="#7EEEDD" stroke-width="2" fill="none" />
              <circle cx="110" cy="95" r="3" fill="#7EEEDD" />
              <circle cx="20" cy="70" r="3" fill="#7EEEDD" />
              <circle cx="90" cy="45" r="5" fill="#FFB347" opacity="0.8" />
              <!-- Radar Waves -->
              <circle cx="90" cy="35" r="10" stroke="#FFB347" stroke-width="1" fill="none" opacity="0.6"/>
              <circle cx="90" cy="35" r="20" stroke="#FFB347" stroke-width="1" fill="none" opacity="0.4"/>
              <circle cx="90" cy="35" r="30" stroke="#FFB347" stroke-width="1" fill="none" opacity="0.2"/>
              <!-- Satellite Dish -->
              <line x1="90" y1="45" x2="90" y2="35" stroke="white" stroke-width="2" />
              <path d="M80 35 Q 90 25 100 35 Z" fill="#FFF" />
              <circle cx="90" cy="35" r="2" fill="#FF6B35" />
            </svg>
          </div>'''

    html = html.replace('<div class="step-icon">🏁</div>', step2_svg)
    html = html.replace('<div class="step-icon">📡</div>', step3_svg)

    # 3. Fleet Section
    fleet_html = '''
  <!-- ════════════════════════════════════════ FLEET ═══ -->
  <section id="fleet" style="background: var(--color-bg-primary);">
    <div class="container">
      <p class="section-label reveal">// THE VAOIDYACHT FLEET</p>
      <h2 class="section-title reveal">Select Your Vessel</h2>
      <p class="section-sub reveal" style="margin-bottom:3rem;">9 distinct yachts offering varied top speeds, token earnings, and telemetry profiles. Build your ultimate racing lineup.</p>

      <div class="fleet-grid reveal">
        <!-- We will inject the boat cards here -->
'''
    boats_data = [
        ("BLACKJACK 42", "blackjack_42_1775857571041.png", "#FF3366", "42 km/h", "150"),
        ("JETSTREAM", "jetstream_888ve_1775857614168.png", "#00Bfff", "38 km/h", "130"),
        ("PURSUIT 32", "pursuit_32_1775857629922.png", "#FF8C00", "32 km/h", "110"),
        ("ROCKET V2", "rocket_v2_1775857599473.png", "#FFD700", "45 km/h", "160"),
        ("SONICWAKE", "sonicwake_v2_1775857554888.png", "#00FA9A", "36 km/h", "125"),
        ("TRAXXAS M41", "traxxas_m41.png", "#FF4500", "41 km/h", "145"),
        ("SPARTAN SR", "traxxas_spartan_sr_1775857541261.png", "#1E90FF", "39 km/h", "140"),
        ("ZELOS 36", "zelos_36_1775857647736.png", "#8A2BE2", "44 km/h", "155"),
        ("ZONDA 29", "zonda_29_1775857584871.png", "#32CD32", "29 km/h", "95")
    ]

    for name, img, color, speed, earn in boats_data:
        fleet_html += f'''
        <div class="fleet-card">
          <div class="fleet-img">
            <img src="img/{img}" alt="{name}">
          </div>
          <div class="fleet-info">
            <h3>{name}</h3>
            <div class="fleet-stats">
              <div class="stat"><span class="label">SPEED</span><span class="val" style="color: {color}">{speed}</span></div>
              <div class="stat"><span class="label">EARNING</span><span class="val" style="color: var(--color-accent-primary)">+{earn}</span></div>
            </div>
          </div>
        </div>
'''
    fleet_html += '''
      </div>
    </div>
  </section>
'''
    # Add fleet CSS into <style>
    fleet_css = '''
    /* ─── Fleet ──────────────────────────────────────────────────────────── */
    .fleet-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2rem;
    }
    .fleet-card {
      background: rgba(6, 26, 36, 0.6);
      border: 1px solid var(--color-border);
      border-radius: 16px;
      overflow: hidden;
      transition: all 0.3s ease;
      backdrop-filter: blur(8px);
    }
    .fleet-card:hover {
      transform: translateY(-5px);
      border-color: var(--color-accent-primary);
      box-shadow: 0 15px 40px rgba(0, 196, 161, 0.15);
    }
    .fleet-img {
      width: 100%;
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle at center, rgba(0,196,161,0.1), transparent 70%);
      padding: 1rem;
    }
    .fleet-img img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));
    }
    .fleet-info {
      padding: 1.5rem;
      border-top: 1px solid rgba(255,255,255,0.05);
    }
    .fleet-info h3 {
      font-size: 1.2rem;
      margin-bottom: 1rem;
      font-weight: 800;
      letter-spacing: 0.05em;
    }
    .fleet-stats {
      display: flex;
      justify-content: space-between;
    }
    .fleet-stats .stat {
      display: flex;
      flex-direction: column;
    }
    .fleet-stats .label {
      font-family: var(--font-mono);
      font-size: 0.6rem;
      color: var(--color-text-muted);
      letter-spacing: 0.1em;
      margin-bottom: 0.3rem;
    }
    .fleet-stats .val {
      font-weight: 700;
      font-size: 1rem;
    }
    '''
    html = html.replace('</style>', fleet_css + '\n  </style>')
    
    # Insert Fleet section before dashboard
    html = html.replace('<!-- ═════════════════════════════════════ LIVE DASHBOARD ═══ -->', fleet_html + '\n  <!-- ═════════════════════════════════════ LIVE DASHBOARD ═══ -->')

    # 4. Dashboard Table and JS Update
    # Replace the table rows
    tbody_start = html.find('<tbody id="race-tbody">')
    tbody_end = html.find('</tbody>', tbody_start)
    
    new_tbody = '<tbody id="race-tbody">\n'
    JS_BOATS_ARR = []
    T_VALS = [0.0, 0.11, 0.22, 0.33, 0.44, 0.55, 0.66, 0.77, 0.88]
    for i, (name, img, color, speed, earn) in enumerate(boats_data):
        rank = i + 1
        speed_val = int(speed.split(' ')[0])
        # Table Row
        if rank == 1:
            badge = '<span class="rank-badge first">🥇 #1</span>'
        else:
            badge = f'<span class="rank-badge">#{rank}</span>'
        
        row = f'''
              <tr>
                <td>{badge}</td>
                <td><span class="yacht-color-dot" style="background:{color}; width:8px; height:8px; border-radius:50%; display:inline-block; margin-right:0.5rem;"></span>{name}</td>
                <td><span id="s{rank}">{speed_val}</span> km/h</td>
                <td>1:{10 + rank * 3}.2</td>
                <td>3 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e{rank}">{earn}</span></td>
              </tr>'''
        new_tbody += row
        
        # JS boat Array entry
        # "t" spaced evenly
        s_rate = round(speed_val * 0.00001, 5)
        JS_BOATS_ARR.append(f"{{ t: {T_VALS[i]}, speed: {s_rate}, color: '{color}', name: '{name}', token: 'V-00{rank}', lap: 1 }}")
    
    new_tbody += '\n            '

    html = html[:tbody_start] + new_tbody + html[tbody_end:]

    # Replacing the speeds Array and earnings Array in JS
    speeds_arr_repl = "const speeds = [\n" + ",\n".join([f"      document.getElementById('s{i+1}')" for i in range(9)]) + "\n    ];"
    earnings_arr_repl = "const earnings = [\n" + ",\n".join([f"      document.getElementById('e{i+1}')" for i in range(9)]) + "\n    ];"
    
    baseEarnings = ", ".join([earn for _, _, _, _, earn in boats_data])
    baseSpeeds = ", ".join([speed.split(' ')[0] for _, _, _, speed, _ in boats_data])
    
    # We will search with regex
    import re
    html = re.sub(r'const speeds = \[.*?\];', speeds_arr_repl, html, flags=re.DOTALL)
    html = re.sub(r'const earnings = \[.*?\];', earnings_arr_repl, html, flags=re.DOTALL)
    html = re.sub(r'const baseEarnings = \[.*?\];', f'const baseEarnings = [{baseEarnings}];', html)
    html = re.sub(r'const baseSpeeds = \[.*?\];', f'const baseSpeeds = [{baseSpeeds}];', html)

    # Replacing JS boats array
    js_boats_str = "const boats = [\n      " + ",\n      ".join(JS_BOATS_ARR) + "\n    ];"
    html = re.sub(r'const boats = \[.*?\];', js_boats_str, html, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

process_file()
