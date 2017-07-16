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



import numpy as np

import pyparticles.pset.particles_set as ps

import pyparticles.forces.linear_spring_constrained as lsc

import pyparticles.forces.const_force as cf
import pyparticles.forces.multiple_force as mf
import pyparticles.forces.drag as dr
import pyparticles.forces.damping as da

import pyparticles.pset.constrained_x as csx
import pyparticles.pset.constrained_force_interactions as cfi


import pyparticles.measures.elastic_potential_energy as epe
import pyparticles.measures.kinetic_energy as ke
import pyparticles.measures.momentum as mm
import pyparticles.measures.total_energy as te

import pyparticles.animation.animated_ogl as aogl

import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver_constrained as lpc
import pyparticles.ode.stormer_verlet_solver_constrained as svc
import pyparticles.ode.runge_kutta_solver_constrained as rkc
import pyparticles.ode.midpoint_solver_constrained as mdc


def spring_constr():
    """
    Constrained catenary springs demo
    """
    
    dt = 0.01
    steps = 1000000
    
    K = 60

    x = list([])
    m = list([])
    #v = list([])
    
    d = 0.1
    
    ar = np.arange( -4.0 , 4.0+d , d )
    
    for i in ar :
        x.append( list( [i,i,3.0] ) )
        m.append( list([ 1.0 / float( len(ar) ) ] ) )
        #v.append( list([0.0]) )
    
    pset = ps.ParticlesSet( len(ar) , 3 )

    pset.X[:] = np.array( x , np.float64 )
    pset.M[:] = np.array( m , np.float64 )
    pset.V[:] = 0.0
        
        
    pset.X[10:12,2] = 4
    pset.X[15:20,1] = 4
    #pset.X[10:15,1] = 6
        
    ci = np.array( [ 0 , len(ar)-1 ] )
    cx = np.array( [
                    [ -4.0 , -4.0 , 3.0] ,
                    [ 4.0 , 4.0 ,  3.0] 
                    ] )
    
    f_conn = list([])
    for i in range( len(ar) - 1 ):
        f_conn.append( list( [ i , i+1 ] ) )
    
    f_conn = np.array( f_conn , np.float64 )
    
    costrs = csx.ConstrainedX( pset )
    costrs.add_x_constraint( ci , cx )
    
    fi = cfi.ConstrainedForceInteractions( pset )
    
    fi.add_connections( f_conn )
    
    spring = lsc.LinearSpringConstrained( pset.size , pset.dim , pset.M , Consts=K , f_inter=fi )
    constf = cf.ConstForce( pset.size , dim=pset.dim , u_force=[ 0 , 0 , -10 ] )
    drag = dr.Drag( pset.size , pset.dim , Consts=0.003 )
    #damp = da.Damping( pset.size , pset.dim , Consts=0.003 )
    
    multif = mf.MultipleForce( pset.size , pset.dim )
    multif.append_force( spring )
    multif.append_force( constf )
    multif.append_force( drag )
    
    multif.set_masses( pset.M )
    
    solver = els.EulerSolverConstrained( multif , pset , dt , costrs )
    #solver = lpc.LeapfrogSolverConstrained( multif , pset , dt , costrs )
    #solver = svc.StormerVerletSolverConstrained( multif , pset , dt , costrs )
    #solver = rkc.RungeKuttaSolverConstrained( multif , pset , dt , costrs )
    #solver = mdc.MidpointSolverConstrained( multif , pset , dt , costrs )
    
    a = aogl.AnimatedGl()
    
    pset.enable_log( True , log_max_size=1000 )
    
    a.trajectory = False
    a.trajectory_step = 1
    
    a.ode_solver = solver
    a.pset = pset
    a.steps = steps
    
    a.init_rotation( -80 , [ 0.7 , 0.05 , 0 ]  )
    
    a.build_animation()
    
    a.start()
    
    return
