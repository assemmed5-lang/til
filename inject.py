content = open('data/banque_sourates.js', encoding='utf-8-sig').read()
html = open('index.html', encoding='utf-8').read()
html = html.replace('<script src="data/banque_sourates.js"></script>', '<script>' + content + '</script>')
open('www/index.html', 'w', encoding='utf-8').write(html)
