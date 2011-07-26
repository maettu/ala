#!/usr/bin/python

# Cartesian Coordinate System Widget
# ----------------------------------



from PyQt4.QtCore import (Qt, QRectF, QPointF, QLineF, QTimer, QObject, SIGNAL, QString)
from PyQt4.QtGui import (QApplication, QGraphicsScene, QGraphicsView, 
    QGraphicsItem, QPen, QColor, QDialog, QVBoxLayout, QBrush, QPainter)

class CartesianCoordinateSystemWidget(QGraphicsItem):
    """This widget is used to draw items on it. It shows axis, grid
    (if desired) and provides the ability to draw items on items
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
        
        # todo: investigate why QRectF needs to be larger than
        # expected.. (does it?!)
        self.Rect = QRectF(-width, -height, width*2, height*2)
        
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
        
    # Translates cartesian coordinates (from own coord. system)
    # to item coordinates
    # i.e. give it x = 2, y = 5 and receive 150,370 or something alike.
    
    # this method supposedly needs to go in separate helper class
    def toItemCoord(self, x, y):
        # number of items is max - min, 12 - -3 = 15 :-)
        numberXItems = self.xMax - self.xMin
        numberYItems = self.yMax - self.yMin
        
        # width / countNumber -> width of one item
        xItem = self.width / numberXItems * x
        yItem = - (self.height/ numberYItems * y)
        
        return QPointF(xItem, yItem)
        

    def paint(self, painter, option, widget=None):
        ordinateColor = QPen(QColor(255, 0, 0))
        normalLineCol = QPen(QColor(0, 0, 255))
        
        for i in range (self.xMin, self.xMax+1):
            if i == 0:
                painter.setPen(ordinateColor)
            else:
                painter.setPen(normalLineCol)
                
            painter.drawLine(
                self.toItemCoord(i,self.yMin), 
                self.toItemCoord(i,self.yMax)
            )
            
            tickCoord = self.toItemCoord(i, 0)
            tickCoord += self.toItemCoord(self.tickXOffset, self.tickYOffset)
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
                self.toItemCoord(self.xMin,i), 
                self.toItemCoord(self.xMax,i)
            )
            
            tickCoord = self.toItemCoord(0,i)
            tickCoord += self.toItemCoord(self.tickXOffset, self.tickYOffset)
            painter.drawText(
                tickCoord,
                QString.number(i)
            )
            
    def addPoint(self, x,y, size, red=0,green=200,blue=0):
        p = self.toItemCoord(x,y)
        x = p.x() - size / 2
        y = p.y() - size / 2
        point = PointMovable(self,x,y,size,red,green,blue)
        return point
        
    def addPointDependent(self, parent, x,y, size,red=0,green=100,blue=0):
        p = self.toItemCoord(x,y)
        x = p.x()
        y = p.y()
        return PointMovable(parent, x,y,size,red,green,blue)
        
    def addLineDependent(self, startPoint, endPoint):
        return LineAutoMove(startPoint, endPoint)

# movable Point, by coordinate system automatically positioned.
# has coordinate system as parent (at the moment, every class could
# instantiate PointMovable)

# should go into separate file, I suppose
class PointMovable(QGraphicsItem):
    """Defines a movable point. """
    
    def __init__(self, parent, x, y, size, red=0, green=255, blue=0):
        super(PointMovable, self).__init__(parent)
        
        self.Rect = QRectF(0, 0, size, size)
        
        self.color = QColor(red, green, blue)
        
        self.x = x
        self.y = y
        self.setPos(QPointF(self.x, self.y))
        
    def boundingRect(self):
        return self.Rect
        
    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(self.Rect)
        
    # at the moment, point is movable by either left or right
    # mouse click. hm...
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            print 'left click'
        elif e.button() == Qt.RightButton:
            print "right click"
        else:
            print "other click"
        
        # save where in Item mouse was clicked
        self.xOnWidget = e.pos().x()
        self.yOnWidget = e.pos().y()
            
    def mouseMoveEvent(self, e):
        
        x_move = e.pos().x() - self.xOnWidget
        y_move = e.pos().y() - self.yOnWidget
        
        self.x = self.x + x_move
        self.y = self.y + y_move
        
        self.setPos(QPointF(self.x, self.y))
        
class LineAutoMove(QGraphicsItem):
    """Defines a line by two points. If points are moved, line follows these movements."""
    
    def __init__(self, startPoint, endPoint):
        super(LineAutoMove, self).__init__(startPoint)
        
        self.startPoint = startPoint
        self.endPoint = endPoint
        
        self.Rect = QRectF(0,0, endPoint.x,endPoint.y)
        
        self.color = QColor(255,0,0)
        
    def boundingRect(self):
        return self.Rect
        
    def paint(self, painter, option, widget=None):
        painter.setPen(QColor("orange"))
        
        # as soon as dependent points are *not relative* to parent points any more,
        # this needs to be changed.
        painter.drawLine(QLineF(0, 0, self.endPoint.x, self.endPoint.y))
        print self.startPoint.x, self.startPoint.y, self.startPoint.x+self.endPoint.x, self.startPoint.y+self.endPoint.y
    
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
  
    
    # eieiei, dependent points have coordinates *relative* to parent point.. :-S
    point1 = ccs.addPoint(3,3,10)
    point2 = ccs.addPointDependent(point1,1,1,10)
    point3 = ccs.addPointDependent(point2,-1,0,10,0,0,100)
    
    line1 = ccs.addLineDependent(point1,point2)
    
    scene.addItem(ccs)
    
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(view)
    dialog.setLayout(layout)
    dialog.setWindowTitle("ala - coordinate system")
    
    
    dialog.show()
    
    app.exec_()
    
    
    
    