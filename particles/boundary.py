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

class Boundary:
    def __init__(self):
        pass
    
    def boundary( self , X ):
        pass

class PeriodicBoundary( Boundary ):

    def __init__( self , bound=(-1,1) , dim=3 ):
        
        
        self.dim = dim
        self.bound = np.zeros((dim,2))
        
        if len(bound) >= 2 :
            self.bound[0,0] = bound[0]
            self.bound[0,1] = bound[1]
            
            if dim >= 2 :
                self.bound[1,0] = bound[0]
                self.bound[1,1] = bound[1]
            
            if dim == 3 :
                self.bound[2,0] = bound[0]
                self.bound[2,1] = bound[1]             
            
            
            
        if len(bound) == 6:
            self.bound[1,0] = bound[2]
            self.bound[1,1] = bound[3] 
            
            self.bound[2,0] = bound[4]
            self.bound[2,1] = bound[5]
            
        if len(bound) == 4:
            self.bound[1,0] = bound[2]
            self.bound[1,1] = bound[3]
        
        if len(bound) not in ( 2 , 6 , 4 ):
            raise ValueError
    
    def boundary( self , X ):
        for i in range(self.dim) :
            delta = self.bound[i,1] - self.bound[i,0]
            
            b_mi = X[:,i] < self.bound[i,0]
            b_mx = X[:,i] > self.bound[i,1]
            
            X[b_mi,i] = X[b_mi,i] + delta
            X[b_mx,i] = X[b_mx,i] - delta