import os

def extract_css(html_file, css_name):
    if not os.path.exists(html_file): return
    content = open(html_file, 'r', encoding='utf-8').read()
    s = content.find('<style>')
    if s == -1: return
    e = content.find('</style>', s)
    if e == -1: return
    
    css_content = content[s+7:e].strip()
    # Add a header to the CSS file
    css_header = f'/* {css_name} */\n\n'
    open(css_name, 'w', encoding='utf-8').write(css_header + css_content)
    
    new_content = content[:s] + f'<link rel=\"stylesheet\" href=\"{css_name}\" />' + content[e+8:]
    open(html_file, 'w', encoding='utf-8').write(new_content)
    print(f'Extracted {css_name}')

def extract_all():
    extract_css('index.html', 'index.css')
    extract_css('simulation.html', 'simulation.css')
    extract_css('litepaper.html', 'litepaper.css')
    extract_css('instructions.html', 'instructions.css')

if __name__ == '__main__':
    extract_all()
