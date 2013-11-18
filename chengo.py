#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Chengo! The Chen Bingo Card Generator
=====================================

**Chengo!** is a variation of bingo. Words and phrases come from the wonderful Dr. Sixiong Chen during his multivariate calculus, linear algebra, and differential equations courses.

The idea is to complete a full row, column, or diagonal within a period with Dr. Chen.

Python 2.7, Jinja2
"""

from __future__ import with_statement
import argparse
import codecs
from collections import namedtuple
from itertools import chain, islice, izip_longest, repeat
from random import randrange, sample
import sys
import cgi

from jinja2 import Environment

Field = namedtuple('Field', ['type', 'value'])

FIELD_EMPTY = Field('empty', None)
FIELD_BONUS = Field('bonus', None)

TEMPLATE = """\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
    <style>
      @media print {
        html,
        body {
          margin: 0;
        }
      }

      h1 {
        font-size: 6mm;
      }

      table {
        border-color: #666666;
        border-spacing: 0;
        border-style: solid;
        border-width: 0 0.25mm 0.25mm 0;
        margin-bottom: 1cm;
      }
      td {
        border-color: #666666;
        border-style: solid;
        border-width: 0.25mm 0 0 0.25mm;
        font-size: 4mm;
        height: 2cm;
        text-align: center;
        width: 3cm;
      }
      td strong {
        font-size: 120%;
        text-transform: uppercase;
      }
    </style>
    <title>Bullshit Bingo</title>
  </head>
  <body>
    {%- for table in tables %}

    <h1>Chengo!</h1>
    <table cellspacing="0">
      {%- for row in table %}
      <tr>
        {%- for field in row %}
        <td>
          {%- if field.type == 'normal' -%}
            {{ field.value }}
          {%- elif field.type == 'bonus' -%}
            <strong>Bingo!</strong>
          {%- elif field.type == 'empty' -%}
            -
          {%- endif -%}
        </td>
        {%- endfor %}
      </tr>
      {%- endfor %}
    </table>
    {%- endfor %}

  </body>
</html>"""

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('words_file',
        metavar='<words file>')

    parser.add_argument('-b', '--bonus-field',
        dest='include_bonus_field',
        action='store_true',
        default=False,
        help='add one bonus field per card')

    parser.add_argument('-c', '--num-cards',
        dest='num_cards',
        type=int,
        default=1,
        help='number of cards to create (default: 1)')

    parser.add_argument('-s', '--card-size',
        dest='card_size',
        type=int,
        default=5,
        help='number of rows and columns per card (default: 5)')

    return parser.parse_args()

def load_words(chen.txt):
    """Load words from a file.

    Every line is to be considered as one word.
    """
    with codecs.open(filename, 'rb', 'utf-8') as f:
        for line in f:
            # Only yield non-empty, non-whitespace lines.
            line = line.strip()
            if line:
                yield line

def build_table(values, size, include_bonus_field=False):
    """Build a 2-dimensional table of the given size with unique, random
    values.

    If the table has more fields than values are available, the remaining
    fields will be empty.
    """
    field_total = size ** 2
    random_values = collect_random_sublist(values, field_total)
    fields = to_fields(random_values, field_total)

    if include_bonus_field:
        # Replace a field at a random position with a bonus field.
        fields[randrange(0, field_total)] = FIELD_BONUS

    # Group into rows.
    return izip_longest(*[iter(fields)] * size)

def collect_random_sublist(values, n):
    """Return unique, random elements from the values.

    Return `n` values or, if `n` is greater than the number of values, all
    values.
    """
    # The sample length must not exceed the number of available values.
    sample_length = min(n, len(values))
    return sample(values, sample_length)

def to_fields(values, n):
    """Create fields from the values, append infinite empty fields, and return
    the first `n` items.
    """
    normal_fields = (Field('normal', value) for value in values)
    fields = chain(normal_fields, repeat(FIELD_EMPTY))
    return take(fields, n)

def take(iterable, n):
    "Return the first `n` items of the iterable as a list."
    return list(islice(iterable, n))

def render_html(tables):
    """Assemble an HTML page with cards from the word tables."""
    env = Environment(autoescape=True)
    template = env.from_string(TEMPLATE)
    return template.render(tables=tables)

if __name__ == '__main__':
    args = parse_args()

    # Load words from given file.
    words = frozenset(load_words(args.words_file))

    # Create tables of words.
    tables = [list(build_table(words, args.card_size, args.include_bonus_field))
        for _ in xrange(args.num_cards)]

    # Write HTML output to stdout.  To create a file, redirect the data by
    # appending something like ``> cards.html`` at the command line.
    html = render_html(tables).encode('utf-8')
    sys.stdout.write(html)
