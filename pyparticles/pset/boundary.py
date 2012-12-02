# PyParticles : Particles simulation in python
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


class Boundary(object):
    def __init__(self):
        pass
    
    def set_boundary( self , bound=(-1,1) , dim=3 ):
        if len(bound) not in ( 2 , 4 , 6 ):
            raise ValueError
        
        self.__dim = dim
        self.__bound = np.zeros((dim,2))
        
        if len(bound) >= 2 :
            self.__bound[0,0] = bound[0]
            self.__bound[0,1] = bound[1]
            
            if dim >= 2 :
                self.__bound[1,0] = bound[0]
                self.__bound[1,1] = bound[1]
            
            if dim == 3 :
                self.__bound[2,0] = bound[0]
                self.__bound[2,1] = bound[1]             
                
        if len(bound) == 6:
            self.__bound[1,0] = bound[2]
            self.__bound[1,1] = bound[3] 
            
            self.__bound[2,0] = bound[4]
            self.__bound[2,1] = bound[5]
            
        if len(bound) == 4:
            self.__bound[1,0] = bound[2]
            self.__bound[1,1] = bound[3]
    
    def get_dim(self):
        return self.__dim
    
    dim = property( get_dim )
    
    def get_bound(self):
        return self.__bound
    
    bound = property( get_bound )
    
    def boundary( self , p_set ):
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )


