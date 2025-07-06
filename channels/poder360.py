import requests

from bs4 import BeautifulSoup
from lxml import etree

def fetch():
    r = requests.get('https://www.poder360.com.br')

    noticias = []

    if (r.ok):
        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))

        query = """
            //*[
                contains(concat(' ', normalize-space(@class), ' '), 'box-news-list')
                    or contains(concat(' ', normalize-space(@class), ' '), 'box-queue')]
            //a[
                not(ancestor::*[
                    contains(@class, 'box-news-list__tag') 
                        or contains(@class, 'box-news-list__author')
                            or contains(@class, 'box-news-list__title')
                                or contains(@class, 'box-queue__category') 
                                    or contains(@class, 'box-title__title')]) 
            ]"""

        for a in dom.xpath(query):
            try:
                titulo = str(a.text).strip()

                if not titulo.strip():
                    continue

                link = str(a.attrib['href']).strip()

                noticias.append([titulo, link])
            except:
                continue

    r = requests.get('https://www.poder360.com.br/poder-economia/')

    if r.ok:
        query = """
            //*[
                contains(concat(' ', normalize-space(@class), ' '), 'box-news-list')
                    or contains(concat(' ', normalize-space(@class), ' '), 'box-queue')
                        or contains(concat(' ', normalize-space(@class), ' '), 'box-highlight__list')]
            //a[
                not(ancestor::*[
                    contains(@class, 'box-news-list__tag') 
                        or contains(@class, 'box-news-list__author')
                            or contains(@class, 'box-news-list__title')
                                or contains(@class, 'box-queue__category') 
                                    or contains(@class, 'box-title__title')]) 
            ]"""

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