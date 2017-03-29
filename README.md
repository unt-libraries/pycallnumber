# pycallnumber [![Build Status](https://travis-ci.org/unt-libraries/pycallnumber.svg?branch=master)](https://travis-ci.org/unt-libraries/pycallnumber)


## About

Use pycallnumber in your library's Python projects to parse, model, and manipulate any type of call number string. Support for Library of Congress, Dewey Decimal, SuDocs, and local call numbers is built in, and you can easily extend built-in classes to customize behavior or model other types of call numbers and formatted strings.

## Installation

### Requirements

  * Python 2
    * Python 2.7 and future
  * OR Python 3, >= 3.4

### Setup

Download the repository to a directory&mdash;we'll use `pycallnumber` for simplicity.

```sh
$ git clone https://github.com/jthomale/pycallnumber.git pycallnumber
```
or (SSH)
```sh
$ git clone git@github.com:jthomale/pycallnumber.git pycallnumber
```

Installing to a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) using pip is recommended.

```sh
$ pip install ./pycallnumber
```
or, if you're updating to a newer version,
```sh
$ pip install --update ./pycallnumber
```

If not using pip, you can run the setuptools install command instead:
```sh
$ cd pycallnumber
$ python setup.py install
```

### Tests

(The below commands assume you're in the repository root.)

Using [tox](https://tox.readthedocs.io/) to run tests is recommended.
```sh
$ pip install tox
$ tox               # run tests against all configured environments
$ tox -e py27       # run tests just against python 2.7
$ tox -e py34       # run tests just against python 3.4
etc.
```

Tox calls [pytest](http://doc.pytest.org/) to run tests, so you can of course also run tests this way.
```sh
$ pip install pytest
$ py.test
```

What's the difference? Running `py.test` directly runs tests using your currently active Python environment. Tox gives you a consistent way to run tests against one or more particular environments without having to juggle them yourself.

Finally, note that you can pass arguments to py.test from tox, using `tox -- ...`. Arguments after the `--` are passed to py.test.
```sh
$ tox -- -x        # -x is passed to py.test
```


## What can you do with pycallnumber?


#### Parse

You can parse call number strings, like Library of Congress call numbers ...

```pycon
>>> import pycallnumber as pycn
>>> cn = pycn.callnumber('MT 1001 .C35 B40 1992 no. 1')
>>> cn
<LC 'MT 1001 .C35 1992'>
>>> cn.classification
<LcClass 'MT 1001'>
>>> cn.classification.letters
<LcClass.ClassLetters 'MT'>
>>> cn.classification.number
<LcClass.ClassNumber '1001'>
>>> cn.cutters[0]
<Cutter 'C35'>
>>> cn.cutters[1]
<Cutter 'B40'>
>>> cn.edition
<Edition '1992'>
>>> cn.item
<Item 'no. 1'>
```

... Dewey Decimal call numbers ...

```pycon
>>> cn = pycn.callnumber('500.1 C226t bk.2')
>>> cn
<Dewey '500.1 C226t bk.2'>
>>> cn.classification
<DeweyClass '500.1'>
>>> cn.cutters[0]
<DeweyCutter 'C226t'>
>>> cn.cutters[0].workmark
<Alphabetic 't'>
>>> cn.item
<Item 'bk.2'>
```

... US SuDocs numbers ...

```pycon
>>> cn = pycn.callnumber('HI.F 3/178-8:A 44/2013 ardocs')
>>> cn
<SuDoc 'HI.F 3/178-8:A 44/2013 ardocs'>
>>> cn.stem
<AgencyDotSeries 'HI.F 3/178-8'>
>>> cn.stem.agency
<Agency 'HI'>
>>> cn.stem.series
<Series 'F 3/178-8'>
>>> cn.stem.series.main_series
<Cutter 'F 3'>
>>> cn.stem.series.related_series
<Series.RelatedSeries '178-8'>
>>> cn.book_number
<BookNumber 'A 44/2013 ardocs'>
>>> cn.book_number.parts[0]
<BookNumber.Component 'A 44'>
>>> cn.book_number.parts[1]
<BookNumber.Component '2013 ardocs'>
```

... and other (i.e. local) call numbers that don't follow the above prescribed patterns.

```pycon
>>> cn = pycn.callnumber('LPCD 100,025-A')
>>> cn
<Local 'LPCD 100,025-A'>
>>> cn.parts[0]
<Alphabetic 'LPCD'>
>>> cn.parts[1]
<Number '100,025'>
>>> cn.parts[2]
<Formatting '-'>
>>> cn.parts[3]
<Alphabetic 'A'>
```

When parsing, pycallnumber is as permissive as possible, allowing for differences in spacing, formatting, and case. As such, it's intended to be suitable for use in a real-world environment, requiring no pre-normalization of call number strings.

```pycon
>>> pycn.callnumber('mt 1001 c35 1992 no. 1')
<LC 'mt 1001 c35 1992 no. 1'>
>>> pycn.callnumber('mt 1001 c35 1992 no. 1').classification
<LcClass 'mt 1001'>
>>> pycn.callnumber('Mt1001 c35 1992 no. 1').classification
<LcClass 'Mt1001'>
>>> pycn.callnumber('Mt   1001 c35 1992 no. 1').classification
<LcClass 'Mt   1001'>
>>> pycn.callnumber('Mt   1001 c35 1992 no. 1').classification.letters
<LcClass.ClassLetters 'Mt'>
>>> pycn.callnumber('Mt   1001 c35 1992 no. 1').classification.number
<LcClass.ClassNumber '1001'>
>>> pycn.callnumber('mt 1001c35 1992 no. 1').cutters[0]
<Cutter 'c35'>
>>> pycn.callnumber('mt 1001.c35 1992 no. 1').cutters[0]
<Cutter 'c35'>
>>> pycn.callnumber('mt 1001 c35 1992 no. 1').cutters[0]
<Cutter 'c35'>
>>> pycn.callnumber('mt 1001 .c35 1992 no. 1').cutters[0]
<Cutter 'c35'>
>>> pycn.callnumber('mt 1001 .c 35 1992 no. 1').cutters[0]
<Cutter 'c 35'>
>>> pycn.callnumber('mt 1001 C 35 1992 no. 1').cutters[0]
<Cutter 'C 35'>
```

Finally, pycallnumber attempts to interpret and parse structured bits that you might find within less structured parts of call numbers, like item-specific information (volume and copy numbers, issue dates, etc.). Numbers may or may not include a thousands separator. Dates&mdash;even partial dates&mdash;if recognized, are parsed into a year, month, and day.

```pycon
>>> pycn.callnumber('LPCD 100,001') == pycn.callnumber('LPCD 100001')
True
>>> cn = pycn.callnumber('MT 1001 .C35 January 2012')
>>> cn.item
<Item 'January 2012'>
>>> cn.item.parts[0]
<DateString 'January 2012'>
>>> cn.item.parts[0].year
<Year '2012'>
>>> cn.item.parts[0].month
<Month 'January'>
>>> cn.item.parts[0].day
>>> cn = pycn.callnumber('MT 1001 .C35 01-31-2012')
>>> cn.item.parts[0].year
<Year '2012'>
>>> cn.item.parts[0].month
<Month '01'>
>>> cn.item.parts[0].day
<Day '31'>
>>>
```

#### Normalize

Any call number can be normalized for sorting ...

```pycon
>>> import pycallnumber as pycn
>>> lc_cn = pycn.callnumber('MT 1001 .C35 B40 1992 no. 1')
>>> dewey_cn = pycn.callnumber('500.1 c226t bk.2')
>>> sudocs_cn = pycn.callnumber('HI.F 3/178-8:A 44/2013 ardocs')
>>> local_cn = pycn.callnumber('LPCD 100,025-A')
>>> lc_cn.for_sort()
u'mt!1001!c!35!b!40!0000001992!!0000000001'
>>> dewey_cn.for_sort()
u'500.1!c!226!t!!0000000002'
>>> sudocs_cn.for_sort()
u'hi.f!3/0000000178-0000000008!!a!0000000044/0000002013!!ardocs'
>>> local_cn.for_sort()
u'lpcd!0000100025!a'
```

... for left-anchored searching ...

```pycon
>>> lc_cn.for_search()
u'mt1001c35b4019921'
>>> dewey_cn.for_search()
u'500.1c226t2'
>>> sudocs_cn.for_search()
u'hif31788a442013ardocs'
>>> local_cn.for_search()
u'lpcd100025a'
```

... and for display.

```pycon
>>> lc_cn.for_print()
u'MT 1001 .C35 B40 1992 no. 1'
>>> dewey_cn.for_print()
u'500.1 c226t bk.2'
>>> sudocs_cn.for_print()
u'HI.F 3/178-8:A 44/2013 ardocs'
>>> local_cn.for_print()
u'LPCD 100,025-A'
```

#### Operate

You can compare call numbers using comparison operators, and the typical methods for sorting work as you'd expect. Comparison operators use the normalized `for_sort` version of the call number as the basis for comparison, so call numbers expressed with differences in spacing or formatting won't throw off comparisons and sorting, as long as the call numbers are recognizable and are parsed correctly.

```pycon
>>> import pycallnumber as pycn
>>> pycn.callnumber('Mt1001 c35 1992 no. 1') == pycn.callnumber('MT 1001 .C35 1992 #1')
True
>>> cnstrings = ['MT 1001 .C35 B40 1992 no. 1',
...              'MT 1001 .C35 B40 1992 no. 2',
...              'MT 1001 .C35 B40 1990',
...              'M 120 .A20 2002 c.2',
...              'MT 100 .S23 1985',
...              'M 120 .A20 2002 copy 1',
...              'MT 1001 .C35 B100 2013',
...              'MT 1001 .C35 B40 1991',
...              'MT 1001 .C35 B40 1992 no. 2 copy 2']
>>> lccns = [pycn.callnumber(cn) for cn in cnstrings]
>>> lccns[1] > lccns[2]
True
>>> lccns[1] < lccns[2]
False
>>> for cn in sorted(lccns): print cn
...
M 120 .A20 2002 copy 1
M 120 .A20 2002 c.2
MT 100 .S23 1985
MT 1001 .C35 B100 2013
MT 1001 .C35 B40 1990
MT 1001 .C35 B40 1991
MT 1001 .C35 B40 1992 no. 1
MT 1001 .C35 B40 1992 no. 2
MT 1001 .C35 B40 1992 no. 2 copy 2
```

You can also work with ***sets*** of call numbers using the same operators you'd use for [built-in Python sets](https://docs.python.org/2/library/stdtypes.html#set).

E.g., given the following ranges:

```pycon
>>> MT0_MT500 = pycn.cnrange('MT 0', 'MT 500')
>>> MT500_MT1000 = pycn.cnrange('MT 500', 'MT 1000')
>>> MT300_MT800 = pycn.cnrange('MT 300', 'MT 800')
>>> MT0_N0 = pycn.cnrange('MT 0', 'N 0')
>>> MT2000_N0 = pycn.cnrange('MT 2000', 'N 0')
>>> for rg in (MT0_MT500, MT500_MT1000, MT300_MT800, MT0_N0, MT2000_N0): print rg
...
<LcClass RangeSet 'MT 0' to 'MT 500'>
<LcClass RangeSet 'MT 500' to 'MT 1000'>
<LcClass RangeSet 'MT 300' to 'MT 800'>
<LcClass RangeSet 'MT 0' to 'N 0'>
<LcClass RangeSet 'MT 2000' to 'N 0'>
```

You can test whether a call number is in a particular range or set.

```pycon
>>> pycn.callnumber('MT 500 .A0 1900').classification in MT0_MT500
False
>>> pycn.callnumber('MT 500 .A0 1900').classification in MT500_MT1000
True
>>> pycn.callnumber('MS 9999.9999 .Z99 9999').classification in MT0_MT500
False
```

Test how sets relate to one another.

```pycon
>>> MT0_MT500 in MT500_MT1000
False
>>> MT0_MT500.issubset(MT500_MT1000)
False
>>> MT0_MT500 > MT500_MT1000
False
>>> MT0_MT500 < MT500_MT1000
False
>>> MT0_MT500.issuperset(MT500_MT1000)
False
>>> MT0_MT500.overlaps(MT500_MT1000)
False
>>> MT0_MT500.isdisjoint(MT500_MT1000)
True
>>> MT0_MT500.issequential(MT500_MT1000)
True
>>> MT0_MT500.isbefore(MT500_MT1000)
True
>>> MT0_MT500.extendslower(MT500_MT1000)
True
>>> MT0_MT500.overlaps(MT300_MT800)
True
>>> MT0_MT500.isdisjoint(MT300_MT800)
False
>>> MT0_MT500.isbefore(MT300_MT800)
False
>>> MT0_MT500.isafter(MT300_MT800)
False
>>> MT300_MT800.extendshigher(MT0_MT500)
True
>>> MT0_MT500.extendslower(MT300_MT800)
True
>>> MT0_MT500 in MT300_MT800
False
>>> MT300_MT800 in MT0_MT500
False
>>> MT0_MT500 in MT0_N0
True
>>> MT0_MT500.issubset(MT0_N0)
True
>>> MT0_MT500 < MT0_N0
True
```

Join two or more sets.

```pycon
>>> MT0_MT500 | MT300_MT800
<LcClass RangeSet 'MT 0' to 'MT 800'>
>>> MT0_MT500 | MT2000_N0
<LcClass RangeSet 'MT 0' to 'MT 500', 'MT 2000' to 'N 0'>
>>> MT0_MT500 | MT2000_N0 | MT500_MT1000
<LcClass RangeSet 'MT 0' to 'MT 1000', 'MT 2000' to 'N 0'>
>>> MT0_MT500.union(MT500_MT1000, MT2000_N0, MT0_N0)
<LcClass RangeSet 'MT 0' to 'N 0'>
```

Intersect two or more sets.

```pycon
>>> MT0_MT500 & MT300_MT800
<LcClass RangeSet 'MT 300' to 'MT 500'>
>>> MT0_MT500 & MT500_MT1000
<RangeSet >
>>> MT300_MT800 & MT500_MT1000 & MT0_N0
<LcClass RangeSet 'MT 500' to 'MT 800'>
>>> MT300_MT800.intersection(MT500_MT1000, MT0_N0)
<LcClass RangeSet 'MT 500' to 'MT 800'>
```

Get the difference of two or more sets.

```pycon
>>> MT0_N0 - MT0_MT500
<LcClass RangeSet 'MT 500' to 'N 0'>
>>> MT0_N0 - MT2000_N0
<LcClass RangeSet 'MT 0' to 'MT 2000'>
>>> MT0_N0 - MT2000_N0 - MT300_MT800
<LcClass RangeSet 'MT 0' to 'MT 300', 'MT 800' to 'MT 2000'>
>>> MT0_N0.difference(MT2000_N0, MT300_MT800)
<LcClass RangeSet 'MT 0' to 'MT 300', 'MT 800' to 'MT 2000'>
```

Get the symmetric difference of two sets&mdash;i.e., the set of things in one or the other but not both.

```pycon
>>> MT300_MT800 ^ MT0_N0
<LcClass RangeSet 'MT 0' to 'MT 300', 'MT 800' to 'N 0'>
>>> MT0_MT500 ^ MT2000_N0
<LcClass RangeSet 'MT 0' to 'MT 500', 'MT 2000' to 'N 0'>
```


#### Extend

You can subclass any of the call number `Unit` classes in your own projects if you need to customize their behavior.

For example, if you want your LC call numbers to be normalized a particular way for display, you can override the `for_print` method:

```python
import pycallnumber as pycn

class MyLC(pycn.units.LC):
    def for_print(self):
        lcclass = '{}{}'.format(str(self.classification.letters).upper(),
                                self.classification.number)
        cutters = ['{}{}'.format(str(c.letters.upper()), c.number)
                   for c in self.cutters]
        output = '{} .{}'.format(lcclass, ' '.join(cutters))
        if self.edition is not None:
            output = '{} {}'.format(output, self.edition)
        if self.item is not None:
            output = '{} {}'.format(output, self.item)
        return output
```
```pycon
>>> MyLC('MT 100 .C35 1992').for_print()
'MT100 .C35 1992'
>>> MyLC('MT 100 c35 1992').for_print()
'MT100 .C35 1992'
>>> MyLC('mt 100 c35 1992 v. 1').for_print()
'MT100 .C35 1992 v. 1'
>>> MyLC('mt 100 c35 e20 1992 v. 1').for_print()
'MT100 .C35 E20 1992 v. 1' 
```

`Unit` classes also have a `derive` class factory method that makes deriving new unit types simpler and less verbose. This is useful if you need to represent call numbers and other formatted strings not included in the package. For example, you could create a unit type for US dollars:

```python
import pycallnumber as pycn

DollarSign = pycn.units.Formatting.derive(
    classname='DollarSign', base_pattern=r'\$', min_length=1, max_length=1
)
DollarAmount = pycn.units.Number.derive(
    classname='DollarAmount', min_decimal_places=0, max_decimal_places=2
)
UsDollars = pycn.units.NumericSymbol.derive(
    classname='UsDollars', separator_type=None,
    groups=[{'name': 'dollarsign', 'min': 1, 'max': 1, 'type': DollarSign},
            {'name': 'amount', 'min': 1, 'max': 1, 'type': DollarAmount}]
)
```
```pycon
>>> UsDollars('$23')
<UsDollars '$23'>
>>> UsDollars('$23.00')
<UsDollars '$23.00'>
>>> UsDollars('$23.03')
<UsDollars '$23.03'>
>>> UsDollars('$23.030')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "pycallnumber/unit.py", line 143, in __init__
    super(CompoundUnit, self).__init__(cnstr, name, **options)
  File "pycallnumber/unit.py", line 28, in __init__
    self._validate_result = type(self).validate(cnstr, self.options)
  File "pycallnumber/unit.py", line 74, in validate
    raise InvalidCallNumberStringError(msg)
pycallnumber.exceptions.InvalidCallNumberStringError: '$23.030' is not a valid UsDollars Unit. It should be a string with 1 ``dollarsign`` grouping and 1 ``amount`` grouping.

**** Here is what was found while attempting to parse '$23.030' ****

'$' matched the dollarsign grouping.
'23.03' matched the ``amount`` grouping.
'0' does not match any grouping.
>>> 
>>> UsDollars('23.00')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "pycallnumber/unit.py", line 143, in __init__
    super(CompoundUnit, self).__init__(cnstr, name, **options)
  File "pycallnumber/unit.py", line 28, in __init__
    self._validate_result = type(self).validate(cnstr, self.options)
  File "pycallnumber/unit.py", line 74, in validate
    raise InvalidCallNumberStringError(msg)
pycallnumber.exceptions.InvalidCallNumberStringError: '23.00' is not a valid UsDollars Unit. It should be a string with 1 ``dollarsign`` grouping and 1 ``amount`` grouping.

**** Here is what was found while attempting to parse '23.00' ****

'23.00' does not match any grouping.
```
