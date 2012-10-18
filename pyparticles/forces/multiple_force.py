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

class MultipleForce(object):
    """
    Combine the effect of some forces, for example constant force and springs.
    It behaves like any other force, and can be used with all methods of numerical integration. 
    """
    def __init__(self , size , dim=3 , m=None , Conts=None ):
        
        self.__forces = []
        
        self.__M = np.zeros(( size , 1 ))
        self.__A = np.zeros(( size , dim ))
        self.__F = np.zeros(( size , dim ))
        
        if m != None :
            self.set_masses( m )
    
        
    def append_force( self , force ):
        """
        Append a new force to the forces list
        """
        self.__forces.append( force )
        

    def set_masses( self , m ):
        """
        Set the masses in the forces system
        """
        self.__M[:] = m
        
        for f in self.__forces :
            f.set_masses( m )

    
    def update_force( self , p_set ):
        self.A[:] = 0.0
        for f in self.__forces :
            self.A[:] = self.A[:] + f.update_force( p_set )
            
        self.__F = self.__A[:] * self.__M[:]
        return self.__A
            
    def getA(self):
        return self.__A
        
    A = property( getA )
        
    def getF(self):
        return self.__F
    
    F = property( getF )
    
    