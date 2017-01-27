"""Work with standard call number types."""
from __future__ import absolute_import

from .dewey import Dewey, DeweyClass
from .lc import LC, LcClass
from .sudoc import SuDoc, Agency, AgencyDotSeries
from .local import Local

__all__ = [Dewey, DeweyClass, LC, LcClass, SuDoc, Agency, AgencyDotSeries,
           Local]
