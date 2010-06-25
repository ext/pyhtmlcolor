#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import re

from names import names

DecimalFactory = lambda v: int(v,16)
FloatFactory = lambda v: int(v,16)/255.0
HexFactory = lambda v: v
ResultClass = DecimalFactory
ColorComponents = 3

# Get a list of all hexadecimal digits.
_hex_literals = [hex(v)[-1] for v in range(0,16)]

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
    if string[0] == '#':
        string = string[1:]
    
    n = len(string)
    fmt = {
        3: '([0-9A-Fa-f]{1})' * 3, # shorthand RGB
        4: '([0-9A-Fa-f]{1})' * 4, # shorthand RGBA
        6: '([0-9A-Fa-f]{2})' * 3, # RGB
        8: '([0-9A-Fa-f]{2})' * 4 # RGBA
    }
    
    match = re.match(fmt[n], string)
    
    if match:
        groups = match.groups()
        
        # shorthand RGB{,A} must be extended
        if n in [3,4]:
            groups = tuple([2*x for x in groups])
        
        return groups
    else:
        raise ValueError,'Unable to parse "%s"' % (string)

def _parse_name(string):
    try:
        return names[string]
    except KeyError:
        raise ValueError,'Unrecognized color name "%s"' % (string)

def _detect_format(string):
    if string[0] == '#':
        return _parse_hex
    elif [item for item in string if item not in _hex_literals] == []:
        return _parse_hex
    else:
        return _parse_name

@enforceComponents()
def parse(string):
    if not isinstance(string, basestring):
        raise ValueError, 'must be a string'
    
    func = _detect_format(string)
    result = func(string)
    
    return tuple([ResultClass(x) for x in result])

class test(unittest.TestCase):
    def test_invalid(self):
        self.assertRaises(ValueError, parse, 0)
    
    def test_invalid_hex(self):
        self.assertRaises(ValueError, parse, '#foobar')
    
    def test_short_hex_rgb(self):
        global ResultClass, ColorComponents
        ResultClass = DecimalFactory
        ColorComponents = 3
        self.assertEqual(parse('#f70'), (255, 119, 0))
    
    def test_short_hex_rgba(self):
        global ResultClass, ColorComponents
        ResultClass = DecimalFactory
        ColorComponents = 4
        self.assertEqual(parse('#f70f'), (255, 119, 0, 255))
    
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
    
    def test_sign(self):
        global ResultClass, ColorComponents
        ResultClass = DecimalFactory
        ColorComponents = 3
        self.assertEqual(parse('#ff7700'), (255, 119, 0))
        self.assertEqual(parse('ff7700'), (255, 119, 0))
    
    def test_name(self):
        global ResultClass, ColorComponents
        ResultClass = DecimalFactory
        ColorComponents = 3
        self.assertEqual(parse('red'), (255, 0, 0))
    
    def test_invalid_name(self):
        self.assertRaises(ValueError, parse, 'foobar')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=2).run(suite)
