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

class TotalEnergy( me.Measure ):
    """
    Class derived from Measure used for computing the total energy of the particle system
        given a potential and a kinetic energy it simply sum the two value
    """
    def __init__( self , kinetic , potential ):
        
        self.__kinetic = kinetic
        self.__potential = potential
        
        self.__tot = 0.0
        
        super( TotalEnergy , self ).__init__( pset=None , force=None )
    
    
    def value(self):
        """
        return the current value of the potential energy
        """
        self.__tot = self.__kinetic.value() + self.__potential.value()
        return self.__tot
    
    
    def update_measure( self ):
        """
        Compute and return the total energy on the current state of pset 
        """
        return self.__tot
        
    
    def shape( self ):
        """
        return a tuple containing the shape of the measures dataset
        """
        return 1,
    
    def dim( self ):
        """
        return the dimension of the measure: 1 for the energy
        """
        return 1
    
    def name(self):
        """
        Return the string: "total energy"
        """
        return "total energy"