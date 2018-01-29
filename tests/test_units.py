from __future__ import unicode_literals

import pytest

from context import units as u
from context import exceptions as e
from helpers import generate_params


# Fixtures, factories, and test data

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
NUMERALS = '0123456789'
SYMBOLS = '`~!@#$%^&*()-_=+\\|[]{}:;"\',<.>/?'

UNITS_DATA = {
    u.Alphabetic: {
        'markers': ['simple', 'Alphabetic'],
        'valid': [ALPHABET],
        'invalid': ['', '1', 'A1', 'A A', 'A-A'],
        'sort': [
            ({'sort_case': ''}, 'A', 'B'),
            ({'sort_case': ''}, 'B', 'a'),
            ({'sort_case': 'upper'}, 'A', 'B'),
            ({'sort_case': 'upper'}, 'a', 'B'),
            ({'sort_case': 'lower'}, 'a', 'B'),
        ],
        'sort_equivalence': [
            ({'sort_case': ''}, 'a', 'a', True),
            ({'sort_case': ''}, 'a', 'A', False),
            ({'sort_case': 'upper'}, 'A', 'A', True),
            ({'sort_case': 'upper'}, 'a', 'A', True),
            ({'sort_case': 'upper'}, 'a', 'B', False),
            ({'sort_case': 'lower'}, 'A', 'A', True),
            ({'sort_case': 'lower'}, 'a', 'A', True),
            ({'sort_case': 'lower'}, 'a', 'B', False),
        ],
        'search': [
            ({'search_case': ''}, 'a', 'a'),
            ({'search_case': ''}, 'A', 'A'),
            ({'search_case': 'upper'}, 'A', 'A'),
            ({'search_case': 'upper'}, 'a', 'A'),
            ({'search_case': 'lower'}, 'A', 'a'),
            ({'search_case': 'lower'}, 'a', 'a'),
        ],
        'display': [
            ({'display_case': 'upper'}, 'aA', 'AA'),
            ({'display_case': 'lower'}, 'aA', 'aa'),
            ({'display_case': ''}, 'aA', 'aA')
        ],
    },
    u.Numeric: {
        'markers': ['simple', 'Numeric'],
        'valid': [NUMERALS],
        'invalid': [ALPHABET, SYMBOLS],
        'sort': [
            ({}, '1', '2'),
            ({}, '2', '10'),
        ],
        'sort_equivalence': [
        ],
        'search': [
            ({}, '0', '0'),
        ],
        'display': [
            ({}, '0', '0'),
        ],
    },
    u.Formatting: {
        'markers': ['simple', 'Formatting'],
        'valid': [SYMBOLS, '  '],
        'invalid': ['', 'A', '1', 'A1-', 'A1 '],
        'sort': [
            ({'use_formatting_in_sort': True}, ' ', '-'),
        ],
        'sort_equivalence': [
            ({'use_formatting_in_sort': True}, ' ', '-', False),
            ({'use_formatting_in_sort': False}, ' ', '-', True),
        ],
        'search': [
            ({'use_formatting_in_search': True}, '-', '-'),
            ({'use_formatting_in_search': False}, '-', '')
        ],
        'display': [
            ({}, ' ', ' '),
            ({}, SYMBOLS, SYMBOLS)
        ],
    },
    u.AlphaNumeric: {
        'markers': ['compound', 'AlphaNumeric'],
        'valid': ['a', '1', 'a1', 'a1a', 'a1a1'],
        'invalid': ['', ' ', 'a 1'],
        'sort': [
            ({'sort_case': ''}, 'A1', 'B1'),
            ({'sort_case': ''}, 'B1', 'a1'),
            ({'sort_case': ''}, 'A1', 'A2'),
            ({'sort_case': 'lower'}, 'A1', 'b1'),
            ({'sort_case': 'upper'}, 'A1', 'b1'),
            ({}, 'A2', 'A10'),
        ],
        'sort_equivalence': [
            ({'sort_case': ''}, 'a1', 'A1', False),
            ({'sort_case': 'lower'}, 'a1', 'A1', True),
            ({'sort_case': 'upper'}, 'a1', 'A1', True),
            ({}, 'a1', 'A01', True),
        ],
        'search': [
            ({'search_case': ''}, 'a1', 'a1'),
            ({'search_case': ''}, 'A1', 'A1'),
            ({'search_case': 'upper'}, 'A1', 'A1'),
            ({'search_case': 'upper'}, 'a1', 'A1'),
            ({'search_case': 'lower'}, 'A1', 'a1'),
            ({'search_case': 'lower'}, 'a1', 'a1'),
            ({'search_case': ''}, 'A1', 'A1'),
        ],
        'display': [
            ({'display_case': 'upper'}, 'aA1', 'AA1'),
            ({'display_case': 'lower'}, 'aA1', 'aa1'),
            ({'display_case': ''}, 'aA1', 'aA1'),
            ({}, 'aA01', 'aA01'),
        ],
    },
    u.AlphaSymbol: {
        'markers': ['compound', 'AlphaSymbol'],
        'valid': ['a ', 'a-', 'a', ' ', '-'],
        'invalid': ['', '1', 'a1', 'a 1', '1 '],
        'sort': [
            ({'use_formatting_in_sort': True}, 'a..b', 'a.a'),
            ({'use_formatting_in_sort': True}, 'a.a', 'a.b'),
            ({'use_formatting_in_sort': True}, 'a.b', 'aa'),
            ({'use_formatting_in_sort': False}, 'a.a', 'a..b'),
            ({'use_formatting_in_sort': False}, 'a.a', 'a.b'),
            ({'use_formatting_in_sort': False}, 'a.b', 'aa'),
        ],
        'sort_equivalence': [
            ({'use_formatting_in_sort': True}, 'a..a', 'a.a', False),
            ({'use_formatting_in_sort': True}, 'a.a', 'aa', False),
            ({'use_formatting_in_sort': False}, 'a..a', 'a.a', True),
            ({'use_formatting_in_sort': False}, 'a.a', 'aa', False),

        ],
        'search': [],  # nothing new to test
        'display': [],  # nothing new to test
    },
    u.NumericSymbol: {
        'markers': ['compound', 'NumericSymbol'],
        'valid': ['1', '1 ', '1-', '1-1', ' ', '-'],
        'invalid': ['', 'a', 'a1', 'a ', 'a 1'],
        'sort': [],  # nothing new to test
        'sort_equivalence': [],  # nothing new to test
        'search': [],  # nothing new to test
        'display': [],  # nothing new to test
    },
    u.AlphaNumericSymbol: {
        'markers': ['compound', 'AlphaNumericSymbol'],
        'valid': ['a', '1', 'a1', '1a' '-', 'a1-', 'a 1', '1 a', ' a1'],
        'invalid': [''],
        'sort': [],  # nothing new to test
        'sort_equivalence': [],  # nothing new to test
        'search': [],  # nothing new to test
        'display': [],  # nothing new to test
    },
    u.Number: {
        'markers': ['numbers', 'Number'],
        'valid': [
            NUMERALS, '0.1', '1.1', '1000', '1,000', '1,000.1', '10,000',
            '100,000', '1,000,000'
        ],
        'invalid': [
            '', '-1', '.1', '-0.1', '-.1', 'a', 'A1', '1 1', '1-1', '1.',
            ',1', '1,', '1,1', '1,11', '0,000'
        ],
        'sort': [
            ({}, '1,111', '1112'),
            ({}, '1111', '1,112'),
            ({}, '1', '2'),
            ({}, '2', '11'),
            ({}, '1.11', '1.2'),
        ],
        'sort_equivalence': [
            ({}, '1.1', '1.10', False),
            ({}, '1,111', '1111', True),
            ({}, '1', '01', True),
        ],
        'search': [
            ({}, '1', '1'),
            ({}, '1.1', '1.1'),
        ],
        'display': [
            ({}, '1', '1'),
            ({}, '01', '01'),
            ({}, '1.0', '1.0'),
            ({}, '10,000', '10,000'),
        ],
    },
    u.OrdinalNumber: {
        'markers': ['numbers', 'OrdinalNumber'],
        'valid': [
            '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th',
            '10th', '100th', '1,000th', '10,000th', '1,000,001st', '1000th'
        ],
        'invalid': ['1', '1sta', '1st1', '1 st', 'st1'],
        'sort': [
            ({}, '1st', '2nd'),
            ({}, '2nd', '10th'),
        ],
        'sort_equivalence': [],  # nothing new to test
        'search': [],  # nothing new to test
        'display': [],  # nothing new to test
    },
    u.dates.parts.Year: {
        'markers': ['dates', 'Year'],
        'valid': ['00', '99', '1000', '2018'],
        'invalid': ['3000', '0000', '1', '0001', '100'],
        'sort': [
            ({}, '2015', '16'),
            ({}, '97', '16'),
        ],
        'sort_equivalence': [
            ({}, '00', '2000', True),
            ({}, '99', '1999', True),
            ({}, '16', '2016', True),
        ],
        'search': [],  # nothing new to test
        'display': [
            ({}, '2016', '2016'),
            ({}, '16', '16'),
            ({}, '1999', '1999'),
            ({}, '99', '99'),
        ],
    },
    u.dates.parts.Month: {
        'markers': ['dates', 'Month'],
        'valid': [
            'Jan', 'jan', 'JAN', 'Jan.', 'January', 'JANUARY', '01', '1',
            'Feb', 'February', '2', 'Mar', 'March', '3', 'Apr', 'April', '4',
            'May', '5', 'Jun', 'June', '6', 'Jul', 'July', '7', 'Aug',
            'August', '8', 'Sep', 'September', '9', 'Oct', 'October', '10',
            'Nov', 'November', '11', 'Dec', 'December', '12', 'Fall', 'Winter',
            'Spring', 'Summer'
        ],
        'invalid': ['Janu', 'J', '0', '13', '001'],
        'sort': [
            ({}, 'Jan', 'Feb'),
            ({}, 'Feb', 'Mar'),
            ({}, 'Mar', 'Apr'),
            ({}, 'Apr', 'May'),
            ({}, 'May', 'Jun'),
            ({}, 'Jun', 'Jul'),
            ({}, 'Jul', 'Aug'),
            ({}, 'Aug', 'Sep'),
            ({}, 'Sep', 'Oct'),
            ({}, 'Oct', 'Nov'),
            ({}, 'Nov', 'Dec'),
        ],
        'sort_equivalence': [
            ({}, 'Jan', '1', True),
            ({}, 'Jan', '01', True),
            ({}, 'Jan', 'January', True),
            ({}, 'Jan', 'Jan.', True),
            ({}, 'Winter', 'January', True),
            ({}, 'Spring', 'March', True),
            ({}, 'Summer', 'June', True),
            ({}, 'Fall', 'September', True),
        ],
        'search': [],  # nothing new to test
        'display': [
            ({}, 'Jan', 'Jan'),
            ({}, 'Jan.', 'Jan.'),
            ({}, 'January', 'January'),
            ({}, '01', '01'),
            ({}, '1', '1'),
            ({}, 'Winter', 'Winter'),
        ],
    },
    u.dates.parts.Day: {
        'markers': ['dates', 'Day'],
        'valid': ['1', '01', '1st', '31st'],
        'invalid': ['32', '32nd', '001', '0'],
        'sort': [
            ({}, '1', '2nd'),
            ({}, '01', '2'),
        ],
        'sort_equivalence': [
            ({}, '1', '1st', True),
            ({}, '1', '01', True),
        ],
        'search': [],  # nothing new to test
        'display': [
            ({}, '1', '1'),
            ({}, '1st', '1st'),
            ({}, '01', '01'),
        ],
    },
    u.DateString: {
        'markers': ['dates', 'DateString'],
        'valid': [
            '01-2016', '01-31-2016', '1-31-2016', '1/31/2016', 'Jan 31st 2016',
            'Jan 31st, 2016', 'Jan 31 2016', '1 31 2016', '1.31.2016',
            '31-1-2016', '2016-1-31', '2016-31-1', '01-31-16', 'Winter 2016'
        ],
        'invalid': ['01312016', 'January 32nd 2016'],
        'sort': [
            ({}, 'Dec 31st 2015', 'Jan 1st 2016'),
            ({}, 'Jan 1st 2016', 'Jan 2nd 2016'),
            ({}, 'Jan 31st 2016', 'Feb 1st 2016'),
            ({}, 'Jan 2016', 'Jan 1 2016'),
            ({}, 'Jan 2016', 'Feb 2016'),
        ],
        'sort_equivalence': [
            ({}, '01-02-2016', 'Jan 2 2016', True),  # Month-first is default
            ({}, '31-01-2016', 'Jan 31 2016', True),
            ({}, 'Jan 31st 2016', 'Jan 31 2016', True),
            ({}, 'Jan 31st, 2016', 'Jan 31 2016', True),
            ({}, '01-31-2016', 'Jan 31 2016', True),
            ({}, '1/31/2016', 'Jan 31 2016', True),
            ({}, '1.31.2016', 'Jan 31 2016', True),
            ({}, '1.31.16', 'Jan 31 2016', True),
            ({}, '2016-01-31', 'Jan 31 2016', True),
            ({}, '2016-31-01', 'Jan 31 2016', True),
        ],
        'search': [],  # nothing new to test
        'display': [],  # nothing new to test
    },
    u.Cutter: {
        'markers': ['callnumbers', 'Cutter'],
        'valid': ['A1', 'Aaa1', 'A1111', 'A 1'],
        'invalid': [
            '', '.A1', 'Aaaa1', 'A-1', 'A', '1', 'A1,111', 'A1.1'
        ],
        'sort': [
            ({}, 'A1', 'AA1'),
            ({'sort_case': ''}, 'AA1', 'AB1'),
            ({'sort_case': ''}, 'AB1', 'Aa1'),
            ({'sort_case': 'upper'}, 'AA1', 'AB1'),
            ({'sort_case': 'upper'}, 'Aa1', 'AB1'),
            ({'sort_case': 'lower'}, 'AA1', 'AB1'),
            ({'sort_case': 'lower'}, 'Aa1', 'AB1'),
            ({}, 'AB1', 'B1'),
            ({}, 'A1', 'A2'),
            ({}, 'A11', 'A2'),
        ],
        'sort_equivalence': [
            ({'sort_case': ''}, 'a1', 'A1', False),
            ({'sort_case': 'upper'}, 'a1', 'A1', True),
            ({'sort_case': 'lower'}, 'a1', 'A1', True),
            ({}, 'A1', 'A01', False),
        ],
        'search': [
            ({'search_case': ''}, 'Aa1', 'Aa1'),
            ({'search_case': 'upper'}, 'Aa1', 'AA1'),
            ({'search_case': 'lower'}, 'Aa1', 'aa1'),
        ],
        'display': [
            ({'display_case': 'upper'}, 'Aaa1', 'AAA1'),
            ({'display_case': 'lower'}, 'Aaa1', 'aaa1'),
            ({'display_case': ''}, 'Aaa1', 'Aaa1'),
        ],
    },
    u.Edition: {
        'markers': ['callnumbers', 'Edition'],
        'valid': ['1111', '1111a', '1111abcd'],
        'invalid': ['1', '11', '111', '11111', '1111 ', '1111 a', '1111-'],
        'sort': [
            ({}, '2000', '2001'),
            ({}, '2001', '2001a'),
            ({}, '2001a', '2001b'),
            ({'sort_case': ''}, '2001A', '2001B'),
            ({'sort_case': ''}, '2001B', '2001a'),
            ({'sort_case': 'upper'}, '2001A', '2001B'),
            ({'sort_case': 'upper'}, '2001a', '2001B'),
            ({'sort_case': 'lower'}, '2001A', '2001B'),
            ({'sort_case': 'lower'}, '2001a', '2001B'),
        ],
        'sort_equivalence': [
            ({'sort_case': ''}, '2001a', '2001A', False),
            ({'sort_case': 'upper'}, '2001a', '2001A', True),
            ({'sort_case': 'lower'}, '2001a', '2001A', True),
        ],
        'search': [
            ({'search_case': ''}, '2001A', '2001A'),
            ({'search_case': 'upper'}, '2001a', '2001A'),
            ({'search_case': 'lower'}, '2001A', '2001a'),
        ],
        'display': [
            ({'display_case': 'upper'}, '2001a', '2001A'),
            ({'display_case': 'lower'}, '2001A', '2001a'),
            ({'display_case': ''}, '2001a', '2001a'),
        ],
    },
    u.Item: {
        'markers': ['callnumbers', 'Item'],
        'valid': ['0', '1', '1.0', '1,000', 'v1', 'v 1', 'v. 1', 'Volume 1',
                  'v. 1 c. 1', 'v1 c1', 'v1 c1 supp.', 'v1 c1 2000',
                  'v1 c1 no. 1', 'a-b 1', 'a 1-1', 'a 1e b 1'],
        'invalid': [''],
        'sort': [
            ({}, '1', '2'),
            ({}, '1', '1a'),
            ({}, '1a', '1b'),
            ({}, 'vol 1', 'vol 2'),
            ({}, 'Volume 1', 'v 2'),
            ({}, 'Volume 1', 'v 1a'),
            ({}, 'v 1', 'v 1 c 1'),
            ({}, 'v 1 c 1', 'v 1 c 2'),
            ({}, 'v 1 c 1', 'v 1-1 c 1'),
            ({}, 'v 1-1 c 1', 'v 1-2 c 1'),
            ({}, 'v 1-A c 1', 'v 1-B c 1'),
            ({}, 'v 1 c 1', 'v 1a c 1'),
            ({}, 'v 1 c a1', 'v 1 c b1'),
            ({}, 'v 1 c 1', 'v 1 c 1 supp.'),
            ({}, 'v 1 c 1 A', 'v 1 c 1 B'),
            ({}, 'v 1 Dec 1995', 'v 1 Jan 1996'),
            ({}, 'v 1 Jan 1996', 'v 1 Feb 1996'),
            ({}, 'v 1 Feb 1996', 'v 1 March 1996'),
            ({}, 'v 1 March 1996', 'v 1 Apr 1996'),
            ({}, 'v 1 Apr 1996', 'v 1 May 1996'),
            ({}, 'v 1 May 1996', 'v 1 June 1996'),
            ({}, 'v 1 June 1996', 'v 1 July 1996'),
            ({}, 'v 1 July 1996', 'v 1 Aug 1996'),
            ({}, 'v 1 Aug 1996', 'v 1 Sep 1996'),
            ({}, 'v 1 Sep 1996', 'v 1 Oct 1996'),
            ({}, 'v 1 Oct 1996', 'v 1 Nov 1996'),
            ({}, 'v 1 Nov 1996', 'v 1 Dec 1996'),
            ({}, 'v 1 Fall 1995', 'v 1 Winter 1996'),
            ({}, 'v 1 Winter 1996', 'v 1 Spring 1996'),
            ({}, 'v 1 Spring 1996', 'v 1 Summer 1996'),
            ({}, 'v 1 Summer 1996', 'v 1 Fall 1996'),
        ],
        'sort_equivalence': [
            ({}, 'volume 1', '1', True),
            ({}, 'volume 1', 'v 1', True),
            ({}, 'v. 1', 'v 1', True),
            ({}, 'v.1', 'v 1', True),
            ({}, 'v1', 'v 1', False),
            ({}, 'v1', '1', False),
            ({}, 'volume 1 copy 1', '1 1', True),
            ({}, 'volume 1 copy 1', 'v1 c1', False),
            ({}, 'volume 1 copy 1', 'v1c1', False),
            ({}, 'volume 1 copy 1', 'v 1 c 1', True),
            ({}, 'v 1 c 1-1', 'v 1-1 c 1', False),
            ({}, 'Dec', 'December', True),
            ({}, 'Jan', 'January', True),
            ({}, 'Feb', 'February', True),
            ({}, 'Mar', 'March', True),
            ({}, 'Apr', 'April', True),
            ({}, 'Jun', 'June', True),
            ({}, 'Jul', 'July', True),
            ({}, 'Aug', 'August', True),
            ({}, 'Sep', 'September', True),
            ({}, 'Oct', 'October', True),
            ({}, 'Nov', 'November', True),
            ({}, 'Dec', 'December', True),
            ({'sort_case': ''}, 'v 1', 'V 1', True),
            ({'sort_case': ''}, 'v 1 supp', 'V 1 SUPP', False),
            ({'sort_case': 'upper'}, 'v 1', 'V 1', True),
            ({'sort_case': 'upper'}, 'v 1 supp', 'V 1 SUPP', True),
            ({'sort_case': 'lower'}, 'v 1', 'V 1', True),
            ({'sort_case': 'lower'}, 'v 1 supp', 'V 1 SUPP', True),
        ],
        'search': [
            ({'search_case': ''}, 'v 1', '1'),
            ({'search_case': ''}, 'v 1 supp', '1supp'),
            ({'search_case': 'upper'}, 'v 1', '1'),
            ({'search_case': 'upper'}, 'v 1 supp', '1SUPP'),
            ({'search_case': 'lower'}, 'V 1', '1'),
            ({'search_case': 'lower'}, 'V 1 SUPP', '1supp'),
        ],
        'display': [
            ({'display_case': 'upper'}, 'Vol. 1-a Supp', 'VOL. 1-A SUPP'),
            ({'display_case': 'lower'}, 'Vol. 1-a Supp', 'vol. 1-a supp'),
            ({'display_case': ''}, 'Vol. 1-a Supp', 'Vol. 1-a Supp')
        ],
    },
    u.LC: {
        'markers': ['callnumbers', 'LC'],
        'valid': [
            'A1 .A1', 'A1.1 A1', 'A 1 .A1', 'A 1 .A 1', 'A1 .A1 A1', 'A1.A1A1',
            'A1 A1A1', 'AAA1 .A1 A1', 'A1111 .A1 A1', 'A1 .A1 A1 1111',
            'A1 .A1 A1 c.1', 'A1 .A1 A1 1111a c.1', 'A1 .A1 A1 1111a v.1 c.1'
        ],
        'invalid': [
            '', 'A1', 'A 1', '.A1', 'AAAA1 .A1 A1', 'A1,111 .A1',
            'A11111 .A1 A1', 'A1111.11111 .A1 A1', 'A-1 .A1', 'A1 .A-1',
            'A1 .A', 'A1 .1', 'A 1:1', 'A1 . A1', 'A1.1.1 A1',
        ],
        'sort': [
            ({}, 'A1 .A1', 'A1.1 .A1'),
            ({}, 'A2 .A1', 'A11 .A1'),
            ({}, 'A1.11 .A1', 'A1.2 .A1'),
            ({}, 'A1 .A1', 'A1 .AA1'),
            ({'sort_case': ''}, 'A1 .A1', 'A1 .B1'),
            ({'sort_case': ''}, 'A1 .B1', 'A1 .a1'),
            ({'sort_case': 'upper'}, 'A1 .A1', 'A1 .B1'),
            ({'sort_case': 'upper'}, 'A1 .a1', 'A1 .B1'),
            ({'sort_case': 'lower'}, 'A1 .A1', 'A1 .B1'),
            ({'sort_case': 'lower'}, 'A1 .a1', 'A1 .B1'),
            ({}, 'A1 .B1', 'A1 .B2'),
            ({}, 'A1 .B11', 'A1 .B2'),
            ({}, 'A1 .B1', 'A1 .B1 C1'),
            ({}, 'A1 .B1 C1', 'A1 .B1 D1'),
            ({}, 'A1 .B1 C1', 'A1 .B1 C2'),
            ({}, 'A1 .B1 C11', 'A1 .B1 C2'),
            ({}, 'A1 .B1 C1', 'A1 .B1 C1 1999'),
            ({}, 'A1 .B1 C1 1999', 'A1 .B1 C1 2000'),
            ({}, 'A1 .B1 C1 2000', 'A1 .B1 C1 2000a'),
            ({}, 'A1 .B1 C1 2000', 'A1 .B1 C1 2000 no.1'),
            ({}, 'A1 .B1 C1 2000 no.1', 'A1 .B1 C1 2000 no.2'),
            ({}, 'A1 .B1 C1 2000 no.2', 'A1 .B1 C1 2000 no.11'),
        ],
        'sort_equivalence': [
            ({}, 'A1 .A1', 'A1.A1', True),
            ({}, 'A1 .A1', 'A1 A1', True),
            ({}, 'A1 .A1', 'A 1 .A1', True),
            ({}, 'A1 .A1', 'A  1 .A1', True),
            ({}, 'A1 .A1', 'A1.A1', True),
            ({}, 'A1 .A1', 'A1A1', True),
            ({}, 'A1 .A1 B2', 'A1 .A1B2', True),
        ],
        'search': [
            ({'search_case': ''}, 'A1 .A1', 'A1A1'),
            ({'search_case': ''}, 'A1 .a1', 'A1a1'),
            ({'search_case': 'upper'}, 'A1 .A1', 'A1A1'),
            ({'search_case': 'upper'}, 'A1 .a1', 'A1A1'),
            ({'search_case': 'lower'}, 'A1 .A1', 'a1a1'),
            ({'search_case': 'lower'}, 'A1 .a1', 'a1a1'),
            ({'use_formatting_in_search': True}, 'A1 .A1', 'a1 .a1'),
            ({'use_formatting_in_search': False}, 'A1 .A1', 'a1a1'),
            ({'use_formatting_in_search': True}, 'A1.1 .A1', 'a1.1 .a1'),
            ({'use_formatting_in_search': False}, 'A1.1 .A1', 'a1.1a1'),
        ],
        'display': [
            ({'display_case': 'upper'}, 'Aa100 .Aa1 Vl.2', 'AA100 .AA1 VL.2'),
            ({'display_case': 'lower'}, 'Aa100 .Aa1 Vl.2', 'aa100 .aa1 vl.2'),
            ({'display_case': ''}, 'Aa100 .Aa1 Vl.2', 'Aa100 .Aa1 Vl.2'),
            ({}, 'A1 .A1', 'A1 .A1'),
            ({}, 'A1 A1', 'A1 A1'),
            ({}, 'A1 A1B1', 'A1 A1B1'),
            ({}, 'A1 A1 B1', 'A1 A1 B1'),
        ],
    },
    u.Dewey: {
        'markers': ['callnumbers', 'Dewey'],
        'valid': [
            '100 A1', '100 Aaa1', '100.1 A1', '100 A1a', '100 A1a B1',
            '100 A1 B1', '100 A1a B1a', '100 A1 B1a', '100 A1a B1 1111',
            '100 A1a B1 1111a', '100 A1a B1 1111a c.1', '100 A1a B1 c.1'
        ],
        'invalid': [
            '1', '100', '1000', '1000 A1', '100 .A1', '100 Aaaa1',
            '100 .1 A1', 'A1:1', 'A 100 A1'
        ],
        'sort': [
            ({}, '100 A1', '101 A1'),
            ({}, '101 A1', '101.1 A1'),
            ({}, '101.11 A1', '101.2 A1'),
            ({}, '100 A1', '100 A2'),
            ({}, '100 A11', '100 A2'),
            ({}, '100 A1', '100 B1'),
            ({}, '100 A1', '100 A1a'),
            ({}, '100 A1a', '100 A1a A1'),
            ({}, '100 A1a', '100 A1a A1'),
            ({}, '100 A1a A1', '100 A1a A1 2000'),
            ({}, '100 A1a A1 2000', '100 A1a A1 2001'),
            ({}, '100 A1a A1 2001', '100 A1a A1 2001a'),
            ({}, '100 A1a A1 2001', '100 A1a A1 2001 c.1'),
            ({}, '100 A1a A1 2001 c.1', '100 A1a A1 2001 c.2'),
            ({'sort_case': ''}, '100 A1', '100 B1'),
            ({'sort_case': ''}, '100 B1', '100 a1'),
            ({'sort_case': 'upper'}, '100 A1', '100 B1'),
            ({'sort_case': 'upper'}, '100 a1', '100 B1'),
            ({'sort_case': 'lower'}, '100 A1', '100 B1'),
            ({'sort_case': 'lower'}, '100 a1', '100 B1'),
        ],
        'sort_equivalence': [
            ({'sort_case': ''}, '100 A1', '100 A1', True),
            ({'sort_case': ''}, '100 a1', '100 A1', False),
            ({'sort_case': 'upper'}, '100 A1', '100 A1', True),
            ({'sort_case': 'upper'}, '100 a1', '100 A1', True),
            ({'sort_case': 'lower'}, '100 A1', '100 A1', True),
            ({'sort_case': 'lower'}, '100 a1', '100 A1', True),
            ({'use_formatting_in_sort': True}, '100 A1', '100 A1', True),
            ({'use_formatting_in_sort': True}, '100 A1', '100A1', False),
            ({'use_formatting_in_sort': False}, '100 A1', '100A1', True),
            ({'use_formatting_in_sort': False}, '100 A1', '100 A1', True),
            ({'use_formatting_in_sort': True}, '100 A1 1', '100 A11', False),
            ({'use_formatting_in_sort': False}, '100 A1 1', '100 A11', False),
        ],
        'search': [
            ({'search_case': ''}, '100 A1', '100A1'),
            ({'search_case': ''}, '100 a1', '100a1'),
            ({'search_case': 'upper'}, '100 A1', '100A1'),
            ({'search_case': 'upper'}, '100 a1', '100A1'),
            ({'search_case': 'lower'}, '100 A1', '100a1'),
            ({'search_case': 'lower'}, '100 a1', '100a1'),
            ({'use_formatting_in_search': True}, '100.1 A1', '100.1 a1'),
            ({'use_formatting_in_search': True}, '100.1A1', '100.1a1'),
            ({'use_formatting_in_search': False}, '100.1 A1', '100.1a1'),
        ],
        'display': [
            ({}, '100 A1', '100 A1'),
            ({}, '100A1', '100A1'),
            ({}, '100 A1a', '100 A1a'),
            ({}, '100 A1a B1', '100 A1a B1'),
            ({}, '100 A1a B1 1900', '100 A1a B1 1900'),
            ({'display_case': ''}, '100 A1a', '100 A1a'),
            ({'display_case': 'upper'}, '100 A1a', '100 A1A'),
            ({'display_case': 'lower'}, '100 A1a', '100 a1a'),
        ],
    },
    u.SuDoc: {
        'markers': ['callnumbers', 'SuDoc'],
        'valid': ['A1.1:', 'A 1.1:', 'A 1.1 :', 'A1.1/1:', 'A1.1:1',
                  'A 1.1 / 1 :', 'A1.1/1-1:', 'X.1/1:', 'Y 3.A 1/1:', 'XJH:',
                  'XJS:'],
        'invalid': ['A', 'A1', 'A1.1', 'A1.1/1', 'A1. 1:', 'A1:', '1:'],
        'sort': [
            ({}, 'A 1.1:', 'AA 1.1:'),
            ({}, 'AA 1.1:', 'AB 1.1:'),
            ({}, 'AB 1.1:', 'B 1.1:'),
            ({}, 'A 1.1:', 'A 2.1:'),
            ({}, 'A 2.1:', 'A 11.1:'),
            ({}, 'A 1.2:', 'A 1.11:'),
            ({}, 'A 1.1:', 'A 1.1/A:'),
            ({}, 'A 1.1/A:', 'A 1.1/1:'),
            ({}, 'A 1.1/1:', 'A 1.1/2:'),
            ({}, 'A 1.1/2:', 'A 1.1/11:'),
            ({}, 'A 1.1/1:', 'A 1.1/1-1:'),
            ({}, 'A 1.1/1-1:', 'A 1.1/1-2:'),
            ({}, 'A 1.1/1-2:', 'A 1.1/1-11:'),
            ({}, 'A 1.1:', 'A 1.1:A'),
            ({}, 'A 1.1:A', 'A 1.1:B'),
            ({}, 'A 1.1:A', 'A 1.1:A 1'),
            ({}, 'A 1.1:A 1', 'A 1.1:A 2'),
            ({}, 'A 1.1:A 2', 'A 1.1:A 11'),
            ({}, 'A 1.1:A', 'A 1.1:1'),
            ({}, 'A 1.1:1', 'A 1.1/A:1'),
            ({}, 'A 1.1:1', 'A 1.1:2'),
            ({}, 'A 1.1:2', 'A 1.1:11'),
            ({}, 'A 1.1:1', 'A 1.1:1-1'),
            ({}, 'A 1.1:1-1', 'A 1.1:1-2'),
            ({}, 'A 1.1:1-2', 'A 1.1:1-11'),
            ({}, 'A 1.1:1/A', 'A 1.1:1/B'),
            ({}, 'A 1.1:1/A', 'A 1.1:1/1'),
            ({}, 'A 1.1:1/1', 'A 1.1:1/2'),
            ({}, 'A 1.1:1/2', 'A 1.1:1/11'),
            ({}, 'A 1.1:1-1/1', 'A 1.1:1/1-1')
        ],
        'sort_equivalence': [
            ({'sort_case': ''}, 'A 1.1:', 'A 1.1:', True),
            ({'sort_case': ''}, 'A 1.1:', 'a 1.1:', False),
            ({'sort_case': 'upper'}, 'A 1.1:', 'A 1.1:', True),
            ({'sort_case': 'upper'}, 'A 1.1:', 'a 1.1:', True),
            ({'sort_case': 'lower'}, 'A 1.1:', 'A 1.1:', True),
            ({'sort_case': 'lower'}, 'A 1.1:', 'a 1.1:', True),
            ({'use_formatting_in_sort': True}, 'A 1.1:', 'A 1.1:', True),
            ({'use_formatting_in_sort': True}, 'A 1.1:', 'A1.1:', False),
            ({'use_formatting_in_sort': False}, 'A 1.1:', 'A1.1:', True),
            ({'use_formatting_in_sort': False}, 'A 1.1:', 'A 1.1:', True),
        ],
        'search': [],  # nothing new to test
        'display': [],  # nothing new to test
    },
    u.Local: {
        'markers': ['callnumbers', 'Local'],
        'valid': ['A1', 'A 1', 'A-1', 'AA-11 BB-22 CC-33'],
        'invalid': [''],
        'sort': [
            ({'sort_case': ''}, 'AA-11', 'AB-11'),
            ({'sort_case': ''}, 'AB-11', 'Aa-11'),
            ({'sort_case': 'upper'}, 'AA-11', 'AB-11'),
            ({'sort_case': 'upper'}, 'Aa-11', 'AB-11'),
            ({'sort_case': 'lower'}, 'AA-11', 'AB-11'),
            ({'sort_case': 'lower'}, 'Aa-11', 'AB-11'),
            ({}, 'AA-11', 'AA-12'),
            ({}, 'AA-12', 'AA-111'),
            ({}, 'AA-11.12', 'AA-11.2'),
            ({}, 'AA.12', 'AA.111'),
            ({'use_formatting_in_sort': True}, 'AA-AA', 'AA-AB'),
            ({'use_formatting_in_sort': True}, 'AA AB', 'AA-AA'),
            ({'use_formatting_in_sort': False}, 'AA-AA', 'AA-AB'),
            ({'use_formatting_in_sort': False}, 'AA AA', 'AA-AB'),
        ],
        'sort_equivalence': [
            ({'sort_case': 'upper'}, 'aa-11', 'AA-11', True),
            ({'sort_case': 'lower'}, 'aa-11', 'AA-11', True),
            ({'sort_case': ''}, 'aa-11', 'AA-11', False),
            ({}, 'AA-11', 'AA-011', True),
            ({}, 'AA-1.0', 'AA-1', True),
            ({'use_formatting_in_sort': True}, 'AA-AA', 'AA AA', False),
            ({'use_formatting_in_sort': False}, 'AA-AA', 'AA AA', True),
            ({'use_formatting_in_sort': False}, 'AA-AA', 'AAAA', False),
        ],
        'search': [
            ({'search_case': ''}, 'aA11', 'aA11'),
            ({'search_case': 'upper'}, 'aA11', 'AA11'),
            ({'search_case': 'lower'}, 'aA11', 'aa11'),
            ({'use_formatting_in_search': True}, 'AA-11', 'aa-11'),
            ({'use_formatting_in_search': False}, 'AA-11', 'aa11'),
        ],
        'display': [
            ({'display_case': 'upper'}, 'aBc-123', 'ABC-123'),
            ({'display_case': 'lower'}, 'aBc-123', 'abc-123'),
            ({'display_case': ''}, 'aBc-123', 'aBc-123'),
            ({}, 'abc-123', 'abc-123'),
        ],
    },
}

