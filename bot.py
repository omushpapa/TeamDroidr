#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import time
import telepot
import json
from telepot.loop import MessageLoop
from pprint import pformat
from scraper import get_highlights
from collections import OrderedDict

token = os.environ['TELEGRAM_TOKEN']

TelegramBot = telepot.Bot(token)


def _display_help(*args):
    comand_list = ''.join(
        ['{} - {}\n'.format(i, COMMANDS[i]['description']) for i in COMMANDS.keys()])
    return 'Command me: \n' + comand_list + '\nteamdroidcommunity.com'


def _display_intro(*args):
    help = _display_help()
    return 'I am TeamDroidr. I was created in the likeness of TeamDroid. \n\nAt TeamDroid, we love to empower Android users.\n\n' + help


def _display_networks(*args):
    social = {
        'facebook': 'web.facebook.com/groups/TeamDroid001/',
        'twitter': 'twitter.com/TeamDroidComm',
        'website': 'teamdroidcommunity.com'
    }

    networks = '\n\n'.join(['{}: {}'.format(i, social[i])
                            for i in social.keys()])
    return networks


def _display_history(*args):
    text = 'TeamDroid.\n\nFounded by Arnold Garry Galiwango.\n\nTeamDroidCommunity.com'
    return text


def _welcome_user(*args):
    try:
        first_name = args[0]
    except IndexError:
        first_name = 'user'
    message = 'Welcome {} to TeamDroid. \n\n{}'.format(
        first_name.title(), _display_intro())
    return message


COMMANDS = OrderedDict([
    ('/start', {'call': _display_intro, 'description': 'Show intro'}),
    ('/help', {'call': _display_help, 'description': 'Show help menu'}),
    ('/highlights', {'call': get_highlights,
                     'description': 'Show highlights from teamdroidcommunity.com'}),
    ('/community', {'call': _display_networks,
                    'description': 'Show a list of TeamDroid social platforms'}),
    ('/history', {'call': _display_history,
                  'description': 'A description of TeamDroid\'s historical growth'}),
])


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    clean = lambda command, bot_name='@TeamDroidbot': command.replace(
        bot_name, '')

    if content_type == 'text':
        cmd = msg.get('text')
        command = clean(cmd.split()[0])
        arguments = cmd.split()[1:]
        func = COMMANDS.get(command.lower())
        if func:
            TelegramBot.sendMessage(chat_id, func['call'](arguments))
        else:
            TelegramBot.sendMessage(chat_id, 'Sorry, I do not understand you!')

    if content_type == 'new_chat_member':
        new_members = msg.get('new_chat_members')
        for member in new_members:
            TelegramBot.sendMessage(
                chat_id, _welcome_user(member['first_name']))


MessageLoop(TelegramBot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print
    sys.exit(0)
