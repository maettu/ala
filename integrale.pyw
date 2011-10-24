#!/usr/bin/python
# -*- coding: utf-8 -*-

# This app allows the user to visualize integrals.
# The user can see how areas are added to integrate a function.


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
                            QLineEdit,
                            QPen, 
                            QColor, 
                            QDialog, 
                            QVBoxLayout, 
                            QHBoxLayout, 
                            QPushButton, 
                            QLabel, 
                            QBrush, 
                            QPainter,
                            QSpinBox,
                            QMessageBox
                        )

import sys
import time

from ala.CartesianCoordinateSystem import CartesianCoordinateSystemWidget


class MainWindow( QDialog ):
    def __init__( self, parent=None ):
        super( MainWindow, self ).__init__(parent)
        
        
        # (object) variable definitions
        # -----------------------------
        
        width  = 500
        height = 1000
        
        
        # General setup
        # -------------
        
        self.sceneFunction = QGraphicsScene()
        self.sceneFunction.setSceneRect( 0, 0, width, height/3 )
        
        self.sceneIntegral = QGraphicsScene()
        self.sceneIntegral.setSceneRect( 0, 0, width, height/3 )

        viewFunction = QGraphicsView()
        viewFunction.setScene(self.sceneFunction)
        viewFunction.setRenderHint(QPainter.Antialiasing)
        
        self.ccsFunction = CartesianCoordinateSystemWidget( self.sceneFunction, width, height/3, 10, -5,5, -2,8 )
        
        self.ccsIntegral = CartesianCoordinateSystemWidget( self.sceneIntegral, width, height/3, 10, -5,5, -2,8 )
        
        viewIntegral = QGraphicsView()
        viewIntegral.setScene(self.sceneIntegral)
        viewIntegral.setRenderHint(QPainter.Antialiasing)
        
        
        # Layout & widgets
        # ----------------
        
        # set function
        #~ self.function = '2*x*math.exp(x**2) / 100'
        self.function = 'x**2'
        
        self.editFunction = QLineEdit( self.function )
        self.editFunction.selectAll()
        self.editFunctionMessage = QLabel( "ok" )
        
        # TODO: calculate (?)
        self.integral = 'x**3/3'
        
        self.editIntegral = QLineEdit( self.integral )
        self.editIntegralMessage = QLabel( "ok" )
        
        self.numberRectangles = 10
        self.start = 0
        self.end   = 2
        
        self.rectanglesFunction = []
        self.rectanglesIntegral = []
        
        self.numberRectanglesMax = 1000
        
        # I did not succeed in removing rectangles (segfaluts..)
        # So, there are numberRectanglesMax rectangles predefined
        # which are setPosition and setVisible on changeFunction.
        # This is not preemptive optimization, this is a workaround.
        for i in range ( self.numberRectanglesMax ):
            self.rectanglesFunction.append( self.ccsFunction.addRectangle( 
                    QPointF( 0, 0 ) , QPointF( 1, 0 ) ) 
            ) 
            self.rectanglesFunction[i].setVisible( False ) 
            
            self.rectanglesIntegral.append( 
                    self.ccsIntegral.addLine( QPointF(0,0), QPointF(1,0), False, False, 'blue' ) 
            )
            self.rectanglesIntegral[i].setVisible( False ) 
        
        self.numberRectanglesSpinBox = QSpinBox()
        self.numberRectanglesSpinBox.setMinimum ( 1 )
        self.numberRectanglesSpinBox.setMaximum ( self.numberRectanglesMax )
        self.numberRectanglesSpinBox.setValue( 10 )
        self.numberRectanglesSpinBox.setSingleStep( 1 )
       

        self.functionPlot = self.ccsFunction.addFunction( self.function )
        
        self.changeFunction()
        
        self.integralPlot = self.ccsIntegral.addFunction( self.integral )
        
        # TODO: check that on scale out ccs expand.
        
        
        self.scaleInButton  = QPushButton( "scale in" )
        self.scaleOutButton = QPushButton( "scale out" )

        self.sceneFunction.addItem                   ( self.ccsFunction )
        
        self.sceneIntegral.addItem                   ( self.ccsIntegral )

        layout = QVBoxLayout            ()
        
        
        layoutTop = QHBoxLayout        ()
        layoutTop.addWidget            ( self.scaleInButton )
        layoutTop.addWidget            ( self.scaleOutButton )
        
        # Buttons are auto activated by default. That means, that when <Enter>
        # is pressed anywhere, they fire clicked(), which is not what we need here.
        # Otherwise upon changin the formula, the coordinate system is simultaneously
        # scaled in or out.
        self.scaleInButton.setAutoDefault(False)
        self.scaleOutButton.setAutoDefault(False)
        
        layout.addLayout                ( layoutTop )
        
        layout.addWidget                ( viewFunction )
        
        layoutChangeFunction = QHBoxLayout   ()
        layout.addLayout                ( layoutChangeFunction )
        layoutChangeFunction.addWidget  ( self.editFunction                                  )
        layoutChangeFunction.addWidget  ( self.editFunctionMessage                           )
        
        layoutChangeFunction.addWidget  ( self.numberRectanglesSpinBox )
        
        layout.addWidget                ( viewIntegral )
        
        layout.addWidget                ( QLabel( "Funktion: " ) )
        layoutChangeIntegral = QHBoxLayout   ()
        layout.addLayout                ( layoutChangeIntegral )
        layoutChangeIntegral.addWidget  ( self.editIntegral                                  )
        
        layoutChangeIntegral.addWidget  ( self.editIntegralMessage                           )
        
        
        
        

        
        separator3 = QFrame()
        separator3.setFrameStyle (QFrame.HLine)
        layout.addWidget(separator3)
        
        self.setLayout              ( layout )

        # signal - method connections
        # ---------------------------
        
        self.connect                (self.editFunction, SIGNAL( "returnPressed()" ),
                                                                self.changeFunction     )
                                                                
        self.connect                (self.editIntegral, SIGNAL( "returnPressed()" ),
                                                                self.changeIntegral     )
        
        self.connect                ( self.scaleInButton, SIGNAL( "clicked()" ),
                                                                self.scaleIn            )
        self.connect                ( self.scaleOutButton, SIGNAL( "clicked()" ),
                                                                self.scaleOut           )
                                                                
        self.connect                (self.numberRectanglesSpinBox, SIGNAL( "valueChanged(int)" ),
                                                                self.changeFunction           )
                                                                
                                                                
        self.setWindowTitle         ( "Integrale anzeigen und raten"  )
        
    
    # methods for scaling the whole app in and out
    def scaleIn( self ):
        self.ccsFunction.scaleMe( 1.4 )
        self.ccsIntegral.scaleMe( 1.4 )
        
        
    def scaleOut( self ):
            self.ccsFunction.scaleMe( 0.7 )
            self.ccsIntegral.scaleMe( 0.7 )
            
            
        
    # reset the app.
    def reset( self ):
        self.ccsFunction.update()
        self.ccsIntegral.update()
    
    # When the function is changed it is redefined as well as the derivation,
    # then the app is reset.
    def changeFunction( self ):
        
        # All rectangles under the function and all lines on the
        # integral are set invisible. 
        for i in range ( self.numberRectanglesMax ):
            self.rectanglesFunction[i].setVisible( False ) 
            self.rectanglesIntegral[i].setVisible( False )
        
        # the function is redefined and painted.
        # TODO: this needs some input validation..
        self.function = str( self.editFunction.text() )
        self.functionPlot.redefine  ( self.function )
        
        # ySum is the sum of all rectangles below the function
        ySum = 0
        
        self.numberRectangles = self.numberRectanglesSpinBox.value()
        
        # iterate over the number of rectangles, set their position and
        # make them visible.
        for i in range( self.numberRectangles ):
            # x i "in the middle" of a rectangle.
            # x is the variable in the function string and gets eval'ed
            x = float( self.end - self.start ) / self.numberRectangles * (i + 0.5)
            
            # x1 is "on the left" of a rectangle, x2 is "on the right"
            x1 = float( self.end - self.start ) / self.numberRectangles * ( i )
            x2 = float( self.end - self.start ) / self.numberRectangles * (i+1)
            
            self.rectanglesFunction[i].setPosition( QPointF( x1, 0) , QPointF( x2, eval( self.function ) ) )
            self.rectanglesFunction[i].setVisible( True )
            
            # simply add sum up
            ySum = ySum + eval( self.function )
            
            # The value of the integral is dependent on the whole range and the number
            # of rectangles. 
            y = float( ySum ) * ( float (self.end - self.start) / self.numberRectangles )
            
            self.rectanglesIntegral[i].setPosition( QPointF(x1, y), QPointF(x2,y) ) 
            self.rectanglesIntegral[i].setVisible( True )
        
        self.reset()
        
        # TODO: put this in to check eval before applying ;-)
        
        #~ try:
            #~ # predefine x, because it is needed in eval
            #~ x = 1;
            
            #~ # test if string evaluates correctly. I.E. no other
            #~ # variables than x are allowed.
            
            #~ # TODO: eulers number: replace 'e' with 2.71.. 
            #~ testEval = eval( str( self.editFunction.text() ) )
            
            #~ self.function = str( self.editFunction.text() )
            
            #~ self.displayMessage.setText("ok")
            
            #~ self.functionPlot.redefine  ( self.function )
            #~ self.point1.redefine        ( self.function )
            #~ self.point2.redefine        ( self.function )
            
            #~ # just give it any yDelta..
            #~ self.point1.updateYourself  ( -self.point1.x ,1     )
            #~ self.point2.updateYourself  ( 1 - self.point2.x,1   )
            #~ self.point3.updateYourself  ( 1,1                   )
            
            

            #~ self.ccs.update()
            
        #~ except:
            #~ text = self.editFunction.text() 
            
            #~ self.editFunction.setText    ( text )
            #~ self.displayMessage.setText ("nicht evaluierbar")
            
    # TODO: This needs some input validation, too
    def changeIntegral( self ):
        self.integral = str( self.editIntegral.text() )
        self.integralPlot.redefine( self.integral )


# main program
# ------------

app = QApplication(sys.argv)

dialog = MainWindow(  )

dialog.show()

app.exec_()