VALID_TEST_PARAMS = generate_params(UNITS_DATA, 'valid')
INVALID_TEST_PARAMS = generate_params(UNITS_DATA, 'invalid')
SORT_TEST_PARAMS = generate_params(UNITS_DATA, 'sort')
SORT_EQ_TEST_PARAMS = generate_params(UNITS_DATA, 'sort_equivalence')
DISPLAY_TEST_PARAMS = generate_params(UNITS_DATA, 'display')
SEARCH_TEST_PARAMS = generate_params(UNITS_DATA, 'search')


# Tests

@pytest.mark.parametrize('tclass, tstr', VALID_TEST_PARAMS)
def test_Unit_validate_is_valid(tclass, tstr):
    """The test string should validate when a Unit subclass is
    initialized.

    """
    tclass(tstr)


@pytest.mark.parametrize('tclass, tstr', INVALID_TEST_PARAMS)
def test_Unit_validate_not_valid(tclass, tstr):
    """The test string should not validate when a Unit subclass is
    initialized. It should raise an InvalidCallNumberStringError.

    """
    with pytest.raises(e.InvalidCallNumberStringError):
        tclass(tstr)


@pytest.mark.parametrize('tclass, opts, tstr, expected', DISPLAY_TEST_PARAMS)
def test_Unit_forprint(tclass, opts, tstr, expected):
    """When the ``for_print`` method of the given Unit subclass is
    called, the test string should normalize to the expected output.

    """
    unit = tclass(tstr, **opts)
    assert unit.for_print() == expected


