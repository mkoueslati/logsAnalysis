# Database code for the DB Forum.
#
# This is still NOT the full solution!

import psycopg2
import bleach
import datetime
DBNAME = "forum"


def most_popular_articles():
    """1. What are the most popular three articles of all time?"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select title, count(log.id) as views_number
                from
                articles, log
                where log.path like CONCAT('%',articles.slug,'%')
                group by title
                order by views_number DESC
                LIMIT 3;""")
    result = c.fetchall()
    return result
    db.close()


def most_popular_authors_articles():
    """2. Who are the most popular article authors of all time?"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select name, count(log.id) as views_number
                from
                authors, articles, log
                where log.path like CONCAT('%',articles.slug,'%')
                and authors.id = articles.author
                group by name
                order by views_number desc;""")
    result = c.fetchall()
    return result
    db.close()


def errors_more_than_1_per_cent_by_day():
    """3. On which days did more than 1% of requests lead to errors?"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select requests.date,
                err.http_errors * 100 / requests.http_requests::float
                from
                (select date_trunc('day', time) as date,
                count(*) as http_requests from log group by date) as requests,
                (select date_trunc('day', time) as date,
                count(*) as http_errors from log
                where status like'4%' or status like'5%' group by date) as err
                where requests.date = err.date
                and err.http_errors * 100 / requests.http_requests::float > 1
                order by requests.date desc;""")
    result = c.fetchall()
    return result
    db.close()


if __name__ == '__main__':
  popular_articles = most_popular_articles()
  popular_authors = most_popular_authors_articles()
  errors = errors_more_than_1_per_cent_by_day()
  for p_art in popular_articles:
    print ("{} --- {} views".format(p_art[0] , p_art[1]))
  for p_auth in popular_authors:
    print ("{} --- {} views".format(p_auth[0] , p_auth[1]))
  for p_err in errors:
    print ("{} --- {} views".format(p_err[0] , p_err[1]))


def to_short_date(date):
    d = str(date).split(' ', 1)[0]
    short_date = datetime.datetime.strptime(d,
                                            '%Y-%m-%d').strftime('%b %d, %Y')
    return short_date
