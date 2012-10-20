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

class ElasticPotentialEnergy( object ):
    """
    Mesure for computing the total potential energy of the particle system
    """
    def __init__( self , pset=None ):
        super( Mass , self ).__init__( pset=pset , force=force )
    
     
    def value( self ):
        """
        The value of the potential energy taken from the current status of the psrticles system.
        """
        
        m = self.pset.size
        
        s = (m * (m - 1) / 2) 
        
        self.__D = dist.pdist( p_set.X , 'euclidean' )
        
        
        return 22
    
    def shape( self ):
        """
        return a tuple containing the shape of the measures dataset
        """
        return 1,
    
    def dim( self ):
        """
        return the dimension of the measure: 1 for the potential energy
        """
        return 1
    
    def name(self):
        """
        Return the string: "potential energy"
        """
        return "potential energy"