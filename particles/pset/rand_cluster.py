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
import particles.pset.cluster as clu


class RandCluster( clu.Cluster ):
    def __init__(self):
        pass
    
    def insert3( self , X , M=None ,V=None ,
                start_indx=0 ,
                n=100 ,
                centre=(0.0,0.0,0.0) ,
                radius=1.0 ,
                mass_rng=(0.5,1) ,
                vel_rng=(0.5,1.0) ,
                vel_mdl=None ,
                vel_dir=None ,
                randg=np.random.rand ):
        
        r = randg(n)*radius
        
        theta = np.random.rand(n) * 2.0*np.pi
        phi   = np.random.rand(n) * np.pi
        
        si = start_indx
        ei = start_indx + n
        
        X[si:ei,0] = centre[0] + r * np.cos( theta ) * np.sin( phi )
        X[si:ei,1] = centre[1] + r * np.sin( theta ) * np.sin( phi )
        X[si:ei,2] = centre[2] + r * np.cos( phi )
        
        if M != None:
            M[si:ei,0] = mass_rng[0] + randg(n)*( mass_rng[1] - mass_rng[0] )
            
        if V != None and "bomb" in vel_mdl :
            self.bomb_vel( X , V , n=n , start_indx=start_indx , centre=centre , randg=randg , vel_rng=vel_rng)
            
        if V != None and "const" in vel_mdl :
            self.const_vel( X , V , n=n , start_indx=start_indx , randg=randg , vel_rng=vel_rng , vel_dir=vel_dir )
    
    
    def bomb_vel( self , X , V ,
                  start_indx=0 ,
                  n=100 ,
                  centre=(0.0,0.0,0.0),
                  vel_rng=(0.5,1.0) ,
                  randg=np.random.rand ):
        
        si = start_indx
        ei = start_indx + n
        
        mX = X[si:ei,:] - centre
        
        U = ( mX.T / np.sqrt( np.sum( mX**2.0 , 1 ) ) ).T
        
        V[si:ei,:] = V[si:ei,:] + ( U.T * ( vel_rng[0] + randg( n ) * ( vel_rng[1] - vel_rng[0] ) ) ).T
    
        
    def const_vel( self , X , V ,
                   start_indx=0 ,
                   n=100 ,
                   vel_rng=(0.5,1.0) ,
                   vel_dir=[1,0,0] ,
                   randg=np.random.rand ):

        si = start_indx
        ei = start_indx + n
        
        v_dir = np.zeros( V[si:ei,:].shape ) + vel_dir
        
        #print( np.array(vel_dir) )
        
        V[si:ei,:] = V[si:ei,:] + ( v_dir.T * ( vel_rng[0] + randg( n ) * ( vel_rng[1] - vel_rng[0] ) ) ).T
        
