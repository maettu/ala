#!/usr/bin/python
# -*- coding: utf-8 -*-

# Yes, it is true: python insists on explicitly asking for unicode support
# when using unicode characters in comments.

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
        
        width  = 520
        height = 520
        
        # user presses "go!" button, then ona step
        # after the other is executed:
        # - draw point on function
        # - calculate next point on x-axis
        # - draw line
        # - ...
        self.nextStep = 0;
        
        # The starting point for the next iteration
        # is altered during the iteration process.
        # This fires the "startPoint changed" signal. 
        # When changing the starting point manually, we
        # want to reset the app and start a fresh iteration.
        # When the starting point is changed automatically,
        # the program can set resetApp False and no reset happens.
        self.resetApp = True
        
        # Layout & widgets
        # ----------------
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, width, height)

        view = QGraphicsView()
        view.setScene(scene)
        view.setRenderHint(QPainter.Antialiasing)
        
        self.ccs = CartesianCoordinateSystemWidget(scene, width, height, 10, -5,5, -2,8)

        # the parameters of the function ax³ + bx² + cx + d
        # The function can be ax³ + bx² + cx + d and nothing else for this app.
        # This is a somewhat narrow limitation but it is enough.
        self.a = QDoubleSpinBox()
        # set minimum to a (large) negative number. Default is 0..
        self.a.setMinimum   ( -1000 )
        self.a.setValue( 0 )
        self.a.setSingleStep( 0.1 )
        
        self.b = QDoubleSpinBox()
        self.b.setMinimum   ( -1000 )
        self.b.setValue( 1 )
        self.b.setSingleStep( 0.1 )
        
        self.c = QDoubleSpinBox()
        self.c.setMinimum   ( -1000 )
        self.c.setValue( 0 )
        self.c.setSingleStep( 0.1 )
        
        self.d = QDoubleSpinBox()
        self.d.setMinimum   ( -1000 )
        self.d.setValue     ( -2 )
        self.d.setSingleStep( 0.1 )
        
        self.x__3 = QLabel( "x<sup>3</sup> +" )
        self.x__2 = QLabel( "x<sup>2</sup> +" )
        self.x__1 = QLabel( "x +" )
        
        # set function
        self.fn()
        
        self.functionPlot = self.ccs.addFunction ( self.function )
        
        # calculate derivation
        self.dn()
        
        # make sure that one can not scale out more than to original scale
        self.scaleLevel = 0
        
        self.scaleInButton  = QPushButton( "scale in" )
        self.scaleOutButton = QPushButton( "scale out" )

        scene.addItem                   ( self.ccs )

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
        
        layout.addWidget                ( view )
        
        layout.addWidget                ( QLabel( "Funktion: " ) )
        
        layoutFunction = QHBoxLayout    ()
        layout.addLayout                ( layoutFunction )
        
        # Spinboxes for the function
        layoutFunction.addWidget        ( self.a )
        layoutFunction.addWidget        ( self.x__3 )
        
        layoutFunction.addWidget        ( self.b )
        layoutFunction.addWidget        ( self.x__2 )
        
        layoutFunction.addWidget        ( self.c )
        layoutFunction.addWidget        ( self.x__1 )
        
        layoutFunction.addWidget        ( self.d )
        
        layoutFunction.addStretch()
        
        
        layoutStart = QHBoxLayout ()
        layout.addLayout          ( layoutStart )
        layoutStart.addWidget     ( QLabel( "<html>Startpunkt f&uuml;r Ann&auml;herung:</html>" ) )
        
        # starting point for newton iteration
        self.startX = QDoubleSpinBox()
        self.startX.setMinimum   ( -1000 )
        self.startX.setValue( 0 )
        self.startX.setSingleStep( 0.1 )
        # make this spin box very precise!
        self.startX.setDecimals( 20 )
        
        layoutStart.addWidget ( self.startX )
        layoutStart.addStretch()
        
        layoutNext = QHBoxLayout ()
        layoutNext.addWidget ( QLabel( "<html>N&auml;chster Schritt:</html>" ) )
        # This label changes its text accordung to next step.
        self.nextLabel = QLabel ( "Punkt auf Funktion bestimmen" )
        layoutNext.addWidget( self.nextLabel )
        layoutNext.addStretch()
        self.startButton  = QPushButton( "go!" )
        layoutNext.addWidget( self.startButton )
        self.startButton.setAutoDefault(False)
        
        self.startPoint = self.ccs.addPoint(self.startX.value(),0, 10)
        self.startPoint.set_draggable( False )
        
        # add the point on the function already to prevent from
        # "object not defined" eroors later on.
        # We can do so safely because it is set invisible.
        self.pointOnFunction = self.ccs.addPointXFunction ( [self.startPoint], 0, self.function, 10 )
        self.pointOnFunction.setVisible ( False )
        self.pointOnFunction.set_draggable ( False )
        
        # Add line and invisible point as well. Reason see above.
        self.pointNew = self.ccs.addPoint(1,0, 0, 200,0,0)
        self.pointNew.set_draggable( False )
        self.lineToNextXZero = self.ccs.addLineDependent ( self.pointNew, self.pointOnFunction , True, False, 'red', 2 )
        self.lineToNextXZero.setVisible ( False )
        
        layoutNextZero = QHBoxLayout ()
        layout.addLayout          ( layoutNext )
        layout.addLayout             ( layoutNextZero )
        # force interpretation of html-characters with an <html> container
        layoutNextZero.addWidget     ( QLabel( "<html>N&auml;chste Nullstelle:</html>" ) )
        
        self.nextZeroLabel = QLabel ()
        layoutNextZero.addWidget( self.nextZeroLabel )

        # signal - method connections
        
        self.setLayout              ( layout                                            )
        
        
        self.connect                ( self.scaleInButton, SIGNAL( "clicked()" ),
                                                                self.scaleIn            )
        self.connect                ( self.scaleOutButton, SIGNAL( "clicked()" ),
                                                                self.scaleOut           )
                                                                
        self.connect                ( self.startButton, SIGNAL( "clicked()" ),
                                                                self.startAnimation     )
                                                                
        self.connect                (self.a, SIGNAL( "valueChanged(double)" ),
                                                                self.updateUi           )
                                                                
        self.connect                (self.b, SIGNAL( "valueChanged(double)" ),
                                                                self.updateUi           )
        self.connect                (self.c, SIGNAL( "valueChanged(double)" ),
                                                                self.updateUi           )
                                                                
        self.connect                (self.d, SIGNAL( "valueChanged(double)" ),
                                                                self.updateUi           )
                                                                
        self.connect                (self.startX, SIGNAL( "valueChanged(double)" ),
                                                                self.setStartPoint      )
                                                                
        self.setWindowTitle         ( "Nullstellen von Funktionen numerisch bestimmen"  )
        
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
            

    def startAnimation( self ):
        
        # to keep steps separated..
        # user hits button repeatedly to see next step 
        # of algorithm.
        if self.nextStep == 0:
            self.nextLabel.setText ( "Tangente bestimmen" )

            self.pointOnFunction.setVisible( True )
            self.pointOnFunction.set_x( self.startX.value() )
            
            # update whole coordinate system object for the case that
            # pointOnFunction does not change coordinates when being set 
            # visible (my happen at start of program, e.g., because 
            # pointOnFunction already is correctly set).
            self.ccs.update()
            
            self.nextStep += 1
            
        elif self.nextStep == 1:
            nextZero = self.nZ()
            self.nextLabel.setText ( "<html>Startpunkt f&uuml;r n&auml;chste Iteration setzen</html>" )
            
            self.pointNew.set_x( nextZero )
            self.lineToNextXZero.setVisible( True )
            
            # make sure everything displays correctly.
            # See comment above.
            self.ccs.update()
            
            self.nextStep += 1
            
        elif self.nextStep == 2:
            self.nextLabel.setText ( "<html>Punkt auf Funktion und Tangente l&ouml;schen</html>" )
            nextZero = self.nZ()
            self.nextZeroLabel.setText( str( nextZero ) )
            
            # just move old points to show only last iteration:
            self.startPoint.set_x( nextZero )
            
            # problem: this immediately triggers a "setStartPoint" which
            # in turn would trigger a reset(). Therefore resetApp is set to False
            # which prohibits from resetting whole app.
            self.resetApp = False
            self.startX.setValue ( nextZero )
            self.nextStep += 1
        
        else:
            self.nextLabel.setText ( "erneut Punkt auf Funktion bestimmen" )
            self.lineToNextXZero.setVisible( False )
            self.pointOnFunction.setVisible( False )
            self.ccs.update()
            self.nextStep = 0
        
    def nZ( self ):
        # x must be set because it is contained in the evaled string
        x = self.startX.value()
        function   = eval( self.function )
        derivation = eval( self.derivation )
        
        # Newton can not determine next zero if
        # tangent never crosses x-axis.
        # Therefore annoy user and reset app.
        if derivation == 0:
            warning = "Am gewählten Startpunkt ist die Steigung der Funktion Null."
            warning +="\nDie Tangente hat somit keine Steigung."
            warning +="\nSie ist parallel zur x-Achse und schneidet diese nicht."
            warning +="\nBitte einen anderen Startpunkt wählen!"
            QMessageBox.warning( 
                self, 
                unicode( "Steigung ist Null" ), 
                unicode( warning )
            )
            
            self.reset()
            return 0
            
        # formula shown in script. :-)
        # it is a prretty one which can be deduced with 
        # affordable pain..
        return self.startX.value() - function / derivation
        
    def reset( self ):
        # reset "animation"
        self.nextLabel.setText ( "Punkt auf Funktion bestimmen" )
        self.nextStep = 0

        self.lineToNextXZero.setVisible( False )
        
        self.nextZeroLabel.setText( "" )
        
        self.pointOnFunction.setVisible( False )
        self.pointOnFunction.redefine ( self.function )
        
    def setStartPoint( self ):
        self.startPoint.set_x( self.startX.value() )
        if self.resetApp:
            self.reset()
        self.ccs.update()
        
        self.resetApp = True

    def updateUi( self ):
        self.fn()
        self.functionPlot.redefine  ( self.function )
        
        self.dn()
        
        self.reset()
        
        self.ccs.update()
        
    def fn( self ):
        self.function = str( self.a.value())
        self.function += "*x**3 + "
        
        self.function += str( self.b.value())
        self.function += "*x**2 + "
        
        self.function += str( self.c.value())
        self.function += "*x + "
        
        self.function += str( self.d.value())

    def dn( self ):
        self.derivation = str (3*self.a.value())
        self.derivation += "*x**2 + " 
        self.derivation += str (2*self.b.value())
        self.derivation += "*x + "
        self.derivation += str (self.c.value())


app = QApplication(sys.argv)


dialog = MainWindow(  )

dialog.show()

app.exec_()
