with open('index.html', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 682-705 (0-indexed: 681-704) contain the old connectors and cards 2+3
# Replace them with new boat SVG cards
new_cards = '''        <!-- BOAT CARD 02 - Teal hull -->
        <div class="step-card reveal">
          <div class="step-boat-header">
            <svg class="step-boat-svg" width="180" height="110" viewBox="0 0 180 110" fill="none" xmlns="http://www.w3.org/2000/svg">
              <ellipse cx="90" cy="88" rx="72" ry="14" fill="rgba(0,196,161,0.08)"/>
              <ellipse cx="90" cy="91" rx="52" ry="9" fill="rgba(0,196,161,0.06)"/>
              <ellipse cx="92" cy="82" rx="58" ry="10" fill="rgba(0,0,0,0.35)"/>
              <path d="M20 62 Q28 82 90 84 Q152 82 160 62 L148 50 Q120 44 90 44 Q60 44 32 50 Z" fill="#00C4A1"/>
              <path d="M40 55 Q90 50 140 55 Q120 48 90 47 Q60 47 40 55Z" fill="rgba(255,255,255,0.18)"/>
              <path d="M24 65 Q90 68 156 65" stroke="rgba(255,255,255,0.2)" stroke-width="2" fill="none"/>
              <rect x="68" y="32" width="44" height="22" rx="6" fill="#008f76"/>
              <rect x="72" y="35" width="16" height="10" rx="2" fill="rgba(255,255,255,0.15)"/>
              <rect x="92" y="35" width="16" height="10" rx="2" fill="rgba(255,255,255,0.12)"/>
              <line x1="90" y1="32" x2="90" y2="10" stroke="#00C4A1" stroke-width="1.5"/>
              <circle cx="90" cy="9" r="3" fill="#00C4A1"/>
              <circle cx="90" cy="9" r="5" fill="rgba(0,196,161,0.3)">
                <animate attributeName="r" values="5;9;5" dur="2.2s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.4;0;0.4" dur="2.2s" repeatCount="indefinite"/>
              </circle>
              <circle cx="90" cy="64" r="10" fill="rgba(0,0,0,0.4)"/>
              <text x="90" y="68" text-anchor="middle" font-family="DM Mono, monospace" font-size="9" fill="white" font-weight="700">02</text>
            </svg>
          </div>
          <div class="step-num">STEP 02</div>
          <div class="step-title">Race &amp; Earn</div>
          <p class="step-desc">Your NavAgent competes in real-time pond races. Finish positions unlock $NAVRCE token rewards and leaderboard XP.</p>
        </div>

        <!-- BOAT CARD 03 - Amber hull -->
        <div class="step-card reveal">
          <div class="step-boat-header">
            <svg class="step-boat-svg" width="180" height="110" viewBox="0 0 180 110" fill="none" xmlns="http://www.w3.org/2000/svg">
              <ellipse cx="90" cy="88" rx="72" ry="14" fill="rgba(0,196,161,0.08)"/>
              <ellipse cx="90" cy="91" rx="52" ry="9" fill="rgba(0,196,161,0.06)"/>
              <ellipse cx="92" cy="82" rx="58" ry="10" fill="rgba(0,0,0,0.35)"/>
              <path d="M20 62 Q28 82 90 84 Q152 82 160 62 L148 50 Q120 44 90 44 Q60 44 32 50 Z" fill="#FFB347"/>
              <path d="M40 55 Q90 50 140 55 Q120 48 90 47 Q60 47 40 55Z" fill="rgba(255,255,255,0.18)"/>
              <path d="M24 65 Q90 68 156 65" stroke="rgba(255,255,255,0.2)" stroke-width="2" fill="none"/>
              <rect x="68" y="32" width="44" height="22" rx="6" fill="#c88020"/>
              <rect x="72" y="35" width="16" height="10" rx="2" fill="rgba(255,255,255,0.15)"/>
              <rect x="92" y="35" width="16" height="10" rx="2" fill="rgba(255,255,255,0.12)"/>
              <line x1="90" y1="32" x2="90" y2="10" stroke="#FFB347" stroke-width="1.5"/>
              <circle cx="90" cy="9" r="3" fill="#FFB347"/>
              <circle cx="90" cy="9" r="5" fill="rgba(255,179,71,0.3)">
                <animate attributeName="r" values="5;9;5" dur="2.6s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.4;0;0.4" dur="2.6s" repeatCount="indefinite"/>
              </circle>
              <circle cx="90" cy="64" r="10" fill="rgba(0,0,0,0.4)"/>
              <text x="90" y="68" text-anchor="middle" font-family="DM Mono, monospace" font-size="9" fill="white" font-weight="700">03</text>
            </svg>
          </div>
          <div class="step-num">STEP 03</div>
          <div class="step-title">Data Marketplace</div>
          <p class="step-desc">Every race generates telemetry data. Sell your boat\'s performance logs on the NavRace data marketplace for passive income.</p>
        </div>
'''

# Replace lines 682-705 (1-indexed) = indices 681-704 (0-indexed)
new_lines = lines[:681] + [new_cards] + lines[705:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Done. Total lines: {len(new_lines)}")
print("Lines 681-686 now:")
for l in new_lines[681:686]:
    print(repr(l[:80]))
