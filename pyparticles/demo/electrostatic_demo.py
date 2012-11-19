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

import sys

def electro():
    """
    Pseudo bubble simulation
    """
    
    steps = 1000000
    dt = 0.01
    
    r_min=1.5
    
    Ke = 8.9875517873681764e9
    qe = 1.60217646e-19
    
    me = 9.10938188e-31
    mp = 1.67262158e-18
    
    rand_c = rc.RandCluster()
    
    pset = ps.ParticlesSet( 10 )
    
    pset.Q[:5] = qe
    pset.Q[5:10] = -qe
    
    pset.M[:] = 30.0 * mp
    
    rand_c.insert3( X=pset.X ,
                    M=pset.M ,
                    start_indx=0 ,
                    n=pset.size ,
                    radius=5.0 ,
                    mass_rng=(0.5,0.8) ,
                    r_min=0.0 )
    
    elecs = esf.Electrostatic( pset.size , dim=3 , Consts=Ke )

    
    multif.set_masses( pset.M )
    
    #solver = els.EulerSolver( multif , pset , dt )
    #solver = lps.LeapfrogSolver( lennard_jones , pset , dt )
    #solver = svs.StormerVerletSolver( multif , pset , dt )
    solver = rks.RungeKuttaSolver( lennard_jones , pset , dt )    
    #solver = mds.MidpointSolver( lennard_jones , pset , dt ) 
    
    bound = rb.ReboundBoundary( bound=(-5.0,5.0) )
    
    pset.set_boundary( bound )
    
    a = aogl.AnimatedGl()
    
    a.ode_solver = solver
    a.pset = pset
    a.steps = steps
    
    a.build_animation()
    
    a.start()
    
    return