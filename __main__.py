#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from htmlcolor import *

suite = unittest.TestLoader().loadTestsFromNames(['htmlcolor.test', 'htmlcolor.factory_test', 'htmlcolor.components_test'])
unittest.TextTestRunner(verbosity=2).run(suite)

print
print ' *** Sample usage ***'

values = ['#ff7700', 'ff7700', '#f70', '#ff770077', 'hotpink']
parser = Parser()

print '\nRGB Decimal factory'
parser.ResultFactory = DecimalFactory
parser.Components = 3
for cur in values:
    print cur, '=>', parser.parse(cur)

print '\nRGBA Float factory'
parser.ResultFactory = FloatFactory
parser.Components = 4
for cur in values:
    print cur, '=>', parser.parse(cur)
