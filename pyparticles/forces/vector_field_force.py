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
import scipy.spatial.distance as dist

import pyparticles.forces.force as fr

class VectorFieldForce( fr.Force ) :
    def __init__(self , size , dim=3 , m=None ):
        self.__dim = dim
        self.__size = size
        self.__A = np.zeros( ( size , dim ) )
        self.__M = np.zeros( ( size , size ) )
        if m != None :
            self.set_messes( m )
        
    
    def set_masses( self , m ):
        self.__M[:] = m
    
    def update_force( self , p_set ):
        self.__A[:] = self.vect_fun( p_set.X )
        return self.__A
    
    def vect_fun( self , X ):
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
    
    def getA(self):
        return self.__A
    
    A = property( getA )


    def getF(self):
        return self.__A * self.__M[:]
    
    F = property( getF )
