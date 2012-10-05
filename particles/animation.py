

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

import particles.particles_set as ps
import particles.rand_cluster as clu
import particles.gravity as gr

import matplotlib.animation as animation

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import particles.boundary as bd


FLOOR = -5
CEILING = 5

class Animation(object):
    pass

class AnimatedScatter(Animation):
    
    def __init__(self, numpoints=50):
        
        self.n = 1000
        n = self.n
        self.dt = 0.01
        self.steps = 10000
        G = 0.001
        
        self.pset = ps.ParticlesSet( self.n )
        
        self.cs = clu.RandCluster()
        
        self.cs.insert3( self.pset.X() , M=self.pset.M() , n = n/2 )
        self.cs.insert3( self.pset.X() , M=self.pset.M() , n = int(n/2) , centre=(1.5,0.5,0.5) , start_indx=int(n/2))
        self.grav = gr.Gravity(n , Consts=G )
        
        self.grav.set_masses( self.pset.M() )
        
        self.bound = bd.PeriodicBoundary( (-5.0 , 5.0) )
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.stream = self.data_stream()
        
        
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, 
                                           init_func=self.setup_plot, blit=True)
        
        
        
       

    def setup_plot(self):
        
        j = next(self.stream)
        
        self.scat = self.ax.scatter( self.pset.X()[:,0] , self.pset.X()[:,1] , self.pset.X()[:,2] ,
                                     animated=True , marker='o' , alpha=None , s=3)
        

        self.ax.set_xlim3d(FLOOR, CEILING)
        self.ax.set_ylim3d(FLOOR, CEILING)
        self.ax.set_zlim3d(FLOOR, CEILING)

        return self.scat,


    def data_stream(self):
        
        for j in range(self.steps):
            
            self.bound.boundary( self.pset.X() )
            
            self.grav.update_force( self.pset.X() )

            self.pset.V()[:] = self.pset.V()[:] + self.grav.F() * self.dt
            self.pset.X()[:] = self.pset.X() + self.pset.V()*self.dt
            
            yield j
            


    def update(self, i):
        """Update the scatter plot."""
        j = next(self.stream)
         
        self.scat._offsets3d = ( np.ma.ravel(self.pset.X()[:,0]) , np.ma.ravel(self.pset.X()[:,1]) , np.ma.ravel(self.pset.X()[:,2]) )       
                
        plt.draw()
        return self.scat,

    def show(self):
        plt.show()
        
    