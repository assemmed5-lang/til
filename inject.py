content = open('data/banque_sourates.js', encoding='utf-8-sig').read()
html = open('index.html', encoding='utf-8').read()

if '<script src="data/banque_sourates.js"></script>' in html:
    print("TAG TROUVÉ - injection en cours")
    html = html.replace('<script src="data/banque_sourates.js"></script>', '<script>' + content + '</script>')
else:
    print("TAG NON TROUVÉ - vérifier index.html")

open('www/index.html', 'w', encoding='utf-8').write(html)
