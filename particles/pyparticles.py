
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

import matplotlib.animation as animation

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import particles.periodic_boundary as pb
import particles.rebound_boundary as rb
import particles.const_force as cf
import particles.vector_field_force as vf
import particles.linear_spring as ls
import particles.file_cluster as fc

import particles.solar_system as sol

import particles.parse_args as arg 

import particles.problem_config as pc 



import sys

if sys.version_info[0] == 2:
    import particles.animated_ogl as aogl




class MyField( vf.VectorFieldForce ):
    def __init__(self,size,dim):
        super(MyField,self).__init__(size)
        self.v = np.zeros((dim,size))
    
    def vect_fun( self , X ):
        self.v[:] = ( X**2 ).T
        return ( self.v * -X.T/np.sqrt( np.sum(self.v,0) ) ).T


def main():
    
    np.seterr(all='ignore')
    
    options = arg.parse_args()
    
    cfg = pc.ParticlesConfig()
    
    if options.config_model :
        file_name = "example_pyparticles_config.cfg"
        cfg.write_example_config_file("example_pyparticles_config.cfg")
        print( "A file named: %s has been ritten in the current directory" % file_name )
        print( "" )
        return     
    
    
    if options.path_name == None:
        
        print("")
        print("Start the simulation example:")
        print(" Solar system")
        print("")
        print(" Use your mouse for rotating, zooming and tranlating the scene.")
        print("")
        print("For more details type:")
        print(" pyparticles --help")
        print("")
        
        sol.solar_system()
        return 
    

    
    if options.path_name != None :
        
        cfg.read_config( options.path_name )
        ( an , pset , force , ode_solver ) = cfg.build_problem()
        an.build_animation()
        
        print("")
        print("Start the simulation described in: %s ... " % options.path_name )
        
        an.start()
        return 
    
    
    return 
    
    ##################################
    ##################################
    ##################################
    
    #### Old code .....
    
    return
    
    n = 700
    dt = 3600
    #dt = 0.0023453
    
    steps = 1000000
    
    G = 0.001
    G = 6.67384e-11
    
    FLOOR = -10
    CEILING = 10
    


    ff = fc.FileCluster()
    ff.open( options.path_name )
    
    pset = ps.ParticlesSet( n )
    ff.insert3( pset )
    ff.close()  
        
    pset.unit = 149597870700.0
    pset.mass_unit = 5.9736e24
    
    
    cs = clu.RandCluster()
    
    #cs.insert3( pset.X , M=pset.M , V=pset.V ,
    #            n = n/2 , centre=(-1.5,1,0.5) , mass_rng=(0.5,5.0) ,
    #            vel_rng=(0,0) , vel_mdl="bomb" )
    #
    #cs.insert3( pset.X , M=pset.M , V=pset.V ,
    #            start_indx=int(n/2) , n = int(n/2) , centre=(1.5,-0.5,0.5) ,
    #            vel_rng=(0.2,0.4) , vel_mdl="const" , vel_dir=[-1.0,0.0,0.0] )
    #
    
    grav = gr.Gravity( pset.size , Consts=G )
    #grav = cf.ConstForce(n , u_force=[0,0,-1.0] )
    #grav = MyField( pset.size , dim=3 )
    #grav = ls.LinearSpring( pset.size , Consts=10e8 )
    
    grav.set_masses( pset.M )
    
    
    bound = None
    #bound = pb.PeriodicBoundary( (-50.0 , 50.0) )
    #bound = rb.ReboundBoundary(  (-10.0 , 10.0)  )
    
    pset.set_boundary( bound )
    grav.update_force( pset )
    
    solver = els.EulerSolver( grav , pset , dt )
    #solver = lps.LeapfrogSolver( grav , pset , dt )
    #solver = svs.StormerVerletSolver( grav , pset , dt )
    #solver = rks.RungeKuttaSolver( grav , pset , dt )    
        
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
    

if __name__ == '__main__':
    main()
