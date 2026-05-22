from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = s.replace('Purpose not', 'Useful when')
s = s.replace('contact. may be useful', 'Contact may be useful')
p.write_text(s, encoding='utf-8')
