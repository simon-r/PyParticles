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
    
    
class glAxis(object):
    def __init__(self):
        self.__arrow_len = 5.0
        
    def get_arrow_len(self):
        return self.__arrow_len
    
    def set_arrow_len( self , leng ):
        self.__arrow_len = leng
        
    arrow_len = property( get_arrow_len , set_arrow_len )
    
    def draw_axis(self):
        
        self.draw_arrow( ( 1.0 , 0.0 , 0.0 ) , "x" )
        self.draw_arrow( ( 0.0 , 1.0 , 0.0 ) , "y" )
        self.draw_arrow( ( 0.0 , 0.0 , 1.0 ) , "z" )
    
        
    def draw_arrow( self , color , axis , leng=None ):
        
        if leng == None :
            leng = self.arrow_len
            
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
        
        