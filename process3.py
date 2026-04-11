import re

def process_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    replacements = [
        ('BOAT — NavRace Protocol', 'VAOIDYACHT — Vaoid Protocol'),
        ('nav-logo">BOAT', 'nav-logo">VAOID<span>YACHT</span>'),
        ('hero-title">BOAT', 'hero-title">VAOIDYACHT'),
        ('footer-logo">BOAT', 'footer-logo">VAOIDYACHT'),
        ('NavRace', 'VaoidYacht'),
        ('NavAgent', 'VaoidAgent'),
        (r'\$NAVRCE', '$VAOID'),
        (r'\bNAVRCE\b', 'VAOID'),
        (r'BOAT #01', 'YACHT #01'),
        (r'\bboat(-color-dot)\b', r'yacht\1'),
    ]

    for old, new in replacements:
        if 'nav-logo' in old or 'hero-title' in old or 'footer-logo' in old:
            html = html.replace(old, new)
        else:
            html = re.sub(old, new, html, flags=re.IGNORECASE if 'boat' in old else 0)

    # Convert generic lowercase "boat" -> "yacht" where valid (like strings)
    # Be careful not to replace CSS classes like .boat-mode etc unless intended
    html = html.replace('boat mode', 'yacht mode')
    html = html.replace('boat-mode', 'yacht-mode')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        print("Replacement successful.")

if __name__ == "__main__":
    process_file()
