
from objects import Shape, Circle, Ellipse, Rhombus
import os


# Function to load shapes from a file
def loadTheFile(theFile):

    numberofLines = 0 # Counter for the number of lines in the file

    numberofErrors = 0 # Counter for the number of errors encountered while loading the file

    global theShapes # List to store the loaded shapes

    theShapes = [] # Initialize the list


    print(f"Processing {theFile}...!!!")

    try:
        with open(theFile, 'r') as file:
            for line in file:
                numberofLines += 1
                parameters = line.strip().split() # Split the line into individual parameters

                if len(parameters) == 0:
                    continue

                nameOfShape = parameters[0].lower() # Get the name of the shape from the first parameter

                if nameOfShape == 'shape':
                    shape = Shape() # Create a Shape object
                    theShapes.append(shape) # Add the shape to the list



                elif nameOfShape == 'ellipse':
                    if len(parameters) >= 3:

                        try:
                            a = float(max(parameters[1], parameters[2])) # Get the major axis of the ellipse
                            b = float(min(parameters[1], parameters[2])) # Get the minor axis of the ellipse

                            if b < 0 or a < 0 :
                                raise ValueError()
                            

                            shape = Ellipse(a, b) # Create an Ellipse object
                            theShapes.append(shape) # Add the shape to the list


                        except ValueError:
                            numberofErrors += 1
                            print(f"Error: Invalid Ellipse on line {numberofLines}: {line.strip()}")
                            continue

                    else:
                        numberofErrors += 1
                        print(f"Error: Invalid Ellipse on line {numberofLines}: {line.strip()}")
                        continue


                elif nameOfShape == 'circle':
                    if len(parameters) >= 2:

                        try:
                            radius = float(parameters[1]) # Get the radius of the circle

                            if radius < 0:
                                raise ValueError()
                            
                            shape = Circle(radius) # Create a Circle object
                            theShapes.append(shape) # Add the shape to the list


                        except ValueError:
                            print(f"Error: Invalid Circle on line {numberofLines}: {line.strip()}")
                            numberofErrors += 1
                            continue

                    else:
                        numberofErrors += 1
                        print(f"Error: Invalid Circle on line {numberofLines}: {line.strip()}")
                        continue

                
                elif nameOfShape == 'rhombus':
                    if len(parameters) >= 3:

                        try:
                            p = float(parameters[1]) # Get the first diagonal of the rhombus
                            q = float(parameters[2]) # Get the second diagonal of the rhombus

                            if q < 0 or p < 0:
                                raise ValueError()
                            

                            shape = Rhombus(p, q) # Create a Rhombus object
                            theShapes.append(shape) # Add the shape to the list


                        except ValueError:
                            numberofErrors += 1
                            print(f"Error: Invalid Rhombus on line {numberofLines}: {line.strip()}")
                            continue


                    else:
                        numberofErrors += 1
                        print(f"Error: Invalid Rhombus on line {numberofLines}: {line.strip()}")
                        continue



                else:
                    numberofErrors += 1
                    print(f"Error: Invalid Shape on line {numberofLines}: {line.strip()}")
                    continue




        print(f"Processed {numberofLines} row(s), {len(theShapes)} shape(s) added, {numberofErrors} error(s).")
        return theShapes



    except IOError:
        print(f"We can't open {theFile}. !!")
        return []



# Function to remove duplicate shapes from the list
def to_set(theShapes):
    nonrepetitivesets = set()
    nonrepetitiveshapes = []
    

    for shape in theShapes:
        shape_str = str(shape)

        if shape_str not in nonrepetitivesets:
            nonrepetitivesets.add(shape_str)
            nonrepetitiveshapes.append(shape)


    print("Success!!")
    theShapes = nonrepetitiveshapes

    return theShapes


# Function to save shapes to a file
def saveShapes(file, theShapes):
    with open(file, 'w') as f:

        for shape in theShapes:
            f.write(f"{str(shape)}\n")


    print(f"We saved it in {file}. !!")


# Function to print the details of shapes
def printShapes(theShapes):
    for shape in theShapes:
        shape.print()


# Function to print a summary of the shapes
def summary(theShapes):
    countsOfShapes = {}

    for shape in theShapes:
        nameOfShapes = shape.__class__.__name__
        countsOfShapes[nameOfShapes] = countsOfShapes.get(nameOfShapes, 0) + 1

    
    totalShapes = sum(countsOfShapes.values())
    

    print("Here is your summary: ")

    for i, (nameOfShapes, theCount) in enumerate(sorted(countsOfShapes.items())):

        if i != len(countsOfShapes) - 1:
            print(f"{nameOfShapes} (s): {theCount}")

    print(f"Shape(s): {totalShapes}")



# Function to print the details of shapes
def details(theShapes):
    for shape in theShapes:
        print(shape)




# Main function to run the program
def main():
    theShapes = []
    filesPutIn = False

    while True:

        print("\n --- MENU --- ")
        print(" 1. LOAD file ")
        print(" 2. TOSET ")
        print(" 3. SAVE file ")
        print(" 4. PRINT ")
        print(" 5. SUMMARY ")
        print(" 6. DETAILS ")
        print(" 7. QUIT ")


        theChoice = input("Make a choice!! (1-7): ")




        if theChoice == '1':

            if filesPutIn:
                print("File Already IN!!")
                continue


            file = input("Enter the name of the file to load in: ")

            if not os.path.isfile(file):
                print("We can not find your file!!")
                continue


            theShapes = loadTheFile(file)
            filesPutIn = True


        elif theChoice == '2':

            if not filesPutIn:
                print("Choose 1 to load a file first!! Then use the other choices from the menu!!")
                continue
            

            theShapes = to_set(theShapes)


        elif theChoice == '3':

            if not filesPutIn:
                print("Choose 1 to load a file first!! Then use the other choices from the menu!!")
                continue


            file = input("Name the file you want to save your data in! ")
            saveShapes(file, theShapes)


        elif theChoice == '4':

            if not filesPutIn:
                print("Choose 1 to load a file first!! Then use the other choices from the menu!!")
                continue


            printShapes(theShapes)


        elif theChoice == '5':

            if not filesPutIn:
                print("Choose 1 to load a file first!! Then use the other choices from the menu!!")
                continue

            summary(theShapes)


        elif theChoice == '6':

            if not filesPutIn:
                print("Choose 1 to load a file first!! Then use the other choices from the menu!!")
                continue


            details(theShapes)


        elif theChoice == '7':

            print("Good bye!!!!")
            break


        else:
            print("Choose between 1 and 6. If you want to quit choose 7!!")



if __name__ == '__main__':
    main()
