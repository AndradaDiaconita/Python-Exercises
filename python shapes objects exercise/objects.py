import math

class Shape:
# Class variable to keep track of the count of shape instances
    countID = 0


    def __init__(self):
        # Class variable to keep track of the count of shape instances
        Shape.countID += 1
        self.id = Shape.countID




    def print(self):
        # Calculate perimeter and area using the respective methods,
        # if the shape supports them; otherwise, set them as 'undefined'
        perimeter = self.perimeter() if self.perimeter() is not None else 'undefined'

        area = self.area() if self.area() is not None else 'undefined'


# Print the shape's ID, class name, perimeter, and area
        print(f"{self.id}: {self.__class__.__name__}, perimeter: {perimeter}, area: {area}", end = " ")



        if isinstance(self, Ellipse):
            # If the shape is an Ellipse, also print its linear eccentricity
            print(f"linear eccentricity: {self.eccentricity()}", end=" ")


        elif isinstance(self, Rhombus):
            # If the shape is a Rhombus, also print its side length and in-radius
            print(f"side: {self.side()}, in-radius: {self.inradius()}", end=" ")



            



        print()  




    def area(self):
        # Default implementation for area calculation,
        # returns None as it should be implemented in specific shape classes
        return None
    


    def perimeter(self):
        # Default implementation for perimeter calculation,
        # returns None as it should be implemented in specific shape classes
        return None





    def __str__(self):
        # Convert the shape instance to a string representation
        if isinstance(self, Circle):
            return f"{self.__class__.__name__.lower()} {self.radius}"
        
        
        elif isinstance(self, Ellipse):
            return f"{self.__class__.__name__.lower()} {self.a} {self.b}"
        
        
        elif isinstance(self, Rhombus):
            return f"{self.__class__.__name__.lower()} {self.p} {self.q}"
        
        
        return f"{self.__class__.__name__.lower()}"





class Circle(Shape):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius

    def area(self):
        # Calculate the area of the circle
        return  round(self.radius ** 2 * math.pi, 5)

    def perimeter(self):
        # Calculate the perimeter (circumference) of the circle
        return round(math.pi * self.radius * 2, 5)






class Rhombus(Shape):
    def __init__(self, p, q):
        super().__init__()
        self.p = p
        self.q = q

    def side(self):
        # Calculate the side length of the rhombus using the Pythagorean theorem
        return round(((self.p ** 2 + self.q ** 2) ** 0.5) / 2, 5)
    

    def perimeter(self):
         # Calculate the perimeter of the rhombus
        return round(2 * (self.p ** 2 + self.q ** 2) ** 0.5, 5)


    def area(self):
        # Calculate the area of the rhombus
        return round((1/2) * (self.p * self.q), 5)


    def inradius(self):
        try:
            # Calculate the in-radius of the rhombus using a formula
            return round((self.p * self.q) / ((self.p ** 2 + self.q ** 2) ** 0.5), 5)
        
        except ValueError:
            return None
        




class Ellipse(Shape):

    def __init__(self, a, b):

        super().__init__()
        # Assign the larger value to 'a' and the smaller value to 'b'
        self.a = max(a, b)
        self.b = min(a, b)
        

    def area(self):
        # Calculate the area of the ellipse using the formula
        return round(math.pi * self.a * self.b, 5)

    def eccentricity(self):
        try:
            # Calculate the linear eccentricity of the ellipse using a formula
            return round((self.a ** 2 - self.b ** 2) ** 0.5, 5)
        
        except ValueError:
            # If the calculation fails due to a ValueError, return None
            return None



