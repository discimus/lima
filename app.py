from channels import (
    g1, 
    poder360, 
    uol, 
    infomoney,
    diario_de_minas,
    otempo
)

from datetime import datetime, timedelta
from sqlescapy import sqlescape

import argparse
import json
import logging
import os
import sqlite3

logging.basicConfig(
    filename='erros.log',
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def fetch(channel, channel_name):
    try:
        return channel.fetch()
    except Exception as e:
        logging.error(F"{channel_name} error", exc_info=True)
        return []

def fetch_headline(channel, channel_name):
    try:
        return channel.fetch_headline()
    except Exception as e:
        logging.error(F"{channel_name} error", exc_info=True)
        return []
    
def persist_articles_in_sqlite(articles, path, offset_plus=0, offset_minus=0):
    try:
        if not os.path.exists(path):
            with open(path, 'w'): pass
        
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()

            query = f"""
                create table if not exists tb_article(
                    article_id integer PRIMARY key,
                    article_title varchar(500),
                    article_link varchar(500),
                    article_channel varchar(255),
                    article_content text,
                    article_published_at text,
                    article_created_at text);
            """

            cursor.execute(query)
            conn.commit()

            now = datetime.now() + timedelta(hours=offset_plus) - timedelta(hours=offset_minus)
            current_date = now.strftime('%Y-%m-%d %H:%M:%S')

            for [title, link] in articles:
                parsed_title = sqlescape(title)
                parsed_link = sqlescape(link)

                query = f"""
                    insert into tb_article(
                        article_title,
                        article_link,
                        article_channel,
                        article_content,
                        article_published_at,
                        article_created_at)
                    select 
                        '{parsed_title}',
                        '{parsed_link}',
                        '',
                        '',
                        '{current_date}',
                        '{current_date}'
                    where not exists (
                        select 1
                            from tb_article
                                where article_link = '{parsed_link}' or article_title = '{parsed_title}');
                """

                cursor.execute(query)

            conn.commit()
    except:
        logging.error(F"SQLite error", exc_info=True)

def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--g1', required=False, action='store_true', help='News channel G1')
    parser.add_argument('--poder360', required=False, action='store_true', help='News channel Poder 360')
    parser.add_argument('--uol', required=False, action='store_true', help='News channel UOL')
    parser.add_argument('--infomoney', required=False, action='store_true', help='News channel Info Money')

    parser.add_argument('--g1-headline', required=False, action='store_true', help='Headline from channel G1')
    parser.add_argument('--uol-headline', required=False, action='store_true', help='Headline from channel Uol')
    parser.add_argument('--diariodeminas-headline', required=False, action='store_true', help='Headline from channel Diário de Minas')
    parser.add_argument('--otempo-headline', required=False, action='store_true', help='Headline from channel O Tempo')

    parser.add_argument('--output-json', required=False, action='store_true', help='Output format as JSON')
    parser.add_argument('--sqlite-path', required=False, type=str, help='Path to persist articles in SQLite file')

    parser.add_argument('--offset-plus', required=False, type=int, help='Offset GMT/UTC +')
    parser.add_argument('--offset-minus', required=False, type=int, help='Offset GMT/UTC -')

    args = parser.parse_args()

    articles = []

    #   FETCH ARTICLES
    if args.g1:
        articles += fetch(channel=g1, channel_name='G1')
    if args.poder360:
        articles += fetch(channel=poder360, channel_name='Poder 360')
    if args.uol:
        articles += fetch(channel=uol, channel_name='UOL')
    if args.infomoney:
        articles += fetch(channel=infomoney, channel_name='Info Money')
        
    if args.g1_headline:
        articles += fetch_headline(channel=g1, channel_name='G1')
    if args.uol_headline:
        articles += fetch_headline(channel=uol, channel_name='Uol')
    if args.diariodeminas_headline:
        articles += fetch_headline(channel=diario_de_minas, channel_name='Diário de Minas')
        articles += fetch_headline(channel=uol, channel_name='Uol')
    if args.otempo_headline:
        articles += fetch_headline(channel=otempo, channel_name='O Tempo')

    #   OUTPUT AS JSON
    if args.output_json:
        print(json.dumps(articles))

    offsetplus = args.offset_plus if args.offset_plus else 0
    offsetminus = args.offset_minus if args.offset_minus else 0

    #   PERSIST IN SQLITE FILE
    if args.sqlite_path and str(args.sqlite_path).strip():
        persist_articles_in_sqlite(
            articles=articles, 
            path=args.sqlite_path,
            offset_plus=offsetplus,
            offset_minus=offsetminus)
    else:
        logging.error(F"SQLite error: invalid path", exc_info=True)

if __name__ == '__main__':
    main()