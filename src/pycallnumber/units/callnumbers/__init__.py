"""Work with standard call number types."""
from __future__ import absolute_import

from pycallnumber.units.callnumbers.dewey import Dewey, DeweyClass
from pycallnumber.units.callnumbers.lc import LC, LcClass
from pycallnumber.units.callnumbers.sudoc import SuDoc, Agency, AgencyDotSeries
from pycallnumber.units.callnumbers.local import Local

__all__ = ['Dewey', 'DeweyClass', 'LC', 'LcClass', 'SuDoc', 'Agency',
           'AgencyDotSeries', 'Local']
