
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
    r"""
    If a particle exits form the boundary it's moved to a default position according to the function 'defualt_pos'
    
    
    :param bound: A tuple that describe the boundary - (min , max) or (x_min,x_man,y_min,y_max,z_min,z_max) 
    :param dim: dimension of the system
    :param defualt_pos: default position function
    
    | Where:
    |  defualt_pos( pset , indx ) update the X and/or V of the particles set pset 
    |  pset: particles set
    |  indx: indices of the involved particles
    """
    def __init__( self , bound=(-1,1) , dim=3 , defualt_pos=None ):
        self.set_boundary( bound , dim )
        self.__defualt_pos = defualt_pos

    
    def boundary( self , p_set ):
        for i in range( self.dim ) :
            
            b_mi, = np.where( p_set.X[:,i] < self.bound[i,0] )
            b_mx, = np.where( p_set.X[:,i] > self.bound[i,1] )
            
            if len( b_mi ) > 0 :
                self.__defualt_pos( p_set , b_mi )
                
            if len( b_mx ) > 0 :
                self.__defualt_pos( p_set , b_mx )