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

class Electrostatic( fr.Force ) :
    r"""
    Compute the electrostatic force using the Culomb law.
        
    ..note::
     
        The real forces of an electrodynamic system is given by the **Maxwell equations**! and not from the Culomb law.
        
        The Culomb law is adapt for computing forces in a static system of particles and not for moving particles.
        
        But for a very slow movement it should be a good approximation.
        
    .. math::
        
        \vec F = k \, q_1 \, q_2 \, \frac {\vec r_1 - \vec r_2}{\left \| \vec r_1 - \vec r_2 \right \|^3}
    """
    def __init__(self , size , dim=3 , m=None , q=None , Consts=1.0 ):
        
        self.__dim = dim
        self.__size = size
        self.__K = Consts # Culomb constant!
        self.__A = np.zeros( ( size , dim ) )
        self.__Fm = np.zeros( ( size , size ) )
        self.__V = np.zeros( ( size , size ) )
        self.__D = np.zeros( ( size , size ) )
        self.__Q = np.zeros( ( size , size ) )
        self.__M = np.zeros( ( size , 1 ) )
        
        if m != None :
            self.set_masses( m )
        
        if q != None :
            self.set_charges( q )
        
    
    def set_masses( self , m ):
        self.__M[:] = m
        
    def set_charges( self , q ):
        self.__Q[:,:] = q
        self.__Q[:,:] = self.__Q * self.__Q.T
    
    def update_force( self , p_set ):
        
        self.__D[:] = dist.squareform( dist.pdist( p_set.X , 'euclidean' ) )
        
        self.__Fm[:] = self.__K * self.__Q[:] / ( ( self.__D[:] ) ** 3.0 )

        #for j in range( self.__size ) :
        #    self.__Fm[j,j] = 0.0
            
        np.fill_diagonal( self.__Fm , 0.0 )
        
        for i in range( self.__dim ):
            self.__V[:,:] = p_set.X[:,i]
            self.__V[:,:] = ( self.__V[:,:].T - p_set.X[:,i] ).T 
                        
            self.__A[:,i] = np.sum( self.__Fm * self.__V[:,:] , 0 ) / self.__M.T
        
        
        #print( self.__X )
        
        return self.__A
    
    def getA(self):
        return self.__A
    
    A = property( getA )


    def getF(self):
        return self.__A * self.__M
    
    F = property( getF )

