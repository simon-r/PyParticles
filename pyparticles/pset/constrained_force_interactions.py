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
from collections import deque

import scipy.sparse.dok as dok

import pyparticles.pset.particles_set as ps
import pyparticles.pset.constraint as ct



class ConstrainedForceInteractions ( ct.Constraint ):
    def __init__ ( self , pset=None ):
        
        self.__S = dok.dok_matrix( (1,1) , dtype=np.byte )
        
        if pset != None :
            self.pset = pset 
        
        
    
    def get_pset(self):
        return super(ConstrainedForceInteractions,self).get_pset()
    
    def set_pset( self , pset ):
        self.__S.resize( ( pset.size , pset.size ) )
        super(ConstrainedForceInteractions,self).set_pset( pset )
        
    pset = property( get_pset , set_pset )     
            
        
    def add_connections( self , fc ):
        """
        Adds the connections listed in *fc* .
            fc must be a list of list or a 2d array of pairs
            for example::
            
                cfi = ConstrainedForceInteractions( pset )
                a = [[1,1],[3,5]]
                cfi.add_connections( a )
        """
        for c in fc :
            #print(c)
            self.__S[ c[0] , c[1] ] = True
        
    def remove_connections( self , fc ):
        """
        Removes the connections listed in *fc* .
            fc must be a list of list or a 2d array of pairs
            for example::
            
                cfi = ConstrainedForceInteractions( pset )
                a = [[1,1],[3,5]]
                cfi.remove_connections( a )
        """       
        for c in fc :
            self.__S[ c[0] , c[1] ] = False


    def get_dense(self):
        """
        Return the dense reppresentations of the connections matrix.
            Don't use this function in a loop, don't use this function in a loop, but execute the conversion to a dense matix before the loop.
        """
        return np.bool8( self.__S.todense() )
    
    dense = property( get_dense )
    
    
    def get_sparse(self):
        """
        Return the reference to the dok_matrix sparse matrix of the connections.
            For the operations with a dense matricies, don't use this function in a loop, but execute the conversion to a dense matix before the loop.
        """
        return self.__S
    
    sparse = property( get_sparse )
    
    
    def get_items(self):
        """
        list of the commection ((i,j), value) pairs, ...)
        """
        return self.__S.items()
    
    items = property( get_items )
