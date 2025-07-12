import requests

from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urljoin

def fetch_headline():
    baseurl = 'https://amazonas1.com.br/'

    r = requests.get(baseurl)

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))

        query = """
            (//div[contains(concat(' ', normalize-space(@class), ' '), 'destaque-layout-01')]//a)[1]
        """

        for a in dom.xpath(query):
            try:
                div = a.find('div')
                h2 = div.find('h2')

                titulo = str(h2.text).strip()
                link = str(a.attrib['href']).strip()

                if not link or not titulo:
                    continue

                noticias.append([titulo, link])
            except:
                continue

    return noticias