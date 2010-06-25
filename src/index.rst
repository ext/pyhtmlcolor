Documentation
=============

Sample usage
------------

Parsing a color

>>> import htmlcolor
>>> htmlcolor.parse('#ff7700')
(255, 119, 0)

Float values

>>> htmlcolor.ResultClass = htmlcolor.FloatFactory
>>> htmlcolor.parse('#ff7700')
(1.0, 0.46666666666666667, 0.0)

Custom factory

>>> htmlcolor.ResultClass = lambda x: int(x,16)*2
>>> htmlcolor.parse('#ff7700')
(510, 238, 0)

Attributes
----------

.. attribute:: ResultFactory
 
   A callable which converts the format of the color elements.
   Default is DecimalFactory.

.. attribute:: ColorComponents

  Specifies how many color components the result should be. (RGB: 3, RGBA: 4)
