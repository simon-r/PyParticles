
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
from OpenGL.GLUT import *
from OpenGL.GLU import *




class DrawVectorField( object , limits , density ):
    def __init__(self):
        
        self.__fields = dict()
        self.__col_fun = dict()
    
        self.__size = size
        self.__density = density
    
    def add_vector_fun( self , fun , color_fun , key=None , time_dep=False ):
        if key == None :
            key = str( random.randint( 0 , 2**64 ) )
            
        self.__fields[key] = { "fum": fun , "color": color_fun , "time_dep" : time_dep , "display_list" : None }
        
        return key
    
    def ogl_init(self):
        pass
    
    def draw(self):
        pass