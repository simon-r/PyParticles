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
import scipy.spatial.distance as dist

import pyparticles.forces.force as fr


class LenardJones( fr.Force ) :
    r"""
    Compute the lenard jones force between the particles

    The L. J. force between two particles is defined as follow:

    .. math::

        \mathbf{F}(r) = 4 \epsilon \left(12\,{\frac{{\sigma}^{12}}{{r}^{13}}}-6\,{\frac{{\sigma}^{6}}{{r}^{7}}}\right)\hat{\mathbf{r}}

    Constructor:

    :param    size:        the number of particles in the system
    :param    dim:         the dimension of the system
    :param    m:           a vector containig the masses
    :param    Const:       An indexable object[*] with the two contants
        

    [*] Const[0] = :math:`\epsilon`
        Const[1] = :math:`\sigma`

    """


    def __init__( self , size , dim=3 , m=None , Consts=( 1.0 , 1.0 ) ):
        self.__dim = dim
        self.__size = size
        self.__E = Consts[0]
        self.__O = Consts[1]

        self.__M = np.zeros( ( size , 1 ) )
        
        self.__pF = np.zeros(( (size**2-size)/2 ))
        
        self.__V = np.zeros( ( size , size ) )
        
        self.__A = np.zeros( ( size , dim ) )
        
        if m != None :
            self.set_masses( m )
        
        
    def set_masses( self , m ):
        """
        Set the masses used for computing the forces.
        """
        self.__M[:] = m
       
    
    def update_force( self , p_set ):
        """
        Compute the force of the current status of the system and return the accelerations of every particle in a *size by dim* array
        
        :param    p_set:     Particles set obj.
        """
        
        r =  dist.pdist( p_set.X , 'euclidean' )
        
        self.__pF[:] = 4.0 * self.__E * ( 12.0 * self.__O**12.0 / r**13.0 - 6.0 * self.__O**6.0 / r**7.0  ) / ( r )
        
        F = dist.squareform( self.__pF[:] )
        
        for i in range( p_set.dim ) :
            self.__V[:,:] = p_set.X[:,i]
            self.__V[:,:] = ( self.__V[:,:].T - p_set.X[:,i] ).T
            
            self.__A[:,i] = np.sum( F * self.__V[:,:] / self.__M.T , 0 )
            
            
        return self.__A
    
    def getA(self):
        """
        Return the currents accelerations of the particles
        """
        return self.__A
    
    A = property( getA , doc="Return the currents accelerations of the particles (getter only)")


    def getF(self):
        """
        Return the currents forces on the particles
        """
        return self.__A * self.__M[:,0]
    
    F = property( getF , doc="Return the currents forces on the particles (getter only)")