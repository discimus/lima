import requests
import re

from bs4 import BeautifulSoup
from lxml import etree

def fetch():
    r = requests.get('https://www.infomoney.com.br/')

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))

        for a in soup.select('a'):
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

                pattern = re.compile('https:\/\/www.infomoney.com.br\/(?!tudo\-sobre)(?!blog)(?!ferramentas)(?!authentication)[a-zA-Z0-9\-]*\/*[a-zA-Z0-9\-]*\/([a-zA-Z0-9]+[\-]+)+[a-zA-Z0-9]+\/[a-zA-Z0-9\-]*')

                if (pattern.match(link)):
                    noticias.append([titulo, link])

            except:
                continue

    return noticias