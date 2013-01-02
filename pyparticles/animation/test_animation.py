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
import pyparticles.ode.stormer_verlet_solver as svs

#import pyparticles.ode.euler_solver_constrained as asc
#import pyparticles.ode.leapfrog_solver as lfs
#import pyparticles.ode.stormer_verlet_solver_constrained as svc
#import pyparticles.ode.runge_kutta_solver_constrained as rkc
#import pyparticles.ode.midpoint_solver_constrained as mdc


import matplotlib.pyplot as plt
import numpy as np

import pyparticles.forces.const_force as cf
import pyparticles.forces.drag as dr
import pyparticles.forces.multiple_force as mf
import pyparticles.forces.linear_spring as ls
import pyparticles.forces.damping as da

import pyparticles.pset.constrained_x as csx
import pyparticles.pset.constrained_force_interactions as cfi

from matplotlib.ticker import FuncFormatter



def free_fall( t , m=1. , g=10. , k=1. ):
    z = (np.sqrt(2.*g*k)*t*m**2.-2.*m**(5./2.)*np.log((1./2.)*np.exp(np.sqrt(2.)*np.sqrt(g*k)*t/np.sqrt(m))+1./2.))/(m**(3./2.)*k)
    return np.array( [ 0.0 , 0.0 , z ] )

def harmonic( t ):
    a = np.cos( t ) / np.sqrt(3.0)
    return np.array( [ a , a , a ] )

def damp_harmonic( t ):
    a = (1./15.)*np.sqrt(15.)*np.exp(-(1./4.)*t)*np.sin((1./4.)*np.sqrt(15.)*t)+np.exp(-(1./4.)*t)*np.cos((1./4.)*np.sqrt(15.)*t)
    a = a / np.sqrt(3.0)

    return np.array( [ a , a , a ] )


class TestAnimation( pan.Animation ):
    """
    Test the free fall with the fluid drag
    """
    def __init__(self):
        super( TestAnimation , self ).__init__()
        
        self.__analytical_sol = free_fall
 
    def set_analytical_sol( self , f ):
        self.__analytical_sol = f
        
    def get_analytical_sol( self ):
        return self.__analytical_sol
        
    analytical_sol = property( get_analytical_sol , set_analytical_sol )
 
 
 
    def set_ip( self , i ):
        self.__ip = i
        
    def get_ip( self ):
        return self.__ip    
    
    ip = property( get_ip , set_ip )
 
 
    def init_pset(self):
        self.pset.M[:] = 1.0
        self.pset.V[:] = 0.0
        self.pset.X[:] = 0.0
 
    def build_animation(self):
        
        self.steps = 3000
        
        self.pset = ps.ParticlesSet( 1 , 3 )
        
        self.ip = 0
        
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
        
        self.odes = dict()
        
        self.odes["Euler      "] = els.EulerSolver( multi , self.pset , dt ) 
        self.odes["Runge Kutta"] = rks.RungeKuttaSolver( multi , self.pset , dt ) 
        self.odes["Leap Frog  "] = lps.LeapfrogSolver( multi , self.pset , dt ) 
        self.odes["MidPoint   "] = mps.MidpointSolver( multi , self.pset , dt ) 
        self.odes["Verlet     "] = svs.StormerVerletSolver( multi , self.pset , dt ) 
        
    def data_stream( self ):
        
        for i in range( self.steps ) :
            
            self.t[i] = self.ode_solver.time
            
            #print( self.t[i] )
            
            self.x[i,:] = self.analytical_sol( self.t[i] )
        
            self.xn[i,:] = self.pset.X[self.ip,:]
            
            #print( " t: %f , x: %s , xn: %s " % ( self.t[i] , self.x[i,:] , self.xn[i,:] ) )
            self.ode_solver.step()
            
            

    def start(self):
        
        print( "Start testing:" )
        
        j = 0
        
        print("")
        print("Errors:")
        
        #plt.ion()
        
        for ky in self.odes.keys():
            
            self.init_pset()
            
            self.ode_solver = self.odes[ky]
            self.data_stream()
        
            err = np.sqrt( np.sum( (self.x-self.xn)**2 , 1 ) )
        
            merr = np.mean( err )
        
            mt = np.array( [ self.t[0] , self.t[self.steps-1] ] )
            me = np.array( [ merr , merr ] )
            
            print( " %s - mean err: %f " % ( ky , merr ) )
        
            ax = plt.subplot( 230+j+1 )
                    
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.1f')%(x*1e3)))
        
            p1, = plt.plot( self.t[:] , err , linewidth=2 )
            p2, = plt.plot( mt , me , linewidth=1 , color="g" )
            
            plt.title( "Absolute error: %s " % ky )
            plt.xlabel( "Time" )
            plt.ylabel( "Abs error [1e-3]" )
        
            plt.legend([p1, p2], ["Abs Error", "Mean"] , loc=4 )
        
            plt.grid(1)
            
            plt.draw()
            
            j += 1
        
        plt.show()
        

        
