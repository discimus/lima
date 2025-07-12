import requests

from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urljoin

def fetch_headline():
    baseurl = 'https://www.estadaomatogrosso.com.br/'

    r = requests.get(baseurl)

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))

        query = """
            (//a//h2//parent::a)[1]
        """

        for a in dom.xpath(query):
            try:
                link = str(a.attrib['href']).strip()

                h2 = a.find('h2')
                titulo = h2.text


                if not link or not titulo:
                    continue

                noticias.append([titulo, link])
            except:
                continue

    return noticias