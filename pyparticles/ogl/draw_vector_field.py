
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
import random 

import pyparticles.geometry.transformations as tr

from OpenGL.GL import *
from OpenGL.GLU import *


class DrawVectorField( object ):
    """
    Draw the given vector fields.
    
    Constructor:
    
            ========== ==============================================================
            Arguments
            ========== ==============================================================
            limits     size of the draw volume: (x_min,x_max,y_min,y_max,z_min,z_max)
            density    distance between the plotted vectors  
            ========== ==============================================================
    """
    def __init__( self , limits , density , unit_len=1.0):
        
        self.__fields = dict()
        self.__col_fun = dict()
        
        if len(limits) not in ( 4 , 6 ):
            raise ValueError("limits are allowed only for 2D or 3D")
        
        self.__limits = limits
        self.__density = density
        
        self.__unit_len = unit_len
        
        self._build_coords()
    
    
    def _build_coords(self):
        """
        private: build the coordinates of the vectors
        """
        
        li = self.__limits
        de = self.__density
        
        sz_x = int( ( li[1] - li[0] ) / de )
        sz_y = int( ( li[3] - li[2] ) / de )
        
        if len(li) == 6 :
            sz_z = int( ( li[5] - li[4] ) / de )
        else: 
            sz_z = 1
            li[4] = 0.0
            li[5] = 0.0
        
        self.__X = np.zeros(( sz_x * sz_y * sz_z , 3 ))
        self.__V = np.zeros(( sz_x * sz_y * sz_z , 3 ))
        self.__Vs = np.zeros(( sz_x * sz_y * sz_z , 3 ))
        
        x = np.float64( li[0] )
        y = np.float64( li[2] )
        z = np.float64( li[4] )
        
        indx = 0
        for i in range(sz_z):
            x = li[0]
            for j in range(sz_x):
                y = li[2]
                for l in range(sz_y):
                    self.__X[indx,:] = np.array([x,y,z])
                    indx+=1
                    y = y + de
                x = x + de
            z = z + de
    
    def add_vector_fun( self , fun , color_fun , key=None , time_dep=False ):
        r"""
        Insert a new vector function, 
        
            ========== ==============================================================
            Arguments
            ========== ==============================================================
            fun        Vector filed function
            color_fun  Colors function
            key        [optional] a key used for distinguish the vector field
            time_dep   [True or **False** ] if True Is a time dependent filed  
            ========== ==============================================================        
        
        where functions are defined:
            fun( V , X )
            color_fun( RGBA , X )
            
        | X : (n by DIM) coordinates array
        | V : (n by DIM) resulting vector field
        | RGBA : (n by 4) colors array
        """
        if key == None :
            key = str( random.randint( 0 , 2**64 ) )
            
        self.__fields[key] = { "fun": fun , "color": color_fun , "time_dep" : time_dep , "display_list" : None }
        
        return key
    
    
    def ogl_init(self):
        for key in self.__fields.keys() :
            if not self.__fields[key]["time_dep"] :
                dl = glGenLists(1)
                
                glNewList( dl , GL_COMPILE );
                self._draw_field(key)
                glEndList() 
                
                self.__fields[key]["display_list"] = dl
    
    
    def _draw_field( self , key ):
        
        sz = self.__X.shape[0]
        
        transf = tr.Transformations()
        
        self.__fields[key]["fun"]( self.__V , self.__X )
        
        # Vector in spherical coordinates
        self.__Vs[:,0] = np.sqrt( np.sum( self.__X**2 , 1 ) )
        self.__Vs[:,1] = np.arccos( self.__X[:,2] / self.__Vs[:,0]  ) 
        self.__Vs[:,2] = np.arctan( self.__X[:,1] / self.__X[:,0] )
        
        for i in range(sz):
            
            x = self.__X[i,0]
            y = self.__X[i,1]
            z = self.__X[i,2]
            
            transf.push_matrix()
            transf.translation( x , y , z )
            
            transf.rotZ( self.__Vs[i,2] )
            transf.rotY( -( np.pi/2.0 - self.__Vs[i,1] ) )
            
            le = self.__Vs[:,0] / self.__unit_len
            
            transf.append_point( [ 0 , 0 , 0 ] )
            transf.append_point( [ le , 0 , 0 ] )
            
            
            transf.pop_matrix()
    
    def draw(self):
        pass
    
    
    
    
    