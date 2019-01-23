#!/usr/bin/env python2
from flask import Flask, request, redirect, url_for, Response
from logsAnalysisDB import *
from string import Template
import sys
import datetime

app = Flask(__name__)
# HTML template for the page
HT = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Reporting tool</title>
  </head>
  <body>
    <h1>Reporting tool ($action)</h1>
    <ul>
    %s
    </ul>
  </body>
</html>
'''
# HTML template for an individual item
IT = '''\
   <li>"%s" ----- %s views</li>
'''
ERR = '''\
  <li> {} - {} errors </li>
  '''


@app.route('/articles', methods=['GET'])
def get_popular_articles():
    posts = "".join(IT % (t, v) for t, v in most_popular_articles())
    HT2 = Template(HT).safe_substitute(action="Popular articles!")
    html = HT2 % posts
    return html


@app.route('/authors', methods=['GET'])
def get_most_popular_authors():
    posts = "".join(IT % (au, v) for au, v in most_popular_authors_articles())
    HT2 = Template(HT).safe_substitute(action="Popular authors!")
    html = HT2 % posts
    return html


@app.route('/errors', methods=['GET'])
def get_errors():
    posts = "".join(ERR.format(to_short_date(d), str(round(e, 2))+"%")
                    for d, e in errors_more_than_1_per_cent_by_day())
    HT2 = Template(HT).safe_substitute(action="Errors!")
    html = HT2 % posts
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
