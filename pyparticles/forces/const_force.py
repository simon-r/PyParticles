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
import pyparticles.forces.force as fr

class ConstForce( fr.Force ) :
    """
    Constant force field.
    
    Constructor
         
    :param    size:        the number of particles in the system
    :param    dim:         the dimension of the system
    :param    m:           a vector containig the masses
    :param    u_force:     The force vector (Force per unit of mass)
    """
    
    def __init__(self , size , dim=3 , m=None , u_force=[0,0,0] , Consts=1.0 ):
        self.__dim = dim
        self.__size = size
        self.__G = Consts
        self.__UF = np.array( u_force )
        self.__A = np.zeros( ( size , dim ) )
        self.__M = np.zeros( ( size , 1 ) )
        if m != None :
            self.set_messes( m )
            
        self.__A[:] = self.__UF
        
    
    def set_masses( self , m ):
        self.__M[:] = m
        
    def update_force( self , p_set ):
        return self.__A
    
    def getA(self):
        return self.__A
    
    A = property( getA )
    
    def getF(self):
        return self.__A * self.__M

    F = property( getF )

