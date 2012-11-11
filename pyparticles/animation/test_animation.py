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


import pyparticles.forces.gravity as gr
import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.midpoint_solver as mps

import matplotlib.pyplot as plt
import numpy as np

import pyparticles.forces.const_force as cf
import pyparticles.forces.drag as dr
import pyparticles.forces.multiple_force as mf


def free_fall( t , m=1. , g=10. , k=1. ):
    return (np.sqrt(2.*g*k)*t*m**2.-2.*m**(5./2.)*np.log((1./2.)*np.exp(np.sqrt(2.)*np.sqrt(g*k)*t/np.sqrt(m))+1./2.))/(m**(3./2.)*k)


def free_fall_b( t , g=-10. ):
    return 1./2. * g * t**2

class TestAnimation( pan.Animation ):
    
    def __init__(self):
        super( TestAnimation , self ).__init__()

 
    def build_animation(self):
        
        self.steps = 3000
        
        self.pset = ps.ParticlesSet( 1 , 3 )
        self.pset.M[:] = 1.0
        self.pset.V[:] = 0.0
        
        self.t = np.zeros(( self.steps ))
        self.x = np.zeros(( self.steps , self.pset.dim ))
        
        self.xn = np.zeros(( self.steps , self.pset.dim ))
        
        constf = cf.ConstForce( self.pset.size , u_force=[ 0 , 0 , -10.0 ] , dim=self.pset.dim )
        drag = dr.Drag( self.pset.size , Consts=1.0 )
        
        multi = mf.MultipleForce( self.pset.size )
        
        multi.append_force( constf )
        multi.append_force( drag )
        
        multi.set_masses( self.pset.M )
        
        dt = 0.001
        
        self.ode_solver = els.EulerSolver( multi , self.pset , dt )
        self.ode_solver = rks.RungeKuttaSolver( multi , self.pset , dt )
        #self.ode_solver = lps.LeapfrogSolver( multi , self.pset , dt )
        #self.ode_solver = mps.MidpointSolver( multi , self.pset , dt )
        
    def data_stream( self , i ):
        
        self.t[i] = self.ode_solver.time
        self.x[i,2] = free_fall( self.t[i] , g=10.0)
        
        self.xn[i,2] = self.pset.X[0,2]
        
        print( " t: %f , x: %f , xn: %f " % ( self.t[i] , self.x[i,2] , self.xn[i,2] ) )
        
        self.ode_solver.step()
            

    def start(self):
        for i in range( self.steps ):
            self.data_stream( i )
        
        #print( self.xn[:,2] )
        
        plt.plot( self.t[:] , self.x[:,2] )
        plt.plot( self.t[:] , self.xn[:,2] )
        
        plt.grid(1)
        
        plt.show()
