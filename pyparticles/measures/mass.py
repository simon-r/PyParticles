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

class Mass( object ):
    """
    'Meaure' for computing the total mass of the particle system
    """
    def __init__( self , pset=None, force=None  ):
        super( Mass , self ).__init__( pset=pset , force=force )
        self.__M = 0.0
    
     
    def update_measure( self ):
        """
        Compute and return the totale mass of the system
        """
        self.__M = np.sum( self.pset.M[:] )
        return self.__M
    
    
    def value(self):
        """
        Return the current measured total mass 
        """
        return self.__M
    
    
    def shape(self ):
        """
        return a tuple containing the shape of the measures dataset
        """
        return 1,
    
    def dim( self ):
        """
        return the dimension of the measure: 1 for the mass
        """
        return 1
    
    def name(self):
        """
        Return the string: "mass"
        """
        return "mass"