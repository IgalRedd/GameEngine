# Game Engine
from tkinter import *
from time import sleep

# Stores how many decimal points we keep
decimals = 3

# Creates global variables for the width and height to be used later
width = 600
height = 600

# Creates a list of drawn objects
objects = []

# Creates a global variable to see if a key is pressed
keyPressed = False
key = None

# Creates variables to keep track of mouse clicks
mousePressed = 0
mousePos = None

# Initilizes all the information for the game, this must be run first
def inits(GivenWidth: int = 600, GivenHeight: int = 600, dec: int = 3):
    # Creates global variables for the width and height of the canvas
    # as well as the decimals we keep
    global width, height, decimal
    # Creates global variables for the root of tkinter and canvas
    # so I can create it in here and use it later
    global root, c

    # Sets the width, height to the given width, given height
    # respectively if the player wants to reset it
    width = GivenWidth
    height = GivenHeight
    decimals = dec

    # Init the root of canvas and tkinter root
    root = Tk()
    c = Canvas(width = width, height = height)

    # Creates bind to see if a player pressed a key or mouse event
    c.focus_set()
    c.bind("<KeyPress>", keyboardEvent)
    c.bind("<Button-1>", leftClick)
    c.bind("<Button-3>", rightClick)
    
    c.pack()

#----------------------------------------------------------------------------------------------------------

# Creates a vector object to be able to help with vector calculations
class Vector:
    def __init__(self, x: int, y: int):
        # Stores the 2 only useful information; x and y
        self.x = x
        self.y = y

    # Finds the magnitude of the vector
    def magnitude(self):
        # Finds the unsquared vector magnitude
        unsquared = self.x**2 + self.y**2

        # Returns the square rooted magnitude
        return unsquared**(1/2)

    # Allows addition of vectors
    def __add__(self, other: object):
        # Returns the now added vector
        return Vector(self.x + other.x, self.y + other.y)

    # Returns the normalized vector
    def normalize(self):
        # Finds the magnitude of the vector
        vecMag = self.magnitude()

        # Returns the normal vector (aka with a magnitude of 1)
        return Vector(round(self.x / vecMag, decimals), round(self.y / vecMag, decimals))

    # Allows scalar mulitplication of vectors
    def scalarMulti(self, multiple: float):
        # Returns the new vector multiplied by the scalar
        return Vector(self.x * multiple, self.y * multiple)

# Helps create vectors
def createVector(x: int, y: int):
    # Just creates the vector
    return Vector(x, y)

#----------------------------------------------------------------------------------------------------------

