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

import pyparticles.forces.force_constrained as fcr
import numpy as np

import scipy.sparse.dok as dok
import scipy.sparse.csr as csr

class LinearSpringConstrained ( fcr.ForceConstrained ):
    def __init__( self , size , dim , m=np.array([]) , Consts=1.0 , f_inter=None ):
        super( LinearSpringConstrained , self ).__init__( size , dim , m , Consts , f_inter=f_inter )
        
        self.__dim = dim
        self.__size = size
        
        self.__K = Consts
        
        self.__A = np.zeros( ( size , dim ) )
        self.__F = np.zeros( ( size , dim ) )
        
        self.__Fm = dok.dok_matrix( ( size , size ) )
        self.__Fm2 = csr.csr_matrix( ( size , size ) )
                
        self.__M = np.zeros( ( size , 1 ) )
        if len(m) != 0 :
            self.set_masses( m )
        
    def set_masses( self , m ):
        """
        set the masses of the particles
        """
        self.__M[:] = m
        
    
    def update_force( self , pset ):
        
        dk = self.force_interactions.sparse.keys()
        
        for i in range( self.__dim ):
            #self.__Fm = dok.dok_matrix( ( pset.size , pset.size ) )
            
            for k in dk :
                self.__Fm[k[0],k[1]] = pset.X[k[1],i]
                self.__Fm[k[1],k[0]] = pset.X[k[0],i]
            
            self.__Fm2 = -self.__K * ( self.__Fm.T - self.__Fm ).T 
        
            self.__F[:,i] = self.__Fm2.sum( 0 )
        
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
