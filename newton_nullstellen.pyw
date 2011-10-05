#!/usr/bin/python
# -*- coding: utf-8 -*-

# Yes, it is true: python insists on explicitly asking for unicode support
# when using unicode characters in comments.

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
                            QDoubleSpinBox
                        )

import sys

from ala.CartesianCoordinateSystem import CartesianCoordinateSystemWidget



class MainWindow( QDialog ):
    def __init__( self, parent=None ):
        super( MainWindow, self ).__init__(parent)
        
        width  = 520
        height = 520
        
        # May be ax³ + bx² + cx + d and nothing else for this app.
        # This is a somewhat narrow limitation but it is enough
        # for educational purposes.
        function ="1.0*x**3 + 4.0*x**2 + 2.0*x - 2.0"


        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, width, height)

        view = QGraphicsView()
        view.setScene(scene)
        view.setRenderHint(QPainter.Antialiasing)
        
        self.ccs = CartesianCoordinateSystemWidget(scene, width, height, 10, -5,5, -2,8)

        # the parameters of the function ax³ + bx² + cx + d
        self.a = QDoubleSpinBox()
        # set minimum to a (large) negative number. Default is 0..
        self.a.setMinimum   ( -1000 )
        self.a.setValue( 1 )
        
        self.b = QDoubleSpinBox()
        self.b.setMinimum   ( -1000 )
        self.b.setValue( 4 )
        
        self.c = QDoubleSpinBox()
        self.c.setMinimum   ( -1000 )
        self.c.setValue( 2 )
        
        self.d = QDoubleSpinBox()
        self.d.setMinimum   ( -1000 )
        self.d.setValue     ( -2 )
        
        self.x__3 = QLabel( "x<sup>3</sup> +" )
        self.x__2 = QLabel( "x<sup>2</sup> +" )
        self.x__1 = QLabel( "x +" )
        
        
        self.displayMessage = QLabel( "ok" )

        self.function = function
        
        # to make sure that one can not scale out more than original scale
        self.scaleLevel = 0
        
        self.scaleInButton  = QPushButton( "scale in" )
        self.scaleOutButton = QPushButton( "scale out" )

        # two points on a function
        #~ self.point1 = self.ccs.addPointXFunction                          ( None,           0, self.function, 10, 0,0,200   )
        #~ self.point2 = self.ccs.addPointXFunction                          ( [self.point1],  1, self.function, 10            )
        #~ # third point, invisible, to form triangle
        #~ self.point3 = self.ccs.addPointWithXFromOnePointAndYFromAnother   ( self.point2, self.point1                        )

        #~ self.line1 = self.ccs.addLineDependent                            ( self.point1, self.point2 , True, True, 'red', 2 )
        #~ self.line2 = self.ccs.addLineDependent                            ( self.point2, self.point3                        )
        #~ self.line3 = self.ccs.addLineDependent                            ( self.point1, self.point3                        )

        self.functionPlot = self.ccs.addFunction                          ( self.function                                   )

        scene.addItem               ( self.ccs                                          )

        layout = QVBoxLayout        (                                                   )
        
        
        layoutOben = QHBoxLayout    ()
        layoutOben.addWidget        ( self.scaleInButton )
        layoutOben.addWidget        ( self.scaleOutButton )
        
        # Buttons are auto activated by default. That means, that when <Enter>
        # is pressed anywhere, they fire clicked(), which is not what we need here.
        # Otherwise upon changin the formula, the coordinate system is simultaneously
        # scaled in or out.
        self.scaleInButton.setAutoDefault(False)
        self.scaleOutButton.setAutoDefault(False)
        
        layout.addLayout            ( layoutOben )
        
        layout.addWidget            ( view )
        
        layoutUnten = QHBoxLayout   ()
        
        layout.addLayout            ( layoutUnten )
        

        layoutUnten.addWidget       ( self.a )
        layoutUnten.addWidget       ( self.x__3 )
        layoutUnten.addWidget       ( self.b )
        layoutUnten.addWidget       ( self.x__2 )
        layoutUnten.addWidget       ( self.c )
        layoutUnten.addWidget       ( self.x__1 )
        layoutUnten.addWidget       ( self.d )
        
        #~ layoutUnten.addWidget       ( self.spacer )
        layoutUnten.addStretch()
        
        layoutUnten.addWidget       ( self.displayMessage                               )
        
        self.setLayout              ( layout                                            )
        
        
        self.connect                ( self.scaleInButton, SIGNAL( "clicked()" ),
                                                                self.scaleIn            )
        self.connect                ( self.scaleOutButton, SIGNAL( "clicked()" ),
                                                                self.scaleOut           )
                                                                
        self.connect                (self.a, SIGNAL( "valueChanged(double)" ),
                                                                self.updateUi           )
                                                                
        self.connect                (self.b, SIGNAL( "valueChanged(double)" ),
                                                                self.updateUi           )
        self.connect                (self.c, SIGNAL( "valueChanged(double)" ),
                                                                self.updateUi           )
                                                                
        self.connect                (self.d, SIGNAL( "valueChanged(double)" ),
                                                                self.updateUi           )
        
        self.setWindowTitle         ( "Steigungen von Funktionen annaehernd bestimmen"  )
        
    def scaleIn( self ):
        # it can scale in indefinitely..
        self.ccs.scaleMe( 1.4 )
        self.scaleLevel += 1
        
    def scaleOut( self ):
        # .. whereas it can't scale out more than
        # original scale
        if self.scaleLevel > 0:
            self.ccs.scaleMe( 0.7 )
            self.scaleLevel -= 1

    def updateUi( self ):
        
        self.function = str( self.a.value())
        self.function += "*x**3 + "
        
        self.function += str( self.b.value())
        self.function += "*x**2 + "
        
        self.function += str( self.c.value())
        self.function += "*x + "
        
        self.function += str( self.d.value())
        
        print self.function
        self.functionPlot.redefine  ( self.function )
        
        self.ccs.update()




app = QApplication(sys.argv)


dialog = MainWindow(  )

dialog.show()

app.exec_()
