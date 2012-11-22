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

import pyparticles.forces.electrostatic as esf

import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.stormer_verlet_solver as svs
import pyparticles.ode.midpoint_solver as mds

import pyparticles.measures.kinetic_energy as ke
import pyparticles.measures.total_energy as te

import pyparticles.pset.rand_cluster as rc
import pyparticles.pset.rebound_boundary as rb

import pyparticles.animation.animated_ogl as aogl
import pyparticles.ogl.draw_particles_ogl as drp

import sys

def electro():
    """
    Electrostatic demo
    """
    
    steps = 1000000
    dt = 0.01
    
    r_min=1.5
    
    Ke = 8.9875517873681764e9
    qe = 1.60217646e-19 * 1.0e8
    
    me = 9.10938188e-31
    mp = 1.67262158e-18
    
    rand_c = rc.RandCluster()
    
    pset = ps.ParticlesSet( 10 , charge=True )
    
    pset.Q[:5] = qe
    pset.Q[5:10] = -qe
    
    pset.M[:] = 1e-3
    
    pset.V[:] = 0.0
    
    pset.X[:] = 1.0e-3 * np.array( [
                            [ 0.0 , 0.0 , 0.0  ] ,
                            [ 0.0 , 0.0 , 1.0  ] ,
                            [ 0.0 , 0.0 , -1.0  ] ,
                            [ 0.0 , 1.0 , 1.0  ] ,
                            [ -1.0 , -1.0 , -1.0  ] ,
                            [ 2.0 , -2.0 , 4.0  ] ,
                            [ 4.0 , 7.0 , 2.0  ] ,
                            [ -3.0 , -5.0 , 1.0  ] ,
                            [ 4.0 , 4.0 , -7.0  ] ,
                            [ 2.0 , 8.0 , -6.0  ] 
                            ]
                        )
    
    #rand_c.insert3( X=pset.X ,
    #                M=pset.M ,
    #                start_indx=0 ,
    #                n=pset.size ,
    #                radius=5.0 ,
    #                mass_rng=(0.5,0.8) ,
    #                r_min=0.0 )
    
    elecs = esf.Electrostatic( pset.size , dim=3 , Consts=Ke )

    
    elecs.set_masses( pset.M )
    elecs.set_charges( pset.Q )
    
    #solver = els.EulerSolver( multif , pset , dt )
    #solver = lps.LeapfrogSolver( lennard_jones , pset , dt )
    #solver = svs.StormerVerletSolver( multif , pset , dt )
    solver = rks.RungeKuttaSolver( elecs , pset , dt )    
    #solver = mds.MidpointSolver( lennard_jones , pset , dt ) 
    
    bound = rb.ReboundBoundary( bound=( -10.0e-3 , 10.0e-3 ) )
    pset.set_boundary( bound )
    
    pset.unit = 2e-3
    pset.mass_unit = 1e-3
    
    pset.enable_log( True , log_max_size=1000 )
    
    solver.update_force()
    
    a = aogl.AnimatedGl()
    
    a.ode_solver = solver
    
    a.trajectory = True
    
    a.pset = pset
    a.steps = steps
    
    a.draw_particles.color_fun = drp.charged_particles_color
    
    a.build_animation()
        
    a.start()
    
    return