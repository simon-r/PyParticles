
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

import particles.particles_set as ps

import numpy as np
import sys


try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    _____foo = None


class DrawParticlesGL(object):
    
    def __init__( self , pset=None ):
        self.__pset = pset
        self.__trajectory = False
    
    def get_pset(self):
        return self.__pset
    
    def set_pset(self , pset):
        self.__pset = pset
        
    pset = property( get_pset , set_pset )
    
    
    def get_trajectory( self ) :
        return self.__trajectory
    
    def set_trajectory( self , tr ):
        self.__trajectory = tr
        
    trajectory = property( get_trajectory , set_trajectory , doc="enable or disable the trajectory" )
    
    
    def draw_trajectory(self):
        
        if self.pset.log_size < 3 :
            return 
        
        unit = self.pset.unit
        glLineWidth( 1.0 )
        
        for i in range( self.pset.size ) :
            
            glBegin(GL_LINE_STRIP)
            
            for X in self.pset.logX :
                
                glVertex3f( X[i,0] / unit ,
                            X[i,1] / unit ,
                            X[i,2] / unit )

            glEnd()

    
    
    def draw(self):
        
        glPointParameterf( GL_POINT_SIZE_MAX , 10.0 )
        glPointParameterf( GL_POINT_SIZE_MIN , 4.0 )    
    
        unit = self.pset.unit
        mass_unit = self.pset.mass_unit
    
        glEnable(GL_POINT_SMOOTH)
    
        for i in range( self.pset.size ):
            
            glPointSize( self.pset.M[i] / mass_unit )
            
            glBegin(GL_POINTS)
            glColor3f( 1.0 , 1.0 , 1.0 )    
                    
            glVertex3f( self.pset.X[i,0] / unit ,
                        self.pset.X[i,1] / unit ,
                        self.pset.X[i,2] / unit )
    
            glEnd()
        
        if self.pset.log_X_enabled and self.trajectory :
            self.draw_trajectory()

                









