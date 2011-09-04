#!/usr/bin/python

# Cartesian Coordinate System Widget
# ----------------------------------

from PyQt4.QtCore import (Qt, QRectF, QPointF, QLineF, QTimer, QObject, SIGNAL, QString)
from PyQt4.QtGui import (QApplication, QGraphicsScene, QGraphicsView, 
    QGraphicsItem, QPen, QColor, QDialog, QVBoxLayout, QBrush, QPainter)

from CartesianCoordinateSystemElements.Point import Point
from CartesianCoordinateSystemElements.PointXFunction import PointXFunction
from CartesianCoordinateSystemElements.Line  import Line
from CartesianCoordinateSystemElements.PointWithXFromOneParentAndYFromAnother import PointWithXFromOneParentAndYFromAnother
from CartesianCoordinateSystemElements.FunctionPlotter import FunctionPlotter

import Helper.CoordinateSystemTransformation as CST

class CartesianCoordinateSystemWidget(QGraphicsItem):
    """This widget is used to draw items on. It shows axis, grid
    (if desired) and provides the ability to draw items
    according to its coordinate system. It translates the underlying
    coordinate system into its own according to users settings."""
    
    def __init__(
            self, widthPixel=500, 
            heightPixel=500, 
            marginPixel = 10, 
            xMin = -10, 
            xMax = 10, 
            yMin = -10, 
            yMax = 10, 
            tickXOffset=0.1, 
            tickYOffset=0.1
        ):
        super(CartesianCoordinateSystemWidget, self).__init__()
        
        self.width          = widthPixel - marginPixel * 2
        self.height         = heightPixel - marginPixel * 2
        self.margin         = marginPixel
        self.xMin           = xMin
        self.xMax           = xMax
        self.yMin           = yMin
        self.yMax           = yMax
        self.tickXOffset    = tickXOffset
        self.tickYOffset    = tickYOffset
        
        self.Rect = QRectF( -width/2, -height/2 , width, height)
        
        # centre of logical coordinate system gets
        # positioned where (0,0) of the origin of
        # ordinates of the cartesian coordinate system lies.
        # Unless both extremes are either positive or negative.
        # Then, it is on either side of the visible area.
        
        # note for self: is this desired? ordinates could as well
        # be outside visible area
        
        # todo: catch when min > max or min == max
        
        if xMin <= 0 and xMax <= 0:
            self.xAxis = width
        elif xMin >= 0 and xMax >= 0:
            self.xAxis = 0
        else:
            self.xAxis = width / (xMax - xMin) * -xMin + self.margin / 2
            
        if yMin <= 0 and yMax <= 0:
            self.yAxis = height
        elif yMin >= 0 and yMax >= 0:
            self.yAxis = 0
        else:
            self.yAxis = height - (height / (yMax - yMin) * -yMin) - self.margin / 2
        
        self.setPos(QPointF(self.xAxis, self.yAxis))
        
        # some fun :-)
        # rotate the coordinate system
        
        #~ self.timer = QTimer()
        #~ QObject.connect(self.timer, SIGNAL("timeout()"), self.timeout)
            
        #~ self.timer.start(20)
            
    #~ def timeout(self):
        #~ self.rotate(1)
     
        # end of fun
        
    # implementation mandatory
    def boundingRect(self):
        return self.Rect

    def paint(self, painter, option, widget=None):
        ordinateColor = QPen(QColor(255, 0, 0))
        normalLineCol = QPen(QColor(0, 0, 255))
        
        for i in range (self.xMin, self.xMax+1):
            if i == 0:
                painter.setPen(ordinateColor)
            else:
                painter.setPen(normalLineCol)
                
            painter.drawLine(
                CST.toCcsCoord(self, i,self.yMin), 
                CST.toCcsCoord(self, i,self.yMax)
            )
            
            tickCoord = CST.toCcsCoord(self, i, 0)
            tickCoord += CST.toCcsCoord(self, self.tickXOffset, self.tickYOffset)
            painter.drawText(
                tickCoord,
                QString.number(i)
            )

        for i in range (self.yMin, self.yMax+1):
            
            if i == 0:
                painter.setPen(ordinateColor)
            else:
                painter.setPen(normalLineCol)
            
            painter.drawLine(
                CST.toCcsCoord(self, self.xMin,i), 
                CST.toCcsCoord(self, self.xMax,i)
            )
            
            tickCoord = CST.toCcsCoord(self, 0,i)
            tickCoord += CST.toCcsCoord(self, self.tickXOffset, self.tickYOffset)
            painter.drawText(
                tickCoord,
                QString.number(i)
            )
            
    def addPoint(self, x,y, size, red=0,green=200,blue=0):
        point = Point(self, self,x,y,size,red,green,blue)
        # After addPointDependet is removed, 2nd parameter becomes obsolete(?)
        return point
    # This Point is not really needed. It makes for an
    # linearily dependet point. Who wanted this?!
    # Interesting are points with a dependence according to a
    # mathematical function. there, of course, should it be *very* easy to
    # emulate a linearily depending point.
    # TODO factor out
    def addPointDependent( self, parent, x,y, size,red=0,green=100,blue=0 ):
        return Point( self, parent, x,y,size,red,green,blue )

    def addPointXFunction( self, parent, x, function, size,red=200,green=0,blue=0 ):
        # make a point of its own; directly dependent to coordinate system
        point = PointXFunction( self, self, x, size,red,green,blue, function )

        # make itself a child of another point; or some points
        # (no type checking so far)
        if parent:
            for p in parent:
                p.addChildPoint(point)
        
        return point

    def addPointWithXFromOnePointAndYFromAnother( self, xParent, yParent ):
        point = PointWithXFromOneParentAndYFromAnother( self, xParent, yParent )  
        xParent.addChildPoint(point)
        yParent.addChildPoint(point)
        return point
        
    def addLineDependent( self, startPoint, endPoint ):
        line = Line(
            startPoint, 
            endPoint, 
            ccs = self
        )
        # TODO This needs a rename..
        startPoint.addChildPoint(line)
        endPoint.addChildPoint(line)
        return line

    def addFunction( self, function ):
        function = FunctionPlotter( self, function )
        return function
    
if __name__ == '__main__':
    import sys

    # this is to be factored out into a general loader.
    app = QApplication(sys.argv)
    
    width = 520
    height = 520
    
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, width, height)
    
    view = QGraphicsView()
    view.setScene(scene)
    view.setRenderHint(QPainter.Antialiasing)
    
    ccs = CartesianCoordinateSystemWidget(width, height, 10, -2,4,-1,10)
    
    # coordinates are always relative to coordinate system, as it should be
    #point1 = ccs.addPoint(3,3,10)
    #point2 = ccs.addPointDependent(point1,1,1,10)
    #point3 = ccs.addPointDependent(point2,-1,0,10,0,0,100)
    
    function = '0.5*x**2'
    
    # two points on a function
    point1 = ccs.addPointXFunction                          ( None,    1, function, 10 )
    point2 = ccs.addPointXFunction                          ( [point1],  2, '0.5*x**2', 10 )
    # third point, invisible, to form triangle
    point3 = ccs.addPointWithXFromOnePointAndYFromAnother   ( point2, point1 )

    line1 = ccs.addLineDependent( point1, point2 )
    line2 = ccs.addLineDependent( point2, point3 )
    line3 = ccs.addLineDependent( point1, point3 )
    
    function = ccs.addFunction( function )
    
    scene.addItem( ccs )
    
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget( view )
    dialog.setLayout(layout)
    dialog.setWindowTitle( "ala - coordinate system" )
    
    
    dialog.show()
    
    app.exec_()
    
    
    
    
    
