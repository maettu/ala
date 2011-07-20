#!/usr/bin/python

# Cartesian Coordinate System Widget
# ----------------------------------

# This widget is used to draw items on it. It shows axis, grid
# (if desired) and provides the ability to draw items on items
# according to its coordinate system. It translates the underlying
# coordinate system into its own according to users settings.

from PyQt4.QtCore import (Qt, QRectF, QPointF, QTimer, QObject, SIGNAL, QString)
from PyQt4.QtGui import (QApplication, QGraphicsScene, QGraphicsView, 
    QGraphicsItem, QPen, QColor, QDialog, QVBoxLayout, QBrush)

class CartesianCoordinateSystemWidget(QGraphicsItem):
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
        
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.timeout)
            
        self.timer.start(20)
            
    def timeout(self):
        self.rotate(1)
     
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
            
    def addPoint(self, x,y, size):
        p = self.toItemCoord(x,y)
        x = p.x()
        y = p.y()
        print x,y
        point = PointMovable(0,255,0,x,y,size, self)

# movable Point, by coordinate system automatically positioned.
# has coordinate system as parent (at the moment, every class could
# instantiate PointMovable

# should go into separate class, I suppose
class PointMovable(QGraphicsItem):
    def __init__(self, red, green, blue, x, y, size, parent):
        super(PointMovable, self).__init__(parent)
        
        self.Rect = QRectF(0, 0, size, size)
        
        self.color = QColor(red, green, blue)
        
        self.x = x
        self.y = y
        self.setPos(QPointF(self.x-size/2, self.y-size/2))
        
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
    
    ccs = CartesianCoordinateSystemWidget(width, height, 10, -2,4,-1,10)
    scene.addItem(ccs)
    
    ccs.addPoint(3,3,10)
    
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(view)
    dialog.setLayout(layout)
    dialog.setWindowTitle("ala - coordinate system")
    
    
    dialog.show()
    
    app.exec_()
    
    
    
    