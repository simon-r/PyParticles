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

import pyparticles.pset.particles_set as ps

import pyparticles.animation.animation as pan

#import pyparticles.rand_cluster as clu
#import pyparticles.euler_solver as els
#import pyparticles.leapfrog_solver as lps
#import pyparticles.runge_kutta_solver as rks

import matplotlib.animation as animation

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
#import pyparticles.periodic_boundary as pb
#import pyparticles.rebound_boundary as rb



FLOOR = -10
CEILING = 10

class AnimatedScatter( pan.Animation ):
    
    def __init__(self, numpoints=50):
        super( AnimatedScatter , self ).__init__()

 
    def build_animation(self):       
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.stream = self.data_stream()
        
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, 
                                           init_func=self.setup_plot, blit=True)
        
        
    def setup_plot(self):
        
        j = next(self.stream)
        self.scat = self.ax.scatter( self.pset.X[:,0]/self.pset.unit ,
                                     self.pset.X[:,1]/self.pset.unit ,
                                     self.pset.X[:,2]/self.pset.unit ,
                                     animated=True , marker='o' , alpha=None , s=10)
        
        self.ax.set_xlim3d( self.xlim )
        self.ax.set_ylim3d( self.ylim )
        self.ax.set_zlim3d( self.zlim )
        
        return self.scat,


    def data_stream(self):
        
        self.ode_solver.update_force()
        
        for j in range(self.steps):
            self.ode_solver.step()            
            yield j
            


    def update(self, i):
        """Update the scatter plot."""
        j = next(self.stream)
         
        self.scat._offsets3d = ( np.ma.ravel(self.pset.X[:,0]/self.pset.unit) ,
                                 np.ma.ravel(self.pset.X[:,1]/self.pset.unit) ,
                                 np.ma.ravel(self.pset.X[:,2]/self.pset.unit)
                                 )       
                
        plt.draw()
        return self.scat,

    def start(self):
        plt.show()
        
