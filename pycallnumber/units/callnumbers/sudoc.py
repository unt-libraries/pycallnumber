"""Work with US SuDocs numbers as Units."""

from __future__ import unicode_literals
from __future__ import absolute_import

from pycallnumber.template import CompoundTemplate
from pycallnumber.unit import CompoundUnit
from pycallnumber.units.simple import Alphabetic, Numeric, Formatting,\
                                      DEFAULT_SEPARATOR_TYPE
from pycallnumber.units.compound import AlphaNumericSymbol
from .parts import Cutter


# Various base SimpleUnits for SuDoc component classes

LettersFirst = Alphabetic.derive(
    classname='LettersFirst',
    for_sort=lambda x: '{}{}'.format(CompoundUnit.sort_break,
                                     Alphabetic.for_sort(x))
)

Period = Formatting.derive(
    classname='Period',
    short_description='a period',
    min_length=1,
    max_length=1,
    base_pattern=r'\.',
    use_formatting_in_sort=True
)

Slash = Formatting.derive(
    classname='Slash',
    short_description='a forward slash',
    min_length=1,
    max_length=1,
    base_pattern=r'\s*/\s*',
    use_formatting_in_sort=True
)

FormattingNoSlash = Formatting.derive(
    classname='FormattingNoSlash',
    short_description=('any non-alphanumeric character except a forward '
                       'slash'),
    min_length=1,
    max_length=1,
    base_pattern=r'[^A-Za-z0-9/]'
)

Dash = Formatting.derive(
    classname='Dash',
    short_description='a dash (hyphen)',
    min_length=1,
    max_length=1,
    base_pattern=r'\s*-\s*',
    use_formatting_in_sort=True
)

Colon = Formatting.derive(
    classname='Colon',
    short_description='a colon',
    min_length=1,
    max_length=1,
    base_pattern=r'\s*:\s*'
)


class Agency(AlphaNumericSymbol):

    short_description = ('either \'X/A\' (for the Congressional Record) or '
                         'a 1- to 4-letter alphabetic department code and '
                         'optional numeric code for a subordinate office')

    Department = Alphabetic.derive(
        classname='Agency.Department',
        min_length=1,
        max_length=4,
    )

    XaDepartment = AlphaNumericSymbol.derive(
        classname='Agency.XaDepartment',
        short_description='\'X/A\'',
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'x', 'min': 1, 'max': 1,
             'type': Alphabetic.derive(min_length=1, max_length=1,
                                       base_pattern=r'[Xx]')},
            {'name': 'slash', 'min': 1, 'max': 1, 'type': Slash},
            {'name': 'a', 'min': 1, 'max': 1,
             'type': LettersFirst.derive(min_length=1, max_length=1,
                                         base_pattern=r'[Aa]')}
        ]
    )

    Office = Numeric.derive(
        classname='Agency.Office'
    )

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'department', 'min': 1, 'max': 1,
             'possible_types': [XaDepartment, Department]},
            {'name': 'office', 'min': 0, 'max': 1, 'type': Office}
        ]
    )


XjhsAgency = CompoundUnit.derive(
    options_defaults=Alphabetic.options_defaults.copy(),
    classname='XjhsAgency',
    definition='the House or Senate Journal designation',
    short_description='the string \'XJH\' or \'XJS\'',
    groups=[
        {'name': 'agency', 'min': 1, 'max': 1,
         'type': Alphabetic.derive(min_length=1, max_length=1,
                                   base_pattern=r'[Xx][Jj](?:[Hh]|[Ss])')}
    ]
)


class Series(AlphaNumericSymbol):

    short_description = ('a Cutter number or a number denoting the category/'
                         'series of the publication, optionally followed '
                         'by a forward slash and one or two alphabetic or '
                         'numeric codes separated by a hyphen, which denote '
                         'a related series'),

    NumericSeries = Numeric.derive(
        classname='Series.NumericSeries'
    )

    RelatedSeries = AlphaNumericSymbol.derive(
        classname='Series.RelatedSeries',
        groups=[
            {'name': 'parts', 'min': 1, 'max': None,
             'possible_types': [LettersFirst, Numeric], 'inner_sep_type': Dash}
        ]
    )

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'main_series', 'min': 1, 'max': 1,
             'possible_types': [Cutter, NumericSeries]},
            {'name': 'slash', 'min': 0, 'max': 1, 'type': Slash,
             'is_separator': True},
            {'name': 'related_series', 'min': 0, 'max': 1,
             'type': RelatedSeries}
        ]
    )


AgencyDotSeries = AlphaNumericSymbol.derive(
        classname='AgencyDotSeries',
        definition=('information about the department, agency, or office that '
                    'published the item along with the format or publication '
                    'series it falls under'),
        short_description=('a string with the following parts: ``agency``, '
                           '{}; dot; ``series``, {}'
                           ''.format(Agency.describe_short(False),
                                     Series.describe_short(False))),
        groups=[
            {'name': 'agency', 'min': 1, 'max': 1, 'type': Agency},
            {'name': 'period', 'min': 1, 'max': 1, 'type': Period,
             'is_separator': True},
            {'name': 'series', 'min': 1, 'max': 1, 'type': Series},
        ]
    )


class BookNumber(AlphaNumericSymbol):

    definition = ('information that helps differentiate items with the same '
                  'class stem from each other, such as volume numbers or '
                  'agency-specific designators')
    short_description = ('a string containing any characters; letters sort '
                         'before numbers')

    Component = AlphaNumericSymbol.derive(
        classname='BookNumber.Component',
        groups=[
            {'name': 'parts', 'min': 1, 'max': None,
             'possible_types': [LettersFirst, Numeric, Dash,
                                FormattingNoSlash]}
        ]
    )

    template = CompoundTemplate(
        groups=[
            {'name': 'parts', 'min': 0, 'max': None, 'inner_sep_type': Slash,
             'type': Component},
        ]
    )


class SuDoc(AlphaNumericSymbol):

    definition = ('a call number that uses the US Superintendent of Documents '
                  'Classification scheme')

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'stem', 'min': 1, 'max': 1,
             'possible_types': [XjhsAgency, AgencyDotSeries]},
            {'name': 'colon', 'min': 1, 'max': 1, 'type': Colon},
            {'name': 'book_number', 'min': 1, 'max': 1, 'type': BookNumber}
        ]
    )

    def __init__(self, cnstr, name='default', **options):
        super(SuDoc, self).__init__(cnstr, name, **options)
        if hasattr(self.stem, 'series'):
            if not getattr(self.stem.series, 'related_series'):
                blank_related_series = Formatting.derive(
                    min_length=0,
                    for_sort=lambda x: CompoundUnit.sort_break
                )('')
                self.stem.series._parts.append(blank_related_series)
