from __future__ import annotations
import math
import typing

class Point2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
    def distance2(self, other: Point2 = type('',(object,),{"x": 0, "y": 0})()) -> float: # type: ignore
        return (self.x-other.x)*(self.x-other.x) + (self.y-other.y)*(self.y-other.y)

    def distance(self, other: Point2 = type('',(object,),{"x": 0, "y": 0})()) -> float: # type: ignore
        return math.sqrt(self.distance2(other))
    
    def __abs__(self) -> float:
        return self.distance()
    
    def __neg__(self) -> Point2:
        return Point2(-self.x, -self.y)
    
    def __pos__(self) -> Point2:
        return Point2(self.x, self.y)

    def __add__(self, other: Point2) -> Point2:
        return Point2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Point2) -> Point2:
        return Point2(self.x - other.x, self.y - other.y)
    
    def __truediv__(self, k: float) -> Point2:
        return Point2(self.x/k, self.y/k) 
    
    def __mul__(self, k: float) -> Point2:
        return Point2(k*self.x, k*self.y) 
      
    def __rmul__(self, k: float) -> Point2:
        return Point2(k*self.x, k*self.y)   

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"
    
    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, Point2)): return False
        return self.x==other.x and self.y==other.y
    
    def __ne__(self, other: object) -> bool:
        return not self==other
    
    def iter(self):
        yield self.x
        yield self.y
        

class Vector2(Point2):
    pass