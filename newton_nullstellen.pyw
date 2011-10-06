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
        
        # The animation is quite slow (on purpose)
        # user has enough time to watch what is going on
        self.sleepTime = 2
        
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
        self.a.setSingleStep( 0.1 )
        
        self.b = QDoubleSpinBox()
        self.b.setMinimum   ( -1000 )
        self.b.setValue( 4 )
        self.b.setSingleStep( 0.1 )
        
        self.c = QDoubleSpinBox()
        self.c.setMinimum   ( -1000 )
        self.c.setValue( 2 )
        self.c.setSingleStep( 0.1 )
        
        self.d = QDoubleSpinBox()
        self.d.setMinimum   ( -1000 )
        self.d.setValue     ( -2 )
        self.d.setSingleStep( 0.1 )
        
        self.x__3 = QLabel( "x<sup>3</sup> +" )
        self.x__2 = QLabel( "x<sup>2</sup> +" )
        self.x__1 = QLabel( "x +" )
        
        # May be ax³ + bx² + cx + d and nothing else for this app.
        # This is a somewhat narrow limitation but it is enough
        # for educational purposes.
        self.function ="1.0*x**3 + 4.0*x**2 + 2.0*x - 2.0"
        
        self.dn()
        
        # to make sure that one can not scale out more than original scale
        self.scaleLevel = 0
        
        self.scaleInButton  = QPushButton( "scale in" )
        self.scaleOutButton = QPushButton( "scale out" )

        self.functionPlot = self.ccs.addFunction                          ( self.function                                   )

        scene.addItem                   ( self.ccs )

        layout = QVBoxLayout            ()
        
        
        layoutOben = QHBoxLayout        ()
        layoutOben.addWidget            ( self.scaleInButton )
        layoutOben.addWidget            ( self.scaleOutButton )
        
        # Buttons are auto activated by default. That means, that when <Enter>
        # is pressed anywhere, they fire clicked(), which is not what we need here.
        # Otherwise upon changin the formula, the coordinate system is simultaneously
        # scaled in or out.
        self.scaleInButton.setAutoDefault(False)
        self.scaleOutButton.setAutoDefault(False)
        
        layout.addLayout                ( layoutOben )
        
        layout.addWidget                ( view )
        
        layout.addWidget                ( QLabel( "Funktion: " ) )
        
        layoutFunction = QHBoxLayout    ()
        layout.addLayout                ( layoutFunction )
        

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
        # can be changed until "go!" is pressed
        self.startX = QDoubleSpinBox()
        self.startX.setMinimum   ( -1000 )
        self.startX.setValue( 0 )
        self.startX.setSingleStep( 0.1 )
        self.startX.setDecimals( 10 )
        
        layoutStart.addWidget ( self.startX )
        layoutStart.addStretch()
        
        layoutNext = QHBoxLayout ()
        layoutNext.addWidget ( QLabel( "<html>N&auml;chster Schritt:</html>" ) )
        self.nextLabel = QLabel ( "Punkt auf Funktion bestimmen" )
        layoutNext.addWidget( self.nextLabel )
        layoutNext.addStretch()
        self.startButton  = QPushButton( "go!" )
        layoutNext.addWidget( self.startButton )
        
        self.startPoint = self.ccs.addPoint(self.startX.value(),0, 10)
        self.startPoint.set_draggable( False )
        
        layoutNextZero = QHBoxLayout ()
        layout.addLayout          ( layoutNext )
        layout.addLayout             ( layoutNextZero )
        # force interpretation of html-characters with an <html> container
        layoutNextZero.addWidget     ( QLabel( "<html>N&auml;chste Nullstelle:</html>" ) )
        
        self.nextZeroLabel = QLabel ()
        layoutNextZero.addWidget( self.nextZeroLabel )
        
        # define point on function to be able and draw it only
        # after user presses "go!"
        self.pointOnFunction = False
        
        # same goes for "newPoint"
        self.pointNew = False
        

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
            if self.pointOnFunction:
                self.pointOnFunction.setVisible( True )
                self.pointOnFunction.set_x( self.startX.value() )
            else:
                # TODO make point non draggable!
                self.pointOnFunction = self.ccs.addPointXFunction ( [self.startPoint],  self.startX.value(), self.function, 10 )
            self.nextStep += 1
            
        elif self.nextStep == 1:
            nextZero = self.nZ()
            self.nextLabel.setText ( "<html>Startpunkt f&uuml;r n&auml;chste Iteration setzen</html>" )
            
            # new point on x-axis.
            if self.pointNew:
                self.pointNew.set_x( nextZero )
                
                self.lineToNextXZero.setVisible( True )
            
                self.ccs.update()
                
            else:
                # first pass
                nextZero = self.nZ()
                self.pointNew = self.ccs.addPoint(nextZero,0, 0, 200,0,0)
                self.pointNew.set_draggable( False )
                self.lineToNextXZero = self.ccs.addLineDependent  ( self.pointNew, self.pointOnFunction , True, False, 'red', 2 )
                self.ccs.update()
            
            self.nextStep += 1
            
        elif self.nextStep == 2:
            self.nextLabel.setText ( "<html>Punkt auf Funktion und Tangente l&ouml;schen</html>" )
            nextZero = self.nZ()
            self.nextZeroLabel.setText( str( nextZero ) )
            
            # just move old points to show only last iteration:
            self.startPoint.set_x( nextZero )
            self.startX.setValue ( nextZero )
            self.nextStep += 1
        
        else:
            self.nextLabel.setText ( "erneut Punkt auf Funktion bestimmen" )
            self.lineToNextXZero.setVisible( False )
            self.pointOnFunction.setVisible( False )
            self.ccs.update()
            self.nextStep = 0
            
            
        # TODO set "forward" button active
        # TODO set function and startpoint inactiv
        
    def nZ( self ):
        # x must be set because it is contained in the evaled string
        x = self.startX.value()
        function   = eval( self.function )
        derivation = eval( self.derivation )
            
        # formula shown in script. :-)
        # it is a prretty one which can be deduced with 
        # affordable pain..
        return self.startX.value() - function / derivation
        
    def wait( self ):
        time.sleep( self.sleepTime )
        
    def reset( self ):
        # reset "animation"
        self.nextLabel.setText ( "Punkt auf Funktion bestimmen" )
        self.nextStep = 0
        try:
            self.lineToNextXZero.setVisible( False )
        except:
            pass
        self.pointOnFunction.setVisible( False )
        self.ccs.update()

        #~ pass
        # TODO enable app to reset itself so that
        # function an startpoint can be changed
        
    def setStartPoint( self ):
        self.startPoint.set_x( self.startX.value() )
        self.reset()

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
        
        #~ self.startPoint.set_x( self.startX.value() )
        
        self.dn()
        #~ self.functionPlot.redefine  ( self.derivation )
        
        self.reset()
        
        self.ccs.update()

    def dn( self ):
        self.derivation = str (3*self.a.value())
        self.derivation += "*x**2 + " 
        self.derivation += str (2*self.b.value())
        self.derivation += "*x + "
        self.derivation += str (self.c.value())
        #~ print "Derivation"
        #~ print self.derivation


app = QApplication(sys.argv)


dialog = MainWindow(  )

dialog.show()

app.exec_()
