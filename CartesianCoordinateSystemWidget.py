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
    def __init__(self):
        super(CartesianCoordinateSystemWidget, self).__init__()
        
        self.Rect = QRectF(-100, -100, 200, 200)
        
        self.setPos(QPointF(250, 250))
     
    # needs implementation 
    def boundingRect(self):
        return self.Rect

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(QColor(255, 0, 0)))
        painter.drawLine(-250,0,250,0)
        painter.drawLine(0,-250,0,250)
        
  

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 500, 500)
    
    view = QGraphicsView()
    view.setScene(scene)
    
    ccs = CartesianCoordinateSystemWidget()
    scene.addItem(ccs)
    
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(view)
    dialog.setLayout(layout)
    dialog.setWindowTitle("ala - coordinate system")
    
    
    dialog.show()
    
    app.exec_()
    