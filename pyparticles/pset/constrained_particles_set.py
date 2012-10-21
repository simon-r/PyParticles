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


class ConstrainedParticlesSet ( ps.ParticlesSet ):
    def __init__ ( self , size=1 , dim=3 , boundary=None ,
                  label=False , mass=True , velocity=True , charge=False ,
                  log_X=False , log_V=False , log_max_size=0 ):
        
        self.__X_cr   = None
        self.__X_cr_i = None
        
        super(ConstrainedParticlesSet.self).__init__( size , dim , boundary , label , mass , velocity , charge , log_X , log_V , log_max_size )
        
    
    def add_x_constraint( self , indx , constr ):
        """
        Add new postional contraint
        contraints are concatenad to the stored contraints, we don't tests the uniqness of the indicies.
        be careful with the double indicies
            ========== ================================
            Arguments:
            ========== ================================
            indx:      indicies of the new contraints
            constr:    the new contraints
            ========== ================================
        """
        if  self.__X_cr == None :
            self.__X_cr = np.array( constr )
            self.__X_cr_i = np.array( indx )
            return 
        
        self.__X_cr_i = np.concatenate( ( self.__X_cr_i , indx ) )
        self.__X_cr = np.concatenate( ( self.__X_cr , constr ) )

        
    def remove_x_constraint( self , indxs ):
        """
        Remove the element indixed in indxs from the contraits 
         Arguments:
            #. indxs: an interable containig the indicies of the old contraints.
        """
        ix = np.array([]) 
        for i in indxs :
            e, = np.where( i )
            ix = np.concatenate( ( ix, e ) )
            
        self.__X_cr = np.delete( __X_cr , ix , 0 )
        self.__X_cr_i = np.delete( __X_cr_i , ix , 0 )


    def get_cx_indicies(self):
        """
        Return a copy of the constrained indicies of the position
        """
        return copy(self.__X_cr_i)
        

    def clear_all_x_constraint(self):
        """
        clear all positional contraints 
        """
        del self.__X_cr
        del self.__X_cr_i
        self.__X_cr   = None
        self.__X_cr_i = None
        

    def get_cX( self ):
        return self.X[elf.__X_cr_i]
    
    cX = property( get_cX , doc="return the constrained X alements" )
    
    
    
    
    
    