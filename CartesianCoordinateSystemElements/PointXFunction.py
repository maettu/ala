#!/usr/bin/python

from Point import Point
import Helper.CoordinateSystemTransformation as CST

class PointXFunction( Point ):
    """Defines a movable point with an y which is functionally
    dependent on its x value."""

    # TODO function as a parameter
    def __init__( self, ccs, parent, x, y, size, red=200, green=0,
                    blue=0 ):
        super(PointXFunction, self).__init__(ccs,
            parent, x, y, size, red, green, blue)

    def calculatePosition( self, e ):
        # only needs x_move here as y is calculated dependently on x
        x_move = e.pos().x() - self.xOnWidget

        p = CST.toCcsCoord( self.ccs, self.x, self.y, self,
                            self.parent )
        x = p.x() + x_move

        p = CST.fromCcsCoord( self.ccs, x, 0, self, self.parent )
        self.x = p.x()
        # TODO function still hardcoded..
        self.y = self.x**2
        
        self.setPos( CST.toCcsCoord(
            self.ccs, self.x, self.y )
        )


    def updateYourself( self, xDelta, yDelta ):
        # TODO point moves *relatively* to parent, does not just take
        # its x value
        self.x = self.x + xDelta
        self.y = self.x**2
        self.setPos( CST.toCcsCoord(
            self.ccs, self.x, self.y )
        )
