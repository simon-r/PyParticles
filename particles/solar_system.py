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

import matplotlib.animation as animation



from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import particles.animated_scatter as anim

import particles.particles_set as ps

import particles.animation as pan

import particles.rand_cluster as clu
import particles.gravity as gr
import particles.euler_solver as els
import particles.leapfrog_solver as lps
import particles.runge_kutta_solver as rks
import particles.stormer_verlet_solver as svs
import particles.midpoint_solver as mds

import numpy as np
import particles.periodic_boundary as pb
import particles.rebound_boundary as rb
import particles.const_force as cf
import particles.vector_field_force as vf
import particles.linear_spring as ls
import particles.file_cluster as fc


import particles.parse_args as arg 

import particles.problem_config as pc 

import sys

if sys.version_info[0] == 2:
    import particles.animated_ogl as aogl


def solar_system():
        
    dt = 10*3600
    steps = 1000000
    
    G = 6.67384e-11
    
    FLOOR = -10
    CEILING = 10
    
    pset = ps.ParticlesSet( 10 , 3 )
    
    pset.X[:] = np.array(  [[  1.49597871e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Earth
                            [  7.78357721e+11 ,  0.00000000e+00 ,  0.00000000e+00],    # Jupiter
                            [  2.27987155e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Mars
                            [  5.83431696e+10 ,  0.00000000e+00  , 0.00000000e+00],    # Mercury
                            [  4.49691199e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Neptune
                            [  5.91360383e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Pluto
                            [  1.42701409e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Saturn
                            [  2.86928716e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Uranus
                            [  1.04718509e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Venus
                            [  0.00000000e+00 ,  0.00000000e+00  , 0.00000000e+00]] )  # Sun
    
    pset.M[:] = np.array(  [[  5.98000000e+24] ,
                            [  1.90000000e+27] ,
                            [  6.42000000e+23] ,
                            [  3.30000000e+23] ,
                            [  1.02000000e+26] ,
                            [  1.29000000e+22] ,
                            [  5.69000000e+26] ,
                            [  8.68000000e+25] ,
                            [  4.87000000e+24] ,
                            [  1.98910000e+30]] )

    pset.V[:] = np.array( [[  0. , 29800.  ,    0.] ,
                            [ 0. , 13100.  ,    0.] ,
                            [ 0. , 24100.  ,    0.] ,
                            [ 0. , 47900.  ,    0.] ,
                            [ 0. ,  5400.  ,    0.] ,
                            [ 0. ,  4700.  ,    0.] ,
                            [ 0. ,  9600.  ,    0.] ,
                            [ 0. ,  6800.  ,    0.] ,
                            [ 0. , 35000.  ,    0.] ,
                            [ 0. ,     0.  ,    0.]] )

    incl = np.array([ 0.0 ,
                      1.305 ,
                      1.850 ,
                      7.005 ,
                      1.767975,
                      17.151 ,
                      2.485 ,
                      0.772 ,
                      3.394 ,
                      0.0   ])



    incl[:] = incl * 2.0*np.pi / 360.0
    
    pset.V[:,2] = np.sin( incl ) * pset.V[:,1]
    pset.V[:,1] = np.cos( incl ) * pset.V[:,1]
        
    pset.unit = 149597870700.0
    pset.mass_unit = 5.9736e24
    
    grav = gr.Gravity( pset.size , Consts=G )
    
    grav.set_masses( pset.M )
    
    
    bound = None
    
    pset.set_boundary( bound )
    
    pset.enable_log( True , log_max_size=700 )
    
    grav.update_force( pset )
    
    #solver = els.EulerSolver( grav , pset , dt )
    solver = lps.LeapfrogSolver( grav , pset , dt )
    #solver = svs.StormerVerletSolver( grav , pset , dt )
    #solver = rks.RungeKuttaSolver( grav , pset , dt )    
    #solver = mds.MidpointSolver( grav , pset , dt )    
        
    a = aogl.AnimatedGl()
   # a = anim.AnimatedScatter()
        
    
    a.xlim = ( FLOOR , CEILING )
    a.ylim = ( FLOOR , CEILING )
    a.zlim = ( FLOOR , CEILING )
    
    a.ode_solver = solver
    a.pset = pset
    a.steps = steps
    
    a.build_animation()
    
    a.start()
    
    return 
