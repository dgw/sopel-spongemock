# coding=utf8
"""sopel-spongemock - Sopel "Mocking SpongeBob" Plugin

Copyright 2020-2022 dgw, technobabbl.es
"""
from __future__ import print_function, division, unicode_literals, absolute_import

import random
import re
import unicodedata

from sopel import module, tools


def setup(bot):
    if 'mock_lines' not in bot.memory:
        bot.memory['mock_lines'] = tools.SopelMemory()


def shutdown(bot):
    try:
        del bot.memory['mock_lines']
    except KeyError:
        pass


@module.echo
@module.rule('(.*)')
@module.priority('low')
@module.require_chanmsg
@module.unblockable
def cache_lines(bot, trigger):
    if trigger.sender not in bot.memory['mock_lines']:
        bot.memory['mock_lines'][trigger.sender] = tools.SopelMemory()

    line = trigger.group()
    # don't store /me commands, or obvious bot commands
    if not line.startswith('\x01ACTION') and not re.match(bot.config.core.prefix, line):
        bot.memory['mock_lines'][trigger.sender][trigger.nick] = line


@module.echo
@module.event('PART')
@module.priority('low')
@module.unblockable
def part_prune(bot, trigger):
    if trigger.nick == bot.nick:
        # We left; clean up everything cached for that channel.
        bot.memory['mock_lines'].pop(trigger.sender, None)
    else:
        # Someone else left; remove their cache entry.
        bot.memory['mock_lines'].get(trigger.sender, {}).pop(trigger.nick, None)


@module.echo
@module.event('QUIT')
@module.priority('low')
@module.unblockable
def quit_prune(bot, trigger):
    for channel in bot.memory['mock_lines'].keys():
        bot.memory['mock_lines'][channel].pop(trigger.nick, None)


@module.echo
@module.event('KICK')
@module.priority('low')
@module.unblockable
def kick_prune(bot, trigger):
    if trigger.nick == bot.nick:
        # We were kicked; clean up everything cached for that channel.
        bot.memory['mock_lines'].pop(trigger.sender, None)
    else:
        # Some other poor sod (or spammer) got kicked; remove their cache entry.
        bot.memory['mock_lines'].get(trigger.sender, {}).pop(trigger.nick, None)


def get_cached_line(bot, channel, nick):
    channel = tools.Identifier(channel)
    nick = tools.Identifier(nick)
    line = bot.memory['mock_lines'].get(channel, {}).get(nick, '')
    if line:
        return '<{}> {}'.format(nick, line)


@module.commands('spongemock', 'smock')
@module.example('.spongemock Fortnite is the best game ever!')
def spongemock(bot, trigger):
    """Make sPonGeMoCk text from the input (or the last thing a user said)."""
    if not trigger.group(2):
        bot.reply('I need text, or a nickname!')
        return module.NOLIMIT

    if trigger.group(3) and not trigger.group(4):
        line = get_cached_line(bot, trigger.sender, trigger.group(3))
    else:
        line = None

    if line:
        # last thing someone else said
        nick, sep, text = line.partition(' ')
        bot.say(sep.join([nick, mock_case(text)]))
    else:
        # use given text
        bot.say(mock_case(trigger.group(2)))


def mock_case(text):
    text = text.strip()

    out = text[0].lower()
    lower = True
    repeat = 1

    for char in text[1:]:
        lo = char.lower()
        up = char.upper()

        if unicodedata.category(char) == 'Zs' or lo == up:
            # whitespace shouldn't affect the case-repeat counting
            # nor should characters whose case cannot be transformed
            out += char
            continue

        if repeat == 2:
            repeat = 1
            lower = not lower
            out += lo if lower else up
        else:
            which = random.choice([True, False])
            if which:
                out += lo
            else:
                out += up
            if lower == which:
                repeat += 1
            else:
                repeat = 1
                lower = which

    return out
