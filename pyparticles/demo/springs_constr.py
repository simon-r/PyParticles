import numpy as np

import pyparticles.pset.particles_set as ps

import pyparticles.forces.linear_spring as ls
import pyparticles.forces.const_force as cf
import pyparticles.forces.multiple_force as mf
import pyparticles.forces.drag as dr

import pyparticles.pset.constrained_x as csx

import pyparticles.pset.rebound_boundary as rb

import pyparticles.measures.elastic_potential_energy as epe
import pyparticles.measures.kinetic_energy as ke
import pyparticles.measures.momentum as mm
import pyparticles.measures.total_energy as te

import pyparticles.animation.animated_ogl as aogl

import pyparticles.ode.euler_solver_constrained as asc


import sys

def spring_constr():
    """
    Constrained springs demo
    """
    
    dt = 0.02
    steps = 1000000
    
    K = 0.5

    pset = ps.ParticlesSet( 5 , 3 )
    
    
    pset.X[:] = np.array(  [
                            [  2.0 ,  4.0  , 1.0 ],    # 1
                            [ -2.0 , -2.0  , -3.0 ],    # 2
                            [  3.0 , -5.0 ,  2.0 ],    # 3
                            [  3.0 ,  5.0 , -2.0 ],    # 3
                            [  0.0 ,  0.0 ,  2.0 ]     # 3
                            ] )

    pset.M[:] = np.array(  [
                            [  1.1 ] ,
                            [  1.9 ] ,
                            [  1.5 ] ,
                            [  1.4 ] ,
                            [  1.8 ]
                            ] )

    pset.V[:] = np.array( [
                            [ 0. , 0. , 0.] ,
                            [ 0. , 0  , 0.] ,
                            [ 0. , 0  , 0.] ,
                            [ 0. , 0  , 0.] ,
                            [ 0. , 0  , 0.]
                            ] )
    
    
    
    ci = np.array( [ 0 , 4 ] )
    
    cx = np.array( [
                    [  4.0 ,  4.0 ,  4.0] ,
                    [ -4.0 , -4.0 , -4.0] 
                    ] )
    
    costrs = csx.ConstrainedX( pset )
    costrs.add_x_constraint( ci , cx )
    
    spring = ls.LinearSpring( pset.size , pset.dim , pset.M , Consts=K )
    
    solver = asc.EulerSolverConstrained( spring , pset , dt , costrs )
    
    a = aogl.AnimatedGl()
    
    pset.enable_log( True , log_max_size=1000 )
    
    a.trajectory = True
    a.trajectory_step = 1
    
    a.ode_solver = solver
    a.pset = pset
    a.steps = steps
    
    a.build_animation()
    
    a.start()
    
    return
