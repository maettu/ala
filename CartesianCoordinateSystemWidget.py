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
    def __init__(self, width=500, height=500):
        super(CartesianCoordinateSystemWidget, self).__init__()
        
        self.width = width
        self.height= height
        
        self.Rect = QRectF(-width/2, -height/2, width, height)
        
        self.setPos(QPointF(width/2, height/2))
     
    # needs implementation 
    def boundingRect(self):
        return self.Rect

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(QColor(255, 0, 0)))
        painter.drawLine(-self.width/2,0,self.width/2,0)
        painter.drawLine(0,-self.height/2,0,self.height/2)
        
  


if __name__ == '__main__':
    import sys

    # this ist to be factored out into a general loader.
    app = QApplication(sys.argv)
    
    width = 700
    height = 200
    
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
    
    
    
    