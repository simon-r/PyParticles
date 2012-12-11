
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

import matplotlib.animation as animation

from pyparticles.utils.pypart_global import *

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import pyparticles.pset.particles_set as ps
import pyparticles.pset.logger as log

import pyparticles.animation.animated_scatter as anim

import pyparticles.animation as pan

import pyparticles.animation.test_animation as test

import pyparticles.pset.rand_cluster as clu
import pyparticles.forces.gravity as gr

import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.stormer_verlet_solver as svs

import matplotlib.animation as animation


import pyparticles.pset.periodic_boundary as pb
import pyparticles.pset.rebound_boundary as rb
import pyparticles.forces.const_force as cf
import pyparticles.forces.vector_field_force as vf
import pyparticles.forces.linear_spring as ls
import pyparticles.pset.file_cluster as fc

import pyparticles.demo.solar_system as sol
import pyparticles.demo.springs as spr
import pyparticles.demo.gas_lennard_jones as lj
import pyparticles.demo.bubble as bu
import pyparticles.demo.springs_constr as spc
import pyparticles.demo.test as tst
import pyparticles.demo.electrostatic_demo as eld
import pyparticles.demo.electromagnetic_demo as emd
import pyparticles.demo.fountain as fou
import pyparticles.demo.gravity_clusters as grav

import pyparticles.utils.parse_args as arg 

import pyparticles.utils.problem_config as pc
import pyparticles.pset.octree as ot

from pyparticles.geometry.dist import distance

import pyparticles.pset.constrained_x as ct
import pyparticles.pset.constrained_force_interactions as cfi

import pyparticles.geometry.transformations as tr

import time 

import sys

import pyparticles.animation.animated_ogl as aogl


def main():
    
    #my_test()
    
    np.seterr(all='ignore')

    options = arg.parse_args()
    
    cfg = pc.ParticlesConfig()
    
    if options.version :
        print( py_particle_version() )
        return
    
    if options.about :
        about()
        return
    
    if options.test :
        print("")
        print("Start a test simulation:")
        print(" It compares the simulated solution with the analytical solution in a specific problem")
        tst.test( options.test )
        return
    
    if options.config_model :
        file_name = "example_pyparticles_config.cfg"
        cfg.write_example_config_file("example_pyparticles_config.cfg")
        print( "A file named: %s has been written in the current directory" % file_name )
        print( "" )
        return     
    
    if options.demo == "fountain" :
        print("")
        print("Start the simulation example:")
        print(" 250K Particles fountain")
        fou.fountain()
        return    
    
    if options.demo == "springs" :
        print("")
        print("Start the simulation example:")
        print(" 3 body springs")
        spr.springs()
        return
    
    if options.demo == "cat_spri" :
        print("")
        print("Start the simulation example:")
        print(" catenary springs (constraints demo)")
        spc.spring_constr()
        return
    
    if options.demo == "gas_lj" :
        print("")
        print("Start the simulation example:")
        print(" Pseudo gas with Lennard Jones potential")
        lj.gas_lj()
        return    
    
    if options.demo == "bubble" :
        print("")
        print("Start the simulation example:")
        print(" Pseudo bubble demo")
        bu.bubble()
        return
    
    if options.demo == "el_static" :
        print("")
        print("Start the simulation example:")
        print(" electrostatic")
        eld.electro()
        return  
    
    if options.demo == "elmag_field" :
        print("")
        print("Start the simulation example:")
        print(" electromagnetic fields")
        emd.electromag_field()
        return      
    
    if options.demo == "galaxy" :
        print("")
        print("Start the simulation example:")
        print(" Gravitational clusters")
        grav.gravity_cluster()
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







