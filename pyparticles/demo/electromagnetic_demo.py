# PyParticles : Particles simulation in python
# Copyright (C) 2012  Simone Riva mail: simone.rva {at} gmail {dot} com
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
import pyparticles.pset.default_boundary as db

import pyparticles.forces.electromagnetic_field as elmf

import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.stormer_verlet_solver as svs
import pyparticles.ode.midpoint_solver as mds

import pyparticles.animation.animated_ogl as aogl
import pyparticles.ogl.draw_particles_ogl as drp

def electric_field( E , X ):
    E[:] = np.array( [ 10 , 10 , 10 ] )
    

def magnetic_field( B , X ):
    #B[:] = 1000.0 * np.sin( 500.0 * X )
    B[:] = np.array( [ 0 , 0 , 1000 ] )
    

def magf_color( RGBA , X ):
    RGBA[:] = np.array([ 0.4 , 0.4 , 1.0 , 0.6 ])

def elf_color( RGBA , X ):
    RGBA[:] = np.array([ 0.4 , 1.0 , 0.4 , 0.6 ])

def default_pos( pset , indx ):
    pset.X[indx,:] = 0.0
    pset.V[indx,:] = ( ( np.random.rand( len(indx) , 3 ) - 0.5 ) / 3.0 )


def electromag_field():
    """
    Electrimagnetic field demo
    """
    
    steps = 1000000
    size = 25000
    dt = 1e-4
    
    qe = 1.60217646e-19 
    
    me = 9.10938188e-31
    mp = 1.67262158e-18
    
    pset = ps.ParticlesSet( size , charge=True )
    
    pset.X[:] = 10.0e-3 * ( ( 2.0*np.random.rand( size , 3 ) - 1.0 )  )
    
    pset.Q[:] = qe * np.sign( np.random.rand( size , 1 ) - 0.5 )
    
    pset.V[:] = 0.5 * ( ( np.random.rand( size , 3 ) - 0.5 ) / 2.0 )
     
    pset.M[:] = mp
    
    elmag = elmf.ElectromagneticField( pset.size , dim=pset.dim , m=pset.M , q=pset.Q )
    
    elmag.append_electric_field( electric_field )
    elmag.append_magnetic_field( magnetic_field )
    
    #solver = els.EulerSolver( elmag , pset , dt )
    #solver = lps.LeapfrogSolver( elmag , pset , dt )
    #solver = svs.StormerVerletSolver( elmag , pset , dt )
    #solver = rks.RungeKuttaSolver( elmag , pset , dt )    
    solver = mds.MidpointSolver( elmag , pset , dt )
    
    pset.unit = 2e-3
    pset.mass_unit = 1e-3   
    
    bound = db.DefaultBoundary( ( -pset.unit*5.0 , pset.unit*5.0 ) , dim=3 , defualt_pos=default_pos )
    pset.set_boundary(bound)
    
    pset.enable_log( True , log_max_size=200 )
    
    solver.update_force()
    
    a = aogl.AnimatedGl()
    
    a.ode_solver = solver
    
    a.trajectory = False
    
    a.xlim = ( -pset.unit*5.0 , pset.unit*5.0 )
    a.ylim = ( -pset.unit*5.0 , pset.unit*5.0 )
    a.zlim = ( -pset.unit*5.0 , pset.unit*5.0 )
    
    a.add_vector_field_fun( magnetic_field , 2000.0 , pset.unit , color_fun=magf_color )
    a.add_vector_field_fun( electric_field , 50.0 ,  pset.unit , color_fun=elf_color )
    
    a.draw_vector_field = False
    
    a.pset = pset
    a.steps = steps
    
    a.draw_particles.color_fun = drp.charged_particles_color
    
    a.draw_particles.vect_color_fun = drp.charged_particles_vect_color
    
    a.draw_particles.set_draw_model( a.draw_particles.DRAW_MODEL_VECTOR )
    
    a.build_animation()
        
    a.start()
    
    return
    
