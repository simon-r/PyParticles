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

import pyparticles.forces.gravity as gr

import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.stormer_verlet_solver as svs
import pyparticles.ode.midpoint_solver as mds

import pyparticles.measures.kinetic_energy as ke
import pyparticles.measures.total_energy as te

import pyparticles.animation.animated_ogl as aogl


def solar_system():
    """
    Solar system demo
    """
    dt = 3.0*3600.0
    steps = 1000000
    
    G = 6.67384e-11
    
    FLOOR = -10
    CEILING = 10
    
    pset = ps.ParticlesSet( 12 , 3 , label=True )
    
    pset.label[0] = "Sun"
    pset.label[1] = "Earth"
    pset.label[2] = "Jupiter"
    pset.label[3] = "Mars"
    pset.label[4] = "Mercury"
    pset.label[5] = "Neptune"
    pset.label[6] = "Pluto"
    pset.label[7] = "Saturn"
    pset.label[8] = "Uranus"
    pset.label[9] = "Venus"
    pset.label[10] = "Ceres"
    pset.label[11] = "Moon"
    
    
    # Coordinates
    pset.X[:] = np.array(  [
                            [  0.00000000e+00 ,  0.00000000e+00  , 0.00000000e+00],    # Sun
                            [  1.49597871e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Earth
                            [  7.78357721e+11 ,  0.00000000e+00 ,  0.00000000e+00],    # Jupiter
                            [  2.27987155e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Mars
                            [  5.83431696e+10 ,  0.00000000e+00  , 0.00000000e+00],    # Mercury
                            [  4.49691199e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Neptune
                            [  5.91360383e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Pluto
                            [  1.42701409e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Saturn
                            [  2.86928716e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Uranus
                            [  1.04718509e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Venus
                            [  4.138325875e+11,  0.00000000e+00  , 0.00000000e+00],    # Ceres
                            [  1.499604410e+11,  0.00000000e+00  , 0.00000000e+00]     # Moon
                            ]) 
    
    
    # Mass
    pset.M[:] = np.array(  [
                            [  1.98910000e+30] ,
                            [  5.98000000e+24] ,
                            [  1.90000000e+27] ,
                            [  6.42000000e+23] ,
                            [  3.30000000e+23] ,
                            [  1.02000000e+26] ,
                            [  1.29000000e+22] ,
                            [  5.69000000e+26] ,
                            [  8.68000000e+25] ,
                            [  4.87000000e+24] ,
                            [  9.43000000e+20] ,
                            [  7.34770000e+22]
                            ] )

    # Speed
    pset.V[:] = np.array( [ [ 0. ,   0.    ,    0.] ,
                            [ 0. , 29800.  ,    0.] ,
                            [ 0. , 13100.  ,    0.] ,
                            [ 0. , 24100.  ,    0.] ,
                            [ 0. , 47900.  ,    0.] ,
                            [ 0. ,  5400.  ,    0.] ,
                            [ 0. ,  4700.  ,    0.] ,
                            [ 0. ,  9600.  ,    0.] ,
                            [ 0. ,  6800.  ,    0.] ,
                            [ 0. , 35000.  ,    0.] ,
                            [ 0  , 17882.  ,    0.] ,
                            [ 0  , 30822.  ,    0.] 
                            ] )

    # Inclination
    incl = np.array([ 0.0 ,
                      0.0 ,
                      1.305 ,
                      1.850 ,
                      7.005 ,
                      1.767975,
                      17.151 ,
                      2.485 ,
                      0.772 ,
                      3.394 ,
                      10.587 ,
                      0.0 ,
                      ])
    
    # Longitude of the ascending node
    lan = np.array([ 0.0 ,
                     348.73936 ,
                     100.492 ,
                     49.562 ,
                     48.331 ,
                     131.794310 ,
                     110.286 ,
                     113.642 ,
                     73.989 ,
                     76.678 ,
                     80.3932 ,
                     348.73936 
                    ])



    incl[:] = incl * 2.0*np.pi / 360.0
    
    lan[:]  = lan * 2.0*np.pi / 360.0
    
    pset.V[:,2] = np.sin( incl ) * pset.V[:,1]
    pset.V[:,1] = np.cos( incl ) * pset.V[:,1]
    
    for i in range ( pset.V.shape[0] ) :
        x = pset.V[i,0]
        y = pset.V[i,1]
        
        pset.V[i,0] = x * np.cos( lan[i] ) - y * np.sin( lan[i] )
        pset.V[i,1] = x * np.sin( lan[i] ) + y * np.cos( lan[i] )
        

    for i in range ( pset.X.shape[0] ) :
        x = pset.X[i,0]
        y = pset.X[i,1]
        
        pset.X[i,0] = x * np.cos( lan[i] ) - y * np.sin( lan[i] )
        pset.X[i,1] = x * np.sin( lan[i] ) + y * np.cos( lan[i] )

    
    #outf = fc.FileCluster()
    #outf.open( "solar_system.csv" , "wb" )
    #outf.write_out( pset )
    
        
    pset.unit = 149597870700.0
    pset.mass_unit = 5.9736e24
    
    grav = gr.Gravity( pset.size , Consts=G )
    
    grav.set_masses( pset.M )
    
    
    bound = None
    
    pset.set_boundary( bound )
    
    pset.enable_log( True , log_max_size=1000 )
    
    grav.update_force( pset )
    
    #solver = els.EulerSolver( grav , pset , dt )
    #solver = lps.LeapfrogSolver( grav , pset , dt )
    #solver = svs.StormerVerletSolver( grav , pset , dt )
    solver = rks.RungeKuttaSolver( grav , pset , dt )    
    #solver = mds.MidpointSolver( grav , pset , dt )    
        
        
    ken = ke.KineticEnergy( pset , grav )
    ken.set_str_format( "%e" )
    
    #
    ken.update_measure()
    
    a = aogl.AnimatedGl()
   # a = anim.AnimatedScatter()
   
    a.trajectory = True
    a.trajectory_step = 1
        
    
    a.xlim = ( FLOOR , CEILING )
    a.ylim = ( FLOOR , CEILING )
    a.zlim = ( FLOOR , CEILING )
    
    a.ode_solver = solver
    a.pset = pset
    a.steps = steps
    
    a.add_measure( ken )

    
    a.build_animation()
    
    a.start()
    
    return 
