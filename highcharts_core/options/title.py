from typing import Optional
from decimal import Decimal

from validator_collection import validators

from highcharts_core import errors
from highcharts_core.metaclasses import HighchartsMeta


class Title(HighchartsMeta):
    """The chart's main title."""

    def __init__(self, **kwargs):
        self._align = None
        self._floating = None
        self._margin = None
        self._style = None
        self._text = None
        self._use_html = None
        self._vertical_align = None
        self._width_adjust = None
        self._x = None
        self._y = None

        self.align = kwargs.get('align', None)
        self.floating = kwargs.get('floating', None)
        self.margin = kwargs.get('margin', None)
        self.style = kwargs.get('style', None)
        self.text = kwargs.get('text', None)
        self.use_html = kwargs.get('use_html', None)
        self.vertical_align = kwargs.get('vertical_align', None)
        self.width_adjust = kwargs.get('width_adjust', None)
        self.x = kwargs.get('x', None)
        self.y = kwargs.get('y', None)

    @property
    def align(self) -> Optional[str]:
        """The horizontal alignment of the title. Defaults to
        ``'center'``.

        Accepts:

          * ``'left'``
          * ``'center'``
          * ``'right'``

        :returns: The alignment of the title.
        :rtype: :class:`str <python:str>`
        """
        return self._align

    @align.setter
    def align(self, value):
        value = validators.string(value, allow_empty = True)
        if value:
            value = value.lower()
            if value not in ['left', 'center', 'right']:
                raise errors.HighchartsValueError(f'align must be either "left", "center"'
                                                  f', or "right". Was: {value}')

        self._align = value

    @property
    def floating(self) -> Optional[bool]:
        """If ``True`, sets the title to floating. When the title is floating, the
        plot area will not move to make space for it. Defaults to ``False``.

        :rtype: :class:`bool <python:bool>`
        """
        return self._floating

    @floating.setter
    def floating(self, value):
        if value is None:
            self._floating = None
        else:
            self._floating = bool(value)

    @property
    def margin(self) -> Optional[int | float | Decimal]:
        """The margin between the title and the plot area, or if a subtitle is present,
        the margin between the subtitle and the plot area. Defaults to ``15``.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._margin

    @margin.setter
    def margin(self, value):
        self._margin = validators.numeric(value, allow_empty = True)

    @property
    def style(self) -> Optional[str]:
        """CSS styling to apply to the title. Defaults to
        ``'{ "color": "#333333", "fontSize": "18px" }'``.

         .. note::

           Use this for font styling, but use :meth:`Title.align`, :meth:`Title.x`, and
           :meth:`Title.y` for text alignment.

        :rtype: :class:`str` or :obj:`None <python:None>`
        """
        return self._style

    @style.setter
    def style(self, value):
        self._style = validators.string(value, allow_empty = True, coerce_value = True)

    @property
    def text(self) -> Optional[str]:
        """The text of the title. Defaults to ``'Chart title'``.

        .. note::

          To disable the title, set to :obj:`None <python:None>`.

        :rtype: :class:`str <python:str>`
        """
        return self._text

    @text.setter
    def text(self, value):
        self._text = validators.string(value, allow_empty = True)

    @property
    def use_html(self) -> Optional[bool]:
        """If ``True``, will use HTML to render the title. If ``False``, will
        use SVG or WebGL as applicable.

        Defaults to ``False``.

        :returns: Flag indicating whether to render the title using HTML.
        :rtype: :class:`bool <python:bool>`
        """
        return self._use_html

    @use_html.setter
    def use_html(self, value):
        if value is None:
            self._use_html = None
        else:
            self._use_html = bool(value)

    @property
    def vertical_align(self) -> Optional[str]:
        """The vertical alignment of the title. Defaults to
        :obj:`None <python:None>`.

        Accepts:

          * ``'bottom'``
          * ``'middle'``
          * ``'top'``

        .. note::

          When set to ``'middle'``, the title behaves as if :meth:`Subtitle.floating`
          were set to ``True``.

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
    def width_adjust(self) -> Optional[int | float | Decimal]:
        """Adjustment made to the title width, normally to reserve space for the export
        hamburger menu. Defaults to ``-44``.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._width_adjust

    @width_adjust.setter
    def width_adjust(self, value):
        self._width_adjust = validators.numeric(value, allow_empty = True)

    @property
    def x(self) -> Optional[int | float | Decimal]:
        """The x position of the title relative to the alignment within
        :meth:`Options.chart.spacing_left` and :meth:`Option.chart.spacing_right`.
        Defaults to ``0``.

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = validators.numeric(value, allow_empty = True)

    @property
    def y(self) -> Optional[int | float | Decimal]:
        """The y position of the title relative to the alignment within
        :meth:`Options.chart.spacing_top` and :meth:`Option.chart.spacing_bottom`.
        Defaults to :obj:`None <python:None>`, which positions the title below the
        title (unless the title is floating).

        :rtype: numeric or :obj:`None <python:None>`
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = validators.numeric(value, allow_empty = True)

    @classmethod
    def _get_kwargs_from_dict(cls, as_dict):
        kwargs = {
            'align': as_dict.get('align', None),
            'floating': as_dict.get('floating', None),
            'margin': as_dict.get('margin', None),
            'style': as_dict.get('style', None),
            'text': as_dict.get('text', 'Chart title'),
            'use_html': as_dict.get('useHTML', None),
            'vertical_align': as_dict.get('verticalAlign', None),
            'width_adjust': as_dict.get('widthAdjust', None),
            'x': as_dict.get('x', None),
            'y': as_dict.get('y', None)
        }

        return kwargs

    def _to_untrimmed_dict(self, in_cls = None) -> dict:
        untrimmed = {
            'align': self.align,
            'floating': self.floating,
            'margin': self.margin,
            'style': self.style,
            'text': self.text,
            'useHTML': self.use_html,
            'verticalAlign': self.vertical_align,
            'widthAdjust': self.width_adjust,
            'x': self.x,
            'y': self.y
        }

        return untrimmed