# Creates the circle class to use because its easier to work with classes
class Circle:
    # Init's variables
    def __init__(self, tkObj: object, radius: int, pos: list[float], colour: str, velocity: list[float]):
        # Init's all important, non-default values
        self.radius = radius
        self.pos = pos

        # Init's the possible default values
        self.colour = colour
        self.velocity = velocity

        # Sets a var for the tkinter object
        self.tkObj = tkObj

    # Function to destroy the tkinter object
    def destroy(self, itself: object):
        # Uses the global objects list
        global objects
        
        # Deletes the tkinter object
        c.delete(self.tkObj)
        # Removes the object from being drawn
        objects.remove(itself)

    # Returns the tkinter object of the circle
    def getObj(self):
        return self.tkObj

    # Updates velocities (applying acceleration)
    def updateVel(self, xAccel: float, yAccel: float):
        self.velocity[0] += xAccel
        self.velocity[1] += yAccel

    # Allows changes of the object's colour
    def changeColour(self, newColour: str):
        # Changes the tkinter object
        c.itemconfig(self.tkObj, fill = newColour)
        # Changes the var of the object
        self.colour = newColour

    # Moves the object to a set new position, not based on velocity
    def moveTo(self, newPos):
        # Resets the pos vector
        self.pos = newPos

        # Moves the tkinter object
        c.coords(self.tkObj, round(self.pos[0]), round(self.pos[1]))
    
    # Moves the object
    def move(self, rate: float):
        # Updates its x,y positions 
        self.pos[0] += self.velocity[0] * rate
        self.pos[1] += self.velocity[1] * rate

        # Changes its coords to the new positon, rounded for pixels
        c.coords(self.tkObj, round(self.pos[0]), round(self.pos[1]), round(self.pos[0] + 2 * self.radius), round(self.pos[1] + 2 * self.radius))
        

    # Checks collision with borders of canvas
    # (these are future checks, aka if we add velocity)
    def collisionBorder(self, rate: float):
        yBool = False
        
        # Finds the new y position after moving with it's velocity
        newY = self.pos[1] + (self.velocity[1] * rate)  
        # Checks if it will cross the height or 0 border
        if newY + self.radius >= height or newY <= 0:
            yBool = True

        xBool = False
    
        # Finds the new x after moving with it's velocity
        newX = self.pos[0] + (self.velocity[0] * rate)
        # Checks if it will cross the width or 0 border
        if newX + self.radius >= width or newX <= 0:
            xBool = True

        # Returns if it collided with the border of x or y
        return (xBool, yBool)

    # Checks if there is a collision with the another circle
    # It works by checking if the distance between the 2 center
    # points is <= to the 2 radii summed up.
    def circleCircleCollison(self, rate: float, C2: object):
        # Gets the center of the 2 circles
        center1 = self.giveCenter()
        center2 = C2.giveCenter()

        # Calculates distance between 2 center points
        distance = round(( (center1[0] - center2[0])**2 + (center1[1] - center2[1])**2 )**(1/2), decimals)

        # Returns if that distance <= to the 2 radii summed up
        return distance <= self.radius + C2.radius

    # A function to find the center of the circle, given to decimal places
    def giveCenter(self):
        # Returns center of the circle
        return (self.pos[0] + self.radius, self.pos[1] + self.radius)

    # Checks if there is a collision between a point and the circle
    def pointCollison(self, point):
        # Finds the center of the circle
        cen = self.giveCenter()
        
        # Returns if it is inside the circle using
        # (x-r)^2 + (y-z)^2 = r^2
        return ((point[0] - cen[0])**2 + (point[1] - cen[1])**2) <= (self.radius**2)
        
# Allows the player to create circles
def createCircle(radius: int, startingPos: list[float], velocity: list[float], colour: str = "white"):
    # Allows us to manipulate the global objects and use canvas
    global objects, c

    # Creates the local var of the new circle and it's object
    newCircle = c.create_oval(startingPos[0], startingPos[1], startingPos[0] + radius * 2, startingPos[1] + radius * 2, fill = colour)
    circle = Circle(newCircle, radius, startingPos, colour, velocity)

    # Adds the circle to the objects list
    objects.append(circle)

    # Returns the circle object so it can be manipulated
    return circle

#----------------------------------------------------------------------------------------------------------

# Creates a line object
class Line:
    # Initilizes the line with 2 vertexs, a colour and a tkinter object
    def __init__(self, tkObj: object, vertex1: list[int], vertex2: list[int], colour: str):
        # Stores the 2 vertexes
        self.vertex1 = vertex1
        self.vertex2 = vertex2

        # Stores the colour and the length of the line
        self.colour = colour
        self.length = self.calcLength()

        # Stores the tkinter object
        self.tkObj = tkObj

    # Function to destroy the tkinter object and remove it from the list
    def destroy(self, itself: object):
        # Uses global objects to delete itself from the list of objects
        global objects

        # Deletes the tkinter object
        c.delete(self.tkObj)
        # Deletes it from list
        objects.remove(itself)

    # Allows only 1 vertex of a line to change
    def moveVertex(self, vertToChange: int, newVert: list[int]):
        # Which vertex to change: 1 or 2
        if vertToChange == 1:
            # Changes the coords of the line
            c.coords(self.tkObj, newVert[0], newVert[1], self.vertex2[0], self.vertex2[0])

            # Resets the proper vertex
            self.vertex1 = newVert
        else:
            # Changes the coords of the line
            c.coords(self.tkObj, self.vertex1[0], self.vertex1[1], newVert[0], newVert[1])

            # Resets the proper vertex
            self.vertex2 = newVert

        # Recalculates the new length
        self.length = self.calcLength()

    
    # Function to calculate length of the line given 2 vertexes of the line
    def calcLength(self):
        return round(((self.vertex1[0] - self.vertex2[0])**2 + (self.vertex1[1] - self.vertex2[1])**2)**(1/2), decimals)

