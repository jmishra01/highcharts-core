from typing import Optional

from highcharts.decorators import class_sensitive
from highcharts.metaclasses import HighchartsMeta
from highcharts.utility_classes.javascript_functions import CallbackFunction


class AnnotationControlPointOption(HighchartsMeta):
    """Options for annotation's control points."""

    def __init__(self, **kwargs):
        self._positioner = None

        self.positioner = kwargs.get('positioner', None)

    @property
    def positioner(self) -> Optional[CallbackFunction]:
        """A JavaScript callback function to modify annotation's positioner controls.

        The JavaScript function should receive two arguments, ``this`` being the
        annotation's control point and ``target`` being the annotation's controllable.

        :returns: A JavaScript callback function to modify the annotation's positioner
          controls.
        :rtype: :class:`CallbackFunction` or :obj:`None <python:None>`
        """
        return self._positioner

    @positioner.setter
    @class_sensitive(CallbackFunction)
    def positioner(self, value):
        self._positioner = value

    @classmethod
    def from_dict(cls, as_dict):
        kwargs = {
            'positioner': as_dict.get('positioner', None)
        }

        return cls(**kwargs)

    def _to_untrimmed_dict(self) -> dict:
        untrimmed = {
            'positioner': self.positioner
        }

        return untrimmed
