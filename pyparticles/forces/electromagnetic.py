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

class Electromagnetic( fr.Force ) :
    r"""
    Compute the electromagnetic force of a self-interacting particles system according to the Lorenz formulation.
    
    
    
    Not yet tested.
    """
    def __init__( self , size , dim=3 , m=None , Consts=1.0 ):
        
        self.__dim = dim
        self.__size = size
        
        self.__Ke = Consts[0]
        self.__Km = Consts[1]

        self.__Am = np.zeros( ( size , dim ) )
        self.__Ae = np.zeros( ( size , dim ) )
        
        self.__Fe = np.zeros( ( size , size ) )
        self.__Fm = np.zeros( ( size , size ) )
        
        self.__V = np.zeros( ( size , size ) )
        self.__D = np.zeros( ( size , size ) )
        self.__Q = np.zeros( ( size , size ) )
        self.__M = np.zeros( ( size , 1 ) )
        
        self.__r = np.zeros( ( size , dim ) )
        
        self.__Cr = np.zeros( ( size , dim ) )
        
        if m != None :
            self.set_masses( m )
          
    def set_masses( self , m ):
        self.__M[:] = m
        
    def set_charges( self , q ):
        self.__Q[:,:] = q
        self.__Q[:,:] = self.__Q * self.__Q.T
    
    def update_force( self , p_set ):        
        self.__D[:] = dist.squareform( dist.pdist( p_set.X , 'euclidean' ) )
        
        self.__Fe[:] = self.__Ke * self.__Q[:] / ( ( self.__D[:] ) ** 3.0 )
        self.__Fm[:] = self.__Km * self.__Q[:] / ( ( self.__D[:] ) ** 2.0 )

        np.fill_diagonal( self.__Fe , 0.0 )
        np.fill_diagonal( self.__Fm , 0.0 )
                
        for i in range( self.__dim ):
            self.__V[:,:] = p_set.X[:,i]
            self.__V[:,:] = ( self.__V[:,:].T - p_set.X[:,i] ).T 
                        
            self.__Ae[:,i] = np.sum( self.__Fe * self.__V[:,:] , 0 ) 
        
        r = self.__r
        for j in range( self.__size ) :
            r[:] = p_set.X[j,:] - p_set.X[:]
            
            r[:] = (r.T / np.sqrt( np.sum(r**2,1))).T
            r[j,:] = 0.0
            
            r[:] = np.cross( p_set.V[:] , r[:] )
            r[:] = np.cross( p_set.V[j,:] , r[:] )
            
            self.__Am[j,:] = np.sum( self.__Fm[:,j].T * r[:] , 0 ).T / self.__M[j]
            
            
        #print( self.__X )
        self.__A[:] = self.__Ae + self.__Am
        
        return self.__A
    
    def getA(self):
        return self.__A
    
    A = property( getA )


    def getF(self):
        return self.__A * self.__M
    
    F = property( getF )
