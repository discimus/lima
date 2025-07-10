import requests

from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urljoin

def fetch_headline():
    baseurl = 'https://www.otempo.com.br'

    r = requests.get(baseurl)

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))

        query = """
            (//a[contains(concat(' ', normalize-space(@class), ' '), 'list__link')])[1]
        """

        for a in dom.xpath(query):
            try:
                path = str(a.attrib['href']).strip()
                titulo = str(a.attrib['title']).strip()

                link = urljoin(baseurl, path)

                if not link or not titulo:
                    continue

                noticias.append([titulo, link])
            except:
                continue

    return noticias