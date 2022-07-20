from typing import Optional, List
from decimal import Decimal

from validator_collection import validators

from highcharts import constants, errors
from highcharts.decorators import class_sensitive, validate_types
from highcharts.plot_options.generic import GenericTypeOptions
from highcharts.plot_options.levels import SunburstLevelOptions, LevelSize
from highcharts.utility_classes.gradients import Gradient
from highcharts.utility_classes.patterns import Pattern
from highcharts.utility_classes.breadcrumbs import BreadcrumbOptions
from highcharts.utility_classes.shadows import ShadowOptions


class SunburstOptions(GenericTypeOptions):
    """General options to apply to all Sunburst series types.

    A Sunburst displays hierarchical data, where a level in the hierarchy is
    represented by a circle. The center represents the root node of the tree. The
    visualization bears a resemblance to both treemap and pie charts.

    .. figure:: _static/sunburst-example.png
      :alt: Sunburst Example Chart
      :align: center

    """

    def __init__(self, **kwargs):
        self._color_index = None
        self._crisp = None
        self._shadow = None
        self._allow_traversing_tree = None
        self._border_color = None
        self._border_width = None
        self._breadcrumbs = None
        self._center = None
        self._color_by_point = None
        self._fill_color = None
        self._level_is_constant = None
        self._levels = None
        self._level_size = None
        self._root_id = None
        self._size = None
        self._sliced_offset = None
        self._start_angle = None

        self.color_index = kwargs.pop('color_index', None)
        self.crisp = kwargs.pop('crisp', None)
        self.shadow = kwargs.pop('shadow', None)
        self.allow_traversing_tree = kwargs.pop('allow_traversing_tree', None)
        self.border_color = kwargs.pop('border_color', None)
        self.border_width = kwargs.pop('border_width', None)
        self.breadcrumbs = kwargs.pop('breadcrumbs', None)
        self.center = kwargs.pop('center', None)
        self.color_by_point = kwargs.pop('color_by_point', None)
        self.fill_color = kwargs.pop('fill_color', None)
        self.level_is_constant = kwargs.pop('level_is_constant', None)
        self.levels = kwargs.pop('levels', None)
        self.level_size = kwargs.pop('level_size', None)
        self.root_id = kwargs.pop('root_id', None)
        self.size = kwargs.pop('size', None)
        self.sliced_offset = kwargs.pop('sliced_offset', None)
        self.start_angle = kwargs.pop('start_angle', None)

        super().__init__(**kwargs)

    @property
    def allow_traversing_tree(self) -> Optional[bool]:
        """If ``True``, the user can click on a point which is a parent and zoom in on its
        children. Defaults to ``False``.

        :rtype: :class:`bool <python:bool>` or :obj:`None <python:None>`
        """
        return self._allow_traversing_tree

    @allow_traversing_tree.setter
    def allow_traversing_tree(self, value):
        if value is None:
            self._allow_traversing_tree = None
        else:
            self._allow_traversing_tree = bool(value)

    @property
    def border_color(self) -> Optional[str | Gradient | Pattern]:
        """The color of the border surrounding each slice. When :obj:`None <python:None>`,
        the border takes the same color as the slice fill. This can be used together with
        a :meth:`border_width <PieOptions.border_width>` to fill drawing gaps created by
        antialiazing artefacts in borderless pies. Defaults to ``'#ffffff'``.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._border_color

    @border_color.setter
    def border_color(self, value):
        if not value:
            self._border_color = None
        elif isinstance(value, (Gradient, Pattern)):
            self._border_color = value
        elif isinstance(value, (dict, str)) and 'linearGradient' in value:
            try:
                self._border_color = Gradient.from_json(value)
            except ValueError:
                if isinstance(value, dict):
                    self._border_color = Gradient.from_dict(value)
                else:
                    self._border_color = validators.string(value)
        elif isinstance(value, dict) and 'linear_gradient' in value:
            self._border_color = Gradient(**value)
        elif isinstance(value, (dict, str)) and 'patternOptions' in value:
            try:
                self._border_color = Pattern.from_json(value)
            except ValueError:
                if isinstance(value, dict):
                    self._border_color = Pattern.from_dict(value)
                else:
                    self._border_color = validators.string(value)
        elif isinstance(value, dict) and 'pattern_options' in value:
            self._border_color = Pattern(**value)
        else:
            raise errors.HighchartsValueError(f'Unable to resolve value to a string, '
                                              f'Gradient, or Pattern. Value received '
                                              f'was: {value}')

    @property
    def border_width(self) -> Optional[int | float | Decimal]:
        """The width of the border surrounding each slice. Defaults to ``1``.

        When setting the border width to ``0``, there may be small gaps between the slices
        due to SVG antialiasing artefacts. To work around this, keep the border width at
        ``0.5`` or ``1``, but set the :meth:`border_color <PieOptions.border_color>` to
        :obj:`None <python:None>` instead.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._border_width

    @border_width.setter
    def border_width(self, value):
        self._border_width = validators.numeric(value,
                                                allow_empty = True,
                                                minimum = 0)

    @property
    def breadcrumbs(self) -> Optional[BreadcrumbOptions]:
        """Options for the breadcrumbs, the navigation at the top leading the way up
        through the traversed levels. Defaults to :obj:`None <python:None>`.

        """
        return self._breadcrumbs

    @breadcrumbs.setter
    @class_sensitive(BreadcrumbOptions)
    def breadcrumbs(self, value):
        self._breadcrumbs = value

    @property
    def center(self) -> Optional[List[str | int | float | Decimal | constants.EnforcedNullType]]:
        """The center of the sunburst chart relative to the plot area.

        Can be percentages or pixel values. The default behaviour if
        :obj:`None <python:None>` is to center the pie so that all slices and data labels
        are within the plot area. As a consequence, the pie may actually jump around in a
        chart with dynamic values, as the data labels move. In that case, the center
        should be explicitly set, for example to ``["50%", "50%"]``.

        Defaults to ``['50%', '50%']``.

        :rtype: :obj:`None <python:None>` or :class:`list <python:list>` of numeric or
          :class:`str <python:str>` values
        """
        return self._center

    @center.setter
    def center(self, value):
        if not value:
            self._center = None
        else:
            value = validators.iterable(value)
            if len(value) != 2:
                raise errors.HighchartsValueError(f'center expects a 2-member array. '
                                                  f'Received a {len(value)}-member array.')
            processed_values = []
            for item in value:
                try:
                    item = validators.string(value)
                    if '%' not in item:
                        raise ValueError
                except ValueError:
                    item = validators.numeric(value)

                processed_values.append(item)

            self._center = processed_values

    @property
    def color_by_point(self) -> bool:
        """When using automatic point colors pulled from the global colors or
        series-specific collections, this option determines whether the chart should
        receive one color per series (``False``) or one color per point (``True``).

        Defaults to ``True``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._color_by_point

    @color_by_point.setter
    def color_by_point(self, value):
        self._color_by_point = bool(value)

    @property
    def color_index(self) -> Optional[int]:
        """When operating in :term:`styled mode`, a specific color index to use for the
        series, so that its graphic representations are given the class name
        ``highcharts-color-{n}``.

        Defaults to :obj:`None <python:None>`.

        :rtype: :class:`int <python:int>` or :obj:`None <python:None>`
        """
        return self._color_index

    @color_index.setter
    def color_index(self, value):
        self._color_index = validators.integer(value,
                                               allow_empty = True,
                                               minimum = 0)

    @property
    def crisp(self) -> Optional[bool]:
        """If ``True``, each point or column edge is rounded to its nearest pixel in order
        to render sharp on screen. Defaults to ``True``.

        .. hint::

          In some cases, when there are a lot of densely packed columns, this leads to
          visible difference in column widths or distance between columns. In these cases,
          setting ``crisp`` to ``False`` may look better, even though each column is
          rendered blurry.

        :rtype: :class:`bool <python:bool>` or :obj:`None <python:None>`
        """
        return self._crisp

    @crisp.setter
    def crisp(self, value):
        if value is None:
            self._crisp = None
        else:
            self._crisp = bool(value)

    @property
    def fill_color(self) -> Optional[str | Gradient | Pattern]:
        """If the total sum of the pie's values is ``0``, the series is represented as an
        empty circle . The ``fill_color`` setting defines the color of that circle.
        Use :meth:`PieOptions.border_width` to set the border thickness.

        Defaults to :obj:`None <python:None>`.

        :rtype: :obj:`None <python:None>`, :class:`Gradient`, or :class:`Pattern`
        """
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        if not value:
            self._fill_color = None
        elif isinstance(value, (Gradient, Pattern)):
            self._fill_color = value
        elif isinstance(value, (dict, str)) and 'linearGradient' in value:
            try:
                self._fill_color = Gradient.from_json(value)
            except ValueError:
                if isinstance(value, dict):
                    self._fill_color = Gradient.from_dict(value)
                else:
                    self._fill_color = validators.string(value)
        elif isinstance(value, dict) and 'linear_gradient' in value:
            self._fill_color = Gradient(**value)
        elif isinstance(value, (dict, str)) and 'patternOptions' in value:
            try:
                self._fill_color = Pattern.from_json(value)
            except ValueError:
                if isinstance(value, dict):
                    self._fill_color = Pattern.from_dict(value)
                else:
                    self._fill_color = validators.string(value)
        elif isinstance(value, dict) and 'pattern_options' in value:
            self._fill_color = Pattern(**value)
        else:
            raise errors.HighchartsValueError(f'Unable to resolve value to a string, '
                                              f'Gradient, or Pattern. Value received '
                                              f'was: {value}')

    @property
    def level_is_constant(self) -> Optional[bool]:
        """If ``True``, the level will be the same as the tree structure. If ``False``,
        the first level visible when drilling is considered to be level one. Defaults to
        ``True``.

        :rtype: :class:`bool <python:bool>` or :obj:`None <python:None>`
        """
        return self._level_is_constant

    @level_is_constant.setter
    def level_is_constant(self, value):
        if value is None:
            self._level_is_constant = None
        else:
            self._level_is_constant = bool(value)

    @property
    def levels(self) -> Optional[List[SunburstLevelOptions]]:
        """Set options on specific levels. Takes precedence over series options, but not
        node and link options.

        :rtype: :obj:`None <python:None>`, or :class:`list <python:list>` of
          :class:`SunburstLevelOptions`
        """
        return self._levels

    @levels.setter
    @class_sensitive(SunburstLevelOptions, force_iterable = True)
    def levels(self, value):
        self._levels = value

    @property
    def level_size(self) -> Optional[LevelSize]:
        """Determines the width of the ring per level.

        :rtype: :class:`LevelSize` or :obj:`None <python:None>`
        """
        return self._level_size

    @level_size.setter
    @class_sensitive(LevelSize)
    def level_size(self, value):
        self._level_size = value

    @property
    def root_id(self) -> Optional[str]:
        """Indicates which point to use as a root in the visualization. Defaults to
        :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._root_id

    @root_id.setter
    def root_id(self, value):
        self._root_id = validators.string(value, allow_empty = True)

    @property
    def shadow(self) -> Optional[bool | ShadowOptions]:
        """Configuration for the shadow to apply to the tooltip. Defaults to
        ``False``.

        If ``False``, no shadow is applied.

        :returns: The shadow configuration to apply or a boolean setting which hides the
          shadow or displays the default shadow.
        :rtype: :class:`bool <python:bool>` or :class:`ShadowOptions`
        """
        return self._shadow

    @shadow.setter
    def shadow(self, value):
        if isinstance(value, bool):
            self._shadow = value
        elif not value:
            self._shadow = None
        else:
            value = validate_types(value,
                                   types = ShadowOptions)
            self._shadow = value

    @property
    def size(self) -> Optional[str | int]:
        """The diameter of the pie relative to the plot area, expressed as a percentage or
        pixel value given as an integer.

        If :obj:`None <python:None>`, scales the pie to the plot area and gives room for
        data labels within the plot area.

        .. note::

          :meth:`PieOptions.sliced_offset` is also included in the default size
          calculation. As a consequence, the size of the pie may vary when points are
          updated and data labels more around. In that case it is best to set a fixed
          value, for example ``"75%"``.

        :rtype: :class:`str <python:str>`, :class:`int <python:int>`, or
          :obj:`None <python:None>`
        """
        return self._size

    @size.setter
    def size(self, value):
        if value is None:
            self._size = None
        else:
            try:
                value = validators.string(value)
                if '%' not in value:
                    raise ValueError
            except ValueError:
                value = validators.integer(value, minimum = 0)

            self._size = value

    @property
    def sliced_offset(self) -> Optional[int | float | Decimal]:
        """If a point is sliced, moved out from the center, how many pixels should it be
        moved? Defaults to ``10``.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._sliced_offset

    @sliced_offset.setter
    def sliced_offset(self, value):
        self._sliced_offset = validators.numeric(value, allow_empty = True)

    @property
    def start_angle(self) -> Optional[int | float | Decimal]:
        """The start angle of the dependency wheel, in degrees where ``0`` is up. Defaults
        to ``0``.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        self._start_angle = validators.numeric(value,
                                               allow_empty = True,
                                               minimum = 0,
                                               maximum = 360)

    @classmethod
    def _get_kwargs_from_dict(cls, as_dict):
        kwargs = {
            'accessibility': as_dict.pop('accessibility', None),
            'allow_point_select': as_dict.pop('allowPointSelect', False),
            'animation': as_dict.pop('animation', None),
            'class_name': as_dict.pop('className', None),
            'clip': as_dict.pop('clip', True),
            'color': as_dict.pop('color', None),
            'cursor': as_dict.pop('cursor', None),
            'custom': as_dict.pop('custom', None),
            'dash_style': as_dict.pop('dashStyle', None),
            'data_labels': as_dict.pop('dataLabels', None),
            'description': as_dict.pop('description', None),
            'enable_mouse_tracking': as_dict.pop('enableMouseTracking', True),
            'events': as_dict.pop('events', None),
            'include_in_data_export': as_dict.pop('includeInDataExport', None),
            'keys': as_dict.pop('keys', None),
            'label': as_dict.pop('label', None),
            'linked_to': as_dict.pop('linkedTo', None),
            'marker': as_dict.pop('marker', None),
            'on_point': as_dict.pop('onPoint', None),
            'opacity': as_dict.pop('opacity', None),
            'point': as_dict.pop('point', None),
            'point_description_formatter': as_dict.pop('pointDescriptionFormatter', None),
            'selected': as_dict.pop('selected', False),
            'show_checkbox': as_dict.pop('showCheckbox', False),
            'show_in_legend': as_dict.pop('showInLegend', None),
            'skip_keyboard_navigation': as_dict.pop('skipKeyboardNavigation', None),
            'states': as_dict.pop('states', None),
            'threshold': as_dict.pop('threshold', None),
            'tooltip': as_dict.pop('tooltip', None),
            'turbo_threshold': as_dict.pop('turboThreshold', None),
            'visible': as_dict.pop('visible', True),

            'color_index': as_dict.pop('colorIndex', None),
            'crisp': as_dict.pop('crisp', None),
            'shadow': as_dict.pop('shadow', None),
            'allow_traversing_tree': as_dict.pop('allowTraversingTree', None),
            'border_color': as_dict.pop('borderColor', None),
            'border_width': as_dict.pop('borderWidth', None),
            'breadcrumbs': as_dict.pop('breadcrumbs', None),
            'center': as_dict.pop('center', None),
            'color_by_point': as_dict.pop('colorByPoint', None),
            'fill_color': as_dict.pop('fillColor', None),
            'level_is_constant': as_dict.pop('levelIsConstant', None),
            'levels': as_dict.pop('levels', None),
            'level_size': as_dict.pop('levelSize', None),
            'root_id': as_dict.pop('rootId', None),
            'size': as_dict.pop('size', None),
            'sliced_offset': as_dict.pop('slicedOffset', None),
            'start_angle': as_dict.pop('startAngle', None)
        }

        return kwargs

    def to_dict(self) -> dict:
        untrimmed = {
            'colorIndex': self.color_index,
            'crisp': self.crisp,
            'shadow': self.shadow,
            'allowTraversingTree': self.allow_traversing_tree,
            'borderColor': self.border_color,
            'borderWidth': self.border_width,
            'breadcrumbs': self.breadcrumbs,
            'center': self.center,
            'colorByPoint': self.color_by_point,
            'fillColor': self.fill_color,
            'levelIsConstant': self.level_is_constant,
            'levels': self.levels,
            'levelSize': self.level_size,
            'rootId': self.root_id,
            'size': self.size,
            'slicedOffset': self.sliced_offset,
            'startAngle': self.start_angle
        }
        parent_as_dict = super(self).to_dict()

        for key in parent_as_dict:
            untrimmed[key] = parent_as_dict[key]

        return self.trim_dict(untrimmed)