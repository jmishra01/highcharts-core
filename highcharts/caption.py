from typing import Optional, Any
from decimal import Decimal

from validator_collection import validators

from highcharts import constants, errors
from highcharts.metaclasses import HighchartsMeta


class Caption(HighchartsMeta):
    """The chart's caption, which will render below the chart and will be part of
    exported charts.

    .. note::

      The caption can be updated after chart initialization in JavaScript through the
      ``Chart.update()`` or ``Chart.caption.update()`` methods.

    """

    def __init__(self, **kwargs):
        self._align = constants.DEFAULT_CAPTION_ALIGN
        self._floating = False
        self._margin = constants.DEFAULT_CAPTION_MARGIN
        self._style = constants.DEFAULT_CAPTION_STYLE
        self._text = None
        self._use_html = False
        self._vertical_align = constants.DEFAULT_CAPTION_VERTICAL_ALIGN
        self._x = constants.DEFAULT_CAPTION_X
        self._y = constants.DEFAULT_CAPTION_Y

        self.align = kwargs.pop('align', constants.DEFAULT_CAPTION_ALIGN)
        self.floating = kwargs.pop('floating', False)
        self.margin = kwargs.pop('margin', constants.DEFAULT_CAPTION_MARGIN)
        self.style = kwargs.pop('style', None)
        self.text = kwargs.pop('text', None)
        self.use_html = kwargs.pop('use_html', False)
        self.vertical_align = kwargs.pop('vertical_align',
                                         constants.DEFAULT_CAPTION_VERTICAL_ALIGN)

    @property
    def align(self) -> str:
        f"""The alignment of the caption. Defaults to
        ``'{constants.DEFAULT_CAPTION_ALIGN}'``.

        Accepts:

          * ``'left'``
          * ``'center'``
          * ``'right'``

        :returns: The alignment of the caption.
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
    def floating(self) -> bool:
        """If ``True`, sets the caption to floating. When the caption is floating, the
        plot area will not move to make space for it. Defaults to ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._floating

    @floating.setter
    def floating(self, value):
        self._floating = bool(value)

    @property
    def margin(self) -> Any[int, float, Decimal]:
        f"""The margin between the caption and the plot area. Defaults to
        ``{constants.DEFAULT_CAPTION_MARGIN}``.

        :rtype: numeric
        """
        return self._margin

    @margin.setter
    def margin(self, value):
        self._margin = validators.numeric(value)

    @property
    def style(self) -> Optional[str]:
        f"""CSS styling to apply to the caption. Defaults to
        ``{constants.DEFAULT_CAPTION_STYLE}``.

        :rtype: :class:`str` or :obj:`None <python:None>`
        """
        return self._style

    @style.setter
    def style(self, value):
        self._style = validators.string(value, allow_empty = True)

    @property
    def text(self) -> str:
        """The caption text of the chart. Defaults to an empty string (``''``).

        :rtype: :class:`str <python:str>`
        """
        return self._text or ''

    @text.setter
    def text(self, value):
        self._text = validators.string(value, allow_empty = True)

    @property
    def use_html(self) -> bool:
        """If ``True``, will use HTML to render the caption. If ``False``, will
        use SVG or WebGL as applicable.

        Defaults to ``False``.

        :returns: Flag indicating whether to render the caption using HTML.
        :rtype: :class:`bool <python:bool>`
        """
        return self._use_html

    @use_html.setter
    def use_html(self, value):
        self._use_html = bool(value)

    @property
    def vertical_align(self) -> str:
        f"""The vertical alignment of the caption. Defaults to
        ``{constants.DEFAULT_CAPTION_VERTICAL_ALIGN}``.

        Accepts:

          * ``'bottom'``
          * ``'middle'``
          * ``'top'``

        :rtype: :class:`str <python:str>`
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
    def x(self) -> Any[int, float, Decimal]:
        f"""The x position of the caption relative to the alignment within
        :meth:`Options.chart.spacing_left` and :meth:`Option.chart.spacing_right`.
        Defaults to ``{constants.DEFAULT_CAPTION_X}``.

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
    def y(self) -> Optional[int]:
        f"""The y position of the caption relative to the alignment within
        :meth:`Options.chart.spacing_left` and :meth:`Option.chart.spacing_right`.
        Defaults to ``{constants.DEFAULT_CAPTION_Y}``.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = validators.numeric(value, allow_empty = True)

    @classmethod
    def from_dict(cls, as_dict):
        kwargs = {
            'align': as_dict.pop('align',
                                 constants.DEFAULT_CAPTION_ALIGN),
            'floating': as_dict.pop('floating', False),
            'margin': as_dict.pop('margin', constants.DEFAULT_CAPTION_MARGIN),
            'style': as_dict.pop('style', None),
            'text': as_dict.pop('text', None),
            'use_html': as_dict.pop('useHTML', False),
            'vertical_align': as_dict.pop('verticalAlign',
                                          constants.DEFAULT_CAPTION_VERTICAL_ALIGN),
            'x': as_dict.pop('x', constants.DEFAULT_CAPTION_X),
            'y': as_dict.pop('y', constants.DEFAULT_CAPTION_Y)
        }

        return cls(**kwargs)

    def to_dict(self):
        return {
            'align': self.align,
            'floating': self.floating,
            'margin': self.margin,
            'style': self.style,
            'text': self.text,
            'useHTML': self.use_html,
            'verticalAlign': self.vertical_align,
            'x': self.x,
            'y': self.y
        }
