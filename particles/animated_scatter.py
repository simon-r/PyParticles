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

import particles.particles_set as ps

import particles.animation as pan

import particles.rand_cluster as clu
import particles.gravity as gr
import particles.euler_solver as els
import particles.leapfrog_solver as lps
import particles.runge_kutta_solver as rks

import matplotlib.animation as animation

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import particles.periodic_boundary as pb
import particles.rebound_boundary as rb
import particles.const_force as cf
import particles.vector_field_force as vf
import particles.linear_spring as ls


FLOOR = -10
CEILING = 10

class MyField( vf.VectorFieldForce ):
    def vect_fun( self , X ):
        v = ( X**2 ).T
        return ( v * -X.T/np.sqrt( np.sum(v,0) ) ).T
    

class AnimatedScatter( pan.Animation ):
    
    def __init__(self, numpoints=50):
        
        self.n = 500
        n = self.n
        self.dt = 0.01
        self.steps = 10000
        G = 0.0001
        
        self.pset = ps.ParticlesSet( self.n )
        
        self.cs = clu.RandCluster()
        
        self.cs.insert3( self.pset.X , M=self.pset.M , V=self.pset.V , n = n/2 ,
                        centre=(-1.5,1,0.5) , vel_rng=(0.5,2) , mass_rng=(0.5,5.0) )
        
        self.cs.insert3( self.pset.X , M=self.pset.M , n = int(n/2) , centre=(1.5,-0.5,0.5) , start_indx=int(n/2))
        
        self.grav = gr.Gravity(n , Consts=G )
        self.grav = cf.ConstForce(n , u_force=[1,0,-1.0] )
        #self.grav = MyField( n )
        #self.grav = ls.LinearSpring( n , Consts=0.1 )
        
        self.grav.set_masses( self.pset.M )
        
        self.bound = None
        #self.bound = pb.PeriodicBoundary( (-5.0 , 5.0) )
        #self.bound = rb.ReboundBoundary(  (-10.0 , 10.0)  )
        
        self.pset.set_boundary( self.bound )
        
        #solver = els.EulerSolver( self.grav , self.pset , self.dt )
        #solver = lps.LeapfrogSolver( self.grav , self.pset , self.dt )
        solver = rks.RungeKuttaSolver( self.grav , self.pset , self.dt )
        
        self.ode_solver = solver
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.stream = self.data_stream()
        
        
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, 
                                           init_func=self.setup_plot, blit=True)
        
        
        
       

    def setup_plot(self):
        
        j = next(self.stream)
        
        self.scat = self.ax.scatter( self.pset.X[:,0] , self.pset.X[:,1] , self.pset.X[:,2] ,
                                     animated=True , marker='o' , alpha=None , s=self.pset.M*10)
        

        self.ax.set_xlim3d(FLOOR, CEILING)
        self.ax.set_ylim3d(FLOOR, CEILING)
        self.ax.set_zlim3d(FLOOR, CEILING)

        return self.scat,


    def data_stream(self):
        
        self.ode_solver.update_force()
        
        for j in range(self.steps):
            self.ode_solver.step()            
            yield j
            


    def update(self, i):
        """Update the scatter plot."""
        j = next(self.stream)
         
        self.scat._offsets3d = ( np.ma.ravel(self.pset.X[:,0]) , np.ma.ravel(self.pset.X[:,1]) , np.ma.ravel(self.pset.X[:,2]) )       
                
        plt.draw()
        return self.scat,

    def start(self):
        plt.show()
        
