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

class Drag( fr.Force ) :
    r"""
    Calculate the forces of resistance. Drag is a force that reacts to the movement with respect to a square law speed. It's commonly used for describing the resistance  of a fluid

    The force is given the equation:

    .. math::

        F_i=-\frac{1}{2}K\dot{X}^2

    Constructor:
        
    :param    size:        the number of particles in the system
    :param    dim:         the dimension of the system
    :param    m:           a vector containig the masses
    :param    Const:       the drag factor K
    """

    def __init__(self , size , dim=3 , m=None , Consts=1.0 ):
        
        self.__dim = dim
        self.__size = size
        
        self.__G = np.zeros( ( size , 1 ) )
        self.__G[:] = Consts
        
        self.__A = np.zeros( ( size , dim ) )
        self.__F = np.zeros( ( size , dim ) )
        
        self.__V = np.zeros( ( size , 1 ) )
        
        self.__M = np.zeros( ( size , 1 ) )
        if m != None :
            self.set_masses( m )
        
        
    
    def set_masses( self , m ):
        self.__M[:] = m
    
    
    def update_force( self , pset ):
        
        self.__V.T[:] = np.sqrt( np.sum( pset.V[:]**2 , 1 )  )
        
        #print( self.__V[:] )
        #print( pset.V[:] )
        
        self.__F[:] =  -1./2. * self.__V[:] * pset.V[:] * self.__G[:]
        
        self.__A = self.__F[:] / self.__M
        
        return self.__A
    

    def getA(self):
        return self.__A
    
    A = property( getA )


    def getF(self):
        return self.__A * self.__M[:,0]
    
    F = property( getF )
