#!/usr/bin/env python
"""
parsing.py

A small attempt at parsing a simple query language of boolean expressions.

Syntax:
'+' : OR (infix)
'*' : AND (infix)
'^' ": XOR (infix)
'(...)' : Logical Grouping
'!' : NOT (prefix)
"""

import re

class operators:
    OR_OP = '+'
    AND_OP = '*'
    XOR_OP = '^'
    NOT_OP = '!'
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'

    ALL_OPS = [OR_OP, AND_OP, XOR_OP, NOT_OP, LEFT_PAREN, RIGHT_PAREN]

class tokenizer(object):

    def __init__(self, string):
        self.string = string

    def get_tokens_generator(self):
        token = ''
        for c in self.string:
            if c.isspace(): continue
            if c in operators.ALL_OPS:
                if token: yield token
                yield c
                token = ''
            else:
                token += c


if __name__ == '__main__':
    test_case = 'Apple+Banana * C +D ( A + E)*(F+ G)'
    expected = ['Apple', '+', 'Banana', '*', 'C', '+','D', '(', 'A', '+', 'E', ')', '*', '(', 'F', '+', 'G', ')']
    result = list(tokenizer(test_case).get_tokens_generator())
    print "I expected", expected
    print "I got     ", result
