import os, re

files = ['home.html', 'index.html', 'simulation.html', 'litepaper.html', 'instructions.html']

new_nav = '''        <ul class="vy-nav-links">
            <li><a href="home.html">Home</a></li>
            <li><a href="index.html">Mint</a></li>
            <li><a href="simulation.html">Simulation</a></li>
            <li><a href="litepaper.html">Litepaper</a></li>
            <li><a href="instructions.html">Instructions</a></li>
        </ul>'''

for f in files:
    if not os.path.exists(f): continue
    content = open(f, 'r', encoding='utf-8').read()
    
    # Replace anything between <ul class="vy-nav-links"> and </ul>
    content = re.sub(r'<ul class=\"vy-nav-links\">.*?</ul>', new_nav, content, flags=re.DOTALL)
    
    open(f, 'w', encoding='utf-8').write(content)
    print(f'Updated navbar in {f}')
