
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

import pyparticles.pset.particles_set as ps

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
        self.__trajectory_step = 1
        
        self.__color_fun = lambda pset , i : ( 1.0 , 1.0 , 1.0 , 1.0 )
    
    
    def get_pset(self):
        return self.__pset
    
    def set_pset(self , pset):
        self.__pset = pset
        
    pset = property( get_pset , set_pset )
    
    
    def set_color_fun( self , fun ):
        self.__color_fun = fun
    
    def get_color_fun( self , fun ):
        return self.__color_fun
    
    color_fun = property( get_color_fun , set_color_fun , doc="Set and get the function for calculating the particle color:\n"
                                                            " definition of the function color,"
                                                            " it take as args a particle_set obj. and the particle index "
                                                            " \n (R,G,B,A) = cfun( pset , index ) " )
    
    def get_trajectory( self ) :
        return self.__trajectory
    
    def set_trajectory( self , tr ):
        self.__trajectory = tr
        
    trajectory = property( get_trajectory , set_trajectory , doc="enable or disable the trajectory" )
    

    def get_trajectory_step( self ) :
        return self.__trajectory_step
    
    def set_trajectory_step( self , trs ):
        self.__trajectory_step = trs
        
    trajectory_step = property( get_trajectory_step , set_trajectory_step , doc="set or get the step for drawing the trajectory" )

    
    
    
    def draw_trajectory(self):
        
        if self.pset.log_size < self.trajectory_step + 1 :
            return 
        
        unit = self.pset.unit
        glLineWidth( 1.0 )
        
        if self.trajectory_step <= 1 :
            
            for i in range( self.pset.size ) :
                glBegin(GL_LINE_STRIP)
                for X in self.pset.logX :
                    glVertex3f( X[i,0] / unit ,
                                X[i,1] / unit ,
                                X[i,2] / unit )

                glEnd()        
        else:
            
            for i in range( self.pset.size ) :
                glBegin(GL_LINE_STRIP)
                j = 0
                for X in self.pset.logX :
                    j += 1
                    if ( j % self.trajectory_step ) == 0  :
                        glVertex3f( X[i,0] / unit ,
                                    X[i,1] / unit ,
                                    X[i,2] / unit )
    
                glEnd()

    
    def get_pcolor(self):
        return 
    
    
    def draw(self):
         
        glPointParameterf( GL_POINT_SIZE_MAX , 10.0 )
        glPointParameterf( GL_POINT_SIZE_MIN , 4.0 )    
    
        unit = self.pset.unit
        mass_unit = self.pset.mass_unit
    
        glEnable(GL_POINT_SMOOTH)
    
        for i in range( self.pset.size ):
            
            glPointSize( 0.01 + self.pset.M[i] / mass_unit )
            
            glBegin(GL_POINTS)
            
            glColor4f( *self.__color_fun( self.pset , i ) )    
                    
            glVertex3f( self.pset.X[i,0] / unit ,
                        self.pset.X[i,1] / unit ,
                        self.pset.X[i,2] / unit )
    
            glEnd()
        
        if self.pset.log_X_enabled and self.trajectory :
            self.draw_trajectory()

                









