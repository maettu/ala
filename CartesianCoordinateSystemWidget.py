#!/usr/bin/python

# Cartesian Coordinate System Widget
# ----------------------------------

# This widget is used to draw items on it. It shows axis, grid
# (if desired) and provides the ability to draw items on items
# according to its coordinate system. It translates the underlying
# coordinate system into its own according to users settings.

from PyQt4.QtCore import (Qt, QRectF, QPointF)
from PyQt4.QtGui import (QApplication, QGraphicsScene, QGraphicsView, 
    QGraphicsItem, QPen, QColor, QDialog, QVBoxLayout)

class CartesianCoordinateSystemWidget(QGraphicsItem):
    def __init__(self, width=500, height=500, xMin = -10, xMax = 1, yMin = -1, yMax = 10):
        super(CartesianCoordinateSystemWidget, self).__init__()
        
        self.width  = width
        self.height = height
        self.xMin   = xMin
        self.xMax   = xMax
        self.yMin   = yMin
        self.yMax   = yMax
        
        self.Rect = QRectF(-width/2, -height/2, width, height)
        
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
            
        print self.xAxis, self.yAxis
        
        self.setPos(QPointF(self.xAxis, self.yAxis))
     
    # implementation mandatory
    def boundingRect(self):
        return self.Rect

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(QColor(255, 0, 0)))
        
        #~ for i in range (self.xMin, self.xMax+1):
            #~ painter.drawLine(-self.height/2, , self.heigt/2
            #~ print i
            
        # todo..
        painter.drawLine(-self.width, 0, self.width, 0)
        painter.drawLine(0,-self.height/2,0,self.height/2)
        
  


if __name__ == '__main__':
    import sys

    # this ist to be factored out into a general loader.
    app = QApplication(sys.argv)
    
    width = 500
    height = 500
    
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, width, height)
    
    view = QGraphicsView()
    view.setScene(scene)
    
    ccs = CartesianCoordinateSystemWidget(width, height)
    scene.addItem(ccs)
    
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(view)
    dialog.setLayout(layout)
    dialog.setWindowTitle("ala - coordinate system")
    
    
    dialog.show()
    
    app.exec_()
    
    
    
    