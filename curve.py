from __future__ import annotations
from typing import Any
from basic import *
from basic import Point2
import functools

def C(n, k) -> int:
    if (k<0 or k>n): raise Exception("k must be in range [0, n]")
    if (k==0 or k==n): return 1
    p = 1
    for i in range(k+1, n+1):
        p *= i
    for i in range(1,n-k+1):
        p /= i
    return int(p)

def perp(v: Point2) -> Point2:
    return Point2(-v.y, v.x)

# 2D curve a(t) where 0 <= t <=1
class Curve2:
    def __call__(self, t: float) -> Point2:
        return Point2(0,0)
    
    def min_distance(self, p: Point2) -> float:
        return 0
    
    # returns tangent vector
    def tangent(self, t: float) -> Point2:
        return Point2(1,0)
    
    # returns normal (perpendicular) vector
    def normal(self, t: float) -> Point2:
        return Point2(0,1)
    
class BezieCurve2(Curve2):
    def __init__(self, points: list[Point2]):
        if (len(points)==0): 
            raise Exception("Must have at least one point")
        self.N: int = len(points)-1
        self.points: list[Point2] = points.copy()
    
    @functools.cache
    def __call__(self, t: float) -> Point2: # type: ignore
        s: Point2 = Point2(0,0)
        n = self.N
        # for k in range(self.N, -1, -1):
        for k in range(self.N+1):
            s += C(n,k) * self.points[k] * (t**(n-k)) * ((1-t)**k) 
        return s
    
    def tangent(self, t: float) -> Point2:
        s: Point2 = Point2(0,0)
        n = self.N
        # for k in range(self.N, -1, -1):
        for k in range(self.N+1):
            if (k==0):
                s += self.points[k] * (n-k) * (t**(n-k-1))
            elif (n-k==0):
                s += self.points[k] * (-1) * k * ((1-t)**(k-1))
            else:
                s += C(n,k) * self.points[k] * (t**(n-k-1)) * ((1-t)**(k-1)) * ( n - n*t - k ) 
        s = s / abs(s)
        return s
    
    def normal(self, t: float) -> Point2:
        return perp(self.tangent(t))