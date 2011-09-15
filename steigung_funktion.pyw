#!/usr/bin/python

from PyQt4.QtCore import (Qt, QRectF, QPointF, QLineF, QTimer, QObject, SIGNAL, QString)
from PyQt4.QtGui import (QApplication, QGraphicsScene, QGraphicsView, 
    QGraphicsItem, QPen, QColor, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QBrush, QPainter,
    QLineEdit )

import sys

from ala.CartesianCoordinateSystem import CartesianCoordinateSystemWidget


class MainWindow( QDialog ):
    def __init__( self, function = 'x**2', parent=None ):
        super( MainWindow, self ).__init__(parent)
        
        width  = 520
        height = 520

        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, width, height)

        view = QGraphicsView()
        view.setScene(scene)
        view.setRenderHint(QPainter.Antialiasing)
        
        self.ccs = CartesianCoordinateSystemWidget(scene, width, height, 10, -5,5,-1,10)

        self.editFormula = QLineEdit( function )
        self.editFormula.selectAll()
        self.displayMessage = QLabel( "ok" )

        self.function = function
        
        # to make sure that one can not scale out more than original scale
        self.scaleLevel = 0
        
        self.scaleInButton  = QPushButton( "scale in" )
        self.scaleOutButton = QPushButton( "scale out" )

        # two points on a function
        self.point1 = self.ccs.addPointXFunction                          ( None,           0, self.function, 10, 0,0,200   )
        self.point2 = self.ccs.addPointXFunction                          ( [self.point1],  1, self.function, 10            )
        # third point, invisible, to form triangle
        self.point3 = self.ccs.addPointWithXFromOnePointAndYFromAnother   ( self.point2, self.point1                        )

        self.line1 = self.ccs.addLineDependent                            ( self.point1, self.point2 , True, True, 'red', 2 )
        self.line2 = self.ccs.addLineDependent                            ( self.point2, self.point3                        )
        self.line3 = self.ccs.addLineDependent                            ( self.point1, self.point3                        )

        self.functionPlot = self.ccs.addFunction                          ( self.function                                   )

        scene.addItem               ( self.ccs                                          )

        layout = QVBoxLayout        (                                                   )
        
        
        layoutOben = QHBoxLayout    ()
        layoutOben.addWidget        ( self.scaleInButton )
        layoutOben.addWidget        ( self.scaleOutButton )
        
        layout.addLayout            ( layoutOben )
        
        layout.addWidget            ( view )
        
        layoutUnten = QHBoxLayout   ()
        
        layout.addLayout            ( layoutUnten )
        
        layoutUnten.addWidget       ( self.editFormula                                  )
        layoutUnten.addWidget       ( self.displayMessage                               )
        
        self.setLayout              ( layout                                            )
        self.editFormula.setFocus   (                                                   )
        
        self.connect                (self.editFormula, SIGNAL( "returnPressed()" ),
                                                                self.updateUi           )
        self.connect                (self.scaleInButton, SIGNAL( "clicked()" ),
                                                                self.scaleIn            )
        self.connect                (self.scaleOutButton, SIGNAL( "clicked()" ),
                                                                self.scaleOut            )

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
        try:
            # predefine x, because it is needed in eval
            x = 0;
            
            # test if string evaluates correctly. I.E. no other
            # variables than x are allowed.
            
            # TODO: eulers number: replace 'e' with 2.71.. 
            testEval = eval( str( self.editFormula.text() ) )
            
            self.function = str( self.editFormula.text() )
            
            self.displayMessage.setText("ok")
            
            self.functionPlot.redefine  ( self.function )
            self.point1.redefine        ( self.function )
            self.point2.redefine        ( self.function )
            
            # just give it any yDelta..
            self.point1.updateYourself  ( -self.point1.x ,1     )
            self.point2.updateYourself  ( 1 - self.point2.x,1   )
            self.point3.updateYourself  ( 1,1                   )
            
            #~ self.editFormula.selectAll  ()

            self.ccs.update()
            
        except:
            text = self.editFormula.text() 
            
            self.editFormula.setText    ( text )
            self.displayMessage.setText ("nicht evaluierbar")





app = QApplication(sys.argv)


dialog = MainWindow( '2.718281828459045235**x' )

dialog.show()

app.exec_()

