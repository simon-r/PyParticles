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
import sys

class OdeSolver :
    def __init__( self , force , p_set , dt ):
        self.__force = force
        self.__p_set = p_set
        self.__dt = dt
        
    
    def get_dt( self ):
        return self.__dt

    def set_dt( self , dt ):
        self.__dt = dt

    dt = property( get_dt , set_dt )
    
    def get_force( self ):
        return self.__force
    
    def set_force( self , force ):
        self.__force = force
        
    force = property( get_force , set_force )
    
    def update_force( self ):
        self.__force.update_force( self.pset )
    
    def get_pset( self ):
        return self.__p_set
    
    def set_pset( self , p_set ):
        self.__p_set = p_set
        
    pset = property( get_pset , set_pset )
    
    
    def step( self , dt=None ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
