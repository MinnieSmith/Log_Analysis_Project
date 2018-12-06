#!/usr/bin/env python 2.7
import psycopg2
from datetime import date

DBNAME = "news"


def get_posts(query):
    """ Get the post from the pSQL database using the query argument. """
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        posts = c.fetchall()
        db.close()
        return posts
    except psycopg2.Error as e:
        print("Unable to connect!")
        print(e)
    except Exception as e:
        print("Unknown error occurred")
        print(e)


def popular_articles():
    query = " ".join([
        'SELECT articles.title, COUNT(*) AS views',
        'FROM articles LEFT JOIN log',
        'ON (SELECT concat(\'/article/\', articles.slug)) = log.path',
        'GROUP BY articles.title',
        'ORDER BY views DESC',
        'LIMIT 3;'
        ])
    posts = get_posts(query)
    for (title, count) in posts:
        print('"{}" - {} views'.format(title, count))


def popular_authors():
    query = " ".join([
        'SELECT authors.name, COUNT(*) AS views',
        'FROM (articles LEFT JOIN log',
        'ON (SELECT concat(\'/article/\', articles.slug)) = log.path)',
        'AS articlelog JOIN authors',
        'ON articlelog.author = authors.id',
        'GROUP BY authors.name',
        'ORDER BY views DESC',
        'LIMIT 3;'
    ])
    posts = get_posts(query)
    for (author, count) in posts:
        print('{} - {} views'.format(author, count))


def request_errors():
    query = " ".join([
        'SELECT day, percentage',
        'FROM (SELECT day, ((error_count * 100.0)/(total)) AS percentage',
        'FROM (SELECT date_trunc(\'day\', time) AS day,',
        'COUNT(CASE WHEN STATUS != \'200 OK\' THEN 1 END) AS error_count,',
        'COUNT(*) AS total',
        'FROM log GROUP BY day) AS error_table)',
        'AS error_percentage_table',
        'WHERE percentage > 1.0;',
        ])
    posts = get_posts(query)
    for (datetime, percentage) in posts:
        mydate = datetime.strftime("%B-%d, %Y")
        mypercentage = str(round(percentage, 2))
        print('{} - {} %errors'.format(mydate, mypercentage))


if __name__ == '__main__':
    print("1. What are the most popular three articles of all time?")
    popular_articles()
    print("")
    print("2. Who are the most popular article authors of all time?")
    popular_authors()
    print("")
    print("3. On which days did more than 1% of requests lead to errors?")
    request_errors()
