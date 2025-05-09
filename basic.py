from __future__ import annotations
import math
import typing

def constrain(value, minv, maxv):
    if (value < minv): return minv
    if (value > maxv): return maxv
    return value


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

class Color3:
    def __init__(self, color: tuple[int, int, int]):
        self.r: float = color[0]
        self.g: float = color[1]
        self.b: float = color[2]
        
    def __add__(self, other: Color3):
        r = self.r + other.r
        g = self.g + other.g
        b = self.b + other.b
        return Color3((r, g, b))
    
    def normalize255(self) -> Color3:
        (r, g, b) = map(lambda v: constrain(v, 0, 255), map(int, (self.r, self.g, self.b)))
        return Color3((r,g,b))
    
    def __sub__(self, other: Color3) -> Color3:
        r = self.r - other.r
        g = self.g - other.g
        b = self.b - other.b
        return Color3((r, g, b))
    
    def __truediv__(self, k: float) -> Color3:
        return Color3((self.r/k, self.g/k, self.b/k)) 
    
    def __mul__(self, k: float) -> Color3:
        return Color3((self.r*k, self.g*k, self.b*k)) 
      
    def __rmul__(self, k: float) -> Color3:
        return Color3((self.r*k, self.g*k, self.b*k)) 

    def __repr__(self) -> str:
        return f"r: {self.r}, g: {self.g}, b: {self.b}"
    
    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, Color3)): return False
        return self.r==other.r and self.g==other.g and self.b==other.b
    
    def __ne__(self, other: object) -> bool:
        return not self==other
    
    def __tuple__(self) -> tuple[int, int, int]:
        return tuple(map(lambda v: constrain(v, 0, 255), (self.r, self.g, self.b)))
    
    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b


class Color4(Color3):
    def __init__(self, color: tuple[int,int,int,int]):
        super().__init__(color)
        self.a = color[3]
        
    def normalize255(self) -> Color4:
        (r, g, b, a) = map(lambda v: constrain(v, 0, 255), map(int, (self.r, self.g, self.b, self.a)))
        return Color4((r,g,b,a))
    
    def __tuple__(self) -> tuple[int, int, int]:
        return tuple(map(lambda v: constrain(v, 0, 255), (self.r, self.g, self.b, self.a)))
    
    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b
        yield self.a
    
    def __add__(self, other: Color4) -> Color4:
        r = self.r + other.r
        g = self.g + other.g
        b = self.b + other.b
        a = (self.a + other.a)/2
        return Color4((r, g, b, a))

    def __sub__(self, other: Color4) -> Color4:
        r = self.r - other.r
        g = self.g - other.g
        b = self.b - other.b
        a = (self.a - other.a)/2
        return Color4((r, g, b, a))
    
    def __truediv__(self, k: float) -> Color4:
        return Color4((self.r/k, self.g/k, self.b/k, self.a)) 
    
    def __mul__(self, k: float) -> Color4:
        return Color4((self.r*k, self.g*k, self.b*k, self.a)) 
      
    def __rmul__(self, k: float) -> Color4:
        return Color4((self.r*k, self.g*k, self.b*k, self.a)) 

    def __repr__(self) -> str:
        return f"r: {self.r}, g: {self.g}, b: {self.b}, a: {self.a}"
    
    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, Color4)): return False
        return self.r==other.r and self.g==other.g and self.b==other.b and self.a==other.a
        
class Pixel:
    def __init__(self, clr: Color3, pnt: Point2):
        self.color = clr
        self.point = pnt