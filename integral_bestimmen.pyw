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
                            QCheckBox,
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
                            QDoubleSpinBox,
                            QMessageBox
                        )

import sys
import time
import math

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
        
        self.scaleLevel = 0
        
        self.sceneFunction = QGraphicsScene()
        self.sceneFunction.setSceneRect( 0, 0, width, height/3 )
        
        self.sceneIntegral = QGraphicsScene()
        self.sceneIntegral.setSceneRect( 0, 0, width, height/3 )

        viewFunction = QGraphicsView                ()
        viewFunction.setScene                       ( self.sceneFunction    )
        viewFunction.setRenderHint                  ( QPainter.Antialiasing )
        viewFunction.setHorizontalScrollBarPolicy   ( Qt.ScrollBarAlwaysOff )
        viewFunction.setVerticalScrollBarPolicy     ( Qt.ScrollBarAlwaysOff )
        
        self.ccsFunction = CartesianCoordinateSystemWidget( self.sceneFunction, width, height/3, 10, -5,5, -2,8 )
        
        self.ccsIntegral = CartesianCoordinateSystemWidget( self.sceneIntegral, width, height/3, 10, -5,5, -2,8 )
        
        viewIntegral = QGraphicsView                ()
        viewIntegral.setScene                       ( self.sceneIntegral    )
        viewIntegral.setRenderHint                  ( QPainter.Antialiasing )
        viewIntegral.setHorizontalScrollBarPolicy   ( Qt.ScrollBarAlwaysOff )
        viewIntegral.setVerticalScrollBarPolicy     ( Qt.ScrollBarAlwaysOff )
        
        
        # Layout & widgets
        # ----------------
        
        # set function
        #~ self.function = '2*x*math.exp(x**2) / 100'
        self.function = 'x**2'
        
        self.editFunction = QLineEdit( self.function )
        #~ self.editFunction.selectAll( )
        self.editFunctionMessage = QLabel( "ok" )
        
        self.integral = 'x**3/3'
        
        self.editIntegral = QLineEdit( self.integral )
        self.editIntegralMessage = QLabel( "ok" )
        
        self.numberRectangles = 10
        self.start = 0
        self.end   = 2
        
        self.rectanglesUndersum = []
        self.rectanglesOversum  = []
        self.pointsIntegralUnder = []
        self.pointsIntegralOver  = []
        
        self.numberRectanglesMax = 1000
        
        # I did not succeed in removing rectangles (segfaults..)
        # So, there are numberRectanglesMax rectangles predefined
        # which are setPosition and setVisible on changeFunction.
        # This is not preemptive optimization, this is a workaround.
        for i in range ( self.numberRectanglesMax ):
            self.rectanglesUndersum.append( self.ccsFunction.addRectangle( 
                    QPointF( 0, 0 ) , QPointF( 1, 0 ), 'blue', 'darkViolet' ) 
            ) 
            self.rectanglesOversum.append( self.ccsFunction.addRectangle(
                    QPointF( 0, 0 ) , QPointF( 1, 0 ), 'red', 'orangeRed' )
            )
            self.rectanglesUndersum[i].setVisible( False ) 
            self.rectanglesOversum[i].setVisible( False )
            # sets rectangle behind functionPlot
            self.rectanglesUndersum[i].setZValue( 2 )
            self.rectanglesOversum[i].setZValue( 1 )
            
            #~ self.rectanglesIntegral.append( 
                    #~ self.ccsIntegral.addLine( QPointF(0,0), QPointF(1,0), False, False, 'blue' ) 
            #~ )
            #~ self.rectanglesIntegral[i].setVisible( False ) 
            self.pointsIntegralUnder.append(
                self.ccsIntegral.addPoint( 0, 0, 10, 0, 0, 200 )
            )
            self.pointsIntegralOver.append(
                self.ccsIntegral.addPoint( 0, 0, 10, 200, 0, 0 )
            )
        
            self.pointsIntegralUnder[i].setVisible( False )
            self.pointsIntegralUnder[i].setZValue( 2 )
            self.pointsIntegralOver[i].setVisible( False )
            self.pointsIntegralOver[i].setZValue( 2 )
            
        self.showUndersum = QCheckBox( 'Untersumme' )
        self.showOversum  = QCheckBox( 'Obersumme'  )
        self.showUndersum.setChecked( True )
        self.showOversum. setChecked( True )
        
        self.numberRectanglesSpinBox = QSpinBox()
        self.numberRectanglesSpinBox.setMinimum ( 1 )
        self.numberRectanglesSpinBox.setMaximum ( self.numberRectanglesMax )
        self.numberRectanglesSpinBox.setValue( self.numberRectangles )
        self.numberRectanglesSpinBox.setSingleStep( 1 )
        
        self.lowerIntegrationBorderSpinBox = QDoubleSpinBox()
        self.lowerIntegrationBorderSpinBox.setMinimum( -1000 )
        self.lowerIntegrationBorderSpinBox.setMaximum( 1000 )
        self.lowerIntegrationBorderSpinBox.setValue( self.start )
        self.lowerIntegrationBorderSpinBox.setSingleStep( 0.1 )
        
        self.upperIntegrationBorderSpinBox = QDoubleSpinBox()
        self.upperIntegrationBorderSpinBox.setMinimum( -1000 )
        self.upperIntegrationBorderSpinBox.setMaximum( 1000 )
        self.upperIntegrationBorderSpinBox.setValue( self.end )
        self.upperIntegrationBorderSpinBox.setSingleStep( 0.1 )
       

        self.functionPlot = self.ccsFunction.addFunction( self.function )
        self.functionPlot.setZValue( 1 )
        
        self.changeFunction()
        
        self.integralPlot = self.ccsIntegral.addFunction( self.integral )
        self.integralPlot.setZValue( 1 )
        
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
        
        layout.addWidget( QLabel( "Funktion, Ober- und Untersumme" ) )
        
        layout.addWidget                ( viewFunction )
        
        layout.addWidget                ( QLabel( "Funktion: " ) )
        
        layoutChangeFunction = QHBoxLayout ()
        layout.addLayout                ( layoutChangeFunction )
        layoutChangeFunction.addWidget  ( self.editFunction                                  )
        layoutChangeFunction.addWidget  ( self.editFunctionMessage                           )
        
        layoutChangeNumberRectangles = QHBoxLayout()
        layout.addLayout                ( layoutChangeNumberRectangles )
        
        layoutChangeNumberRectangles.addWidget ( QLabel( "Anzahl Rechtecke (Feinheit der Summe)" ) )
        layoutChangeNumberRectangles.addWidget ( self.numberRectanglesSpinBox )
        layoutChangeNumberRectangles.addStretch ()
        
        layoutIntegrationBorders = QHBoxLayout ()
        layout.addLayout                ( layoutIntegrationBorders )
        layoutIntegrationBorders.addWidget ( QLabel( "Untere Integrationsgrenze" ) )
        layoutIntegrationBorders.addWidget ( self.lowerIntegrationBorderSpinBox )
        
        layoutIntegrationBorders.addWidget ( QLabel( "Obere Integrationsgrenze" ) )
        layoutIntegrationBorders.addWidget ( self.upperIntegrationBorderSpinBox )
        
        layoutShowSums = QHBoxLayout ()
        layoutShowSums.addWidget( self.showUndersum )
        layoutShowSums.addWidget( self.showOversum  )
        layout.addLayout( layoutShowSums )
        
        separator = QFrame()
        separator.setFrameStyle( QFrame.HLine )
        layout.addWidget( separator )
        
        layout.addWidget                ( viewIntegral )
        
        layout.addWidget                ( QLabel( "Funktion: " ) )
        layoutChangeIntegral = QHBoxLayout   ()
        layout.addLayout                ( layoutChangeIntegral )
        layoutChangeIntegral.addWidget  ( self.editIntegral                                  )
        
        layoutChangeIntegral.addWidget  ( self.editIntegralMessage                           )
        


        
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
                                                                
        self.connect                ( self.showUndersum, SIGNAL( "stateChanged(int)" ),
                                                                self.changeFunction     )
        self.connect                ( self.showOversum, SIGNAL( "stateChanged(int)" ),
                                                                self.changeFunction     )
                                                                
        self.connect                (self.numberRectanglesSpinBox, SIGNAL( "valueChanged(int)" ),
                                                                self.changeFunction           )
                                                                
        self.connect                (self.lowerIntegrationBorderSpinBox, SIGNAL( "valueChanged(double)" ),
                                                                self.changeFunction           )
                                                                
        self.connect                (self.upperIntegrationBorderSpinBox, SIGNAL( "valueChanged(double)" ),
                                                                self.changeFunction           )
                                                                
                                                                
        self.setWindowTitle         ( "Integrale anzeigen und raten"  )
        
        self.editFunction.setFocus()
        
    
    # methods for scaling the whole app in and out
    def scaleIn( self ):
        self.ccsFunction.scaleMe( 1.4 )
        self.ccsIntegral.scaleMe( 1.4 )
        self.scaleLevel += 1
        
        
    def scaleOut( self ):
        if self.scaleLevel > 0:
            self.ccsFunction.scaleMe( 0.7 )
            self.ccsIntegral.scaleMe( 0.7 )
            self.scaleLevel -= 1
            
        
    # reset the app.
    def reset( self ):
        self.ccsFunction.update()
        self.ccsIntegral.update()
    
    # When the function is changed it is redefined as well as the derivation,
    # then the app is reset.
    def changeFunction( self ):
        # somewhat lazy input validation: set x=1000 and testEval function
        try:
            # predefine x, because it is needed in eval
            x = 1000;
            testEval = eval( str( self.editFunction.text() ) )
            ok = True
            # if eval is o.k., then print "ok"
            self.editFunctionMessage.setText("ok")
        except:
            self.editFunctionMessage.setText("Fehler in der Funktion.")
            ok = False
        
        if ok:
            # All rectangles under the function and all lines on the
            # integral are set invisible. 
            for i in range ( self.numberRectanglesMax ):
                self.rectanglesUndersum[i].setVisible( False ) 
                self.rectanglesOversum[i].setVisible( False )
                #~ self.rectanglesIntegral[i].setVisible( False )
                self.pointsIntegralUnder[i].setVisible( False )
                self.pointsIntegralOver[i].setVisible( False )
            
            # the function is redefined and painted.
            # TODO: this needs some input validation..
            self.function = str( self.editFunction.text() )
            self.functionPlot.redefine  ( self.function )
            
            # ySum is the sum of all rectangles below the function
            #~ ySum = 0
            yUndersumTotal = 0
            yOversumTotal  = 0
            
            # set all values (lazyness)
            self.numberRectangles = self.numberRectanglesSpinBox.value()
            self.start = self.lowerIntegrationBorderSpinBox.value()
            self.end = self.upperIntegrationBorderSpinBox.value()
            
            # iterate over the number of rectangles, set their position and
            # make them visible.
            for i in range( self.numberRectangles ):
                # x i "in the middle" of a rectangle.
                # x is the variable in the function string and gets eval'ed
                x = self.start + float( self.end - self.start ) / self.numberRectangles * (i + 0.5)
                
                # x1 is "on the left" of a rectangle, x2 is "on the right"
                x1 = self.start + float( self.end - self.start ) / self.numberRectangles * ( i )
                x2 = self.start + float( self.end - self.start ) / self.numberRectangles * (i+1)
                
                xStep = (x2-x1) / 100
                
                # this happens when x1 and x2 are *really* close together.
                # It then does not happen a lot how large yUndersum and yOversum
                # are exactly. There is virtually nothing painted at all, only a 
                # slim line. Doing this prevents from getting exceptions thrown by 
                # getYMin and getYMax respectively
                if xStep == 0:
                    yUndersum = eval( self.function )
                    yOversum = yUndersum
                else:
                    yUndersum = self.functionPlot.getYMin( x1, x2, (x2-x1) / 10 )
                    yOversum  = self.functionPlot.getYMax( x1, x2, (x2-x1) / 10 )
                
                # simply add sum up
                # improve accuracy (and cheat: change determination of x: must be where arithmetic middle
                # of y1 and y2 is, not middle between x1 and x2, so to speak)
                #~ ySum = ySum + eval( self.function )
                x = x1
                y1 = eval( self.function )
                x = x2
                y2 = eval( self.function )
                y = ( y1 + y2 ) / 2

                yUndersumTotal = yUndersumTotal + yUndersum
                yOversumTotal  = yOversumTotal  + yOversum
                
                if self.showUndersum.isChecked() and self.showOversum.isChecked():
                    self.rectanglesUndersum[i].setPosition( QPointF( x1, 0)         , QPointF( x2, yUndersum ) )
                    self.rectanglesUndersum[i].setFillColor( 'blueViolet' )
                    self.rectanglesUndersum[i].setVisible( True )
                    self.rectanglesUndersum[i].updateYourself( )

                    self.rectanglesOversum[i].setPosition(  QPointF( x1, yUndersum) , QPointF( x2, yOversum  ) )
                    self.rectanglesOversum[i].setVisible( True )
                    self.rectanglesOversum[i].updateYourself()
                
                elif self.showUndersum.isChecked():
                    self.rectanglesUndersum[i].setPosition( QPointF( x1, 0)         , QPointF( x2, yUndersum ) )
                    self.rectanglesUndersum[i].setFillColor( 'lightBlue' )
                    self.rectanglesUndersum[i].setVisible( True )
                    self.rectanglesUndersum[i].updateYourself( )

                    
                elif self.showOversum.isChecked():
                    self.rectanglesOversum[i].setPosition(  QPointF( x1, 0) , QPointF( x2, yOversum  ) )
                    self.rectanglesOversum[i].setVisible( True )
                    self.rectanglesOversum[i].updateYourself()
                
                # The value of the integral is dependent on the whole range and the number
                # of rectangles. 

                yIntegralUnder = float( yUndersumTotal ) * ( float( self.end - self.start ) / self.numberRectangles )
                yIntegralOver  = float( yOversumTotal  ) * ( float( self.end - self.start ) / self.numberRectangles )
            
                # only draw last point
                if i == self.numberRectangles-1:
                    self.pointsIntegralOver[i].setPosition( x, yIntegralOver )
                    self.pointsIntegralOver[i].setVisible( True )
                    self.pointsIntegralUnder[i].setPosition( x, yIntegralUnder )
                    self.pointsIntegralUnder[i].setVisible( True ) 
                
            self.reset()
        
    def changeIntegral( self ):
        try:
            # predefine x, because it is needed in eval
            x = 1;
            testEval = eval( str( self.editIntegral.text() ) )
            ok = True
            # if eval is o.k., then print "ok"
            self.editIntegralMessage.setText("ok")
        except:
            self.editIntegralMessage.setText("Fehler in der Funktion.")
            ok = False
            
        if ok:
            self.integral = str( self.editIntegral.text() )
            self.integralPlot.redefine( self.integral )
            self.reset()
            
            
# main program
# ------------

app = QApplication(sys.argv)

dialog = MainWindow(  )

dialog.show()

app.exec_()
