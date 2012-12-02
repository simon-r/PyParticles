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

class LinearSpring( fr.Force ) :
    r"""
     Compute the forces according to the Hooke's law.
     
        .. math::
        
           F_i = -k X
     
    :param    size:      size of the particles system
    :param    dim:       dimension of the system
    :param    m:         an array containing the masses
    :param    const:     spring constant ( K )   
    """
    def __init__(self , size , dim=3 , m=None , Consts=1.0 ):
        
        self.__dim = dim
        self.__size = size
        
        self.__K = Consts
                
        self.__A = np.zeros( ( size , dim ) )
        self.__F = np.zeros( ( size , dim ) )
        self.__Fm = np.zeros( ( size , size ) )
        
        self.__M = np.zeros( ( size , 1 ) )
        if m != None :
            self.set_masses( m )
        
    
    def set_masses( self , m ):
        """
        set the masses of the particles
        """
        self.__M[:] = m
        
    
    def update_force( self , p_set ):
        
        for i in range( self.__dim ):
            self.__Fm[:,:] = p_set.X[:,i]
            self.__Fm[:,:] = -self.__K * ( self.__Fm[:,:].T - p_set.X[:,i] ).T 
        
            self.__F[:,i] = np.sum( self.__Fm , 0 )
        
        self.__A[:,:] = self.__F[:,:] / self.__M[:]
        
        return self.__A
    
    def getA(self):
        return self.__A
    
    A = property( getA )


    def getF(self):
        return self.__F
    
    F = property( getF )
    
    
    def get_const( self ):
        return self.__K       

    const = property( get_const )
