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

import pyparticles.forces.force as fr

class ForceConstrained( fr.Force ) :
    def __init__( size , dim , m=None , Conts=1.0 , f_inter=None ):
        self.__f_iter = f_inter
        
        
    def get_force_iteractions( self ):
        return self.__f_iter
    
    def set_force_iteractions( self , fi ):
        self.__f_iter = fi
        
    force_iteractions = property( get_force_iteractions , set_force_iteractions )
