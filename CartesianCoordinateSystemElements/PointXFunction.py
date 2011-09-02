#!/usr/bin/python

from Point import Point
import Helper.CoordinateSystemTransformation as CST

class PointXFunction(Point):
    """Defines a movable point with an y which is functionally
    dependent on its x value."""

    # TODO function as a parameter
    def __init__( self, ccs, parent, x, y, size, red=200, green=0,
                    blue=0):
        super(PointXFunction, self).__init__(ccs,
            parent, x, y, size, red, green, blue)

    def updateYourself(self, x):
        # TODO point moves *relatively* to parent, does not just take
        # its x value
        self.x = x
        self.y = x**2
        self.setPos( CST.toCcsCoord(
            self.ccs, self.x, self.y)
        )
