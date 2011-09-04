#!/usr/bin/python

from Point import Point
import Helper.CoordinateSystemTransformation as CST

class PointWithXFromOneParentAndYFromAnother( Point ):
    """Handy for making up triangles"""

    def __init__( self, ccs, xParent, yParent, size=0, 
                    red=0, green=0, blue=0):
        super( PointWithXFromOneParentAndYFromAnother, self ).__init__(
                    ccs, ccs, xParent.x, yParent.y, size, red, green,
                    blue )

        self.xParent = xParent
        self.yParent = yParent

    def updateYourself( self, xDelta, yDelta ):
        # discard parameters..
        self.x = self.xParent.x
        self.y = self.yParent.y


