import sys
import os
import re
from math import pi, sqrt

class Shape:
    count = 0

    def __init__(self):
        Shape.count += 1
        self.id = Shape.count

    def print(self):
        perimeter = self.perimeter() if self.perimeter() is not None else 'undefined'
        area = self.area() if self.area() is not None else 'undefined'
        print(f"{self.id}: {self.__class__.__name__}, perimeter: {perimeter}, area: {area}", end = " ")

        if isinstance(self, Rhombus):
            print(f"side: {self.side()}, in-radius: {self.inradius()}", end=" ")

        elif isinstance(self, Ellipse):
            print(f"linear eccentricity: {self.eccentricity()}", end=" ")
            
        print()  


    def perimeter(self):
        return None

    def area(self):
        return None

class Circle(Shape):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius

    def print(self):
        perimeter = self.perimeter()
        area = self.area()
        print(f"{self.id}: {self.__class__.__name__}, perimeter: {perimeter}, area: {area}")

    def perimeter(self):
        return 2 * pi * self.radius

    def area(self):
        return pi * self.radius ** 2

class Ellipse(Shape):
    def __init__(self, a, b):
        super().__init__()
        self.a = max(a, b)
        self.b = min(a, b)

    def print(self):
        perimeter = self.perimeter()
        area = self.area()
        eccentricity = self.eccentricity()
        print(f"{self.id}: {self.__class__.__name__}, perimeter: {perimeter}, area: {area}, linear eccentricity: {eccentricity}")

    def area(self):
        return pi * self.a * self.b

    def eccentricity(self):
        try:
            c = sqrt(self.a ** 2 - self.b ** 2)
            return c
        except ValueError:
            return None

class Rhombus(Shape):
    def __init__(self, p, q):
        super().__init__()
        self.p = p
        self.q = q

    def print(self):
        perimeter = self.perimeter()
        area = self.area()
        side = self.side()
        inradius = self.inradius()
        print(f"{self.id}: {self.__class__.__name__}, perimeter: {perimeter}, area: {area}, side: {side}, in-radius: {inradius}")

    def perimeter(self):
        return 2 * sqrt(self.p ** 2 + self.q ** 2)

    def area(self):
        return 0.5 * self.p * self.q

    def side(self):
        return (sqrt(self.p ** 2 + self.q ** 2)) / 2

    def inradius(self):
        try:
            return (self.p * self.q) / (sqrt(self.p ** 2 + self.q ** 2))
        except ZeroDivisionError:
            return None
        
class space (Shape):
    def print(self):
        print(f"{self.id}: {self.__class__.__name__}, perimeter: undefined, area: undefined")