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

import pyparticles.pset.constraint as ct


class ConstrainedX ( ct.Constraint ):
    def __init__ ( self , pset=None ):
        
        self.__X_cr   = None
        self.__X_cr_i = None
        
        self.__X_free = None
        
        self.__use_slice_const = False
        self.__use_slice_free  = False
        
        super(ConstrainedX,self).__init__( pset=pset )
    
    def add_x_constraint( self , indx , constr ):
        """
        Add new positional constraint and update the referenced particles set.
        constraints are concatenated to the stored constraints, we don't tests the uniqueness of the indices.
        be careful with the double indices
        
            ========== ================================
            Arguments
            ========== ================================
            indx       indices of the new constraint
            constr     the new constraint
            ========== ================================
            
        If constr is a slice the constraints will be constants
        """
        
        if isinstance( indx , slice ):
            self.__X_cr = np.array( constr )
            self.__X_cr_i = indx
            self.__use_slice_const = True
            
            self.pset.X[indx,:] = constr
            
            self._optimize()
            return 
        
        
        if  self.__X_cr == None :
            self.__X_cr = np.array( constr )
            self.__X_cr_i = np.array( indx , dtype=np.int64 )
        else :
            self.__X_cr_i = np.concatenate( ( self.__X_cr_i , indx ) )
            self.__X_cr = np.concatenate( ( self.__X_cr , constr ) )

        self._optimize()

        self.pset.X[indx,:] = constr
      
      
    def _optimize(self):
        """
        If possible it tries to use a slice for the free indices 
        """
        r = list( range( self.pset.size ) )
        
        if isinstance( self.__X_cr_i , slice ):
            ra = range( self.__X_cr_i.start , self.__X_cr_i.stop )
        else:
            ra = self.__X_cr_i
        
        for i in ra :
            r.remove(i)
            
        seq = True
        for i in range( len(r) - 1 ) :
            d = r[i+1] - r[i]
            if d != 1 :
                seq = False
                break
        
        lr = len(r)
            
        if seq :
            self.__X_free = slice( int( r[0] ) , int( r[lr-1] ) + 1 )
        else :
            self.__X_free = np.array( r , dtype=np.int ) 
            
        print( self.__X_free )
      
    
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
        Remove the element indexed in indxs from the constraints   
         Arguments:
            #. indxs: an iterable containing the indices of the old constraints.
        """
        
        if self.__use_slice :
            return
        
        ix = np.array([]) 
        for i in indxs :
            e, = np.where( i == self.__X_cr_i )
            ix = np.concatenate( ( ix, e ) )
        
        self.__X_cr = np.delete( self.__X_cr , ix , 0 )
        self.__X_cr_i = np.delete( self.__X_cr_i , ix , 0 )


    def get_cx_indicies(self):
        """
        Return a copy of the constrained indices
        """
        if isinstance( self.__X_cr_i , slice) :
            return self.__X_cr_i
        else :
            return np.copy(self.__X_cr_i)
        
    def set_free_indicies( self , indx ):
        if isinstance( indx , slice ) :
            self.__X_free = indx
        else :
            self.__X_free = np.concatenate( ( self.__X_free , indx ) )
        
    def get_cx_free_indicies(self):
        """
        Return an array or if it's possible a slice containing the not constrained indices
        """
        return self.__X_free
        
              
    def clear_all_x_constraint(self):
        """
        clear all positional constraints 
        """
        del self.__X_cr
        del self.__X_cr_i
        self.__X_cr   = None
        self.__X_cr_i = None
        
        self.__X_free = None
        

    def get_cX( self ):
        return self.pset.X[self.__X_cr_i,:]
    
    cX = property( get_cX , doc="return the constrained X elements" )
    
    
    
