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

class Cluster:
    pass

class RandCluster( Cluster ):
    def __init__(self):
        pass
    
    def insert3( self , X , M=None ,V=None ,
                start_indx=0 , n=100 , centre=(0.0,0.0,0.0) , radius=1.0 ,
                min_mass=0.5 , max_mass=1.0 , randg=np.random.rand ):
        
        r = randg(n)*radius
        
        theta = np.random.rand(n) * 2.0*np.pi
        phi   = np.random.rand(n) * np.pi
        
        si = start_indx
        ei = start_indx + n
        
        X[si:ei,0] = centre[0] + r * np.cos( theta ) * np.sin( phi )
        X[si:ei,1] = centre[0] + r * np.sin( theta ) * np.sin( phi )
        X[si:ei,2] = centre[0] + r * np.cos( phi )
        
        if M != None:
            M[si:ei,0] = min_mass + randg(n)*( max_mass - min_mass )
    
    