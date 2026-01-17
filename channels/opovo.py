import requests

from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urljoin

def fetch_headline():
    baseurl = 'https://www.opovo.com.br/'

    r = requests.get(baseurl)

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding="utf-8")
        dom = etree.HTML(str(soup))

        query = """
            (//p[contains(concat(' ', normalize-space(@class), ' '), 'matter-emphasis')]//parent::a)[1]
        """

        for a in dom.xpath(query):
            try:
                p = a.find('p')

                titulo = str(p.text).strip()
                link = str(a.attrib['href']).strip()

                if not link or not titulo:
                    continue

                noticias.append([titulo, link])
            except:
                continue

    return noticias