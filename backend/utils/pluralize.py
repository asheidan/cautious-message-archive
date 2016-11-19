"""Pluralize English nouns (stage 6)

This program is part of "Dive Into Python", a free Python book for
experienced programmers.  Visit http://diveintopython.org/ for the
latest version.

Command line usage:
$ python pluralize.py noun
nouns
"""

import re

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision: 1.7 $"
__date__ = "$Date: 2004/05/03 19:40:42 $"
__copyright__ = "Copyright (c) 2004 Mark Pilgrim"
__license__ = "Python"

LANGUAGES = {
    "en": [
        ("^(sheep|deer|fish|moose|aircraft|series|haiku)$", "($)", r"\1"),
        ("[ml]ouse$", "ouse$", "ice"),
        ("child$", "$", "ren"),
        ("booth$", "$", "s"),
        ("foot$", "oot$", "eet"),
        ("ooth$", "ooth$", "eeth"),
        ("l[eo]af$", "af$", "aves"),
        ("sis$", "sis$", "ses"),
        ("^(hu|ro)man$", "$", "s"),
        ("man$", "man$", "men"),
        ("^lowlife$", "$", "s"),
        ("ife$", "ife$", "ives"),
        ("eau$", "$", "x"),
        ("^[dp]elf$", "$", "s"),
        ("lf$", "lf$", "lves"),
        ("[sxz]$", "$", "es"),
        ("[^aeioudgkprt]h$", "$", "es"),
        ("(qu|[^aeiou])y$", "y$", "ies"),
        ("$", "$", "s"),
    ],
}


def create_rule(pattern, search, replace):
    def rule(word):
        return (re.search(pattern, word) and
                re.sub(search, replace, word))

    return rule


def rules(language):
    for line in LANGUAGES.get(language):
        pattern, search, replace = line
        yield create_rule(pattern, search, replace)


def pluralize(noun, language='en'):
    """returns the plural form of a noun"""
    for rule in rules(language):
        result = rule(noun)
        if result:
            return result
