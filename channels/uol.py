import requests

from bs4 import BeautifulSoup
from lxml import etree

def fetch():
    r = requests.get('https://www.uol.com.br/')

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))

        query = """
            //article
        """

        for el in dom.xpath(query):
            try:
                anchors = el.xpath('.//a[@href]')
                el_titulos = el.xpath('.//*[contains(@class, \'title__element\')]')

                if not anchors or not el_titulos:
                    continue

                anchor = anchors[0]
                el_titulo = el_titulos[0]

                if (not el_titulo.text):
                    continue

                titulo = str(el_titulo.text).strip()

                link = str(anchor.get('href')).strip()
                    
                if not titulo or not link:
                    continue

                noticias.append([titulo, link])
            except:
                continue

        query = """
            //aside//ul//li
        """

        for el in dom.xpath(query):
            try:
                anchors = el.xpath('.//a[@href]')
                el_titulos = el.xpath('.//*[contains(@class, \'title__element\')]')

                if not anchors or not el_titulos:
                    continue

                anchor = anchors[0]
                el_titulo = el_titulos[0]

                if (not el_titulo.text):
                    continue

                titulo = str(el_titulo.text).strip()

                link = str(anchor.get('href')).strip()
                    
                if not titulo or not link:
                    continue

                noticias.append([titulo, link])
            except:
                continue

    return noticias