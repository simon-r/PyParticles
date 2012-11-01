import numpy as np

import pyparticles.pset.particles_set as ps

import pyparticles.forces.linear_spring as ls
import pyparticles.forces.linear_spring_constrained as lsc

import pyparticles.forces.const_force as cf
import pyparticles.forces.multiple_force as mf
import pyparticles.forces.drag as dr

import pyparticles.pset.constrained_x as csx
import pyparticles.pset.constrained_force_interactions as cfi

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
    
    dt = 0.03
    steps = 1000000
    
    K = 0.5

    pset = ps.ParticlesSet( 9 , 3 )
    
    
    pset.X[:] = np.array(  [
                            [  4.0 ,  4.0 ,  4.0 ],    # 1
                            [  3.0 ,  3.0 ,  2.0 ],    # 2
                            [  2.0 ,  2.0 ,  4.0 ],    # 2
                            [  1.0 ,  1.0 ,  4.0 ],    # 2
                            [  0.0 ,  0.0 ,  4.0 ],    # 3
                            [ -1.0 , -1.0 ,  4.0 ],    # 2
                            [ -2.0 , -2.0 ,  4.0 ],    # 3
                            [ -3.0 , -3.0 ,  4.0 ],    # 3
                            [ -4.0 , -4.0 ,  4.0 ]     # 3
                            ] )

    pset.M[:] = np.array(  [
                            [  1.0 ] ,
                            [  1.0 ] ,
                            [  1.0 ] ,
                            [  1.0 ] ,
                            [  1.0 ] ,
                            [  1.0 ] ,
                            [  1.0 ] ,
                            [  1.0 ] ,                            
                            [  1.0 ]
                            ] )

    pset.V[:] = np.array( [
                            [ 0. , 0. , 0.] ,
                            [ 0. , 0. , 0.] ,
                            [ 0. , 0. , 0.] ,
                            [ 0. , 0. , 0.] ,
                            [ 0. , 0. , 0.] ,
                            [ 0. , 0. , 0.] ,
                            [ 0. , 0. , 0.] ,
                            [ 0. , 0. , 0.] ,                            
                            [ 0. , 0. , 0.]
                            ] )
    
    
    
    ci = np.array( [ 0 , 8 ] )
    
    cx = np.array( [
                    [  4.0 ,  4.0 ,  4.0] ,
                    [ -4.0 , -4.0 ,  4.0] 
                    ] )
    
    f_conn = np.array( [
                        [ 0 , 1 ] ,
                        [ 1 , 2 ] ,
                        [ 2 , 3 ] ,
                        [ 3 , 4 ] ,
                        [ 4 , 5 ] ,
                        [ 5 , 6 ] ,
                        [ 6 , 7 ] ,
                        [ 7 , 8 ] ,
                     ] )
    
    costrs = csx.ConstrainedX( pset )
    costrs.add_x_constraint( ci , cx )
    
    fi = cfi.ConstrainedForceInteractions( pset )
    
    fi.add_connections( f_conn )
    
    spring = lsc.LinearSpringConstrained( pset.size , pset.dim , pset.M , Consts=K , f_iter=fi )
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
