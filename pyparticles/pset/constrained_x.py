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

import pyparticles.pset.particles_set as ps

import pyparticles.pset.constraint as ct


class ConstrainedX ( ct.Constraint ):
    def __init__ ( self , pset=None ):
        
        self.__X_cr   = None
        self.__X_cr_i = None
        
        super(ConstrainedX,self).__init__( pset=pset )
        
    
    def add_x_constraint( self , indx , constr ):
        """
        Add new postional contraint and update the referenced particles set.
        contraints are concatenad to the stored contraints, we don't tests the uniqness of the indicies.
        be careful with the double indicies
            ========== ================================
            Arguments
            ========== ================================
            indx       indicies of the new contraints
            constr     the new contraints
            ========== ================================
        """
        if  self.__X_cr == None :
            self.__X_cr = np.array( constr )
            self.__X_cr_i = np.array( indx )
        else :
            self.__X_cr_i = np.concatenate( ( self.__X_cr_i , indx ) )
            self.__X_cr = np.concatenate( ( self.__X_cr , constr ) )

        self.pset.X[indx,:] = constr
        
    def get_pset(self):
        """
        Return the current constrained particles set
        """
        return super(ConstrainedX,self).get_pset()
    
    def set_pset( self , pset ):
        """
        set the particles set. And it sets the constrained values in the particles set pset
        """
        pset.X[self.__X_cr_i,:] = self.__X_cr
        super(ConstrainedX,self).set_pset( pset )
        
    pset = property( get_pset , set_pset , doc="get and set the particles set (pset)")   
        
        
    def remove_x_constraint( self , indxs ):
        """
        Remove the element indixed in indxs from the contraits 
         Arguments:
            #. indxs: an interable containig the indicies of the old contraints.
        """
        ix = np.array([]) 
        for i in indxs :
            e, = np.where( i == self.__X_cr_i )
            ix = np.concatenate( ( ix, e ) )
        
        self.__X_cr = np.delete( self.__X_cr , ix , 0 )
        self.__X_cr_i = np.delete( self.__X_cr_i , ix , 0 )


    def get_cx_indicies(self):
        """
        Return a copy of the constrained indicies
        """
        return np.copy(self.__X_cr_i)
        
    def get_cx_free_indicies(self):
        """
        Return an array containing the not constrained indicies
        """
        r = range( self.pset.size )
        for i in self.__X_cr_i :
            r.remove(i)
            
        return np.array( r , dtype=np.int )

    def clear_all_x_constraint(self):
        """
        clear all positional contraints 
        """
        del self.__X_cr
        del self.__X_cr_i
        self.__X_cr   = None
        self.__X_cr_i = None
        

    def get_cX( self ):
        return self.pset.X[self.__X_cr_i,:]
    
    cX = property( get_cX , doc="return the constrained X alements" )
    
    
    