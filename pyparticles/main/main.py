
# PyParticles : Particles simulation in python
# Copyright (C) 2012  Simone Riva : simone.rva {at} gmail {dot} com
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



import pyparticles.pset.particles_set as ps
import pyparticles.animation.animated_scatter as anim

import pyparticles.animation as pan

import pyparticles.pset.rand_cluster as clu
import pyparticles.forces.gravity as gr
import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.stormer_verlet_solver as svs

import matplotlib.animation as animation

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pyparticles.pset.periodic_boundary as pb
import pyparticles.pset.rebound_boundary as rb
import pyparticles.forces.const_force as cf
import pyparticles.forces.vector_field_force as vf
import pyparticles.forces.linear_spring as ls
import pyparticles.pset.file_cluster as fc

import pyparticles.demo.solar_system as sol
import pyparticles.demo.springs as spr
import pyparticles.demo.gas_lennard_jones as lj

import pyparticles.utils.parse_args as arg 

import pyparticles.utils.problem_config as pc
import pyparticles.pset.octree as ot

import time 



import sys

if sys.version_info[0] == 2:
    import pyparticles.animation.animated_ogl as aogl


def main():
    
    #my_test()
    
    np.seterr(all='ignore')
    
    options = arg.parse_args()
    
    cfg = pc.ParticlesConfig()
    
    if options.config_model :
        file_name = "example_pyparticles_config.cfg"
        cfg.write_example_config_file("example_pyparticles_config.cfg")
        print( "A file named: %s has been written in the current directory" % file_name )
        print( "" )
        return     
    
    
    if options.demo == "springs" :
        print("")
        print("Start the simulation example:")
        print(" 3 body springs")
        spr.springs()
        return     
    
    if options.demo == "gas_lj" :
        print("")
        print("Start the simulation example:")
        print(" Pseudo gas with Lennard Jones potential")
        lj.gas_lj()
        return    
    
    if options.path_name == None or options.demo == "solar_system":
        
        print("")
        print("Start the simulation example:")
        print(" Solar system")
        print(" -- Try to watch the Moon ... around the Earth ")
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
    
    print("Ops ... ")
    return 









    
    ##################################
    ##################################
    ##################################    
    #### Old test code .....and tests .... 
   
    
class MyField( vf.VectorFieldForce ):
    def __init__(self,size,dim):
        super(MyField,self).__init__(size)
        self.v = np.zeros((dim,size))
    
    def vect_fun( self , X ):
        self.v[:] = ( X**2 ).T
        return ( self.v * -X.T/np.sqrt( np.sum(self.v,0) ) ).T



def my_test() :
    
    
    
    
    
    n = 10
    dt = 0.005
    #dt = 0.0023453
    
    steps = 1000000
    
    G = 0.001
    #G = 6.67384e-11
    
    FLOOR = -10
    CEILING = 10
    


    #ff = fc.FileCluster()
    #ff.open( options.path_name )
    
    pset = ps.ParticlesSet( n , label=True )
    
    pset.label[8] = "tttt"
    pset.label[9] = "tzzzttt"
    
    pset.add_property_by_name("ciao",dim=1 , model="list")
    
    pset.get_by_name("ciao")[3] = 100
    pset.get_by_name("X")[3,:] = 101
    
    sz = 50
    pset.resize( sz )
    
    tree = ot.OcTree()
    
    pset.get_by_name("X")[:] = np.random.rand(sz,3)
    pset.get_by_name("M")[:] = 1.0
    
    pset.update_centre_of_mass()
    
    print(" C O M pset")
    print( pset.centre_of_mass() )
    print("")
    
    tree.set_global_boundary()
    
    a = time.time()
    tree.build_tree( pset )
    b = time.time()
    
    print( "Tot time: % f" %(b-a) )
    
    print(" C O M")
    print( tree.centre_of_mass )
    print("")
    
    #tree.print_tree()
    
    
    #print( pset.get_by_name( "ciao" ) )
    #print( pset.get_by_name( "X" ) )
    #print("")
    #print( pset.X )
    #print( pset.label )
    
    
    exit()
    return
    
    
    
    #ff.insert3( pset )
    #ff.close()  
        
    #pset.unit = 149597870700.0
    #pset.mass_unit = 5.9736e24
    
    
    cs = clu.RandCluster()
    
    cs.insert3( pset.X , M=pset.M , V=pset.V ,
                n = n/2 , centre=(-1.5,1,0.5) , mass_rng=(0.5,5.0) ,
                vel_rng=(0,0) , vel_mdl="bomb" )
    
    cs.insert3( pset.X , M=pset.M , V=pset.V ,
                start_indx=int(n/2) , n = int(n/2) , centre=(1.5,-0.5,0.5) ,
                vel_rng=(0.2,0.4) , vel_mdl="const" , vel_dir=[-1.0,0.0,0.0] )
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
