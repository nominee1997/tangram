# -*- coding: utf-8 -*-
import pytest
from Quadratic import Quadratic

@pytest.mark.parametrize(
        "A, B, output", 
        [(("-1/2", "-1"), ("1/2", "1"), False), 
         (("1", "1/2"), ("1", "1/2"), True),
         (("-1/2", "1"), ("1/2", "1"), False), 
         (("1", "-1/2"), ("1", "1/2"), False)])
def test__eq_(A, B, output):
    assert (Quadratic(*A) == Quadratic(*B)) == output

@pytest.mark.parametrize(
        "A, result", 
        [(("-1/2", "-1"), ("1/2", "1")), 
         (("1/2", "1"), ("1/2", "1")),
         (("-1/2", "1"), ("1/2", "1")), 
         (("1/2", "-1"), ("1/2", "1"))])
def test__abs_(A, result):
    assert abs(Quadratic(*A)) == Quadratic(*result)

@pytest.mark.parametrize(
        "A, B, output", 
        [(("-1/2", "-1"), ("1/2", "1"), ("0", "0")), 
         (("1", "1/2"), ("1", "1/2"), ("2", "1")),
         (("-3/2", "1"), ("2", "1/2"), ("1/2", "3/2")), 
         (("15/5", "-1/2"), ("1", "1/6"), ("4", "-1/3"))])
def test__add_(A, B, output):
    assert Quadratic(*A) + Quadratic(*B) == Quadratic(*output)
    assert Quadratic(*B) + Quadratic(*A) == Quadratic(*output)

@pytest.mark.parametrize(
        "A, B, output", 
        [(("0", "0"), ("-1/2", "-1"), ("0", "0")), 
         (("2", "1"), ("1", "1/2"), ("3", "2")),
         (("1/2", "3/2"), ("-3/2", "1"), ("9/4", "-7/4"))])
def test__mul_(A, B, output):
    assert Quadratic(*A)*Quadratic(*B) == Quadratic(*output)
    assert Quadratic(*B)*Quadratic(*A) == Quadratic(*output)

@pytest.mark.parametrize(
        "A, B, output", 
        [(("0", "0"), ("-1/2", "-1"), ("1/2", "1")), 
         (("2", "1"), ("1", "1/2"), ("1", "1/2")),
         (("1/2", "3/2"), ("-3/2", "1"), ("2", "1/2")), 
         (("4", "-1/3"), ("15/5", "-1/2"), ("1", "1/6"))])
def test__sub_(A, B, output):
    assert Quadratic(*A) - Quadratic(*B) == Quadratic(*output)

@pytest.mark.parametrize(
        "A, B, output", 
        [(("-1/2", "-1"), ("1/2", "1"), True),
         (("1", "1/2"), ("1", "1/2"), False),
         (("0", "1"), ("1.42", "0"), True),
         (("1", "0"), ("0", "1/2"), False)])
def test__lt__(A, B, output):
    assert (float(Quadratic(*A)) < float(Quadratic(*B))) == output