class TestAnimationHarmonic( TestAnimation ):
    """
    Test the harmonic motion with two particles.
    """
    
    def __init__(self):
        self.analytical_sol = harmonic

    def init_pset(self):
        self.pset.X[0,:] = 0.0
        self.pset.X[1,:] = 1.0 / np.sqrt(3)
        self.pset.M[:] = 1.0
        self.pset.V[:] = 0.0
        
    def build_animation(self):
        
        self.steps = 6000
        dt = 0.004
        
        self.ip = 1
        
        self.pset = ps.ParticlesSet( 2 , 3 )
        self.pset.M[:] = 1.0
        self.pset.V[:] = 0.0
        
        self.pset.X[0,:] = 0.0
        self.pset.X[1,:] = 1.0 / np.sqrt(3)
        
        ci = np.array( [ 0 ] )
        cx = np.array( [ 0.0 , 0.0 , 0.0 ] )
        
        costrs = csx.ConstrainedX( self.pset )
        costrs.add_x_constraint( ci , cx )
        
        self.t = np.zeros(( self.steps ))
        self.x = np.zeros(( self.steps , self.pset.dim ))
        
        self.xn = np.zeros(( self.steps , self.pset.dim ))
                
        spring = ls.LinearSpring( self.pset.size , self.pset.dim , Consts=1.0 )
        
        spring.set_masses( self.pset.M )
               
        self.odes = dict()
        
        self.odes["Euler      "] = els.EulerSolverConstrained( spring , self.pset , dt , costrs )
        self.odes["Runge Kutta"] = rks.RungeKuttaSolverConstrained( spring , self.pset , dt , costrs )
        self.odes["Leap Frog  "] = lps.LeapfrogSolverConstrained( spring , self.pset , dt , costrs )
        self.odes["MidPoint   "] = mps.MidpointSolverConstrained( spring , self.pset , dt , costrs )
        self.odes["Verlet     "] = svs.StormerVerletSolverConstrained( spring , self.pset , dt , costrs )


class TestAnimationDampedHarmonic( TestAnimation ):
    """
    Test the damped harmonic motion with two particles.
    """
    
    def __init__(self):
        self.analytical_sol = damp_harmonic

    def init_pset(self):
        self.pset.X[0,:] = 0.0
        self.pset.X[1,:] = 1.0 / np.sqrt(3)
        self.pset.M[:] = 1.0
        self.pset.V[:] = 0.0
        
    def build_animation(self):
        
        self.steps = 6000
        dt = 0.004
        
        self.ip = 1
        
        self.pset = ps.ParticlesSet( 2 , 3 )
        self.pset.M[:] = 1.0
        self.pset.V[:] = 0.0
        
        self.pset.X[0,:] = 0.0
        self.pset.X[1,:] = 1.0 / np.sqrt(3)
        
        ci = np.array( [ 0 ] )
        cx = np.array( [ 0.0 , 0.0 , 0.0 ] )
        
        costrs = csx.ConstrainedX( self.pset )
        costrs.add_x_constraint( ci , cx )
        
        self.t = np.zeros(( self.steps ))
        self.x = np.zeros(( self.steps , self.pset.dim ))
        
        self.xn = np.zeros(( self.steps , self.pset.dim ))
                
        spring = ls.LinearSpring( self.pset.size , self.pset.dim , Consts=1.0 )
        damp = da.Damping( self.pset.size , self.pset.dim , Consts=0.5 )
        
        multi = mf.MultipleForce( self.pset.size )
        
        multi.append_force( spring )
        multi.append_force( damp )
        
        multi.set_masses( self.pset.M )
               
        self.odes = dict()
        
        self.odes["Euler      "] = els.EulerSolverConstrained( multi , self.pset , dt , costrs )
        self.odes["Runge Kutta"] = rks.RungeKuttaSolverConstrained( multi , self.pset , dt , costrs )
        self.odes["Leap Frog  "] = lps.LeapfrogSolverConstrained( multi , self.pset , dt , costrs )
        self.odes["MidPoint   "] = mps.MidpointSolverConstrained( multi , self.pset , dt , costrs )
        self.odes["Verlet     "] = svs.StormerVerletSolverConstrained( multi , self.pset , dt , costrs )
