#!/usr/bin/python
# -*- coding: utf-8 -*-

# This app allows the user to visualize the newton algorithm to
# approximate solutions to a cubic polynomial function equation 
# specified by the user.
# It draws the function onto a cartesian coordinate system.
# The coordinate system can be zoomed in and out; it can be dragged to show
# the region the user desires.
# The user can specify a desired staring point for iterations uf the algorithm.
# By repeadedly pressing a button the user will see how the algorithm proceeds.


# Yes, it is true: python insists on explicitly asking for unicode support
# when using unicode characters in comments.
from __future__ import unicode_literals

from PyQt4.QtCore import (  Qt, 
                            QRect,
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
        
        width  = 550
        height = 520
        
        # user presses "go!" button, then one step
        # of the algorithm is executed:
        # - draw point on function
        # - calculate next point on x-axis
        # - draw line
        # - clear old point & line
        # - start afresh
        self.nextStep = 0;
        
        # The starting point for the next iteration
        # is altered during the iteration process.
        # This fires the "startPoint changed" signal. 
        # When changing the starting point manually, we
        # want to reset the app and start a fresh iteration.
        # When the starting point is changed automatically,
        # the program can set resetApp False and no reset happens.
        self.resetApp = True
        
        
        # General setup
        # -------------
        
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, width, height)

        view = QGraphicsView()
        view.setScene(scene)
        view.setRenderHint(QPainter.Antialiasing)
        
        self.ccs = CartesianCoordinateSystemWidget(scene, width, height, 10, -5,5, -2,8)
        
        # Layout & widgets
        # ----------------
        
        # the parameters of the function ax³ + bx² + cx + d
        # The function can be ax³ + bx² + cx + d and nothing else for this app.
        # This is a somewhat narrow limitation but it is enough.
        self.a = QDoubleSpinBox()
        # set minimum to a (large) negative number. Default is 0..
        self.a.setMinimum   ( -1000 )
        self.a.setValue( 1 )
        self.a.setSingleStep( 0.1 )
        
        self.b = QDoubleSpinBox()
        self.b.setMinimum   ( -1000 )
        self.b.setValue( 1 )
        self.b.setSingleStep( 0.1 )
        
        self.c = QDoubleSpinBox()
        self.c.setMinimum   ( -1000 )
        self.c.setValue( -2 )
        self.c.setSingleStep( 0.1 )
        
        self.d = QDoubleSpinBox()
        self.d.setMinimum   ( -1000 )
        self.d.setValue     ( 0 )
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
        
        layoutFunction.addWidget        ( QLabel( "y = " ))
        
        # Spinboxes for the function
        layoutFunction.addWidget        ( self.a )
        layoutFunction.addWidget        ( self.x__3 )
        
        layoutFunction.addWidget        ( self.b )
        layoutFunction.addWidget        ( self.x__2 )
        
        layoutFunction.addWidget        ( self.c )
        layoutFunction.addWidget        ( self.x__1 )
        
        layoutFunction.addWidget        ( self.d )
        
        separator1 = QFrame()
        separator1.setFrameStyle (QFrame.HLine)
        layout.addWidget(separator1)
        
        # a stretch takes as much space as possible and
        # shrinks other widgets as much as possible.
        layoutFunction.addStretch()
        
        layoutStart = QHBoxLayout ()
        layout.addLayout          ( layoutStart )
        # force interpretation of html-characters with an <html> container
        layoutStart.addWidget     ( QLabel( "<html>Startpunkt f&uuml;r Ann&auml;herung: x = </html>" ) )
        
        # starting point for newton iteration
        self.startX = QDoubleSpinBox()
        self.startX.setMinimum   ( -1000 )
        self.startX.setValue( 0 )
        self.startX.setSingleStep( 0.1 )
        # make this spin box very precise!
        self.startX.setDecimals( 20 )
        
        separator2 = QFrame()
        separator2.setFrameStyle (QFrame.HLine)
        layout.addWidget(separator2)
        
        
        layoutStart.addWidget ( self.startX )
        layoutStart.addStretch()
        
        layoutNext = QHBoxLayout ()
        layoutNext.addWidget ( QLabel( "<html>N&auml;chster Schritt:</html>" ) )
        
        # This label changes its text accordung to next step.
        self.nextLabel = QLabel ( "Punkt auf Funktion bestimmen" )
        layoutNext.addWidget( self.nextLabel )
        layoutNext.addStretch()
        self.startButton  = QPushButton( "nächster Schritt" )
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
        self.otherPointOnTangent = self.ccs.addPoint( 1,0, 0, 200,0,0 )
        self.otherPointOnTangent.set_draggable( False )
        self.lineToNextXZero = self.ccs.addLineDependent ( self.otherPointOnTangent, self.pointOnFunction , True, False, 'red', 2 )
        self.lineToNextXZero.setVisible ( False )
        
        layoutNextZero = QHBoxLayout ()
        layout.addLayout          ( layoutNext )
        
        separator3 = QFrame()
        separator3.setFrameStyle (QFrame.HLine)
        layout.addWidget(separator3)
        
        layout.addLayout             ( layoutNextZero )
        
        layoutNextZero.addWidget     ( QLabel( "<html>N&auml;chste Ann&auml;herung f&uuml;r Nullstelle:</html>" ) )
        
        self.nextZeroLabel = QLabel ()
        layoutNextZero.addWidget( self.nextZeroLabel )
        
        self.setLayout              ( layout )

        # signal - method connections
        # ---------------------------
        
        self.connect                ( self.scaleInButton, SIGNAL( "clicked()" ),
                                                                self.scaleIn            )
        self.connect                ( self.scaleOutButton, SIGNAL( "clicked()" ),
                                                                self.scaleOut           )
                                                                
        self.connect                ( self.startButton, SIGNAL( "clicked()" ),
                                                                self.doNextStep     )
                                                                
        self.connect                (self.a, SIGNAL( "valueChanged(double)" ),
                                                                self.changeFunction           )
                                                                
        self.connect                (self.b, SIGNAL( "valueChanged(double)" ),
                                                                self.changeFunction           )
        self.connect                (self.c, SIGNAL( "valueChanged(double)" ),
                                                                self.changeFunction           )
                                                                
        self.connect                (self.d, SIGNAL( "valueChanged(double)" ),
                                                                self.changeFunction           )
                                                                
        self.connect                (self.startX, SIGNAL( "valueChanged(double)" ),
                                                                self.setStartPoint      )
                                                                
        self.setWindowTitle         ( "Nullstellen von Funktionen numerisch bestimmen"  )
        
    
    # methods for scaling the whole app in and out
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
            
    
    # This method is called when the user presses the "go!" button.
    # It determines which step is to be executed and does so.
    def doNextStep( self ):
        
        # to keep steps separated..
        # User hits button repeatedly to see next step 
        # of algorithm.
        
        # set point on function
        if self.nextStep == 0:
            self.nextLabel.setText ( "Tangente bestimmen" )

            self.pointOnFunction.setVisible( True )
            self.pointOnFunction.set_x( self.startX.value() )
            
            # update whole coordinate system object for the case that
            # pointOnFunction does not change coordinates when being set 
            # visible (might happen at start of program, e.g., because 
            # pointOnFunction already is correctly set).
            self.ccs.update()
            
            self.nextStep += 1
            
        # "elif", well.. c(++): else if
        # PHP: elseif, Perl: elsif, Python: elif.
        # This shows how languages have become more expressive.. :-)
        
        # show tangent
        elif self.nextStep == 1:
            self.nextLabel.setText ( "<html>Startpunkt f&uuml;r n&auml;chste Iteration setzen</html>" )
            
            # The second point on tangent is "simply" 1 bigger than point on function.
            # Its y-value is calculated with the derivation.
            x = self.startX.value()
            derivation = eval( self.derivation )
            self.otherPointOnTangent.set_x( self.pointOnFunction.x + 1 )
            self.otherPointOnTangent.set_y( self.pointOnFunction.y + derivation )
            
            self.lineToNextXZero.setVisible( True )
            
            # make sure everything displays correctly.
            # See comment above.
            self.ccs.update()
            
            self.nextStep += 1
            
        # show new approximation
        elif self.nextStep == 2:
            self.nextLabel.setText ( "<html>Punkt auf Funktion und Tangente l&ouml;schen</html>" )
            nextZero = self.calculateNextZero()
            self.nextZeroLabel.setText( str( nextZero ) )
            
            # just move old points to show only last iteration:
            self.startPoint.set_x( nextZero )
            
            # problem: this immediately triggers a "setStartPoint" which
            # in turn would trigger a reset(). Therefore resetApp is set to False
            # which prohibits from resetting whole app.
            self.resetApp = False
            self.startX.setValue ( nextZero )
            self.nextStep += 1
        
        # delete tangent and point on function
        else:
            self.nextLabel.setText ( "erneut Punkt auf Funktion bestimmen" )
            self.lineToNextXZero.setVisible( False )
            self.pointOnFunction.setVisible( False )
            self.ccs.update()
            self.nextStep = 0
        
    # Determine next zero. 
    def calculateNextZero( self ):
        # x must be set because this is the variable 
        # contained in the evaled string.
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
            
        # formula shown in explanatory script. :-)
        # It is a prretty one which can be deduced with 
        # affordable pain..
        return self.startX.value() - function / derivation
        
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
        self.ccs.update()
        
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
        
        self.ccs.update()
        
    # concatenate function.. I wonder if this could be done
    # more elegantly in python.
    def fn( self ):
        self.function = str( self.a.value())
        self.function += "*x**3 + "
        
        self.function += str( self.b.value())
        self.function += "*x**2 + "
        
        self.function += str( self.c.value())
        self.function += "*x + "
        
        self.function += str( self.d.value())

    # derivation concatenation
    def dn( self ):
        self.derivation = str (3*self.a.value())
        self.derivation += "*x**2 + " 
        self.derivation += str (2*self.b.value())
        self.derivation += "*x + "
        self.derivation += str (self.c.value())


# main program
# ------------

app = QApplication(sys.argv)

dialog = MainWindow(  )

dialog.show()

app.exec_()
