from typing import Optional, List, Dict
from decimal import Decimal

from validator_collection import validators, checkers

from highcharts_core import constants, errors
from highcharts_core.options.series.data.cartesian import CartesianData


class VectorData(CartesianData):
    """Variant of :class:`CartesianData` which extends the data point with ``direction``
    and ``length`` attributes."""

    def __init__(self, **kwargs):
        self._direction = None
        self._length = None

        self.direction = kwargs.get('direction', None)
        self.length = kwargs.get('length', None)

        super().__init__(**kwargs)

    @property
    def direction(self) -> Optional[int | float | Decimal]:
        """The vector direction expressed in degrees, where ``0`` is north (pointing
        towards south). Defaults to :obj:`None <python:None>`.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = validators.numeric(value, allow_empty = True)

    @property
    def length(self) -> Optional[int | float | Decimal]:
        """The length of the vector. Defaults to :obj:`None <python:None>`.

        .. note::

          The actual length rendered on-screen will be tied to
          :meth:`VectorSeries.vector_length`.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._length

    @length.setter
    def length(self, value):
        self._length = validators.numeric(value, allow_empty = True)

    @classmethod
    def from_array(cls, value):
        if not value:
            return []
        elif checkers.is_string(value):
            try:
                value = validators.json(value)
            except (ValueError, TypeError):
                pass
        elif not checkers.is_iterable(value):
            value = [value]

        collection = []
        for item in value:
            if checkers.is_type(item, 'VectorData'):
                as_obj = item
            elif checkers.is_dict(item):
                as_obj = cls.from_dict(item)
            elif item is None or isinstance(item, constants.EnforcedNullType):
                as_obj = cls()
            elif len(item) == 4:
                as_obj = cls(x = item[0],
                             y = item[1],
                             length = item[2],
                             direction = item[3])
            elif len(item) == 3:
                as_obj = cls(x = None,
                             y = item[0],
                             length = item[1],
                             direction = item[2])
            else:
                raise errors.HighchartsValueError(f'each data point supplied must either '
                                                  f'be a Vector Data Point or be '
                                                  f'coercable to one. Could not coerce: '
                                                  f'{item}')

            if checkers.is_string(as_obj.x) and not as_obj.name:
                as_obj.name = as_obj.x
                as_obj.x = None
            collection.append(as_obj)

        return collection

    @classmethod
    def _get_props_from_array(cls) -> List[str]:
        """Returns a list of the property names that can be set using the
        :meth:`.from_array() <highcharts_core.options.series.data.base.DataBase.from_array>`
        method.
        
        :rtype: :class:`list <python:list>` of :class:`str <python:str>`
        """
        return ['x', 'y', 'length', 'direction', 'name']

    def to_array(self, force_object = False) -> List | Dict:
        """Generate the array representation of the data point (the inversion 
        of 
        :meth:`.from_array() <highcharts_core.options.series.data.base.DataBase.from_array>`).
        
        .. warning::
        
          If the data point *cannot* be serialized to a JavaScript array,
          this method will instead return the untrimmed :class:`dict <python:dict>`
          representation of the data point as a fallback.

        :param force_object: if ``True``, forces the return of the instance's
          untrimmed :class:`dict <python:dict>` representation. Defaults to ``False``.
        :type force_object: :class:`bool <python:bool>`

        :returns: The array representation of the data point.
        :rtype: :class:`list <python:list>` of values or :class:`dict <python:dict>`
        """
        if self.requires_js_object or force_object:
            return self._to_untrimmed_dict()
        
        if self.y is not None:
            y = self.y
        else:
            y = constants.EnforcedNull
            
        if self.length is not None:
            length = self.length
        else:
            length = constants.EnforcedNull
            
        if self.direction is not None:
            direction = self.direction
        else:
            direction = constants.EnforcedNull
            
        if self.x is not None:
            x = self.x
        elif self.name is not None:
            x = self.name
        else:
            x = constants.EnforcedNull
        
        if self.x is None and self.name is None:
            return [y, length, direction]
        
        return [x, y, length, direction]

    @classmethod
    def _get_kwargs_from_dict(cls, as_dict):
        """Convenience method which returns the keyword arguments used to initialize the
        class from a Highcharts Javascript-compatible :class:`dict <python:dict>` object.

        :param as_dict: The HighCharts JS compatible :class:`dict <python:dict>`
          representation of the object.
        :type as_dict: :class:`dict <python:dict>`

        :returns: The keyword arguments that would be used to initialize an instance.
        :rtype: :class:`dict <python:dict>`

        """
        kwargs = {
            'accessibility': as_dict.get('accessibility', None),
            'class_name': as_dict.get('className', None),
            'color': as_dict.get('color', None),
            'color_index': as_dict.get('colorIndex', None),
            'custom': as_dict.get('custom', None),
            'description': as_dict.get('description', None),
            'events': as_dict.get('events', None),
            'id': as_dict.get('id', None),
            'label_rank': as_dict.get('labelrank', None),
            'name': as_dict.get('name', None),
            'selected': as_dict.get('selected', None),

            'data_labels': as_dict.get('dataLabels', None),
            'drag_drop': as_dict.get('dragDrop', None),
            'drilldown': as_dict.get('drilldown', None),
            'marker': as_dict.get('marker', None),
            'x': as_dict.get('x', None),
            'y': as_dict.get('y', None),

            'direction': as_dict.get('direction', None),
            'length': as_dict.get('length', None),
        }

        return kwargs

    def _to_untrimmed_dict(self, in_cls = None) -> dict:
        untrimmed = {
            'direction': self.direction,
            'length': self.length,

            'dataLabels': self.data_labels,
            'dragDrop': self.drag_drop,
            'drilldown': self.drilldown,
            'marker': self.marker,
            'x': self.x,
            'y': self.y,

            'accessibility': self.accessibility,
            'className': self.class_name,
            'color': self.color,
            'colorIndex': self.color_index,
            'custom': self.custom,
            'description': self.description,
            'events': self.events,
            'id': self.id,
            'labelrank': self.label_rank,
            'name': self.name,
            'selected': self.selected,
        }

        return untrimmed
