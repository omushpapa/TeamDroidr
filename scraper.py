#! /usr/bin/env python2.7

import os
import urllib
from bs4 import BeautifulSoup
from pprint import pformat
from datetime import datetime

encode = lambda text: text.encode('utf-8')


def get_highlights(arguments=None):
    link = 'http://teamdroidcommunity.com/home/'
    page = urllib.urlopen(link).read()
    soup = BeautifulSoup(page, 'html.parser')
    divs = soup.find_all('div', 'w-blog-post-body')
    highlights_list = []
    links_list = []
    for i in divs:
        article = i.find('a', 'entry-title')
        try:
            article_link = article.get('href')
        except AttributeError:
            article_link = ''

        if article_link not in links_list:
            links_list.append(article_link)
            title = article.text
            date = i.find('time').text
            timestamp = datetime.strptime(date, "%B %d, %Y").strftime("%s")
            author = i.find('span', 'author').text

            highlights_list.append((timestamp, encode(title), encode(
                date), encode(author), encode(article_link)))

    if highlights_list:
        highlights = 'Highlights:\n'
        for count, i in enumerate(sorted(highlights_list, reverse=True)[:10], 1):
            highlights += '{0}. \t{1}\n\t{2} - {3}\n\t{4}\n\n'.format(count, i[1], i[
                                                                      2], i[3], i[4])

        return highlights
    else:
        return 'No highlights for today.'
