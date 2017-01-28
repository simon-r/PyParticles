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
import pyparticles.pset.cluster as clu
import scipy.spatial.distance as dist

import pyparticles.forces.gravity as gr
import pyparticles.pset.particles_set as ps


class RandCluster( clu.Cluster ):
    def __init__(self):
        pass
    
    def insert3( self ,
                X , 
                M=None ,
                V=None ,
                start_indx=0 ,
                n=100 ,
                centre=(0.0,0.0,0.0) ,
                radius=1.0 ,
                mass_rng=(0.5,1) ,
                vel_rng=(0.5,1.0) ,
                vel_mdl=None ,
                vel_dir=None ,
                randg=np.random.rand ,
                r_min=0.0 ):
        
        
        flag = True
        
        si = int(start_indx)
        ei = int(start_indx + n)
        
        rng = range( si , ei )
        indx = range( si , ei )
            
        while flag :
            nn = len( indx )
            
            r = randg(nn) * radius
            
            theta = np.random.rand(nn) * 2.0*np.pi
            phi   = np.random.rand(nn) * np.pi
            
            X[ indx , 0 ] = centre[0] + r * np.cos( theta ) * np.sin( phi )
            X[ indx , 1 ] = centre[1] + r * np.sin( theta ) * np.sin( phi )
            X[ indx , 2 ] = centre[2] + r * np.cos( phi )
        
            #print( X[indx,:] )
        
            if r_min == 0.0 :
                flag = False
            else:
                d = dist.squareform( dist.pdist( X[rng,:] ) )
                ax , bx = np.where( np.logical_and( d < r_min , d > 0.0 ) )
                
                indx = np.int64( start_indx + np.unique( np.concatenate(( ax , bx )) ) )
                
                if len( indx ) == 0 :
                    flag = False
                
        if M is not None:
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
        
    
        
class RandGalaxyCluster( clu.Cluster ):
    def __init__(self):
        pass
    
    def insert3( self ,
                X , 
                M ,
                V ,
                G ,
                start_indx=0 ,
                n=-1 ,
                centre=(0.0,0.0,0.0) ,
                radius=1.0 ,
                mass_rng=( 0.7 , 1 ) ,
                std=( 3.0 , 0.6 , 0.2 ),
                black_hole_mass=5000.0 
                ):
            
        if n <= 0 :
            n = X.shape[0] - start_indx
            
        si = int(start_indx)
        ei = int(start_indx + n) 
    
        rng = slice( si , ei )
        
        std_x = std[0]
        std_y = std[1]
        std_z = std[2]
            
        X[rng,0] = radius*np.random.normal( 0.0 , std_x , n )
        X[rng,1] = radius*np.random.normal( 0.0 , std_y , n )
        X[rng,2] = radius*np.random.normal( 0.0 , std_z , n )
        
        X[si,:] = np.array([0.0,0.0,0.0])
            
        if M is not None :
            M[rng] = mass_rng[0] + np.random.rand(n,1)*( mass_rng[1] - mass_rng[0] )
            M[si] = black_hole_mass
                
        c = np.cross(X, np.array([ 0 , 0 , 1 ]) )  
        
        c = ( c.T / np.sqrt( np.sum( c**2 , 1 ) ) ).T
        
        c[si,:] = np.array([0.0,0.0,0.0])
        
        pset = ps.ParticlesSet( n )
        
        pset.X[:] = X[rng,:]
        pset.M[:] = M[rng]
        
        grav = gr.Gravity( n , Consts=G )
        
        grav.set_masses( pset.M )
        grav.update_force(pset)
        
        f = np.sqrt( np.sum( grav.F**2 , 1 ) )
        
        r = np.sqrt( np.sum( pset.X**2 , 1 ) )
        
        v = np.sqrt( f * r / pset.M[:,0] ) 
        
        V[rng,:] = (v * c.T).T / 1.3
        
        X[rng,:] = X[rng,:] + np.array( centre ) 
        
                
                
                
                
                  
