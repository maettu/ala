#!/usr/bin/python

# Cartesian Coordinate System Widget
# ----------------------------------

# This widget is used to draw items on it. It shows axis, grid
# (if desired) and provides the ability to draw items on items
# according to its coordinate system. It translates the underlying
# coordinate system into its own according to users settings.

from PyQt4.QtCore import (Qt, QRectF, QPointF, QTimer, QObject, SIGNAL, QString)
from PyQt4.QtGui import (QApplication, QGraphicsScene, QGraphicsView, 
    QGraphicsItem, QPen, QColor, QDialog, QVBoxLayout)

class CartesianCoordinateSystemWidget(QGraphicsItem):
    def __init__(self, width=500, height=500, xMin = -10, xMax = 10, yMin = -10, yMax = 10):
        super(CartesianCoordinateSystemWidget, self).__init__()
        
        self.width  = width
        self.height = height
        self.xMin   = xMin
        self.xMax   = xMax
        self.yMin   = yMin
        self.yMax   = yMax
        
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
            self.xAxis = width / (xMax - xMin) * -xMin
            
        if yMin <= 0 and yMax <= 0:
            self.yAxis = height
        elif yMin >= 0 and yMax >= 0:
            self.yAxis = 0
        else:
            self.yAxis = height / (yMax - yMin) * -yMin
        
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
    def toItemCoord(self, x, y):
        # number of items is max - min, 12 - -3 = 15 :-)
        numberXItems = self.xMax - self.xMin
        numberYItems = self.yMax - self.yMin
        
        # width / countNumber -> width of one item
        xItem = self.width / numberXItems * x
        yItem = self.height/ numberYItems * y
        
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
            
            painter.drawText(
                self.toItemCoord(i, 0),
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
            
            painter.drawText(
                self.toItemCoord(0,i),
                QString.number(i)
            )


if __name__ == '__main__':
    import sys

    # this is to be factored out into a general loader.
    app = QApplication(sys.argv)
    
    width = 500
    height = 500
    
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, width, height)
    
    view = QGraphicsView()
    view.setScene(scene)
    
    ccs = CartesianCoordinateSystemWidget(width, height, -2,4,-10,10)
    scene.addItem(ccs)
    
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(view)
    dialog.setLayout(layout)
    dialog.setWindowTitle("ala - coordinate system")
    
    
    dialog.show()
    
    app.exec_()
    
    
    
    