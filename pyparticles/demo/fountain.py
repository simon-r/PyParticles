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

import pyparticles.pset.opencl_context as occ 

import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.stormer_verlet_solver as svs
import pyparticles.ode.midpoint_solver as mds

import pyparticles.forces.const_force as cf
import pyparticles.forces.drag as dr
import pyparticles.forces.multiple_force as mf

import pyparticles.animation.animated_ogl as aogl

import pyparticles.pset.default_boundary as db

from pyparticles.utils.pypart_global import test_pyopencl

def default_pos( pset , indx ):
    
    t = default_pos.sim_time.time
    
    pset.X[indx,:] = 0.01 * np.random.rand( len(indx) , pset.dim ).astype( pset.dtype )
    
    fs = 1.0 / ( 1.0 + np.exp( -( t*4.0 - 2.0 ) ) ) 
    
    alpha = 2.0 * np.pi * np.random.rand( len(indx) ).astype( pset.dtype ) 
    
    vel_x = 2.0 * fs * np.cos( alpha )
    vel_y = 2.0 * fs * np.sin( alpha )
        
    pset.V[indx,0] = vel_x  
    pset.V[indx,1] = vel_y 
    pset.V[indx,2] = 10.0 * fs + 1.0 * fs * ( np.random.rand( len(indx)) )


def fountain():
    """
    Fountain demo
    """
    steps = 10000000
    dt = 0.005
    pcnt = 100000

    fl = True
    if test_pyopencl() :
        print( "OpenCL is installed and enabled " )
        print( " Try, at least, 200000 particles " )
        
        while fl :
            try :
                print( " " )
                pcnt = int( raw_input('How many particles: ') )
            except :
                print( "Please insert a number! " )
            else :
                fl = False
        
 
    
    pset = ps.ParticlesSet( pcnt , dtype=np.float32 )
    
    pset.M[:] = 0.1
    pset.X[:,2] = 0.7 * np.random.rand( pset.size )
        
    grav = cf.ConstForce( pset.size , dim=pset.dim , u_force=( 0.0 , 0.0 , -10.0 ) )
    
    occx = None
    if test_pyopencl() :
        occx = occ.OpenCLcontext( pset.size , pset.dim , ( occ.OCLC_X | occ.OCLC_V | occ.OCLC_A | occ.OCLC_M ) )
        drag = dr.DragOCL( pset.size , dim=pset.dim , Consts=0.01 , ocl_context=occx )
    else :
        drag = dr.Drag( pset.size , dim=pset.dim , Consts=0.01 )
    
    
    multi = mf.MultipleForce( pset.size , dim=pset.dim )
    
    multi.append_force( grav )
    multi.append_force( drag )
    
    multi.set_masses( pset.M )
    
    #solver = mds.MidpointSolver( multi , pset , dt )
    if test_pyopencl() :
        solver = els.EulerSolverOCL( multi , pset , dt , ocl_context=occx )
    else :
        solver = els.EulerSolver( multi , pset , dt )
    
    
    solver.update_force()
    
    default_pos.sim_time = solver.get_sim_time()
    
    bd = ( -100.0 , 100.0 , -100.0 , 100.0 , 0.0 , 100.0 )
    bound = db.DefaultBoundary( bd , dim=3 , defualt_pos=default_pos )
    
    pset.set_boundary( bound )
    
    a = aogl.AnimatedGl()
    
    a.ode_solver = solver
    a.pset = pset
    a.steps = steps
    
    a.draw_particles.set_draw_model( a.draw_particles.DRAW_MODEL_VECTOR )
    
    a.init_rotation( -80 , [ 0.7 , 0.05 , 0 ]  )
    
    a.build_animation()
    a.start()
    
    return
    
    
