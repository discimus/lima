import requests
import re

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

def fetch_headline():
    r = requests.get('https://g1.globo.com/')
    
    noticias = []

    if (r.ok):
        try:
            content1 = re.search('"items":(\[.*\])', r.content.decode())
            content2 = re.search('"children".*?"content":(\{.*?\}{2})', content1.group(0))
            content3 = re.search('"url":\"(.*?)\"', content2.group(0))
            content4 = re.search('"title":\"(.*?)\"', content2.group(0))
            
            url = content3.group(1)
            title = content4.group(1)
            
            if url and title:
                noticias.append([title, url])
            
        except:
            return noticias

    return noticias