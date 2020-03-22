# -*- coding: utf-8 -*-

from fractions import Fraction

class Quadratic:
    """
    Implements a number in a field of type a + b*sqrt(2), 
    where a,b are rational. Uses Fraction to implement rational numbers.
    """
    def __init__(self, a, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)
    
    def __repr__(self):
        return "{} + {}*sqrt(2)".format(self.a, self.b)
    
    def __add__(self, B):
        a = self.a + B.a
        b = self.b + B.b
        return Quadratic(a, b)
    
    def __abs__(self):
        return Quadratic(abs(self.a), abs(self.b))
    
    def __mul__(self, B):
        a = self.a*B.a + Fraction(2)*self.b*B.b
        b = self.a*B.b + self.b*B.a
        return Quadratic(a, b)
    
    def __sub__(self, B):
        return self + Quadratic(-1)*B
    
    def __float__(self):
        return self.a + 2.0**(0.5)*self.b
    
    def __eq__(self, B):
        return self.a == B.a and self.b == B.b
    
if __name__ == "__main__":
    number = Quadratic(1, 0.5)
    print(number*number)
    print(number + number)
    print(float(number))