####################################################################    
####################################################################    
####################################################################        
####################################################################    
####################################################################    
####################################################################        
#### Old test code .....and tests .... 
####################################################################

    
class MyField( vf.VectorFieldForce ):
    def __init__(self,size,dim):
        super(MyField,self).__init__(size)
        self.v = np.zeros((dim,size))
    
    def vect_fun( self , X ):
        self.v[:] = ( X**2 ).T
        return ( self.v * -X.T/np.sqrt( np.sum(self.v,0) ) ).T



def my_test() :
    
    
    pset = ps.ParticlesSet( 10 )
    
    lo = log.Logger( pset , 10 )
    
    for i in range( 105 ) :
        pset.X[:] =  float(i) 
        lo.log()
        
        print( lo.get_particles_log( 3 ) )
    
    exit()
        
    t = tr.Transformations()
    
    t.set_points_tuple_size(1)
        
    t.rotate( np.radians(90) , 1 , 0 , 0 )
    #t.rotX( np.radians(90) )
    
    t.append_point( list( [1,0,0] ) )
    t.append_point( np.array( [1,1,0] ) )
    t.append_point( np.array( [1,1,1] ) )
    t.append_point( np.array( [0,1,1] ) )    
    
    t.push_matrix()
    t.identity()
    t.translation( 10 , 2 , 2 )
    #t.rotate( np.radians(20) , 1 , 1 , 1 )
    
    t.append_point( [1,1,1] )
    t.append_point( np.matrix( [0,1,1] ).T ) 
    
    t.pop_matrix()
    
    t.append_point( np.array( [1,0,0] ) )
    t.append_point( [1,1,0] )
    t.append_point( np.array( [1,1,1] ) )
    t.append_point( [0,1,1] )   
    
    #print( t.transform(pt[0] , pt[1] , pt[2] ) )
    
    print("")
    
    for (p) in t :
        print( p )
    
    exit()
    
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
    
    sz = 15
    pset.resize( sz )
    
    tree = ot.OcTree()
    
    pset.get_by_name("X")[:] = np.random.rand(sz,3)
    pset.get_by_name("M")[:] = 1.0
    
    pset.update_centre_of_mass()
    
    print(" C O M pset")
    print( pset.centre_of_mass() )
    print("")
    
    csrt = ct.ConstrainedX( pset )
    
    cfit = cfi.ConstrainedForceInteractions( pset )
    
    cfit.add_connections( [[12,3],[4,4],[6,8],[1,1]] )
    cfit.remove_connections( [[12,3]] )
    
    print( cfit.dense )
    print( cfit.sparse )
    print( cfit.items )
    
    cc = np.array( [[1,2,3],[3,3,3]] )
    cc = np.array( [[1,2,3],[3,3,5]] )
    
    csrt.add_x_constraint( [2,5] , cc )
    csrt.add_x_constraint( [7,10] , cc )
    
    print( csrt.get_cx_indicies() )
    print( csrt.cX )
    
    csrt.remove_x_constraint( [2,10] )
    
    print( csrt.get_cx_indicies() )
    print( csrt.cX )
    
    exit() 
    
    tree.set_global_boundary()
    
    a = time.time()
    tree.build_tree( pset )
    b = time.time()
    
    print( "Tot time: % f" %(b-a) )
    
    C = np.array([0.5,0.4,0.3])
    R = 0.05
    
    a = time.time()
    for ix in range( pset.size ):
        nl = tree.search_neighbour( pset.X[ix,:] , R )
    b = time.time()
    
    print( "Tot time octree : % f" %(b-a) )
    
    nl = np.sort( nl )
    
    print("")
    print("nl:")
    print( nl )
    
    print("")
    print("dd:")
    
    a = time.time()
    for ix in range( pset.size ):
        dd = np.sqrt(  np.sum( (pset.X[ix,:] - pset.X)**2 , 1 ) ) 
        din, = np.where( dd <= R )
    b = time.time()
    
    print( "Tot time numpy : % f" %(b-a) )
    
    print( din )
    
    print(" C O M")
    print( tree.centre_of_mass )
    print("")
    
    print ( np.all( nl == din ) )
    
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