# Functions to create and make lines in the engine
def createLine(vertex1: list[int], vertex2: list[int], width: int = 2, colour: str = "black"):
    # Uses the global canvas and objects list
    global objects, c

    # Creates the tkinter object of the line
    newLine = c.create_line(vertex1[0], vertex1[1], vertex2[0], vertex2[1], width = width, fill = colour)
    # Creates the game engine object of the line
    line = Line(newLine, vertex1, vertex2, colour)

    # Adds the line to the objects list
    objects.append(line)

    # Returns the object
    return line

#----------------------------------------------------------------------------------------------------------

# Creates a gameEngine object
class LabelObj:
    def __init__(self, tkObj: object, text: str, pos: list[int]):
        # Stores the tkinter object
        self.tkObj = tkObj

        # Stores the text
        self.text = text
        # Stores the position
        self.pos = pos

    # Function to delete the object from the game
    def destroy(self, itself: object):
        # Uses the global objects list to remove it
        global objects

        # Deletees the tkinter object
        c.delete(self.tkObj)
        # Destroys the object from the list
        objects.remove(itself)

    # Function to move the label object to the given position
    def moveTo(self, newPos: list[int]):
        # Places the object the new position
        self.tkObj.place(x = newPos[0], y = newPos[1])

    # Functions to allow the text to change
    def changeText(self, newText: str):
        # Reconfigures the text of the label
        self.tkObj.configure(text = newText)
    

# Function to create label objects to write text
def createLabel(text: str, pos: list[int], fgColour: str = "black", bgColour: str = None):
    # Uses the global canvas and objects list
    global objects, c

    # If the background colour isn't specified then assume none
    if bgColour is None:
        # Creates a tkinter label with no background colour
        newLabel = Label(c, text = text, fg = fgColour)
    else:
        # Creates tkinter label with specified background colour
        newLabel = Label(c, text = text, fg = fgColour, bg = bgColour)

    # Places the label where the user requested
    newLabel.place(x = pos[0], y = pos[1])

    # Creates the label gameEngine object
    label = LabelObj(newLabel, text, pos)

    # Returns it to the user so it can be manipulated
    return label

#----------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------

# Gets the keyboard events if any happen
def keyboardEvent(event):
    # Uses global variables to store key and key pressed bool
    global keyPressed, key
    
    # Sets the key that was pressed
    key = event.char
    # Informs the bool that a key was pressed
    keyPressed = True


# Detects if a left click occured
def leftClick(event):
    # Uses global variables for mouse pressed and position
    global mousePressed, mousePos

    # Sets the position of the mouse
    mousePos = [event.x, event.y]
    # Switches it to 1 to indicate left click
    mousePressed = 1

# Detects if a right click occured
def rightClick(event):
    # Uses global variables to store mouse type and position
    global mousePressed, mousePos

    # Sets the position of mouse
    mousePos = [event.x, event.y]
    # Switches it to 2 to indiciate right click
    mousePressed = 2
    


# Returns all the drawn objects
def getObjects():
    return objects


# Creates a function to help wait some time    
def wait(sleepTime: int):
    sleep(sleepTime)


# Updates all the objects
def update(rate):
    # Creates global c so it can be used
    global c, keyPressed, mousePressed
    
    # Goes through all the items in the object
    for item in objects:
        if isinstance(item, Circle):
            # Moves the object
            item.move(rate)

    # Calls root.update to draw new frames
    root.update()

    # Creates a return list filled with None
    returnLst = [None, None]

    # Checks if a key was pressed
    if keyPressed:
        # Resets the key
        keyPressed = False
        # Corrects the return list to reflect reality
        returnLst[0] = key

    # Checks if the mouse was clicked
    if mousePressed != 0:
        # Corrects the return list to reflect reality
        returnLst[1] = (mousePressed, mousePos)
        # Resets the mouse press
        mousePressed = 0
        

    # Returns the values
    return returnLst

        


