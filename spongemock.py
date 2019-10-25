# coding=utf8
"""
spongemock.py - Sopel "Mocking SpongeBob" Plugin

Copyright 2019 dgw, technobabbl.es
"""
from __future__ import print_function, division, unicode_literals, absolute_import

import random

from sopel import module


@module.commands('spongemock')
def spongemock(bot, trigger):
    if not trigger.group(2):
        bot.reply('I need text!')
        return module.NOLIMIT

    bot.say(mock_case(trigger.group(2)))


def mock_case(text):
    uppers = text.upper()
    lowers = text.lower()

    out = lowers[0]
    lower = True
    repeat = 1

    for i in range(1, len(text)):
        if text[i] == ' ':
            # spaces shouldn't affect the case-repeat counting
            out += text[i]
            continue
        if repeat == 2:
            repeat = 1
            lower = not lower
            out += lowers[i] if lower else uppers[i]
        else:
            which = random.choice([True, False])
            if which:
                out += lowers[i]
            else:
                out += uppers[i]
            if lower == which:
                repeat += 1
            else:
                repeat = 1
                lower = which

    return out
