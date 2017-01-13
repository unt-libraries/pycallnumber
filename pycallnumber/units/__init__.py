"""Work with predefined types of call numbers and call number parts."""

from simple import Alphabetic, Numeric, Formatting
from compound import AlphaNumeric, AlphaSymbol, NumericSymbol,\
                     AlphaNumericSymbol
from numbers import Number, OrdinalNumber
from dates import DateString
from callnumbers.parts import Cutter, Edition, Item
from callnumbers import LC, LcClass, Dewey, DeweyClass, SuDoc, Agency,\
                        AgencyDotSeries, Local
