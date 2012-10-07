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

class ParticlesSet:
    def __init__( self , size , dim=3 , boundary=None ):
        
        if size < 0 :
            raise
        
        self.__X = np.zeros((size,dim))
        self.__V = np.zeros((size,dim))
        
        self.__mass = np.zeros((size,1))
        
        self.__size = size
        self.__dim  = dim
        self.__centre_mass = None
        
        self.__bound = boundary

    def getX(self):
        return self.__X
    
    X = property( getX )
    
    def getM(self):
        return self.__mass
    
    M = property( getM )
    
    def getV(self):
        return self.__V
    
    V = property( getV )

    def update_boundary( self ):
        if self.__bound != None :
            self.__bound.boundary( self )
        
    def get_boundary( self ):
        return self.__bound
    
    def set_boundary( self , boundary):
        self.__bound = boundary

    boundary = property( get_boundary , set_boundary )

    def update_centre_of_mass(self):
        self.__centre_mass = np.sum( self.__X * self.__mass , axis=0 ) / np.float( self.__size )
        return self.__centre_mass
        
    def centre_of_mass(self):
        return self.__centre_mass
    
    def dim(self):
        return self.dim
    
    def size( self ):
        return self.__size
    
    def add_clusters( self , Cs , n ):
        i = 0
        for c in Cs:
            self.__X[n[i]:n[i]+C.shape[0]] = c
            i = i + 1
            
    