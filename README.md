Para instalação das dependências utilizar
```
pip install -r requirements.txt
```

A aplicação funciona como linha de comando, basta executar

```
python3 app.py <canal> <output desejado>
```

Informando os parâmetros desejados.

Para canais utilizar

| Parâmetro           | Canal                 | Link                  |
| -------------       | -------------         | -------               |
| --g1                | G1                    | https://g1.globo.com/ |
| --poder360          | Poder 360 (Economia)  | https://www.poder360.com.br/poder-economia/ |
| --uol               | UOL                   | https://www.uol.com.br/ |
| --infomoney         | Info Money            | https://www.infomoney.com.br/ |

Para output utilizar

| Parämetro     | Valor esperado              | Efeito
| --             | --                         | --
| --output-json  | Nenhum                     | Imprimte os resultados em um array json
| --sqlite-path  | Caminho do arquivo SQLite  | Persiste os valores encontrados no arquivo sqlite indicado

Exemplos:
```
python app.py --infomoney --output-json
```
```
python app.py --g1 --uol --poder360 --infomoney --sqlite-path="out.db"
```

O arquivo SQLite possui uma tabela

```
tb_article
```

Que possui a seguinte estrutura:

```
create table if not exists tb_article(
    article_id integer PRIMARY key,
    article_title varchar(500),
    article_link varchar(500),
    article_channel varchar(255),
    article_content text,
    article_published_at text,
    article_created_at text);
```

Nenhum erro é impresso no terminal, todos os erros sao logados no arquivo

```
erros.log
```
