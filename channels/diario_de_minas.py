import requests

from bs4 import BeautifulSoup
from lxml import etree

def fetch_headline():
    r = requests.get('https://diariodeminas.com.br/')

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))

        query = """
            (//a[contains(@class, 'aft-post-image-link')])[1]
        """

        for a in dom.xpath(query):
            try:
                titulo = str(a.text).strip()

                if not titulo.strip():
                    continue

                link = str(a.attrib['href']).strip()

                noticias.append([titulo, link])
            except:
                continue

    return noticias