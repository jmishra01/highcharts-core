from typing import Optional
from decimal import Decimal

from validator_collection import validators

from highcharts import constants, errors
from highcharts.decorators import class_sensitive, validate_types
from highcharts.metaclasses import HighchartsMeta
from highcharts.utility_classes.animation import AnimationOptions
from highcharts.utility_classes.gradients import Gradient
from highcharts.utility_classes.patterns import Pattern
from highcharts.utility_classes.shadows import ShadowOptions
from highcharts.utility_classes.ast import TextPath


class Filter(HighchartsMeta):
    """A declarative filter to control of which data labels to display.

    The declarative filter is designed for use when JavaScript callback functions are
    not available, like when the chart options require a pure JSON structure or for
    use with graphical editors. For programmatic control, use the
    :meth:`DataLabel.formatter` instead, and return ``undefined`` to disable a single
    data label."""

    def __init__(self, **kwargs):
        self._operator = None
        self._property = None
        self._value = None

        self.operator = kwargs.pop('operator', None)
        self.property_ = kwargs.pop('property_', None)
        self.value = kwargs.pop('value', None)

    @property
    def operator(self) -> Optional[str]:
        """The operator to compare by. Defaults to :obj:`None <python:None>`.

        Accepts:

          * ``'>'``
          * ``'<'``
          * ``'>='``
          * ``'<='``
          * ``'=='``
          * ``'==='``

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._operator

    @operator.setter
    def operator(self, value):
        self._operator = validators.string(value, allow_empty = True)

    @property
    def property_(self) -> Optional[str]:
        """The point property to filter by. Defaults to :obj:`None <python:None>`.

        Point options are passed directly to properties, additionally there are ``y``
        value, ``percentage``.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._property

    @property_.setter
    def property_(self, value):
        self._property = validators.string(value, allow_empty = True)

    @property
    def value(self) -> Optional[str]:
        """The value to compare against. Defaults to :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._value

    @value.setter
    def value(self, value_):
        self._value = validators.string(value_, allow_empty = True)

    @classmethod
    def from_dict(cls, as_dict):
        kwargs = {
            'operator': as_dict.pop('operator', None),
            'property_': as_dict.pop('property', None),
            'value': as_dict.pop('value', None)
        }

        return cls(**kwargs)

    def to_dict(self):
        return {
            'operator': self.operator,
            'property': self.property_,
            'value': self.value
        }


class DataLabel(HighchartsMeta):
    """Options for the series data labels, appearing next to each data point."""

    def __init__(self, **kwargs):
        self._align = None
        self._allow_overlap = False
        self._animation = None
        self._background_color = None
        self._border_color = None
        self._border_radius = None
        self._border_width = None
        self._class_name = None
        self._color = None
        self._crop = True
        self._defer = None
        self._enabled = False
        self._filter = None
        self._format = None
        self._formatter = None
        self._inside = None
        self._null_format = None
        self._null_formatter = None
        self._overflow = None
        self._padding = None
        self._position = None
        self._rotation = None
        self._shadow = False
        self._shape = None
        self._style = None
        self._text_path = None
        self._use_html = False
        self._vertical_align = None
        self._x = None
        self._y = None
        self._z = None

        self.align = kwargs.pop('align', constants.DEFAULT_DATA_LABEL.get('align', None))
        self.allow_overlap = kwargs.pop('allow_overlap', False)
        self.animation = kwargs.pop('animation', None)
        self.background_color = kwargs.pop('background_color',
                                           constants.DEFAULT_DATA_LABEL.get('background_color', None))
        self.border_color = kwargs.pop('border_color',
                                       constants.DEFAULT_DATA_LABEL.get('border_color', None))
        self.border_radius = kwargs.pop('border_radius',
                                        constants.DEFAULT_DATA_LABEL.get('border_radius', None))
        self.border_width = kwargs.pop('border_width',
                                       constants.DEFAULT_DATA_LABEL.get('border_width'))
        self.class_name = kwargs.pop('class_name',
                                     constants.DEFAULT_DATA_LABEL.get('class_name'))
        self.color = kwargs.pop('color',
                                constants.DEFAULT_DATA_LABEL.get('color'))
        self.crop = kwargs.pop('crop', False)
        self.defer = kwargs.pop('defer', constants.DEFAULT_DATA_LABEL.get('defer'))
        self.enabled = kwargs.pop('enabled', False)
        self.filter = kwargs.pop('filter', None)
        self.format = kwargs.pop('format', None)
        self.formatter = kwargs.pop('formatter', None)
        self.inside = kwargs.pop('inside', None)
        self.null_format = kwargs.pop('null_format', None)
        self.null_formatter = kwargs.pop('null_formatter', None)
        self.overflow = kwargs.pop('overflow',
                                   constants.DEFAULT_DATA_LABEL.get('overflow'))
        self.padding = kwargs.pop('padding', constants.DEFAULT_DATA_LABEL.get('padding'))
        self.position = kwargs.pop('position', constants.DEFAULT_DATA_LABEL.get('position'))
        self.rotation = kwargs.pop('rotation', constants.DEFAULT_DATA_LABEL.get('rotation'))
        self.shadow = kwargs.pop('shadow', False)
        self.shape = kwargs.pop('shape', constants.DEFAULT_DATA_LABEL.get('shape'))
        self.style = kwargs.pop('style', None)
        self.text_path = kwargs.pop('text_path', None)
        self.use_html = kwargs.pop('use_html', False)
        self.vertical_align = kwargs.pop('vertical_align',
                                         constants.DEFAULT_DATA_LABEL.get('vertical_align'))
        self.x = kwargs.pop('x', constants.DEFAULT_DATA_LABEL.get('x'))
        self.y = kwargs.pop('y', constants.DEFAULT_DATA_LABEL.get('y'))
        self.z = kwargs.pop('z', constants.DEFAULT_DATA_LABEL.get('z'))

    @property
    def align(self) -> Optional[str]:
        f"""The alignment of the data label compared to the point. Defaults to
        ``'{constants.DEFAULT_LABEL.get('align', None)}'``.

        Accepts:

          * ``'left'``
          * ``'center'``
          * ``'right'``

        .. hint::

          If right, the right side of the label should be touching the point.

        :returns: The alignment of the annotation's label.
        :rtype: :class:`str <python:str>`
        """
        return self._align

    @align.setter
    def align(self, value):
        value = validators.string(value, allow_empty = False)
        value = value.lower()
        if value not in ['left', 'center', 'right']:
            raise errors.HighchartsValueError(f'align must be either "left", "center", or '
                                              f'"right". Was: {value}')

        self._align = value

    @property
    def allow_overlap(self) -> bool:
        """If ``True``, data labels are allowed to overlap each other.

        Defaults to ``False``.

        .. hint::

          To make the labels less sensitive for overlapping, the :meth:`DataLabel.padding`
          can be set to ``0``.

        :returns: Flag indicating whether to allow data labels to overlap.
        :rtype: :class:`bool <python:bool>`
        """
        return self._allow_overlap

    @allow_overlap.setter
    def allow_overlap(self, value):
        self._allow_overlap = bool(value)

    @property
    def animation(self) -> Optional[AnimationOptions]:
        """Enable or disable the initial animation for the data labels when a series is
        displayed.

        The animation can also be set as a configuration object. Please note that this
        option only applies to the initial animation of the series itself. For other
        animations, see :class:`Chart.animation` and the ``animation`` parameter under the
        (JavaScript) API methods. The following properties are supported:

          * ``defer``: The animation delay time in milliseconds.

        .. warning::

          Due to poor performance, animation is disabled in old IE browsers for several
          chart types.

        :rtype: :class:`AnimationOptions` or :obj:`None <python:None>`
        """
        return self._animation

    @animation.setter
    @class_sensitive(AnimationOptions)
    def animation(self, value):
        self._animation = value

    @property
    def background_color(self) -> Optional[str | Gradient | Pattern]:
        """The background color or gradient for the data label. Defaults to
        :obj:`None <python:None>`.

        :returns: The backgorund color for the data label.
        :rtype: :class:`str <python:str>`, :class:`Gradient`, :class:`Pattern``, or
          :obj:`None <python:None>`
        """
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        if not value:
            self._background_color = None
        elif isinstance(value, (Gradient, Pattern)):
            self._background_color = value
        elif isinstance(value, (dict, str)) and 'linearGradient' in value:
            try:
                self._background_color = Gradient.from_json(value)
            except ValueError:
                if isinstance(value, dict):
                    self._background_color = Gradient.from_dict(value)
                else:
                    self._background_color = validators.string(value)
        elif isinstance(value, dict) and 'linear_gradient' in value:
            self._background_color = Gradient(**value)
        elif isinstance(value, (dict, str)) and 'patternOptions' in value:
            try:
                self._background_color = Pattern.from_json(value)
            except ValueError:
                if isinstance(value, dict):
                    self._background_color = Pattern.from_dict(value)
                else:
                    self._background_color = validators.string(value)
        elif isinstance(value, dict) and 'pattern_options' in value:
            self._background_color = Pattern(**value)
        else:
            raise errors.HighchartsValueError(f'Unable to resolve value to a string, '
                                              f'Gradient, or Pattern. Value received '
                                              f'was: {value}')

    @property
    def border_color(self) -> Optional[str]:
        """The border color for the data label. Defaults to
        :obj:`None <python:None>`

        :returns: The border color for the data label.
        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._border_color

    @border_color.setter
    def border_color(self, value):
        self._border_color = validators.string(value, allow_empty = True)

    @property
    def border_radius(self) -> Optional[int | float | Decimal]:
        f"""The border radius (in pixels) applied to the data label. Defaults to
        ``{constants.DEFAULT_DATA_LABEL.get('border_radius')}``.

        :returns: The border radius to apply to the data label.
        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._border_radius

    @border_radius.setter
    def border_radius(self, value):
        self._border_radius = validators.numeric(value, allow_empty = True)

    @property
    def border_width(self) -> Optional[int | float | Decimal]:
        f"""The border width (in pixels) applied to the data label. Defaults to
        ``{constants.DEFAULT_DATA_LABEL.get('border_width')}``.

        :returns: The border width to apply to the data label.
        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._border_width

    @border_width.setter
    def border_width(self, value):
        self._border_width = validators.numeric(value, allow_empty = True)

    @property
    def class_name(self) -> Optional[str]:
        f"""A classname to apply styling using CSS. Defaults to
        ``'{constants.DEFAULT_LABEL_CLASS_NAME}'``.

        :returns: The classname to apply to enable styling via CSS.
        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._class_name

    @class_name.setter
    def class_name(self, value):
        self._class_name = validators.string(value, allow_empty = True)

    @property
    def color(self) -> Optional[str]:
        """The text color for the data labels. Defaults to :obj:`None <python:None>`.

        .. note::

          For certain series types, like column or map, the data labels can be drawn
          inside the points. In this case the data label will be drawn with maximum
          contrast by default. Additionally, it will be given a ``text-outline`` style
          with the opposite color, to further increase the contrast. This can be
          overridden by setting the ``text-outline`` style to ``none`` in the
          :meth:`DataLabel.style` setting.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._color

    @color.setter
    def color(self, value):
        self._color = validators.string(value, allow_empty = True)

    @property
    def crop(self) -> bool:
        """If ``True``, hide part of the data label that falls outside the plot
        area. Defaults to ``False``.

        .. note::

          By default, the data label is moved inside the plot area as per the
          :meth:`DataLabel.overflow` setting.

        :returns: Flag indicating whether to clip a data label that extends beyond
          the plot area.
        :rtype: :class:`bool <python:bool>`
        """
        return self._crop

    @crop.setter
    def crop(self, value):
        self._crop = bool(value)

    def defer(self) -> Optional[bool | int]:
        """Whether to defer displaying the data labels until the initial series animation
        has finished. If :obj:`None <python:None>`, behaves as if set to ``True``.

        Setting to ``False`` renders the data label immediately.

        If set to ``True`` inherits the defer time set in
        :meth:`PlotOptions.series.animation`.

        If set to a number, defers the animation by that number of milliseconds.

        :rtype: :class:`bool <python:bool>` or :class:`int <python:int>` or
          :obj:`None <python:None>`
        """
        return self._defer

    @defer.setter
    def defer(self, value):
        if value is None:
            self._defer = None
        else:
            if value is True or value is False:
                self._defer = value
            else:
                self._defer = validators.integer(value)

    @property
    def enabled(self) -> Optional[bool]:
        """Enable or disable the data labels. Setting to :obj:`None <python:None>` behaves
        as if set to ``False``.

        :rtype: :class:`bool <python:bool>` or :obj:`None <python:None>`
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if value is None:
            self._enabled = None
        else:
            self._enabled = bool(value)

    @property
    def filter(self) -> Optional[Filter]:
        """A declarative filter to control of which data labels to display.

        The declarative filter is designed for use when JavaScript callback functions are
        not available, like when the chart options require a pure JSON structure or for
        use with graphical editors. For programmatic control, use the
        :meth:`DataLabel.formatter` instead, and return ``undefined`` to disable a single
        data label.

        :rtype: :class:`Filter` or :obj:`None <python:None>`
        """
        return self._filter

    @filter.setter
    @class_sensitive(Filter)
    def filter(self, value):
        self._filter = value

    @property
    def format(self) -> Optional[str]:
        f"""A format string to apply to the label. Defaults to
        ``'{constants.DEFAULT_DATA_LABEL.get('format')}'``.


        :returns: The format string to apply to the labels.
        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._format

    @format.setter
    def format(self, value):
        self._format = validators.string(value, allow_empty = True)

    @property
    def formatter(self) -> Optional[str]:
        """JavaScript callback function to format the data label. Defaults to
        :obj:`None <python:None>`.

        .. note::

          If a :meth:`DataLabel.format` is specified, the formatter will be ignored.

        :returns: A JavaScript callback function.
        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._formatter

    @formatter.setter
    def formatter(self, value):
        self._formatter = validators.string(value, allow_empty = True)

    @property
    def inside(self) -> Optional[bool]:
        """For points with an extent, like columns or map areas, whether to align the data
        label inside the box or to the actual value point. Defaults to
        ``:obj:`None <python:None>`, which behaves like ``False`` in most cases but
        ``True`` in stacked columns.

        :rtype: :class:`bool <python:bool>` or :obj:`None <python:None>`
        """
        return self._inside

    @inside.setter
    def inside(self, value):
        if value is None:
            self._inside = None
        else:
            self._inside = bool(value)

    @property
    def null_format(self) -> Optional[str]:
        """Format for points with the value of ``null``. Defaults to
        :obj:`None <python:None>`.

        .. note::

          Works analogously to :meth:`DataLabel.format`.

        .. warning::

          Can only be applied only to series which support displaying null points.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._null_format

    @null_format.setter
    def null_format(self, value):
        self._null_format = validators.string(value, allow_empty = True)

    @property
    def null_formatter(self) -> Optional[str]:
        """JavaScript callback function to format the text of the data label for visible
        null points.

        .. note::

          Works analogously to :meth:`DataLabel.formatter`.

        .. warning::

          Can only be applied only to series which support displaying null points.

        :rtype: :class:`str <python:None>` or :obj:`None <python:None>`
        """
        return self._null_formatter

    @null_formatter.setter
    def null_formatter(self, value):
        self._null_formatter = validators.string(value, allow_empty = True)

    @property
    def overflow(self) -> Optional[str]:
        f"""Configuration on how to handle a data label that overflows outside of
        the plot area.  Defaults to ``'{constants.DEFAULT_DATA_LABEL.get('overflow')}'``,
        which aligns them inside the plot area. For columns and bars, this means the data
        label will be moved inside the bar.

        .. hint::

          To display data labels outside the plot area, set ``overflow`` to ``'allow'``
          and :meth:`DataLabel.crop` to ``False``.

        Accepts:

          * ``'justify'`` - which forces the label back into the plot area
          * ``'allow'`` - which allows data labels to overflow outside of the plot area

        .. note::

          The overflow treatment is also affected by the :meth:`DataLabel.crop`
          setting.

        :returns: Configuration of overflow setting.
        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._overflow

    @overflow.setter
    def overflow(self, value):
        value = validators.string(value, allow_empty = True)
        if not value:
            self._overflow = None
        else:
            value = value.lower()
            if value not in ['justify', 'none']:
                raise errors.HighchartsValueError(f'overflow accepts "justify" or "none".'
                                                  f' Was: {value}')
            self._overflow = value

    @property
    def padding(self) -> Optional[int]:
        f"""The padding within the border box when either
        :meth:`DataLabel.border_width` or :meth:`DataLabel.background_color` is set.

        Defaults to ``{constants.DEFAULT_LABEL.get('padding')}``.

        :returns: The padding to apply to the data label.
        :rtype: :class:`int <python:int>` or :obj:`None <python:None>`
        """
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = validators.numeric(value, allow_empty = True)

    @property
    def position(self) -> Optional[str]:
        f"""Aligns data labels relative to points. Defaults to
        ``'{constants.DEFAULT_DATA_LABEL.get('position')}'``.

        Accepts the following values:

          * ``'center'`` (the default)
          * ``'left'``
          * ``'right'``

        .. note::

          If ``center`` is not possible, aligns to ``right``.

        :rtype: :class:`str <python:str>`
        """
        return self._position

    @position.setter
    def position(self, value):
        if not value:
            self._position = None
        else:
            value = validators.string(value)
            value = value.lower()
            if value not in ['center', 'left', 'right']:
                raise errors.HighchartsValueError(f'position expects a value of "center",'
                                                  f' "left", or "right". Was: {value}')
            self._position = value

    @property
    def rotation(self) -> Optional[int | float | Decimal]:
        f"""Text rotation in degrees. Defaults to
        ``{constants.DEFAULT_DATA_LABEL.get('rotation')}``

        .. warning::

          Due to a more complex structure, backgrounds, borders and padding will be lost
          on a rotated data label.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._rotation

    @property
    def shadow(self) -> bool | ShadowOptions:
        """Configuration for the shadow to apply to the data label box. Defaults to
        ``False``.

        If ``False``, no shadow is applied.

        :returns: The shadow configuration to apply or ``False``.
        :rtype: :class:`bool <python:bool>` or :class:`ShadowOptions`
        """
        return self._shadow

    @shadow.setter
    def shadow(self, value):
        if value is False:
            self._shadow = False
        elif not value:
            self._shadow = False
        else:
            value = validate_types(value,
                                   types = ShadowOptions)
            self._shadow = value

    @property
    def shape(self) -> str:
        f"""The name of the symbol to use for the border around the label. Defaults to
        ``'{constants.DEFAULT_DATA_LABEL.get('shape')}'``.

        Accepts:

          * ``'rect'``
          * ``'square'``
          * ``'circle'``
          * ``'diamond'``
          * ``'triangle'``
          * ``'callout'``

        :returns: The shape to use for the border around the label.
        :rtype: :class:`str <python:str>`
        """
        return self._shape

    @shape.setter
    def shape(self, value):
        value = validators.string(value, allow_empty = False)
        value = value.lower()
        if value not in ['callout',
                         'connector',
                         'rect',
                         'circle',
                         'diamond',
                         'triangle']:
            raise errors.HighchartsValueError(f'shape expects a supported annotation '
                                              f'label shape. Was: {value}')
        self._shape = value

    @property
    def style(self) -> Optional[str]:
        """CSS styling to apply to the annotation's label.

        The default color setting is ``"contrast"``, which is a pseudo color that
        Highcharts picks up and applies the maximum contrast to the underlying point item,
        for example the bar in a bar chart.

        ``textOutline`` is a pseudo property that applies an outline of the given width
        with the given color, which by default is the maximum contrast to the text. So a
        bright text color will result in a black text outline for maximum readability on
        a mixed background. In some cases, especially with grayscale text, the text
        outline doesn't work well, in which cases it can be disabled by setting it to
        ``"none"``. When :meth:`DataLabel.use_html` is ``True``, the ``textOutline`` will
        not be picked up. In this, case, the same effect can be acheived through the
        ``text-shadow`` CSS property.

        For some series types, where each point has an extent, like for example tree maps,
        the data label may overflow the point. There are two strategies for handling
        overflow. By default, the text will wrap to multiple lines. The other strategy is
        to set ``textOverflow`` to ellipsis, which will keep the text on one line plus it
        will break inside long words.

        :rtype: :class:`str` or :obj:`None <python:None>`
        """
        return self._style

    @style.setter
    def style(self, value):
        self._style = validators.string(value, allow_empty = True)

    @property
    def text_path(self) -> Optional[TextPath]:
        """Options for a label text which should follow marker's shape.

        .. note::

          Border and background are disabled for a label that follows a path.

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._text_path

    @text_path.setter
    @class_sensitive(TextPath)
    def text_path(self, value):
        self.text_path = value

    @property
    def use_html(self) -> bool:
        """If ``True``, will use HTML to render the data label. If ``False``, will
        use SVG or WebGL as applicable.

        Defaults to ``False``.

        :returns: Flag indicating whether to render data labels using HTML.
        :rtype: :class:`bool <python:bool>`
        """
        return self._use_html

    @use_html.setter
    def use_html(self, value):
        self._use_html = bool(value)

    @property
    def vertical_align(self) -> Optional[str]:
        """The vertical alignment of the annotation's label. Defaults to
        :obj:`None <python:None>`.

        If :obj:`None <python:None>`, the alignment will depend on the data. For example,
        in a column chart, the label would be above positive values and below negative
        values.

        Accepts:

          * ``'bottom'``
          * ``'middle'``
          * ``'top'``
          * :obj:`None <python:None>`

        :rtype: :class:`str <python:str>` or :obj:`None <python:None>`
        """
        return self._vertical_align

    @vertical_align.setter
    def vertical_align(self, value):
        value = validators.string(value, allow_empty = True)
        if not value:
            self._vertical_align = None
        else:
            value = value.lower()
            if value not in ['bottom', 'middle', 'top']:
                raise errors.HighchartsValueError(f'vertical_align expects either "top", '
                                                  f'"middle", or "bottom". Was: {value}')
            self._vertical_align = value

    @property
    def x(self) -> int | float | Decimal:
        f"""The x position offset of the label relative to the point. Defaults to
        ``{constants.DEFAULT_DATA_LABEL.get('x')}``.

        :rtype: numeric
        """
        return self._x

    @x.setter
    def x(self, value):
        value = validators.numeric(value, allow_empty = True)
        if value is None:
            self._x = 0
        else:
            self._x = value

    @property
    def y(self) -> Optional[int | float | Decimal]:
        f"""The y position offset of the label relative to the point. Defaults to
        ``{constants.DEFAULT_DATA_LABEL.get('y')}``.

        :rtype: numeric
        """
        return self._y

    @y.setter
    def y(self, value):
        value = validators.numeric(value, allow_empty = True)

    @property
    def z(self) -> Optional[int]:
        f"""The Z index of the data labels. Defaults to
        ``{constants.DEFAULT_DATA_LABEL.get('z')}``.

        If :obj:`None <python:None>`, will be placed above the series.

        .. hint::

          Use a Z index of ``2`` to display it behind the series.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._z

    @z.setter
    def z(self, value):
        self._z = validators.numeric(value, allow_empty = True)

    @classmethod
    def from_dict(cls, as_dict):
        kwargs = {
            'align': as_dict.pop('align', constants.DEFAULT_DATA_LABEL.get('align', None)),
            'allow_overlap': as_dict.pop('allowOverlap', False),
            'animation': as_dict.pop('animation', None),
            'background_color': as_dict.pop('backgroundColor',
                                            constants.DEFAULT_DATA_LABEL.get('background_color', None)),
            'border_color': as_dict.pop('borderColor',
                                        constants.DEFAULT_DATA_LABEL.get('border_color', None)),
            'border_radius': as_dict.pop('borderRadius',
                                         constants.DEFAULT_DATA_LABEL.get('border_radius', None)),
            'border_width': as_dict.pop('borderWidth',
                                        constants.DEFAULT_DATA_LABEL.get('border_width')),
            'class_name': as_dict.pop('className',
                                      constants.DEFAULT_DATA_LABEL.get('class_name')),
            'color': as_dict.pop('color',
                                 constants.DEFAULT_DATA_LABEL.get('color')),
            'crop': as_dict.pop('crop', False),
            'defer': as_dict.pop('defer', constants.DEFAULT_DATA_LABEL.get('defer')),
            'enabled': as_dict.pop('enabled', False),
            'filter': as_dict.pop('filter', None),
            'format': as_dict.pop('format', None),
            'formatter': as_dict.pop('formatter', None),
            'inside': as_dict.pop('inside', None),
            'null_format': as_dict.pop('nullFormat', None),
            'null_formatter': as_dict.pop('nullFormatter', None),
            'overflow': as_dict.pop('overflow',
                                    constants.DEFAULT_DATA_LABEL.get('overflow')),
            'padding': as_dict.pop('padding', constants.DEFAULT_DATA_LABEL.get('padding')),
            'position': as_dict.pop('position', constants.DEFAULT_DATA_LABEL.get('position')),
            'rotation': as_dict.pop('rotation', constants.DEFAULT_DATA_LABEL.get('rotation')),
            'shadow': as_dict.pop('shadow', False),
            'shape': as_dict.pop('shape', constants.DEFAULT_DATA_LABEL.get('shape')),
            'style': as_dict.pop('style', None),
            'text_path': as_dict.pop('textPath', None),
            'use_html': as_dict.pop('useHTML', False),
            'vertical_align': as_dict.pop('verticalAlign',
                                          constants.DEFAULT_DATA_LABEL.get('vertical_align')),
            'x': as_dict.pop('x', constants.DEFAULT_DATA_LABEL.get('x')),
            'y': as_dict.pop('y', constants.DEFAULT_DATA_LABEL.get('y')),
            'z': as_dict.pop('z', constants.DEFAULT_DATA_LABEL.get('z'))
        }

        return cls(**kwargs)

    def to_dict(self):
        untrimmed = {
            'align': self.align,
            'allowOverlap': self.allow_overlap,
            'animation': self.animation,
            'backgroundColor': self.background_color,
            'borderColor': self.border_color,
            'borderRadius': self.border_radius,
            'borderWidth': self.border_width,
            'className': self.class_name,
            'color': self.color,
            'crop': self.crop,
            'defer': self.defer,
            'enabled': self.enabled,
            'filter': self.filter,
            'format': self.format,
            'formatter': self.formatter,
            'inside': self.inside,
            'nullFormat': self.null_format,
            'nullFormatter': self.null_formatter,
            'overflow': self.overflow,
            'padding': self.padding,
            'position': self.position,
            'rotation': self.rotation,
            'shadow': self.shadow,
            'shape': self.shape,
            'style': self.style,
            'textPath': self.text_path,
            'useHTML': self.use_html,
            'verticalAlign': self.vertical_align,
            'x': self.x,
            'y': self.y,
            'z': self.z
        }
        as_dict = self.trim_dict(untrimmed)

        return as_dict