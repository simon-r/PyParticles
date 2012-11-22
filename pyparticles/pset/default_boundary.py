
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
import pyparticles.pset.boundary as bd


class DefaultBoundary( bd.Boundary ):
    """
    If a particle exits form the boudary it's moved to a default position according to the function 'defualt_pos'
    
    | Where:
    |  X = defualt_pos( pset , indx )
    |  pset: particles set
    |  indx: indecies of the perticles exited
    |  X: New coordinates
    """
    def __init__( self , bound=(-1,1) , dim=3 , defualt_pos=None ):
        self.set_boundary( bound , dim )
        self.__defualt_pos = defualt_pos

    
    def boundary( self , p_set ):
        for i in range( self.dim ) :
            delta = self.bound[i,1] - self.bound[i,0]
            
            b_mi = p_set.X[:,i] < self.bound[i,0]
            b_mx = p_set.X[:,i] > self.bound[i,1]
            
            p_set.X[b_mi,i] = self.__defualt_pos( p_set , b_mi )
            p_set.X[b_mx,i] = self.__defualt_pos( p_set , b_mx )