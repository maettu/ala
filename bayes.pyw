#!/usr/bin/python
# -*- coding: utf-8 -*-

# Visualisation of the Bayes Theorem.


from __future__ import unicode_literals

from PyQt4.QtCore import (  Qt, 
                            QRectF, 
                            QPointF, 
                            QLineF, 
                            QTimer, 
                            QObject, 
                            SIGNAL, 
                            QString
                        )
from PyQt4.QtGui import (   QApplication, 
                            QFrame,
                            QGraphicsScene, 
                            QGraphicsView, 
                            QGraphicsItem, 
                            QPen, 
                            QColor, 
                            QDialog, 
                            QVBoxLayout, 
                            QHBoxLayout, 
                            QPushButton, 
                            QLabel, 
                            QBrush, 
                            QPainter,
                            QDoubleSpinBox,
                            QMessageBox
                        )

import sys
import time

from ala.CartesianCoordinateSystem import CartesianCoordinateSystemWidget


# The main window. Initiates all layouts and widgets.
# Initiates the signal-slot connections.
class MainWindow( QDialog ):
    def __init__( self, parent=None ):
        super( MainWindow, self ).__init__(parent)
        
        
        # (object) variable definitions
        # -----------------------------
        
        width  = 500
        height = 500
        
        
        
        # General setup
        # -------------
        
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, width, height)

        view = QGraphicsView                ()
        view.setScene                       ( scene                 )
        view.setRenderHint                  ( QPainter.Antialiasing )
        view.setHorizontalScrollBarPolicy   ( Qt.ScrollBarAlwaysOff )
        view.setVerticalScrollBarPolicy     ( Qt.ScrollBarAlwaysOff )
        
        self.ccs = CartesianCoordinateSystemWidget(scene, width, height, 10, 0,10, 0,11)
        scene.addItem( self.ccs )
        
        #total probability
        
        self.probabilityTotal = 0.4

        self.probabilityTotalPositiveRectangle = self.ccs.addRectangle( 
            QPointF( 0,0), 
            QPointF( self.probabilityTotal * 10, 10 ), 
            'yellow', 
            'red',
            0.3 
        )
        self.probabilityTotalNegativeRectangle = self.ccs.addRectangle( 
            QPointF( self.probabilityTotal * 10,0), 
            QPointF(10,10), 
            'red', 
            'yellow', 
            0.3 
        )
        
        # relative probabilities
        self.probabilityRelativePositive = 0.7
        self.probabilityRelativeNegative = 0.4
        
        self.probabilityRelativePositiveRectangle = self.ccs.addRectangle(
            QPointF( 0,0 ),
            QPointF( self.probabilityTotal * 10, self.probabilityRelativePositive * 10 ),
            'blue',
            'lightBlue',
            0.5
        )
        
        self.probabilityRelativeNegativeRectangle = self.ccs.addRectangle(
            QPointF( self.probabilityTotal * 10, self.probabilityRelativeNegative * 10 ),
            QPointF( 10 ,0 ),
            'green',
            'lightGreen',
            0.5
        )
        
        # Layout & widgets
        # ----------------
        
        layout = QVBoxLayout            ()
        layout.addWidget                ( view )
        
        # change total probability
        changeTotalLayout = QHBoxLayout()
        
        self.probabilityTotalSpinBox = QDoubleSpinBox()
        self.probabilityTotalSpinBox.setMinimum( 0 )
        self.probabilityTotalSpinBox.setMaximum( 1 )
        self.probabilityTotalSpinBox.setValue( self.probabilityTotal )
        self.probabilityTotalSpinBox.setSingleStep( 0.1 )
        
        changeTotalLayout.addWidget( QLabel( "Total-Wahrscheinlichkeit:" ) )
        changeTotalLayout.addWidget( self.probabilityTotalSpinBox )
        
        layout.addLayout( changeTotalLayout )

        # change to positive relative total
        changeRelativePositiveLayout =  QHBoxLayout()
        self.probabilityRelativePositiveSpinBox =  QDoubleSpinBox()
        self.probabilityRelativePositiveSpinBox.setMinimum( 0 )
        self.probabilityRelativePositiveSpinBox.setMaximum( 1 )
        self.probabilityRelativePositiveSpinBox.setSingleStep( 0.1 )
        self.probabilityRelativePositiveSpinBox.setValue( self.probabilityRelativePositive )
        
        changeRelativePositiveLayout.addWidget(  QLabel ( 
            "relative Wahrscheinlichkeit unter der Bedingung, dass Total-Wahrscheinlichkeit wahr:" ) )
        changeRelativePositiveLayout.addWidget( self.probabilityRelativePositiveSpinBox )
            
        layout.addLayout( changeRelativePositiveLayout )
        
        # change to negative relative total
        changeRelativeNegativeLayout =  QHBoxLayout()
        self.probabilityRelativeNegativeSpinBox =  QDoubleSpinBox()
        self.probabilityRelativeNegativeSpinBox.setMinimum( 0 )
        self.probabilityRelativeNegativeSpinBox.setMaximum( 1 )
        self.probabilityRelativeNegativeSpinBox.setSingleStep( 0.1 )
        self.probabilityRelativeNegativeSpinBox.setValue( self.probabilityRelativeNegative )
        
        changeRelativeNegativeLayout.addWidget(  QLabel ( 
            "relative Wahrscheinlichkeit unter der Bedingung, dass Total-Wahrscheinlichkeit falsch:" ) )
        changeRelativeNegativeLayout.addWidget( self.probabilityRelativeNegativeSpinBox )
            
        layout.addLayout( changeRelativeNegativeLayout )
        
        self.setLayout              ( layout )

        # signal - method connections
        # ---------------------------
        
        self.connect                (self.probabilityTotalSpinBox, SIGNAL( "valueChanged(double)" ),
                                                                self.redraw           )
                                                                
        self.connect                (self.probabilityRelativePositiveSpinBox, SIGNAL( "valueChanged(double)" ),
                                                                self.redraw           )
                                                                
        self.connect                (self.probabilityRelativeNegativeSpinBox, SIGNAL( "valueChanged(double)" ),
                                                                self.redraw           )
                                                    
        self.setWindowTitle         ( "Bedingte Wahrscheinlichkeiten"  )
        
        
    def redraw( self ):
        self.probabilityTotal = self.probabilityTotalSpinBox.value()
        self.probabilityTotalPositiveRectangle.setPosition(
            QPointF( 0,0),
            QPointF( self.probabilityTotal * 10, 10 )
        )
        
        self.probabilityTotalNegativeRectangle.setPosition( 
            QPointF( self.probabilityTotal * 10,0), 
            QPointF(10,10)
        )
        
        self.probabilityRelativePositive = self.probabilityRelativePositiveSpinBox.value()
        self.probabilityRelativePositiveRectangle.setPosition(
            QPointF( 0,0 ),
            QPointF( self.probabilityTotal * 10, self.probabilityRelativePositive * 10 )
        )
        
        self.probabilityRelativeNegative = self.probabilityRelativeNegativeSpinBox.value()
        self.probabilityRelativeNegativeRectangle.setPosition(
            QPointF( self.probabilityTotal * 10, self.probabilityRelativeNegative * 10 ),
            QPointF( 10 ,0 )
        )

        self.ccs.update()


# main program
# ------------

app = QApplication(sys.argv)

dialog = MainWindow(  )

dialog.show()

app.exec_()
