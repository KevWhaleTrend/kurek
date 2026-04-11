import re

def main():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        # Step 1: Replace names
        html = html.replace('BOAT — NavRace Protocol', 'VAOIDYACHT — Vaoid Protocol')
        html = html.replace('nav-logo">BOAT', 'nav-logo">VAOID<span>YACHT</span>')
        html = html.replace('hero-title">BOAT', 'hero-title">VAOIDYACHT')
        html = html.replace('footer-logo">BOAT', 'footer-logo">VAOIDYACHT')
        html = re.sub(r'\bboat\b', 'yacht', html)
        html = re.sub(r'\bBoat\b', 'Yacht', html)
        html = html.replace('NavRace', 'VaoidYacht')
        html = html.replace('NavAgent', 'VaoidAgent')
        html = html.replace('$NAVRCE', '$VAOID')
        html = html.replace('NAVRCE', 'VAOID')

        # Replace SVG placeholders
        print("Replacing SVGs...")
        step2_svg = '''<div class="step-yacht-header" style="height:130px; display:flex; align-items:center; justify-content:center;">
            <svg class="step-yacht-svg" width="180" height="110" viewBox="0 0 180 110" fill="none" xmlns="http://www.w3.org/2000/svg">
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
        
        step3_svg = '''<div class="step-yacht-header" style="height:130px; display:flex; align-items:center; justify-content:center;">
            <svg class="step-yacht-svg" width="180" height="110" viewBox="0 0 180 110" fill="none" xmlns="http://www.w3.org/2000/svg">
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

        print("Building Fleet Section...")
        fleet_data = [
            ("Traxxas Spartan SR", "traxxas_spartan_sr_1775857541261.png", "Deep-V", "Injection-molded ABS", "Velineon 540XL", "VXL-6s Marine", "50+ mph", "36.5\u0022 \u00d7 9.5\u0022"),
            ("Pro Boat Sonicwake V2", "sonicwake_v2_1775857554888.png", "Deep-V", "High-impact ABS", "Spektrum 1900Kv", "Spektrum Smart 160A", "50+ mph", "36\u0022 \u00d7 10.75\u0022"),
            ("Pro Boat Blackjack 42\u0022", "blackjack_42_1775857571041.png", "Catamaran", "Fiberglass", "Spektrum 4985 1350Kv", "Spektrum Smart 160A", "55+ mph", "42\u0022 \u00d7 15\u0022"),
            ("TFL Zonda 29\u0022", "zonda_29_1775857584871.png", "Catamaran", "Hand-laid Fiberglass", "2\u00d7 2900Kv", "2\u00d7 120A", "55+ mph", "29\u0022 \u00d7 8.2\u0022"),
            ("Joysway Rocket V2", "rocket_v2_1775857599473.png", "Deep-V", "Fiberglass", "3660 Brushless", "60A Water-cooled", "50+ mph", "24.4\u0022 \u00d7 6.1\u0022"),
            ("Kyosho Jet Stream", "jetstream_888ve_1775857614168.png", "Deep-V", "FRP", "Orion Outrunner", "80A Water-cooled", "50 mph", "35.4\u0022 \u00d7 7.3\u0022"),
            ("TFL Pursuit 32\u0022", "pursuit_32_1775857629922.png", "Deep-V", "Hand-laid Fiberglass", "3660 1620Kv", "120A", "55+ mph", "32.2\u0022 \u00d7 9.4\u0022"),
            ("Pro Boat Zelos 36\u0022 Twin", "zelos_36_1775857647736.png", "Catamaran", "Fiberglass", "2\u00d7 2000Kv", "2\u00d7 120A", "60+ mph", "36\u0022 \u00d7 11.7\u0022"),
            ("Traxxas M41 Widebody", "traxxas_m41.png", "Catamaran", "Vacuum-molded ABS", "Velineon 540XL", "VXL-6s Marine", "50+ mph", "40.5\u0022 \u00d7 10.5\u0022"),
        ]

        # Check if Fleet section already exists, if so replace it, else push before Live Dashboard
        fleet_section_idx_start = html.find('<!-- ════════════════════════════════════════ FLEET')
        fleet_section_idx_end = html.find('<!-- ═════════════════════════════════════ LIVE DASHBOARD')
        
        fleet_html = '<!-- ════════════════════════════════════════ FLEET ═══ -->\\n<section id="fleet">\\n<div class="container">\\n'
        fleet_html += '<p class="section-label reveal">// THE VAOIDYACHT FLEET</p>\\n<h2 class="section-title reveal">Model Comparison</h2>\\n'
        fleet_html += '<div class="fleet-grid reveal" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem;">\\n'
        
        for name, img, t, hull, motor, esc, speed, dim in fleet_data:
            fleet_html += f"""
            <div class="fleet-card" style="background: rgba(6,26,36,0.8); border: 1px solid var(--color-border); border-radius: 12px; overflow: hidden;">
              <div style="height:200px; padding:20px; display:flex; align-items:center; justify-content:center; background: radial-gradient(circle at center, rgba(0,196,161,0.1), transparent); border-bottom: 1px solid rgba(255,255,255,0.05);">
                <img src="img/{img}" style="max-width:100%; max-height:100%; object-fit:contain; filter:drop-shadow(0 10px 15px rgba(0,0,0,0.5));" alt="{name}">
              </div>
              <div style="padding: 20px;">
                <h3 style="font-size:1.15rem; font-weight:800; color:#fff; margin-bottom:15px;">{name}</h3>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:0.8rem; font-family:var(--font-mono); color:var(--color-text-secondary);">
                  <div><span style="color:var(--color-text-muted);display:block;font-size:0.65rem;">TYPE</span>{t}</div>
                  <div><span style="color:var(--color-text-muted);display:block;font-size:0.65rem;">SPEED</span>{speed}</div>
                  <div><span style="color:var(--color-text-muted);display:block;font-size:0.65rem;">HULL</span>{hull}</div>
                  <div><span style="color:var(--color-text-muted);display:block;font-size:0.65rem;">DIMENSIONS</span>{dim}</div>
                  <div><span style="color:var(--color-text-muted);display:block;font-size:0.65rem;">MOTOR</span>{motor}</div>
                  <div><span style="color:var(--color-text-muted);display:block;font-size:0.65rem;">ESC</span>{esc}</div>
                </div>
              </div>
            </div>"""

        fleet_html += '</div></div></section>\\n\\n'

        if fleet_section_idx_start != -1 and fleet_section_idx_end != -1:
            html = html[:fleet_section_idx_start] + fleet_html + html[fleet_section_idx_end:]
        else:
            if '<!-- ═════════════════════════════════════ LIVE DASHBOARD ═══ -->' in html:
                html = html.replace('<!-- ═════════════════════════════════════ LIVE DASHBOARD ═══ -->', fleet_html + '<!-- ═════════════════════════════════════ LIVE DASHBOARD ═══ -->')
            else:
                print("DASHBOARD COMMENT NOT FOUND!")

        print("Replacing Dashboard Table (from 4 to 9 boats)")
        
        table_html = """
              <tr>
                <td><span class="rank-badge first">🥇 #1</span></td>
                <td><span class="yacht-color-dot" style="background:#FF6B35"></span>STORM-RED</td>
                <td><span id="s1">39</span> km/h</td>
                <td>1:24.3</td>
                <td>3 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e1">147</span></td>
              </tr>
              <tr>
                <td><span class="rank-badge">#2</span></td>
                <td><span class="yacht-color-dot" style="background:#00C4A1"></span>WAVE-TEAL</td>
                <td><span id="s2">34</span> km/h</td>
                <td>1:27.1</td>
                <td>3 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e2">122</span></td>
              </tr>
              <tr>
                <td><span class="rank-badge">#3</span></td>
                <td><span class="yacht-color-dot" style="background:#FFB347"></span>GOLD-RUSH</td>
                <td><span id="s3">32</span> km/h</td>
                <td>1:29.8</td>
                <td>2 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e3">99</span></td>
              </tr>
              <tr>
                <td><span class="rank-badge">#4</span></td>
                <td><span class="yacht-color-dot" style="background:#7B68EE"></span>DEPTH-BLUE</td>
                <td><span id="s4">31</span> km/h</td>
                <td>1:33.2</td>
                <td>2 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e4">75</span></td>
              </tr>
              <tr>
                <td><span class="rank-badge">#5</span></td>
                <td><span class="yacht-color-dot" style="background:#00FA9A"></span>NEON-FLASH</td>
                <td><span id="s5">30</span> km/h</td>
                <td>1:35.4</td>
                <td>2 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e5">55</span></td>
              </tr>
              <tr>
                <td><span class="rank-badge">#6</span></td>
                <td><span class="yacht-color-dot" style="background:#FFD700"></span>ROCKET-STAR</td>
                <td><span id="s6">28</span> km/h</td>
                <td>1:40.1</td>
                <td>1 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e6">42</span></td>
              </tr>
              <tr>
                <td><span class="rank-badge">#7</span></td>
                <td><span class="yacht-color-dot" style="background:#FF4500"></span>BLAZE-X</td>
                <td><span id="s7">27</span> km/h</td>
                <td>1:43.6</td>
                <td>1 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e7">30</span></td>
              </tr>
              <tr>
                <td><span class="rank-badge">#8</span></td>
                <td><span class="yacht-color-dot" style="background:#1E90FF"></span>AQUA-ZERO</td>
                <td><span id="s8">25</span> km/h</td>
                <td>1:48.8</td>
                <td>1 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e8">15</span></td>
              </tr>
              <tr>
                <td><span class="rank-badge">#9</span></td>
                <td><span class="yacht-color-dot" style="background:#8A2BE2"></span>PURPLE-HAZE</td>
                <td><span id="s9">24</span> km/h</td>
                <td>1:52.2</td>
                <td>1 / 5</td>
                <td style="color:var(--color-cta-amber)">+<span id="e9">8</span></td>
              </tr>"""

        # Replace tbody content
        start_tbody = html.find('<tbody id="race-tbody">')
        end_tbody = html.find('</tbody>', start_tbody)
        if start_tbody != -1 and end_tbody != -1:
            html = html[:start_tbody + len('<tbody id="race-tbody">')] + '\\n' + table_html + '\\n            ' + html[end_tbody:]
        else:
            print("TBODY NOT FOUND")

        # Update JavaScript objects for the 9 bots
        print("Updating JS boats arrays...")
        boats_arr_str = """const boats = [
      { t: 0.0, speed: 0.00042, color: '#FF6B35', name: 'STORM-RED', token: 'VAOID-01', lap: 3 },
      { t: 0.11, speed: 0.00038, color: '#00C4A1', name: 'WAVE-TEAL', token: 'VAOID-02', lap: 3 },
      { t: 0.22, speed: 0.00034, color: '#FFB347', name: 'GOLD-RUSH', token: 'VAOID-03', lap: 2 },
      { t: 0.33, speed: 0.00031, color: '#7B68EE', name: 'DEPTH-BLUE', token: 'VAOID-04', lap: 2 },
      { t: 0.44, speed: 0.00029, color: '#00FA9A', name: 'NEON-FLASH', token: 'VAOID-05', lap: 2 },
      { t: 0.55, speed: 0.00027, color: '#FFD700', name: 'ROCKET-STAR', token: 'VAOID-06', lap: 1 },
      { t: 0.66, speed: 0.00025, color: '#FF4500', name: 'BLAZE-X', token: 'VAOID-07', lap: 1 },
      { t: 0.77, speed: 0.00023, color: '#1E90FF', name: 'AQUA-ZERO', token: 'VAOID-08', lap: 1 },
      { t: 0.88, speed: 0.00021, color: '#8A2BE2', name: 'PURPLE-HAZE', token: 'VAOID-09', lap: 1 },
    ];"""

        html = re.sub(r'const boats\s*=\s*\[.*?\];', boats_arr_str, html, flags=re.DOTALL)

        speeds_arr_str = """const speeds = [
      document.getElementById('s1'), document.getElementById('s2'),
      document.getElementById('s3'), document.getElementById('s4'),
      document.getElementById('s5'), document.getElementById('s6'),
      document.getElementById('s7'), document.getElementById('s8'),
      document.getElementById('s9')
    ];"""
        html = re.sub(r'const speeds\s*=\s*\[.*?\];', speeds_arr_str, html, flags=re.DOTALL)

        earnings_arr_str = """const earnings = [
      document.getElementById('e1'), document.getElementById('e2'),
      document.getElementById('e3'), document.getElementById('e4'),
      document.getElementById('e5'), document.getElementById('e6'),
      document.getElementById('e7'), document.getElementById('e8'),
      document.getElementById('e9'),
    ];"""
        html = re.sub(r'const earnings\s*=\s*\[.*?\];', earnings_arr_str, html, flags=re.DOTALL)

        baseEarnings_str = "const baseEarnings = [147, 122, 99, 75, 55, 42, 30, 15, 8];"
        html = re.sub(r'const baseEarnings\s*=\s*\[.*?\];', baseEarnings_str, html)

        baseSpeeds_str = "const baseSpeeds = [39, 34, 32, 31, 30, 28, 27, 25, 24];"
        html = re.sub(r'const baseSpeeds\s*=\s*\[.*?\];', baseSpeeds_str, html)

        # Write output back
        # The formatting string \\n needs literal interpretation so we use raw or interpret it correctly before writing.
        # since it's a python file writing it we don't have to worry about replacing \n
        html = html.replace('\\n', '\n')

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Success! Write complete.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
