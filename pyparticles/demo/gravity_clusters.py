# PyParticles : Particles simulation in python
# Copyright (C) 2012  Simone Riva mail:  simone {dot} rva {at} gmail {dot} com
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

import pyparticles.pset.rand_cluster as clu
import pyparticles.forces.gravity as gr

import pyparticles.ode.euler_solver as els

import pyparticles.pset.particles_set as ps
import pyparticles.pset.opencl_context as occ 

import pyparticles.animation.animated_ogl as aogl

from pyparticles.utils.pypart_global import test_pyopencl

import numpy as np

def gravity_cluster():
    
    if not test_pyopencl() :
        print("")
        print("Attention !!! ")
        print(" This demo works only with PyOpenCL: \n  http://mathema.tician.de/software/pyopencl \n  http://www.khronos.org/opencl/ \n ")
        print(" Please install the package: python-pyopencl for continuing")
        print("")
        return 
        
    
    G = 0.000001
    steps = 100000000
    
    n = 3000
    dt = 0.04
    
    pset = ps.ParticlesSet( n , dtype=np.float32 ) 
        
    cs = clu.RandGalaxyCluster()
    
    print("Building initial galaxy .... ")
    cs.insert3( pset.X, M=pset.M, V=pset.V , G=G )
    
    try :
        occx = occ.OpenCLcontext(  pset.size , pset.dim , (occ.OCLC_X|occ.OCLC_V|occ.OCLC_A|occ.OCLC_M) )
    except :
        print("")
        print("ERROR !!! ")
        print(" Please verify your opencl installation ")
        print(" Probably you must install your GPU OpenCL drivers")
        print("")
        return 
    
    grav = gr.GravityOCL( pset.size , Consts=G , ocl_context=occx  )
    grav.set_masses( pset.M )
    
    grav.update_force( pset )
    
    solver = els.EulerSolverOCL( grav , pset , dt , ocl_context=occx )
    
    a = aogl.AnimatedGl()
        
    a.draw_particles.set_draw_model( a.draw_particles.DRAW_MODEL_VECTOR )
        
    a.ode_solver = solver
    a.pset = pset
    a.steps = steps
    
    a.build_animation()
    
    a.start()
    
    return    
