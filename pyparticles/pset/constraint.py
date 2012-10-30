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

class Constraint( object ):
    def __init__( self , pset=None ):
        self.__pset = pset
        
        
    def get_pset(self):
        return self.__pset
    
    def set_pset( self , pset ):
        self.__pset = pset
        
    pset = property( get_pset , set_pset )    


    
    
    
    
    
    