
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

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def charged_particles_color( pset , i ):
    a = 0.4 
    
    if pset.Q[i] > 0.0 :
        return ( 1.0 , a , a , 1.0 )
    elif pset.Q[i] < 0.0 :
        return ( a , a , 1.0 , 1.0 )
    else :
        return ( a , a , a , 1.0 )


def rand_vect_colors( RGBA , pset ):
    RGBA[:] = np.random.rand( pset.size , 4 )


def charged_particles_vect_color( RGBA , pset ):
    a = 0.4
    
    i, foo = np.where( pset.Q > 0.0 )
    RGBA[ i , : ] = np.array( [ 1.0 , a , a , 1.0 ] )
    
    i, foo = np.where( pset.Q < 0.0 )
    RGBA[ i , : ] = np.array( [ a , a , 1.0 , 1.0 ] )
    
    i, foo = np.where( pset.Q == 0.0 )
    RGBA[ i , : ] = np.array( [ a , a , a , 1.0 ] )


class DrawParticlesGL(object):
    
    DRAW_MODEL_LOOP = 0
    DRAW_MODEL_VECTOR = 1
    
    PARTICLE_MODEL_POINT  = "point"
    PARTICLE_MODEL_SPHERE = "sphere"
    PARTICLE_MODEL_TEAPOT = "teapot"
    
    def __init__( self , pset=None ):
        self.pset = pset
        self.__trajectory = False
        self.__trajectory_step = 1
        
        self.__color_fun = lambda pset , i : ( 1.0 , 1.0 , 1.0 , 1.0 )
        
        self.__vect_color_fun = None
        self.__vect_color_fun_fl = False
    
        self.__draw_particle = self.draw_particle
        
        self.__sph_dl = None
        self.__tea_dl = None
        self.__pt_dl = None
        
        self.__draw_model = self.DRAW_MODEL_LOOP
        
        self.__init_vect_fl = False
        
        self.__log_indices = None
        self.__log_array = None
        
        
    def __del__(self):
        if self.__sph_dl != None :
            glDeleteLists( self.__sph_dl , 1 )
        
        if self.__tea_dl != None :
            glDeleteLists( self.__tea_dl , 1 )
            
        if self.__pt_dl != None :
            glDeleteLists( self.__pt_dl , 1 )
    
    
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
    
    def set_vect_color_fun( self , fun ):
        self.__vect_color_fun = fun
    
    def get_vect_color_fun( self , fun ):
        return self.__vect_color_fun
    
    vect_color_fun = property( get_vect_color_fun , set_vect_color_fun , doc="get and set the vector color function")
    
    
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
        elif model == "teapot" :
            self.__draw_particle = self.draw_particle_teapot            
    
    
    def set_draw_model( self , model ):
        self.__draw_model = model
        
    
    def draw_trajectory(self):
        
        if self.pset.log_size < self.trajectory_step + 1 :
            return
        
        if self.__log_indices == None :
            self.__log_indices = self.pset.get_log_indices_segments( True )
            self.__log_array = np.zeros( ( self.pset.log_max_size , self.pset.dim ) )
                 
        unit = self.pset.unit
        glLineWidth( 1.0 )
        
        for i in range( self.pset.size ):
            glColor4f( *self.__color_fun( self.pset , i ) )
            
            glEnableClientState(GL_VERTEX_ARRAY)
            
            ( b , e ) = self.pset.read_log_array( i , ( self.__log_array, ) )
    
            glVertexPointer( 3 , GL_FLOAT , 0 , self.__log_array / unit )
                        
            glDrawElements( GL_LINES , e , GL_UNSIGNED_INT , self.__log_indices )
            
            glDisableClientState(GL_VERTEX_ARRAY)
            
                
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
    
    def _draw_vectorized(self):
        
        if not self.__init_vect_fl :
            self.__indices = np.arange( self.pset.size * 3 , dtype=np.uint )
            self.__init_vect_fl = True
        
        if not self.__vect_color_fun_fl and self.__vect_color_fun != None :
            self.__color_vect = np.zeros(( self.pset.size , 4 ))
            self.__vect_color_fun( self.__color_vect , self.pset )
            self.__vect_color_fun_fl = True
        
        #glColor4f( *self.__color_fun( self.pset , 1 ) )
        
        if self.__vect_color_fun_fl :
            glEnableClientState(GL_COLOR_ARRAY)
            
        glEnableClientState(GL_VERTEX_ARRAY)
        
        if self.__vect_color_fun_fl :
            glColorPointer( 4 , GL_FLOAT , 0 , self.__color_vect )
        
        glVertexPointer( 3 , GL_FLOAT , 0 , self.pset.X / self.pset.unit )
        glDrawElements( GL_POINTS , self.pset.size , GL_UNSIGNED_INT , self.__indices )
        
        glDisableClientState(GL_VERTEX_ARRAY)
        
        if self.__vect_color_fun_fl :
            glDisableClientState(GL_COLOR_ARRAY)
        
    
    def draw(self):
        
        if self.__draw_model == self.DRAW_MODEL_LOOP : 
            glPointParameterf( GL_POINT_SIZE_MAX , 10.0 )
            glPointParameterf( GL_POINT_SIZE_MIN , 4.0 )    
    
            glEnable(GL_POINT_SMOOTH)
    
            for i in range( self.pset.size ):
                self.__draw_particle( self.pset , i )
            
            if self.pset.log_X_enabled and self.trajectory :
                self.draw_trajectory()
                
        elif self.__draw_model == self.DRAW_MODEL_VECTOR :
            self._draw_vectorized()
                









