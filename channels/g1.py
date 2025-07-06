import requests

from bs4 import BeautifulSoup
from lxml import etree

def fetch():
    r = requests.get('https://g1.globo.com/')

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))

        for a in soup.select('a[class*="gui-color-primary"]'):
            try:
                if not a.text:
                    continue

                titulo = str(a.text).strip()

                if not titulo:
                    continue
                
                href = a.attrs['href']

                if not href:
                    continue

                link = str(href).strip()

                noticias.append([titulo, link])
            except:
                continue

    return noticias