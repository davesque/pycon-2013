#!/usr/bin/env python
import itertools
import sys
from collections import defaultdict
from pyparsing import CharsNotIn, Group, Optional, Word, ZeroOrMore, alphanums

word = Word(alphanums)
space = CharsNotIn(alphanums)
doc = ZeroOrMore(Group(word + Optional(space)))


def find_anagram_groups(content):
    content = content.lower()

    sys.stderr.write('Parsing words...\n')
    parsed = doc.parseString(content)
    words = set(p[0] for p in parsed if not len(p[0]) < 4)

    sys.stderr.write('Getting word combinations...\n')
    combinations = itertools.combinations(words, 2)

    sys.stderr.write('Grouping combinations by anagram (this might take a while)...\n')
    anagrams = defaultdict(list)
    for c in combinations:
        key = ''.join(sorted(c[0] + c[1]))
        ana_words = tuple(itertools.chain(*anagrams[key]))
        if c[0] not in ana_words and c[1] not in ana_words:
            anagrams[key].append(c)

    sys.stderr.write('Sorting anagram groups by length...\n')
    groups = sorted(anagrams.values(), key=lambda g: -len(g))
    if groups:
        max_length = len(groups[0])
        max_length_groups = itertools.takewhile(lambda g: len(g) == max_length, groups)
        return max_length_groups
    else:
        return []

if __name__ == '__main__':
    content = sys.stdin.read()
    groups = find_anagram_groups(content)
    for g in groups:
        sys.stdout.write(', '.join(' '.join(p) for p in g) + '\n')
