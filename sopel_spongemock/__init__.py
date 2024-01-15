# coding=utf8
"""sopel-spongemock - Sopel "Mocking SpongeBob" Plugin

Copyright 2020-2022 dgw, technobabbl.es
"""
from __future__ import print_function, division, unicode_literals, absolute_import

import re

from sopel import plugin, tools
from sopel.config import types

try:
    from spongemock.spongemock import mock as mock_case
except ImportError:
    from .util import mock_case


class SpongeMockSection(types.StaticSection):
    diversity_bias = types.ValidatedAttribute(
        'diversity_bias',
        parse=float,
        default=0.6,
    )
    """Set output diversity bias when using the external mocker ('lib' extra)."""

    always_start_lower = types.BooleanAttribute(
        'always_start_lower',
        default=False,
    )
    """Always start mocked text with a lowercase letter.

    Has no effect if using the built-in mocker, which always starts lowercase.
    """


def setup(bot):
    bot.config.define_section('spongemock', SpongeMockSection)

    if 'mock_lines' not in bot.memory:
        if hasattr(bot, 'make_identifier'):
            # sopel 8+
            new_mem = tools.SopelIdentifierMemory(identifier_factory=bot.make_identifier)
        else:
            # sopel 7
            new_mem = tools.SopelIdentifierMemory()
        bot.memory['mock_lines'] = new_mem


def shutdown(bot):
    try:
        del bot.memory['mock_lines']
    except KeyError:
        pass


@plugin.echo
@plugin.rule('(.*)')
@plugin.priority('low')
@plugin.require_chanmsg
@plugin.unblockable
def cache_lines(bot, trigger):
    if trigger.sender not in bot.memory['mock_lines']:
        if hasattr(bot, 'make_identifier'):
            # sopel 8+
            new_mem = tools.SopelIdentifierMemory(identifier_factory=bot.make_identifier)
        else:
            # sopel 7
            new_mem = tools.SopelIdentifierMemory()
        bot.memory['mock_lines'][trigger.sender] = new_mem

    line = trigger.group()
    # don't store /me commands, or obvious bot commands
    if not line.startswith('\x01ACTION') and not re.match(bot.config.core.prefix, line):
        bot.memory['mock_lines'][trigger.sender][trigger.nick] = line


@plugin.echo
@plugin.event('PART')
@plugin.priority('low')
@plugin.unblockable
def part_prune(bot, trigger):
    if trigger.nick == bot.nick:
        # We left; clean up everything cached for that channel.
        bot.memory['mock_lines'].pop(trigger.sender, None)
    else:
        # Someone else left; remove their cache entry.
        bot.memory['mock_lines'].get(trigger.sender, {}).pop(trigger.nick, None)


@plugin.echo
@plugin.event('QUIT', 'NICK')
@plugin.priority('low')
@plugin.unblockable
def quit_prune(bot, trigger):
    # NICK is treated like the old nick QUITting for simplicity
    for channel in bot.memory['mock_lines'].keys():
        bot.memory['mock_lines'][channel].pop(trigger.nick, None)


@plugin.echo
@plugin.event('KICK')
@plugin.priority('low')
@plugin.unblockable
def kick_prune(bot, trigger):
    if trigger.nick == bot.nick:
        # We were kicked; clean up everything cached for that channel.
        bot.memory['mock_lines'].pop(trigger.sender, None)
    else:
        # Some other poor sod (or spammer) got kicked; remove their cache entry.
        bot.memory['mock_lines'].get(trigger.sender, {}).pop(trigger.nick, None)


def get_cached_line(bot, channel, nick):
    if hasattr(bot, 'make_identifier'):
        # sopel 8+
        channel = bot.make_identifier(channel)
        nick = bot.make_identifier(nick)
    else:
        # sopel 7
        channel = tools.Identifier(channel)
        nick = tools.Identifier(nick)

    try:
        nick = bot.users[nick].nick
    except (KeyError, AttributeError):
        # just keep what we already have; it's better than nothing
        pass

    line = bot.memory['mock_lines'].get(channel, {}).get(nick, '')
    if line:
        return '<{}> {}'.format(nick, line)


@plugin.commands('spongemock', 'smock')
@plugin.example('.spongemock Fortnite is the best game ever!')
def spongemock(bot, trigger):
    """Make sPonGeMoCk text from the input (or the last thing a user said)."""
    if not trigger.group(2):
        bot.reply('I need text, or a nickname!')
        return plugin.NOLIMIT

    if trigger.group(3) and not trigger.group(4):
        line = get_cached_line(bot, trigger.sender, trigger.group(3))
    else:
        line = None

    nick = sep = None
    text = trigger.group(2)
    if line:
        # last thing someone else said
        nick, sep, text = line.partition(' ')

    text = mock_case(text, diversity_bias=bot.config.spongemock.diversity_bias)
    if bot.config.spongemock.always_start_lower:
        for c in text:
            if c.islower():
                break
            elif c.isupper():
                text = text.swapcase()
                break

    if nick is not None:
        text = sep.join((nick, text))

    bot.say(text)
