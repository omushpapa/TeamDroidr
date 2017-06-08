#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import telepot
import argparse
import urllib
from time import sleep
from telepot.loop import MessageLoop
from bs4 import BeautifulSoup
from pprint import pformat
from datetime import datetime

# Django configuration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from data.models import Article, Lookup

token = os.environ['TELEGRAM_TOKEN']

TelegramBot = telepot.Bot(token)

encode = lambda text: text.encode('utf-8')


class CustomAction(argparse.Action):

    def _display_help(self, parser):
        help = parser.format_help()
        help_message = ''.join(help.split(':')[2:])
        return 'Need help? Here\'s some.\n' + help_message

    def _display_intro(self, parser):
        help = self._display_help(parser)
        return 'Hi,\n\nI am TeamDroidr. I was created in the likeness of TeamDroid. \n\nAt TeamDroid, we love to empower Android users.\n\n' + help

    def _display_networks(self):
        social = {
            'Facebook': 'web.facebook.com/groups/TeamDroid001/',
            'Twitter': 'twitter.com/TeamDroidComm',
            'Website': 'teamdroidcommunity.com',
            'Forums': 'forum.teamdroidcommunity.com'
        }

        networks = '\n\n'.join(['{}: {}'.format(i, social[i])
                                for i in social.keys()])
        return 'Community:\n\n' + networks

    def _display_history(self):
        text = 'History:\n\nTeamDroid.\n\nFounded by Arnold Garry Galiwango.\n\nTeamDroidCommunity.com'
        return text

    def _check_recent(self):
        link = 'http://teamdroidcommunity.com/home/'
        page = urllib.urlopen(link).read()

        lookup = Lookup.objects.filter(id=1).update(last=datetime.now())

        soup = BeautifulSoup(page, 'html.parser')
        divs = soup.find_all('div', 'w-blog-post-body')
        for item in divs:
            article = item.find('a', 'entry-title')
            try:
                article_link = article.get('href')
            except AttributeError:
                article_link = ''

            title = article.text
            date = item.find('time').text
            timestamp = datetime.strptime(date, "%B %d, %Y")
            author = item.find('span', 'author').text
            obj, created = Article.objects.get_or_create(link=article_link,
                                                         title=title, date=timestamp, author=author)

    def _get_highlights(self):
        try:
            obj = Lookup.objects.get(id=1)
        except Lookup.DoesNotExist:
            self._check_recent()
        else:
            article_date = obj.last.strftime('%s')
            current_date = datetime.now().strftime('%s')
            time_diff = int(current_date) - int(article_date)
            if time_diff > 6 * 60 * 60:     # Check for update every 6 hours
                print 'Checking for latest'
                self._check_recent()
        finally:
            articles = Article.objects.order_by('-date')[:10]

            if articles:
                highlights = ''
                for count, article in enumerate(articles, 1):
                    highlights += '{0}. \t{1}\n\t{2} - {3}\n\t{4}\n\n'.format(
                        count, encode(article.title), article.date.strftime(
                            '%B %d, %Y'),
                        encode(article.author), encode(article.link))
                return highlights
            else:
                return 'No highlights for today.'


class StartAction(CustomAction):

    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            values = self._display_intro(parser=parser)
        setattr(namespace, self.dest, values)


class HelpAction(CustomAction):

    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            values = self._display_help(parser=parser)
        setattr(namespace, self.dest, values)


class HighlightAction(CustomAction):

    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            values = self._get_highlights()
        setattr(namespace, self.dest, values)


class CommunityAction(CustomAction):

    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            values = self._display_networks()
        setattr(namespace, self.dest, values)


class HistoryAction(CustomAction):

    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            values = self._display_history()
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser(prefix_chars='/', add_help=False)
group = parser.add_argument_group('group')
group.add_argument('/start', '/start@TeamDroidbot',
                   help='Show intro', nargs=0, action=StartAction)
group.add_argument('/help', '/help@TeamDroidbot',
                   help='Show this help menu', nargs=0, action=HelpAction)
group.add_argument('/highlights', '/highlights@TeamDroidbot',
                   help='Show highlights from teamdroidcommunity.com', nargs=0,
                   action=HighlightAction)
group.add_argument('/community', '/community@TeamDroidbot', help='Show a list of TeamDroid social groups',
                   nargs=0, action=CommunityAction)
group.add_argument('/history', '/history@TeamDroidbot',
                   help='Show a description of TeamDroid\'s historical growth', nargs=0, action=HistoryAction)


def _welcome_user(**kwargs):
    intro = ''.join(parser.format_help().split(':')[2:])
    first_name = kwargs.get('first_name')
    message = 'Welcome {} to TeamDroid. \n\nHere are some commands to get you started.\n\n{}'.format(
        first_name.title(), intro)
    return message


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        cmd = encode(msg.get('text'))

        arg_list = cmd.split()
        parsed = parser.parse_known_args(arg_list)
        try:
            options = vars(parsed[0])
        except TypeError:
            print 'command not recognised'
        else:
            if options['start']:
                TelegramBot.sendMessage(chat_id, options.get('start'))
            elif options['help']:
                TelegramBot.sendMessage(chat_id, options.get('help'))
            elif options['highlights']:
                TelegramBot.sendMessage(chat_id, options.get('highlights'))
            elif options['community']:
                TelegramBot.sendMessage(chat_id, options.get('community'))
            elif options['history']:
                TelegramBot.sendMessage(chat_id, options.get('history'))
            else:
                # Escape telepot.exceptions.TelegramError
                pass

    if content_type == 'new_chat_member':
        new_members = msg.get('new_chat_members')
        for member in new_members:
            TelegramBot.sendMessage(
                chat_id, _welcome_user(**member))


MessageLoop(TelegramBot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
try:
    while True:
        sleep(10)
except KeyboardInterrupt:
    print
    sys.exit(0)
