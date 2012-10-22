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

import pyparticles.measures.measure as me

class GravitationalPotentialEnergy( me.Measure ):
    """
    Class derived from Measure usedfor computing the total gravitational potential energy of the particle system
    """
    def __init__( self , pset=None , force=None ):
        
        self.__pot = 0.0
        
        super( GravitationalPotentialEnergy , self ).__init__( pset , force )
    
    
    def value(self):
        """
        return the current value of the potential energy
        """
        return self.__pot
    
    
    def update_measure( self ):
        """
        Compute and return the elestic potential energy on the current state of the pset 
        """
        
        D = dist.pdist( self.pset.X , 'euclidean' )
        Mm = dist.pdist( self.pset.M , lambda v , u : v*u )
        
        self.__pot = np.sum( - Mm/D * self.force.const )
        
        return self.__pot
        
    
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