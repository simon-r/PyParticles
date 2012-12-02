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

import scipy.spatial.distance as dist

class PseudoBubble( fr.Force ) :
    r"""
    Pseudo Bubble is a **fake force** that produce the effect of the bubbles in a fluid.
    
    .. math::
    
        \begin{cases}
         & \text{ if } d_{i,j} < R \,\,\, \text{then} \,\,\,F_{i,j}= -\frac{B}{R}d_{i,j}+\frac{B}{d_{i,j}} \\ 
         & \text{ if } d_{i,j} \geqslant  R \,\,\, \text{then} \,\,\,F_{i,j}= 0
        \end{cases}
    """
    def __init__(self , size , dim=3 , m=None , Consts=( 0.3 , 2.0 ) ):
        self.__dim = dim
        self.__size = size
        
        self.__R = Consts[0]
        self.__B = Consts[1]
        
        self.__A = np.zeros( ( size , dim ) )
        self.__M = np.zeros( ( size , 1 ) )
        
        self.__F = np.zeros( ( size , size ) )
        self.__D = np.zeros( ( size , size ) )
        #self.__bool = np.zeros( ( size , size ) , dtype=np.bool )
        
        self.__V = np.zeros( ( size , size ) )
        
        if m != None :
            self.set_messes( m )
        
    
    def set_masses( self , m ):
        self.__M[:] = m
        
    
    def update_force( self , pset ):
        
        D = self.__D
        
        D[:] = dist.squareform( dist.pdist( pset.X ) )
        ( n , m ) = np.where( np.logical_and( D <= self.__R , D != 0.0 ) )
        
        #print(np.where(b))
        
        self.__F[:] = 0.0
        
        self.__F[n,m] = ( -( self.__B / self.__R ) * D[n,m] + self.__B ) / D[n,m]
        
        for i in range( pset.dim ) :
            self.__V[:,:] = pset.X[:,i]
            self.__V[:,:] = ( self.__V[:,:].T - pset.X[:,i] ).T
            
            self.__A[:,i] = np.sum( self.__F * self.__V[:,:] / self.__M.T , 0 )
        
        return self.__A
    
    def getA(self):
        return self.__A
    
    A = property( getA )
    
    def getF(self):
        return self.__A * self.__M

    F = property( getF )