#contains object classes for the objects used in crackedup.py


#ball object for user to control
class Ball(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r

#obstacle object for gameplay 
class Obstacle(object):
    def __init__(self, initialX, initialY, cx, cy, initialR, r, color, shape):
        self.initialX = initialX
        self.initialY = initialY
        self.cx = cx
        self.cy= cy
        self.initialR = initialR
        self.r = r
        self.color = color
        self.shape = shape
        self.insideCounter = 0

#breakable obstacle object that is a child of the obstacle object
class Breakable(Obstacle):
    def __init__(self, initialX, initialY, cx, cy, initialR, r, initialC, color, shape):
        super().__init__(initialX, initialY, cx, cy, initialR, r, color, shape)
        self.initialC = initialC

    def reset(self):
        self.r = self.initialR
        self.cx = self.initialX
        self.cy = self.initialY
        self.color = self.initialC
