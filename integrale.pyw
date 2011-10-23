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


class MainWindow( QDialog ):
    def __init__( self, parent=None ):
        super( MainWindow, self ).__init__(parent)
        
        
        # (object) variable definitions
        # -----------------------------
        
        width  = 500
        height = 1000
        
        
        # General setup
        # -------------
        
        sceneFunction = QGraphicsScene()
        sceneFunction.setSceneRect( 0, 0, width, height/3 )
        
        sceneIntegral = QGraphicsScene()
        sceneIntegral.setSceneRect( 0, 0, width, height/3 )

        viewFunction = QGraphicsView()
        viewFunction.setScene(sceneFunction)
        viewFunction.setRenderHint(QPainter.Antialiasing)
        
        self.ccsFunction = CartesianCoordinateSystemWidget( sceneFunction, width, height/3, 10, -5,5, -2,8 )
        
        self.ccsIntegral = CartesianCoordinateSystemWidget( sceneIntegral, width, height/3, 10, -5,5, -2,8 )
        
        viewIntegral = QGraphicsView()
        viewIntegral.setScene(sceneIntegral)
        viewIntegral.setRenderHint(QPainter.Antialiasing)
        
        
        # Layout & widgets
        # ----------------
        
        # set function
        #~ self.function = '2*x*math.exp(x**2) / 100'
        self.function = 'x**2'
        
        # TODO: calculate (?)
        self.integral = 'x**3/3'
        
        self.numberRectangles = 50
        self.start = 0
        self.end   = 2
        self.rectanglesFunction = []
        self.rectanglesIntegral = []
        
        ySum = 0
        
        print "nöööö"
        print ( float (self.end - self.start) / self.numberRectangles )
        print "bööö"
        
        for i in range( self.numberRectangles ):
            x = float( self.end - self.start ) / self.numberRectangles * (i + 0.5)
            
            x1 = float( self.end - self.start ) / self.numberRectangles * ( i )
            x2 = float( self.end - self.start ) / self.numberRectangles * (i+1)
            
            self.rectanglesFunction.append( self.ccsFunction.addRectangle( 
                QPointF( x1, 0) , QPointF( x2, eval( self.function ) ) 
            ) )
            
            ySum = ySum + eval( self.function )
           
            y = float( ySum ) * ( float (self.end - self.start) / self.numberRectangles )
            print i, ySum, y
            #~ self.rectanglesIntegral.append( self.ccsIntegral.addRectangle(
                #~ QPointF( x1, 0), QPointF( x2, y )
            #~ ) )
            self.rectanglesIntegral.append( self.ccsIntegral.addPoint( x, y, 5, 0, 0, 200 ) )
       

        self.functionPlot = self.ccsFunction.addFunction( self.function )
        
        self.integralPlot = self.ccsIntegral.addFunction( self.integral )
        
        
        
        # TODO: change this for this app.
        # make sure that one can not scale out more than to original scale
        self.scaleLevel = 0
        
        self.scaleInButton  = QPushButton( "scale in" )
        self.scaleOutButton = QPushButton( "scale out" )

        sceneFunction.addItem                   ( self.ccsFunction )
        
        sceneIntegral.addItem                   ( self.ccsIntegral )

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
        layout.addWidget                ( viewIntegral )
        
        layout.addWidget                ( QLabel( "Funktion: " ) )

        
        separator3 = QFrame()
        separator3.setFrameStyle (QFrame.HLine)
        layout.addWidget(separator3)
        
        self.setLayout              ( layout )

        # signal - method connections
        # ---------------------------
        
        self.connect                ( self.scaleInButton, SIGNAL( "clicked()" ),
                                                                self.scaleIn            )
        self.connect                ( self.scaleOutButton, SIGNAL( "clicked()" ),
                                                                self.scaleOut           )
                                                                
                                                                
        self.setWindowTitle         ( "Integrale anzeigen und raten"  )
        
    
    # methods for scaling the whole app in and out
    def scaleIn( self ):
        # it can scale in indefinitely..
        self.ccsFunction.scaleMe( 1.4 )
        self.ccsIntegral.scaleMe( 1.4 )
        self.scaleLevel += 1
        
    def scaleOut( self ):
        # .. whereas it can't scale out more than
        # original scale
        #~ if self.scaleLevel > 0:
            self.ccsFunction.scaleMe( 0.7 )
            self.ccsIntegral.scaleMe( 0.7 )
            self.scaleLevel -= 1
            
        
    # reset the app.
    def reset( self ):
        # label..
        self.nextLabel.setText ( "Punkt auf Funktion bestimmen" )
        
        # ..first iteration step..
        self.nextStep = 0
        
        # ..point and tangent are invisible..
        self.lineToNextXZero.setVisible( False )
        self.pointOnFunction.setVisible( False )

        # ..clear Label..
        self.nextZeroLabel.setText( "" )
        
        # ..and redefine functionPlot, because
        # function might be changed. No preemptive
        # optimization. Not necessary.
        self.pointOnFunction.redefine ( self.function )
        
    # set start point and reset app if desired
    def setStartPoint( self ):
        self.startPoint.set_x( self.startX.value() )
        
        # This happens if startPoint is changed manually.
        # doNextStep sets resetApp False when it triggers
        # this method quite inadvertently.
        if self.resetApp:
            self.reset()
        self.ccsFunction.update()
        
        # we want to be sure that next time this method is called
        # the app is reset again. I wonder if this is slightly racy
        # but did not encounter any problems.
        self.resetApp = True
    
    # When the function is changed it is redefined as well as the derivation,
    # then the app is reset.
    def changeFunction( self ):
        self.fn()
        self.functionPlot.redefine  ( self.function )
        
        self.dn()
        
        self.reset()
        
        self.ccsFunction.update()


# main program
# ------------

app = QApplication(sys.argv)

dialog = MainWindow(  )

dialog.show()

app.exec_()
