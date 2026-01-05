from objects import Shape, Circle, Ellipse, Rhombus
import os
import re

class shapedb:
    def __init__(self):
        self.shapes = []

    def load(self, filename):
        if not os.path.isfile(filename):
            print(f"Error: Invalid file/path: {filename}")
            return

        print(f"Processing {filename}...")

        with open(filename, 'r') as file:
            lines = file.readlines()

        shape_pattern = re.compile(r"(\w+)\s*([\d\s-]+)")
        error_count = 0
        shape_count = 0

        for line in lines:
            match = shape_pattern.match(line.strip())
            if match:
                shape_name = match.group(1).lower()
                params = match.group(2).split()
                shape = self.create_shape(shape_name, params)
                if shape:
                    self.shapes.append(shape)
                    shape_count += 1
                else:
                    error_count += 1
            elif line.strip() != "":
                error_count += 1

        print(f"Processed {len(lines)} row(s), {shape_count} shape(s) added, {error_count} error(s).")
        return self.shapes

    def create_shape(self, shape_name, params):
        if shape_name == 'shape':
                    shape = Shape()
                    return Shape(shape)
        elif shape_name == "circle":
            if len(params) != 1:
                print(f"Error: Invalid Circle on line {len(self.shapes) + 1}: {shape_name} {' '.join(params)}")
                return None
            
            try:
                radius = float(params[0])
                if radius < 0:
                    raise ValueError
                shape = Circle(radius)
                return Circle(radius)
            except ValueError:
                error_count += 1
                print(f"Error: Invalid Circle on line {len(self.shapes) + 1}: {shape_name} {' '.join(params)}")
                return None
        elif shape_name == "ellipse":
            if len(params) != 2:
                print(f"Error: Invalid Ellipse on line {len(self.shapes) + 1}: {shape_name} {' '.join(params)}")
                return None

            try:
                a = float(params[0])
                b = float(params[1])
                if a < 0 or b < 0:
                    raise ValueError
                shape = Ellipse(a, b)
                return Ellipse(a, b)
            except ValueError:
                print(f"Error: Invalid Ellipse on line {len(self.shapes) + 1}: {shape_name} {' '.join(params)}")
                return None
        elif shape_name == "rhombus":
            if len(params) != 2:
                print(f"Error: Invalid Rhombus on line {len(self.shapes) + 1}: {shape_name} {' '.join(params)}")
                return None
            
            try:
                p = float(params[0])
                q = float(params[1])
                if p < 0 or q < 0:
                    raise ValueError
                shape = Rhombus(p, q)
                return Rhombus(p, q)
              
            except ValueError:
                print(f"Error: Invalid Rhombus on line {len(self.shapes) + 1}: {shape_name} {' '.join(params)}")
                return None
           


    def to_set(self, shapes):
        unique_shapes = []
        unique_set = set()
        for shape in shapes:
            shape_str = str(shape)
            if shape_str not in unique_set:
                unique_set.add(shape_str)
                unique_shapes.append(shape)
        self.shapes = unique_shapes
        return shapes

    def save(self, filename):
        with open(filename, 'w') as file: 
            for shape in self.shapes:
                file.write(shape.__class__.__name__.lower() + " " + self.shape_params(shape) + "\n")


    def print(self):
        for shape in self.shapes:
            shape.print()

    def summary(self):
        shape_counts = {}
        for shape in self.shapes:
            shape_name = shape.__class__.__name__
            shape_counts[shape_name] = shape_counts.get(shape_name, 0) + 1

        total_shapes = sum(shape_counts.values())

        print("Summary:")
        for i, (shape_name, count) in enumerate(sorted(shape_counts.items())):
            if i != len(shape_counts) - 1:
                print(f"{shape_name}(s): {count}")
        print(f"Shape(s): {total_shapes}")


    def details(self):
        for shape in self.shapes:
            print((shape))

    
    def shape_params(shape):
        if isinstance(shape, Circle):
            return str(shape.radius)
        elif isinstance(shape, Ellipse):
            return f"{shape.a} {shape.b}"
        elif isinstance(shape, Rhombus):
            return f"{shape.p} {shape.q}"
        else:
            return ""

    def menu(self):
        fileloaded = False

        while True:
            print("\n--- MENU ---")
            print("1. LOAD file")
            print("2. TOSET")
            print("3. SAVE file")
            print("4. PRINT")
            print("5. SUMMARY")
            print("6. DETAILS")
            print("7. QUIT")

            choice = input("Enter your choice (1-7): ")

            if choice == "1":
                if fileloaded:
                    print("A file is already loaded. Please use TOSET or QUIT to continue.")
                    continue
                filename = input("Enter the filename: ")
                self.load(filename)
                fileloaded = True

            elif choice == "2":
                if not fileloaded:
                    print("No file loaded. Please use LOAD to load a database.")
                    continue

                self.shapes = self.to_set(self.shapes)
                print("Multi-set converted to a set.")

            elif choice == "3":
                filename = input("Enter the filename: ")
                self.save(filename)
                print("Database saved to file.")

            elif choice == "4":
                self.print()

            elif choice == "5":
                self.summary()

            elif choice == "6":
                self.details()

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    db = shapedb()
    db.menu()