
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
        self.pset = pset
        self.__trajectory = False
        self.__trajectory_step = 1
        
        self.__color_fun = lambda pset , i : ( 1.0 , 1.0 , 1.0 , 1.0 )
    
        self.__draw_particle = self.draw_particle
        
        self.__sph_dl = None
        self.__tea_dl = None
        self.__pt_dl = None
    
    def ogl_init(self):
        """
        Initialize opengl display lists (must be called after glutInit!)
        """
        self.init_sphere_dl()
        self.init_teapot_dl()
    
    
    #######################
    def get_pset(self):
        return self.__pset
    
    def set_pset(self , pset):
        self.__pset = pset
        
    pset = property( get_pset , set_pset )
    
    ########################
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

    
    def init_sphere_dl(self):
        self.__sph_dl = glGenLists(1)
        glNewList( self.__sph_dl , GL_COMPILE );
        glutSolidSphere( 1.0 , 10 , 10 )
        glEndList()
        
        
    def init_teapot_dl(self):
        self.__tea_dl = glGenLists(1)
        glNewList( self.__tea_dl , GL_COMPILE );
        glutSolidTeapot( 1.0 )
        glEndList()
        
    
    
    def set_particle_model( self , model="" , user_fun=None ):
        
        if model == "point" :
            self.__draw_particle = self.draw_particle
        elif model == "sphere" :
            self.__draw_particle = self.draw_particle_sphere
        if model == "teapot" :
            self.__draw_particle = self.draw_particle_teapot            
    
    
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
    
    
    def draw_particle( self ,  pset , i ):
            glPointSize( 0.01 + self.pset.M[i] / self.pset.mass_unit )
            glColor4f( *self.__color_fun( pset , i ) )
            
            glBegin(GL_POINTS)
            
            glVertex3f( self.pset.X[i,0] / self.pset.unit ,
                        self.pset.X[i,1] / self.pset.unit ,
                        self.pset.X[i,2] / self.pset.unit )
            
            glEnd()
 
    
    def draw_particle_sphere( self , pset , i ):
        
        radius = 0.5 * ( 0.05 + 0.1 / ( 1.0 + np.exp( -self.pset.M[i] / self.pset.mass_unit ) ) )
        
        glColor4f( *self.__color_fun( pset , i ) )
        glPushMatrix()
        glTranslatef( self.pset.X[i,0] / self.pset.unit ,
                      self.pset.X[i,1] / self.pset.unit ,
                      self.pset.X[i,2] / self.pset.unit )
            
        glScalef( radius , radius , radius )
        glCallList( self.__sph_dl )
        
        glPopMatrix()
    
    
    def draw_particle_teapot( self , pset , i ):
        
        radius = 0.5 * ( 0.05 + 0.1 / ( 1.0 + np.exp( -self.pset.M[i] / self.pset.mass_unit ) ) )
        
        glColor4f( *self.__color_fun( pset , i ) )
        glPushMatrix()
        glTranslatef( self.pset.X[i,0] / self.pset.unit ,
                      self.pset.X[i,1] / self.pset.unit ,
                      self.pset.X[i,2] / self.pset.unit )
            
        glScalef( radius , radius , radius )
        glCallList( self.__tea_dl )
        
        glPopMatrix()
    
    
    def draw(self):
         
        glPointParameterf( GL_POINT_SIZE_MAX , 10.0 )
        glPointParameterf( GL_POINT_SIZE_MIN , 4.0 )    
    
        unit = self.pset.unit
        mass_unit = self.pset.mass_unit
    
        glEnable(GL_POINT_SMOOTH)
    
        for i in range( self.pset.size ):
            self.__draw_particle( self.pset , i )
            
        
            
        if self.pset.log_X_enabled and self.trajectory :
            self.draw_trajectory()

                









