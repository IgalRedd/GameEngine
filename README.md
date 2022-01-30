# GameEngine
This is a game engine that works off Python's built-in library of Tkinter to help make objects and keep track of everything.

After importing the game engine, call gameEngine.inits(width, height, decimal)
The parameters you can input are the width of the Tkinter window, the height and the amount of decimal points the game engine will keep.

There are 4 objects that the game engine currently has:
  1) Circle:
    To create a circle call: gameEngine.createCircle(radius, starting position, velocity, colour).
    The parameters are the radius of the circle, the starting position as a list list[float], starting velocity of the object as a list[float] and the colour as a string of the acceptable Tkinter colours.
    Circle object has built-in:
    1) Circle.destroy(itself) which takes in the object itself and destroys the tkinter object
    2) Circle.getObj() which returns the Tkinter object
    3) Circle.updateVel(x-acceleration, y-acceleration) which takes in the x,y components of acceleration and adds it to the velocity
    4) Circle.changeColour(new colour) which takes in a new colour and changes the tkinter object colour
    5) Circle.move(rate) which takes in a rate in milliseconds and moves the object, treating the velocity as meters / second
    6) Circle.collisionBorder(rate) which takes in a rate and outputs if in the next movement the object will collide with the border
    7) Circle.circleCircleCollision(rate, other circle) which takes in a rate and the other circle object and outputs if in the next movement the 2 circles will collide or not
    8) Circle.giveCenter(), this just returns the center of the circle as a list[float]
    9) Circle.pointCollison(point) which takes in a point and returns if the point is within the circle
  2) Line:
    To create a line call: gameEngine.createLine(vertex 1, vertex 2, width, colour).
    The parameters are the 2 vertex of the line in the form of: list[float], the width of the line and it's colour.
    Line object has built-in:
    1) Line.destroy(itself) which takes in the object itself and destroys the tkinter object
    2) Line.moveVertex(which vertex to change, new vertex) which takes in a number 1 or 2 corresponding to which vertex to move and sets it to the new vertex given
    3) Line.calcLength(), just returns the lenght of the line
  3) Vector:
    To create a vector call: gameEngine.createVector(x component, y component)
    Parameters are the x component of the 2D vector and the y component of the 2D vector
    Vector has built-in:
    1) Vector.magnitude(), just returns the magnitude of the vector
    2) Vector.__add__(other vector) which takes in the other vector and returns a Vector object of the 2 vectors added
    3) Vector.normalize(), just returns a new Vector object that is the current vector normalized
    4) Vector.scalarMulti(scalar) which takes in a scalar and returns a new Vector object that is the scaled version of the vector
  4) LabelObj:
    To create a label call: gameEngine.createLabel(text, position, foreground colour, background colour)
    The parameters are the text of the label, the position of it in the form of list[float], the foreground colour and background colour
    LabelObj has built-in:
    1) LabelObj.destroy(itself) which takes in itself and destroys the tkinter object
    2) LabelObj.moveTo(new position) which takes in a new position in the form of list[float] and moves the label
    3) LabelObj.changeText(new text) which takes in a string of new text and changes the label
    
The other 2 built-in functions in the gameEngine are: gameEngine.wait(sleep time) which pauses the game for the sleep time in milliseconds. The other built-in is gameEngine.update(rate) which takes in a rate of how fast to update, this function updates the frames of the tkinter and moves all the objects with a velocity. It also a list of 2 things. First is any key presses that were done in that frame. Second is a tuple of mouse events, first index of the tuple is either a 1 or 2, 1 indicating left click and 2 indicating right click, the second index of the tuple is a list[float] indicating position x,y.
