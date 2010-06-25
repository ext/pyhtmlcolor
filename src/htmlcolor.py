#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import re

DecimalFactory = lambda x: int(x,16)
FloatFactory = lambda x: int(x,16)/255.0
ResultClass = DecimalFactory
ColorComponents = 3

def enforceComponents():
    def decorate(func):
        def wrapper(*args, **kwargs):
            n = ColorComponents
            fill = ResultClass('ff')
            
            assert n in [3,4]
            
            result = func(*args, **kwargs)
            components = len(result)
            
            if components == n:
                return result
            elif components > n:
                return result[:n]
            else:
                return result + (n - components) * (fill,)
        return wrapper
    return decorate

def _parse_hex(string):
    n = len(string)
    fmt = {
        3: '([0-9A-Fa-f]{1})' * 3, # shorthand RGB
        4: '([0-9A-Fa-f]{1})' * 4, # shorthand RGBA
        6: '([0-9A-Fa-f]{2})' * 3, # RGB
        8: '([0-9A-Fa-f]{2})' * 4 # RGBA
    }
    
    match = re.match(fmt[n], string)
    
    if match:
        color = match.groups()
        color = tuple([ResultClass(x) for x in color])
        
        return color
    else:
        return None

@enforceComponents()
def parse(string):
    if not isinstance(string, basestring):
        raise ValueError, 'must be a string'

    if string[0] == '#':
        string = string[1:]
    
    return _parse_hex(string)

class test(unittest.TestCase):
    def test_invalid(self):
        self.assertRaises(ValueError, parse, 0)
    
    def test_decimal_rgb(self):
        global ResultClass, ColorComponents
        ResultClass = DecimalFactory
        ColorComponents = 3
        self.assertEqual(parse('#ff7700'), (255, 119, 0))
    
    def test_decimal_rgba_fill(self):
        global ResultClass, ColorComponents
        ResultClass = DecimalFactory
        ColorComponents = 4
        self.assertEqual(parse('#ff7700'), (255, 119, 0, 255))
    
    def test_decimal_rgba(self):
        global ResultClass, ColorComponents
        ResultClass = DecimalFactory
        ColorComponents = 4
        self.assertEqual(parse('#ff770077'), (255, 119, 0, 119))

    def test_float_rgb(self):
        global ResultClass, ColorComponents
        ResultClass = FloatFactory
        ColorComponents = 3
        [self.assertAlmostEqual(x,y,1) for (x,y) in zip(parse('#ff7700'), (1.0, 0.46, 0.0))]
    
    def test_float_rgba_fill(self):
        global ResultClass, ColorComponents
        ResultClass = FloatFactory
        ColorComponents = 4
        [self.assertAlmostEqual(x,y,1) for (x,y) in zip(parse('#ff7700'), (1.0, 0.46, 0.0, 1.0))]
    
    def test_float_rgba(self):
        global ResultClass, ColorComponents
        ResultClass = FloatFactory
        ColorComponents = 4
        [self.assertAlmostEqual(x,y,1) for (x,y) in zip(parse('#ff770077'), (1.0, 0.46, 0.0, 0.46))]

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=2).run(suite)
