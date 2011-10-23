#!/usr/bin/python

# Cartesian Coordinate System Widget
# ----------------------------------

from PyQt4.QtCore import (Qt, QRectF, QPointF, QLineF, QTimer, QObject, SIGNAL, QString)
from PyQt4.QtGui import (QApplication, QGraphicsScene, QGraphicsView, 
    QGraphicsItem, QPen, QColor, QDialog, QVBoxLayout, QBrush, QPainter)

from CartesianCoordinateSystemElements.Point import Point
from CartesianCoordinateSystemElements.PointXFunction import PointXFunction
from CartesianCoordinateSystemElements.Line  import Line
from CartesianCoordinateSystemElements.Rectangle  import Rectangle
from CartesianCoordinateSystemElements.PointWithXFromOneParentAndYFromAnother import PointWithXFromOneParentAndYFromAnother
from CartesianCoordinateSystemElements.FunctionPlotter import FunctionPlotter

import Helper.CoordinateSystemTransformation as CST

class CartesianCoordinateSystemWidget(QGraphicsItem):
    """This widget is used to draw items on. It shows axis, grid
    (if desired) and provides the ability to draw items
    according to its coordinate system. It translates the underlying
    coordinate system into its own according to users settings."""
    
    def __init__(
            self, scene, 
            widthPixel=500, 
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
        
        # TODO: swap xMin, xMax and yMin, yMax if min>max
        
        self.width          = widthPixel - marginPixel * 2
        self.height         = heightPixel - marginPixel * 2
        self.margin         = marginPixel
        self.xMin           = xMin
        self.xMax           = xMax
        self.yMin           = yMin
        self.yMax           = yMax
        self.tickXOffset    = tickXOffset
        self.tickYOffset    = tickYOffset
        
        # TODO, hardcoding is bad.
        #~ self.ySkip          = 1
        
        # TODO: yRange needs to be adjusted to axis. start -7, skip = 2 -> Axis not drawn. Bad.
        #~ self.yRange         = []
        #~ for i in range (self.yMin-self.ySkip, self.yMax+2*self.ySkip):
            #~ if i % self.ySkip == 0:
                #~ self.yRange.append( i )
                
        
        # needed for explicit adds of elements like FunctionPlotter. How to get rid of this?
        self.scene = scene
        
        # centre of logical coordinate system gets
        # positioned where (0,0) of the origin of
        # ordinates of the cartesian coordinate system lies.
        # Unless both extremes are either positive or negative.
        # Then, it is on either side of the visible area.
        
        # note for self: is this desired? ordinates could as well
        # be outside visible area
        
        # todo: catch when min > max or min == max
        
        self.initialize();
        
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
        
    def initialize(self):
        if self.xMin <= 0 and self.xMax <= 0:
            self.xAxis = self.width
        elif self.xMin >= 0 and self.xMax >= 0:
            self.xAxis = 0
        else:
            self.xAxis = self.width / ( self.xMax - self.xMin ) * -self.xMin + self.margin / 2
            
        if self.yMin <= 0 and self.yMax <= 0:
            self.yAxis = self.height
        elif self.yMin >= 0 and self.yMax >= 0:
            self.yAxis = 0
        else:
            self.yAxis = self.height - ( self.height / (self.yMax - self.yMin) * -self.yMin ) - self.margin / 2
        
        # make Rect safely larger than window.
        self.Rect = QRectF( 
            self.xMin - self.xAxis - 100, 
            self.yMin - self.yAxis - 100, 
            self.width             + 200, 
            self.height            + 200
        )
        self.setPos( QPointF( self.xAxis, self.yAxis ) )

    def paint(self, painter, option, widget=None):
        ordinateColor = QPen( QColor(255, 0, 0 ) )
        normalLineCol = QPen( QColor(0, 0, 255 ) )
        
        for i in range ( self.xMin-1 , self.xMax+2 ):
            if i == 0:
                painter.setPen( ordinateColor )
            else:
                painter.setPen( normalLineCol )
            
            #~ if i == 0:
            painter.drawLine(
                CST.toCcsCoord( self, i,self.yMin-1 ), 
                CST.toCcsCoord( self, i,self.yMax+1 )
            )
            
            tickCoord = CST.toCcsCoord(self, i, 0)
            tickCoord += CST.toCcsCoord(self, self.tickXOffset, self.tickYOffset)
            painter.drawText(
                tickCoord,
                QString.number(i)
            )

        for i in range (self.yMin-1, self.yMax+2):
        #~ for i in self.yRange :
            #~ print i
            
            if i == 0:
                painter.setPen(ordinateColor)
            else:
                painter.setPen(normalLineCol)
            
            #~ if i == 0:
            painter.drawLine(
                CST.toCcsCoord( self, self.xMin-1,i ), 
                CST.toCcsCoord( self, self.xMax+1,i )
            )
            
            tickCoord = CST.toCcsCoord(self, 0,i)
            tickCoord += CST.toCcsCoord(self, self.tickXOffset, self.tickYOffset)
            painter.drawText(
                tickCoord,
                QString.number(i)
            )
            
    # drag coordinate system around
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # save where in item the mouse was clicked
            self.xOnWidget = e.pos().x()
            self.yOnWidget = e.pos().y()
            self.leftMouseButtonPressed = 1
            
            #~ self.scaleMe( 1.4 )
        
        #~ if e.button() == Qt.RightButton:
            #~ self.scaleMe( 1.4 )
            
    def scaleMe(self, factor):
            self.scale         ( factor, factor )
            self.function.scale( factor, factor )
        
    def mouseMoveEvent(self, e):
        if self.leftMouseButtonPressed:
            x_move = e.pos().x() - self.xOnWidget
            y_move = e.pos().y() - self.yOnWidget
            
            self.xAxis = self.x() + x_move
            self.yAxis = self.y() + y_move
           
            self.setPos( QPointF( self.xAxis, self.yAxis ) )
            
            # xMin is left border (scene-coord = 0) an yMax is top border (scene-coord = 0)
            min = self.mapToScene( CST.toCcsCoord( self, self.xMin, self.yMax ) )
            max = self.mapToScene( CST.toCcsCoord( self, self.xMax, self.yMin ) )
            if min.x() < 0:
                self.xMin += 1
                self.xMax += 1

            if max.x() > self.width:
                self.xMin -= 1
                self.xMax -= 1
                
            if min.y() < 0:
                self.yMin -= 1
                self.yMax -= 1
                #~ print "bumm"
            
            if max.y() > self.height:
                self.yMin += 1
                self.yMax += 1
                
            # reset Rect to allow for infinite moves
            self.Rect = QRectF( 
                    self.xMin - self.xAxis - 100, 
                    self.yMin - self.yAxis - 100, 
                    self.width             + 200, 
                    self.height            + 200
            )
                
            #~ print min.y(), max.y()
                
            
            # TODO: check if coordinate system still covers whole window and adjust if appropriate
            
    def mouseReleaseEvent(self, e):
        self.leftMouseButtonPressed = None
            
    def addPoint(self, x,y, size, red=0,green=200,blue=0):
        point = Point(self, self,x,y,size,red,green,blue)
        # After addPointDependent is removed, 2nd parameter becomes obsolete(?)
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
        
    def addLine( self, startPoint, endPoint, paintToBorder = False, showIncline = False, color = 'orange', minLength = 0):
        line = Line( startPoint, endPoint, self, paintToBorder, showIncline, color, minLength )
        return line
            
        
    def addLineDependent( self, startPoint, endPoint, paintToBorder = False, showIncline = False, color = 'orange', minLength = 0):
        line = Line(
            startPoint, 
            endPoint, 
            self,
            paintToBorder,
            showIncline,
            color,
            minLength
        )
        # TODO This needs a rename..
        startPoint.addChildPoint(line)
        endPoint.addChildPoint(line)
        return line
    
    def addRectangle( self, startPoint, endPoint, color = 'blue' ):
        rect = Rectangle(
            startPoint,
            endPoint,
            self,
            color
        )
        return rect
        
    def addFunction( self, function ):
        self.function = FunctionPlotter( self, function )
        
        # Hmm, obviously function needs an explicit add to the scene..
        self.scene.addItem( self.function ) 
        return self.function
    
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
    
    ccs = CartesianCoordinateSystemWidget(scene, width, height, 10, -5,5,-1,10)
    
    # coordinates are always relative to coordinate system, as it should be
    #point1 = ccs.addPoint(3,3,10)
    #point2 = ccs.addPointDependent(point1,1,1,10)
    #point3 = ccs.addPointDependent(point2,-1,0,10,0,0,100)
    
    function = '2.71**x'
    
    # two points on a function
    point1 = ccs.addPointXFunction                          ( None,    1,   function, 10, 0,0,200 )
    point2 = ccs.addPointXFunction                          ( [point1],  2, function, 10 )
    # third point, invisible, to form triangle
    point3 = ccs.addPointWithXFromOnePointAndYFromAnother   ( point2, point1 )

    line1 = ccs.addLineDependent( point1, point2 , True, True, 'red')
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
    
    
    
    
    
