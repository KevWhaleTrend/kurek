import re, os

files = ['simulation.html']
tag = '<script src="shared.js"></script>'

for fname in files:
    path = os.path.join(os.path.dirname(__file__), fname)
    content = open(path, 'r', encoding='utf-8').read()
    if 'shared.js' not in content:
        content = content.replace('</body>', f'\n    {tag}\n</body>', 1)
        open(path, 'w', encoding='utf-8').write(content)
        print(f'Updated {fname}')
    else:
        print(f'Already has shared.js: {fname}')