@pytest.mark.parametrize('tclass, opts, tstr1, tstr2', SORT_TEST_PARAMS)
def test_Unit_forsort(tclass, opts, tstr1, tstr2):
    """When test string 1 and test string 2 are both normalized via the
    ``for_sort`` method of the given Unit subclass, test string 1
    should sort before test string 2 (assuming a low-to-high sort).

    """
    units = [tclass(tstr, **opts) for tstr in (tstr1, tstr2)]
    assert units[0].for_sort() < units[1].for_sort()


@pytest.mark.parametrize('tclass, opts, tstr1, tstr2, expected',
                         SORT_EQ_TEST_PARAMS)
def test_Unit_forsort_equivalence(tclass, opts, tstr1, tstr2, expected):
    """When text string 1 and test string 2 are both normalized via the
    ``for_sort`` method of the given Unit subclass and tested for
    equality, it should produce the expected result, True or False.

    """
    units = [tclass(tstr, **opts) for tstr in (tstr1, tstr2)]
    assert (units[0].for_sort() == units[1].for_sort()) == expected


@pytest.mark.parametrize('tclass, opts, tstr, expected', SEARCH_TEST_PARAMS)
def test_Unit_forsearch(tclass, opts, tstr, expected):
    """When the test string is normalized via the ``for_search`` method
    of the given Unit subclass, it should produced the expected string.

    """
    unit = tclass(tstr, **opts)
    assert unit.for_search() == expected
