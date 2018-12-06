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
    query = "select articles.title, count(*) as views from articles left join log on " \
            "(select concat('/article/', articles.slug)) = log.path " \
            "group by articles.title order by views desc limit 3;"
    posts = get_posts(query)
    for (title, count) in posts:
        print('"{}" - {} views'.format(title, count))


def popular_authors():
    query = "select authors.name, count(*) as views " \
            "from (articles left join log on (select concat('/article/', articles.slug)) = log.path) " \
            "as articlelog join authors on articlelog.author = authors.id " \
            "group by authors.name order by views desc limit 3;"
    posts = get_posts(query)
    for i in range(len(posts)):
        author = posts[i][0]
        views = str(posts[i][1])
        print('{} - {} views'.format(author, views))


def request_errors():
    query = "select day, percentage from (select day, ((error_count * 100.0)/(total)) as percentage" \
            " from (select date_trunc('day', time) as day, " \
            "count(CASE WHEN STATUS != '200 OK' THEN 1 END) as error_count, count(*) as total from log " \
            "group by day) as error_table) as error_percentage_table where percentage > 1.0;"
    posts = get_posts(query)
    for i in range(len(posts)):
        datetime = posts[i][0]
        mydate = datetime.strftime("%B-%d, %Y")
        percentage = str(round(posts[i][1], 2))
        print('{} - {} %errors'.format(mydate, percentage))


if __name__ == '__main__':
    print("1. What are the most popular three articles of all time?")
    popular_articles()
    print("")
    print("2. Who are the most popular article authors of all time?")
    popular_authors()
    print("")
    print("3. On which days did more than 1% of requests lead to errors?")
    request_errors()
