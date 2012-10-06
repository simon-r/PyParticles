# PyParticles : Particles simulation in python
#Copyright (C) 2012  Simone Riva
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import boundary as bd

class ReboundBoundary( bd.Boundary ):
    
    def __init__( self , bound=(-1,1) , dim=3 ):
        self.set_boundary( bound , dim )
        self.set_normals()
        
    
    def set_normals( self ):
        self.__N = np.zeros( self.bound().shape )
        
        if self.dim() >= 2 :
            self.__N[0,:2] = np.array( [1,0] )
            self.__N[1,:2] = np.array( [-1,0] )

            self.__N[2,:2] = np.array( [0,1] )
            self.__N[3,:2] = np.array( [0,-1] )
    
        if self.dim() == 3 :
            self.__N[4,:] = np.array( [0,0,1] )
            self.__N[5,:] = np.array( [0,0,-1] )
    
    def boundary( self , p_set ):
        for i in range( self.dim() ) :
            delta = self.bound()[i,1] - self.bound()[i,0]
            
            b_mi = p_set.X()[:,i] < self.bound()[i,0]
            b_mx = p_set.X()[:,i] > self.bound()[i,1]
            
            
