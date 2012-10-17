# PyParticles : Particles simulation in python
# Copyright (C) 2012  Simone Riva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np

import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    _____foo = None
    
    
class AxisOgl(object):
    def __init__(self):
        self.__arrow_len = 5.0
        
    def get_axis_len(self):
        return self.__arrow_len
    
    def set_axis_len( self , leng ):
        self.__arrow_len = leng
        
    axis_len = property( get_axis_len , set_axis_len )
    
    def draw_axis(self):
        
        self.draw_arrow( ( 1.0 , 0.0 , 0.0 ) , "x" )
        self.draw_arrow( ( 0.0 , 1.0 , 0.0 ) , "y" )
        self.draw_arrow( ( 0.0 , 0.0 , 1.0 ) , "z" )
    
        self.draw_arrow( ( 1.0 , 0.0 , 0.0 ) , "-x" )
        self.draw_arrow( ( 0.0 , 1.0 , 0.0 ) , "-y" )
        self.draw_arrow( ( 0.0 , 0.0 , 1.0 ) , "-z" )
            
        for pl in self.axis_planes_codes():
            self.draw_plane( pl )    
    
    def axis_planes_codes(self):
        return [ "xy" , "x-y" , "-xy" , "-x-y" , "xz" , "x-z" , "-xz" , "-x-z" , "yz" , "y-z" , "-yz" , "-y-z"  ]
    
    def draw_plane( self , plane="xy", color=( 0.7 , 0.7 , 0.7 , 0.3 ) , leng=None ):
        
        if leng == None :
            leng = self.axis_len
        
        glPushMatrix()
        
        if plane == "xy" :
            glRotatef( 0 , 1 , 0 , 0 )#
        elif plane == "yz" :
            glRotatef( 90 , 0 , 1 , 0 )#
        elif plane == "xz" :
            glRotatef( 90 , 1 , 0 , 0 )#
        elif plane == "-yz" :
            glRotatef( 180 , 1 , 0 , 0 )#
            glRotatef(  90 , 0 , 1 , 0 )
        elif plane == "-y-z" :
            glRotatef( 180 , 1 , 0 , 0 )#
            glRotatef( -90 , 0 , 1 , 0 )
        elif plane == "y-z" :
            glRotatef( -90 , 0 , 1 , 0 )#
        elif plane == "x-y" :
            glRotatef( 180 , 1 , 0 , 0 )#
        elif plane == "-x-y" :
            glRotatef( 180 , 1 , 0 , 0 )#
            glRotatef( 180 , 0 , 1 , 0 )
        elif plane == "x-z" :
            glRotatef( -90 , 1 , 0 , 0 )#
        elif plane == "-x-z" :
            glRotatef( -90 , 1 , 0 , 0 )#
            glRotatef( 180 , 0 , 0 , 1 )
        elif plane == "-xz" :
            glRotatef(  90 , 1 , 0 , 0 )#
            glRotatef( 180 , 0 , 0 , 1 )
        elif plane == "-x-z" :
            glRotatef( -90 , 1 , 0 , 0 )#
            glRotatef( 180 , 0 , 0 , 1 )
        elif plane == "-xy" :
            glRotatef( 180 , 0 , 1 , 0 )#
        
        glColor4f( color[0] , color[1] , color[2] , color[3] )
        
        glBegin(GL_LINES)
        for i in range( 1 , int(leng) ):
            glVertex3f( float(i) ,  0.0 , 0.0 )
            glVertex3f( float(i) , leng , 0.0 )
            
            glVertex3f( 0.0  , float(i) , 0.0 )
            glVertex3f( leng , float(i) , 0.0 )
            
        glEnd()
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor4f( color[0] , color[1] , color[2] , color[3]/2.0 )
        #glBegin( GL_TRIANGLES )
        #
        #glVertex3f( 0.0  , 0.0  , 0.0 )
        #glVertex3f( leng , 0.0  , 0.0 )
        #glVertex3f( leng , leng , 0.0 )
        #
        #glVertex3f( 0.0  , 0.0  , 0.0 )
        #glVertex3f( leng , leng , 0.0 )
        #glVertex3f( 0.0  , leng , 0.0 )
        #
        #glEnd()
        
        glPopMatrix()
        
    def draw_arrow( self , color , axis , leng=None ):
        
        if leng == None :
            leng = self.axis_len
            
        arrh = leng * 0.1
        arrp = leng - arrh
        
        dash = leng * 0.03
        
        glPushMatrix()
        
        if axis == "x" :
            glRotatef( 0 , 1 , 0 , 0 )
        elif axis == "y" :
            glRotatef( 90 , 0 , 0 , 1 )
        elif axis == "z" :
            glRotatef( -90 , 0 , 1 , 0 )
        if axis == "-x" :
            glRotatef( 180 , 0 , 0 , 1 )
        elif axis == "-y" :
            glRotatef( -90 , 0 , 0 , 1 )
        elif axis == "-z" :
            glRotatef( 90 , 0 , 1 , 0 )
        
        glBegin(GL_LINES)
        glColor3f( color[0] , color[1] , color[2] )
        
        glVertex3f( 0.0  , 0.0 , 0.0  )
        glVertex3f( leng , 0.0 , 0.0 )
    
        glVertex3f( leng , 0.0  ,  0.0 )
        glVertex3f( arrp ,-arrh , 0.0 )
        
        glVertex3f( leng , 0.0  , 0.0  )
        glVertex3f( arrp , arrh , 0.0 )
        
        for i in range( 1 , int(leng) ):
            glVertex3f( float(i) ,  dash , 0.0 )
            glVertex3f( float(i) , -dash , 0.0 )
            
        glEnd()
        glPopMatrix()
        
        
        