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

import pyparticles.animation.animated_scatter as anim

import pyparticles.pset.particles_set as ps

import pyparticles.animation as pan

import pyparticles.pset.rand_cluster as clu
import pyparticles.forces.gravity as gr
import pyparticles.ode.euler_solver as els
import pyparticles.ode.leapfrog_solver as lps
import pyparticles.ode.runge_kutta_solver as rks
import pyparticles.ode.stormer_verlet_solver as svs

import pyparticles.ode.midpoint_solver as mds

import numpy as np
import pyparticles.pset.periodic_boundary as pb
import pyparticles.pset.rebound_boundary as rb
import pyparticles.forces.const_force as cf
import pyparticles.forces.vector_field_force as vf
import pyparticles.forces.linear_spring as ls
import pyparticles.pset.file_cluster as fc

import re
import sys

if sys.version_info[0] == 2:
    import ConfigParser
else:
    import configparser as ConfigParser
    

import pyparticles.animation.animated_ogl as aogl


"""

Config file
===========

Config file description:
    
Section: pset_origin
--------------------

    **Define the origin of the particles data set.**

    **Varibles**

           ==========================        ========================
           Variable                          Description
           ==========================        ========================
           media_origin = [file|rand]        Where data the is stored
           file_name = <file>                the dataset file name
           ==========================        ========================
    
Section: set_config
-------------------
    **Particles data set configauration**

    **Varibles:**

           ===========================          ==============================================
           Variable                             Description
           ===========================          ==============================================
           len_unit  = <number>                 How many meters is a unit
           mass_unit = <number>                 How many Kg is a unit
           boundary  = [open|periodic|rebound]  The boundary model used in the simulation
           boundary_lim = <#> <#>               Define the size of the boundary
           sim_log = <number>                   The size of the log queue (0 disable the log)
           sim_log_X = [True|False]             If sim_log is enabled log the position
           sim_log_V = [True|False]             If sim_log is enabled log the velocities
           rand_part_nr = <number>              The total number of particles for a rand set
           ===========================          ==============================================

           Note: len_unit & mass_unit are used only for drawing the particles
    
Section: model
--------------
    **Simulation method and force model**

    **Varibles:**

           ==============================================================      =====================================
           Variable                                                            Description
           ==============================================================      =====================================
           force = [gravity|linear_spring|constant_force]                      Force type used
           ode_solver_name = [euler|runge_kutta|leap_frog|midpoint]            Integration method
           time_step = <number>                                                time step used for the integration
           force_const = <number>                                              Force constant, like G
           force_vector= <number>                                              Force vector, for the constant force
           ==============================================================      =====================================

    
Section: animation
------------------
    **Simulation control & graphic wiew**

    **Variables:**

           ==============================================================      =================================================
           Variable                                                            Description
           ==============================================================      =================================================
           animation_type = [opengl|matplotlib]                                Setup the output interface
           draw_log = [True|False]                                             Draw the simulation log (if enabled)
           xlim = <number> <number>                                            define the limit of the picture (sometime unused)
           ylim = <number> <number> 
           zlim = <number> <number>
           ==============================================================      =================================================

    
Example:
--------
    ::

        [pset_origin]
        media_origin = from_file
        file_name = solar_sys.csv
        
        [set_config]
        len_unit = 149597870700.0
        mass_unit = 5.9736e24
        boundary = open
        
        [model]
        force = gravity
        ode_solver_name = euler
        time_step = 3600
        steps = 1000000
        force_const = 6.67384e-11
        force_vector = 0 0 0
        
        [animation]
        animation_type = opengl
        xlim = -5.0  5.0
        ylim = -5.0  5.0
        zlim = -5.0  5.0 

"""


#ConfigParser.ConfigParser.add_comment = lambda self, section, option, value: self.set(section, '# '+option, value)




class ParticlesConfig(object):

    """
    Parse the config files used for generating the problems:
    """
    def __init__(self):
        
        self.file_name = ""
        
        
        self.default = {
            # section pset_origin
            'media_origin': 'from_file' ,
            'file_name': 'solar_sys.csv' ,
            
            # section set_config
            'len_unit': '149597870700.0' ,
            'mass_unit': '5.9736e24' ,
            'boundary': 'open' ,
            'boundary_lim': '-7 7' ,
            'sim_log': '0' ,
            'sim_log_X': 'True' ,
            'sim_log_V': 'False' ,
            'rand_part_nr': '500' ,
            
            # section model
            'force': 'gravity' ,
            'ode_solver_name': 'euler' ,
            'time_step': '3600' ,
            'steps': '1000000' ,
            'force_const': '6.67384e-11' ,
            'force_vector': '0 0 0' ,
            
            # section animation
            'animation_type': 'opengl' ,
            'draw_trajectory': 'False' ,
            'trajectory_step': '15' ,
            'xlim': '-5.0  5.0' ,
            'ylim': '-5.0  5.0' ,
            'zlim': '-5.0  5.0' ,
            
            # section rand_cluster_* 
            'rc_part_nr': '100' ,
            'rc_centre': '0 0 0' ,
            'rc_radius': '1.0' ,
            'rc_mass_rng': '0.5 1.5' ,
            'rc_vel_rng': '0.5 1.0' ,
            'rc_vel_mdl': 'no' ,
            'rc_vel_dir': '0 1 0' ,
            'rc_r_min': '0.0' ,
            }
    
    def write_example_config_file( self , file_name='example_pyparticles_config.cfg' ):
        """ Write a generic config file """
        config = ConfigParser.ConfigParser()
    
        config.add_section('pset_origin')
        config.set('pset_origin', 'media_origin', 'from_file')
        config.set('pset_origin', 'file_name', 'solar_sys.csv')
    
        config.add_section('set_config')
        config.set('set_config', 'len_unit', '149597870700.0')
        config.set('set_config', 'mass_unit', '5.9736e24')
        config.set('set_config', 'boundary', 'open')
        config.set('set_config', 'boundary_lim', '-7 7')
        config.set('set_config', 'sim_log', '0')
        config.set('set_config', 'sim_log_X', 'True')
        config.set('set_config', 'sim_log_V', 'False')
        config.set('set_config', 'rand_part_nr', '500')
        
        config.add_section('model')
        config.set('model', 'force', 'gravity')
        config.set('model', 'ode_solver_name', 'euler')
        config.set('model', 'time_step', '3600')
        config.set('model', 'steps', '1000000')
        config.set('model', 'force_const', '6.67384e-11')
        config.set('model' , 'force_vector' , '0 0 0' )    
        
    
        config.add_section('animation')
        config.set('animation', 'animation_type', 'opengl')
        config.set('animation', 'draw_trajectory', 'False')
        config.set('animation', 'trajectory_step', '15')
        config.set('animation', 'xlim', '-5.0  5.0')
        config.set('animation', 'ylim', '-5.0  5.0')
        config.set('animation', 'zlim', '-5.0  5.0')
    
        config.add_section('rand_cluster_any')
        config.set('rand_cluster_any', 'rc_part_nr', '100')
        config.set('rand_cluster_any', 'rc_centre', '0 0 0')
        config.set('rand_cluster_any', 'rc_radius', '1.0')
        config.set('rand_cluster_any', 'rc_mass_rng', '0.5  1.0')
        config.set('rand_cluster_any', 'rc_vel_rng', '0.5 1.0')
        config.set('rand_cluster_any', 'rc_vel_mdl', 'bomb')
        config.set('rand_cluster_any', 'rc_vel_dir', '0 1 0')
        config.set('rand_cluster_any', 'rc_r_min', '0.0')
    
        # Writing our configuration file to 'example.cfg'
        with open( file_name , 'wb' ) as configfile:
            config.write(configfile)
        
        
    ###################################################################
    ## read and parse config file
    ###################################################################
    def read_config( self , file_name ):
        """
        Read the configuration file
        """
        
        self.file_name = file_name
        
        config = ConfigParser.ConfigParser(self.default)
        
        fp = None
        
        try :
            fp = open( file_name )
        except IOError:
            print(" Error - config file not fount: %s " % file_name )
            exit()
        
        config.readfp( fp )
        
        #########################################################
        ## Section pset_origin
        self.media_origin = config.get( 'pset_origin' , 'media_origin' ) 
        self.pset_file_name = config.get( 'pset_origin' , 'file_name' )
        
        #########################################################
        ## Section set_config
        self.len_unit    = config.getfloat( 'set_config' , 'len_unit' )
        self.mass_unit   = config.getfloat( 'set_config' , 'mass_unit' )
        self.boudary     = config.get( 'set_config' , 'boundary' )
        self.boudary_lim = config.get( 'set_config' , 'boundary_lim' )
        self.sim_log     = config.getint( 'set_config' , 'sim_log' )
        self.sim_log_X   = config.getboolean( 'set_config' , 'sim_log_X' )
        self.sim_log_V   = config.getboolean( 'set_config' , 'sim_log_V' )
        self.rand_part_nr= config.getint( 'set_config' , 'rand_part_nr' )
        
        #########################################################
        ## Section model
        self.force_name      = config.get( 'model' , 'force' )
        self.ode_solver_name = config.get( 'model' , 'ode_solver_name' )
        self.time_step       = config.getfloat( 'model' , 'time_step' )
        self.steps           = config.getint( 'model' , 'steps' )
        self.force_const     = config.get( 'model' , 'force_const' )
        
        if self.force_name == "constant_force" :
            self.force_vector = config.get( 'model' , 'force_vector' , '-1 0 0' )
        
        ###################################################################
        ## Section animation
        self.animation_type  = config.get( 'animation' , 'animation_type' )
        self.draw_trajectory = config.getboolean( 'animation' , 'draw_trajectory' )
        self.trajectory_step = config.getint( 'animation' , 'trajectory_step' )
        
    def build_problem( self ):
        """
        Build the main problem and return the four main objects:
            return ( self.animation , self.pset , self.force , self.ode_solver )
        """
        self.get_particle_set()
        self.get_force()
        self.get_ode_solver()
        self.get_animation()
        
        return ( self.animation , self.pset , self.force , self.ode_solver )
    
    ################################################################################
    def get_particle_set( self ):
        """
        Build and return a set of particles (class: particles_set)
        """
        
        print("")
        
        self.pset = ps.ParticlesSet()
        
        if self.media_origin == "from_file" :
            ff = fc.FileCluster()
            ff.open( self.pset_file_name )
            ff.insert3( self.pset )
            ff.close()
            print( " setup - particles set - file name: %s " % self.pset_file_name )
            
        elif self.media_origin == "rand" :
            self.pset.realloc( self.rand_part_nr , dim=3 )
            self.__get_rand_clusters()
        else:
            print("  !! Error - particles set - media origin: %s don't exist  " % self.media_origin )
            
        
        print( " setup - particles set - size:      %d " % self.pset.size )
        print( " setup - particles set - dim:       %d " % self.pset.dim )
        
        self.pset.unit = self.len_unit
        self.pset.mass_unit = self.mass_unit
        
        print( " setup - particles set - len  unit:      %e " % self.pset.unit )
        print( " setup - particles set - len  mass unit: %e " % self.pset.mass_unit )
        
        
        
        if self.boudary == "open" :
            self.pset.boundary = None
            print( " setup - particles set - Boundary: open " )
            
        elif self.boudary == "periodic" :
            bound = read_str_list( self.boudary_lim )
            self.pset.boundary = pb.PeriodicBoundary( bound=bound , dim=self.pset.dim )
            print( " setup - particles set - Boundary: periodic " )
            print( " setup - particles set - Boundary size : %s " % (bound,) )
            
        elif self.boudary == "rebound" :
            bound = read_str_list( self.boudary_lim )
            self.pset.boundary = rb.ReboundBoundary( bound=bound , dim=self.pset.dim )
            print( " setup - particles set - Boundary: rebound " )
            print( " setup - particles set - Boundary size : %s " % (bound,) )
            
        if self.sim_log > 0 :
            self.pset.enable_log( log_X=self.sim_log_X , log_V=self.sim_log_V , log_max_size=self.sim_log )
            
            print( " setup - particles set - Simulation log size %d " %  self.sim_log  )
            print( " setup - particles set - Simulation log : X = %r  ;  V = %r " % ( self.sim_log_X , self.sim_log_V )  )
        
        #print( self.pset.X )
        #print( self.pset.M )
        #print( self.pset.V )
        
        return self.pset
    
    ################################################################################
    def get_force(self):
        """
        Build and return an object for mdeling the force (derived form the abstract class force)
        """
        print("")
        
        self.force = None
        
        if self.force_name == "gravity" :
            self.force = gr.Gravity( self.pset.size , self.pset.dim , Consts=float(self.force_const) )
            
            print( " setup - force - Type:  Gravity " )
            print( " setup - force - G:     %e " % float(self.force_const) )
            
        elif self.force_name == "linear_spring" :
            self.force = ls.LinearSpring( self.pset.size , self.pset.dim , Consts=self.force_const )
            
            print( " setup - force - Type:  Linear spring " )
            print( " setup - force - K:     %e " % float(self.force_const) )
            
        elif self.force_name == "constant_force" :
            fv = read_str_list( self.force_vector )
            
            self.force = cf.ConstForce( self.pset.size , dim=self.pset.dim , u_force=fv )
            
            print( " setup - force - Type:  Constant " )
            print( " setup - force - Vect:  %e  %e  %e " % ( float(fv[0]) , float(fv[1]) , float(fv[2]) )  )
        
        self.force.set_masses( self.pset.M )
        
        return self.force
    
    ################################################################################
    def get_ode_solver(self):
        """
        Build and return an object for solving the Newton Law of motion (derived form the abstract class ode_solver)
        """
        print("")
        
        self.ode_solver = None
        
        if self.ode_solver_name == "euler" :
            self.ode_solver = els.EulerSolver( self.force , self.pset , self.time_step )
            
            print( " setup - Integration method:  EULER "  )
               
        elif self.ode_solver_name == "runge_kutta" :
            self.ode_solver = rks.RungeKuttaSolver( self.force , self.pset , self.time_step )
            
            print( " setup - Integration method:  Runge Kutta "  )
            
        elif self.ode_solver_name == "leap_frog" :
            self.ode_solver = lps.LeapfrogSolver( self.force , self.pset , self.time_step )            
            
            print( " setup - Integration method:  Leap Frog "  )
        
        elif self.ode_solver_name == "stormer_verlet" :
            self.ode_solver = svs.StormerVerletSolver( self.force , self.pset , self.time_step )
        
            print( " setup - Integration method:  Stormer Verlet " )
            
        elif self.ode_solver_name == "midpoint" :
            self.ode_solver = mds.MidpointSolver( self.force , self.pset , self.time_step )
        
            print( " setup - Integration method:  Midpoint " )
        
        print( " setup - Integration method - time step: %e " %  self.time_step )   
        return self.ode_solver
    
    ################################################################################
    def get_animation(self):
        """
        Build an Animation object and return the reference to the object
        """
        print("")
        
        self.animation = None
        
        if self.animation_type == "opengl" :
            self.animation = aogl.AnimatedGl()
            
            print(" setup - animation - type: OpenGL")

            
        elif self.animation_type == "matplotlib" :
            self.animation = anim.AnimatedScatter()
            
            print(" setup - animation - type: MatPlotlib")
            
        if self.draw_trajectory == True :
            self.animation.trajectory = self.draw_trajectory
            self.animation.trajectory_step = self.trajectory_step
            
            print(" setup - animation - Draw trajectory : %r " % self.draw_trajectory )
            print(" setup - animation - Trajectory step : %d " % self.trajectory_step )
            if self.sim_log == 0 :
                print("  !! Warning - animation - Trajectory will be not drawn: sim_log is disabled  " )
            
        self.animation.ode_solver = self.ode_solver
        self.animation.pset       = self.pset
        self.animation.steps      = self.steps
        
            
        return self.animation
    
    ################################################################################
    def __get_rand_clusters(self):
        

            # 'rc_part_nr': '100' ,
            # 'rc_centre': '0 0 0' ,
            # 'rc_radius': '1.0' ,
            # 'rc_mass_rng': '0.5 1.5' ,
            # 'rc_vel_rng': '0.5 1.0' ,
            # 'rc_vel_mdl': 'const' ,
            # 'rc_vel_dir': '0 1 0' ,
        
        config = ConfigParser.ConfigParser(self.default)
        config.read( self.file_name )
        
        indx = 0
        
        l_sec = config.sections()
        
        for se in l_sec :
            m = re.search( r"(^rand_cluster_\w+)" , se )
            
            if m != None :
                sect = m.group(1)
                print(" setup - rand cluster - name : %s " % sect )
                
                rc_part_nr  = config.getfloat( sect , 'rc_part_nr' )
                print(" setup - rand cluster - size : %d " % rc_part_nr )
                
                rc_centre   = config.get     ( sect , 'rc_centre' )
                rc_centre   = read_str_list  ( rc_centre , to=float )
                print(" setup - rand cluster - centre : %s " % (rc_centre,) )
                
                rc_radius   = config.getfloat( sect , 'rc_radius' )
                print(" setup - rand cluster - radius : %f " % rc_radius )
                
                rc_mass_rng = config.get     ( sect , 'rc_mass_rng' )
                rc_mass_rng = read_str_list  ( rc_mass_rng , to=float )
                print(" setup - rand cluster - mass range : %s " % (rc_mass_rng,) )
                
                rc_vel_rng  = config.get     ( sect , 'rc_vel_rng' )
                rc_vel_rng  = read_str_list  ( rc_vel_rng , to=float )
                print(" setup - rand cluster - velocity range : %s " % (rc_vel_rng,) )
                
                rc_vel_dir  = config.get     ( sect , 'rc_vel_dir' )
                rc_vel_dir  = read_str_list  ( rc_vel_dir , to=float )
                print(" setup - rand cluster - velocity direction : %s " % (rc_vel_dir,) )                
                
                rc_vel_mdl  = config.get     ( sect , 'rc_vel_mdl' )
                print(" setup - rand cluster - velocity model : %s " % (rc_vel_mdl,) )
                
                rc_r_min   = config.getfloat( sect , 'rc_r_min' )
                print(" setup - rand cluster - minimal dist : %f " % rc_r_min )
                
                cs = clu.RandCluster()
                
                if ( indx + rc_part_nr ) > self.pset.size :
                    print(" !! Error the total size of the rand clusters is too big")
                    exit()
                
                cs.insert3( X=self.pset.X ,
                            M=self.pset.M ,
                            V=self.pset.V ,
                            start_indx=indx ,
                            n = int(rc_part_nr) ,
                            centre=rc_centre ,
                            vel_rng=rc_vel_rng ,
                            vel_mdl=rc_vel_mdl ,
                            vel_dir=rc_vel_dir ,
                            r_min=rc_r_min
                            )
                
                indx += rc_part_nr
                print("")
                
        
def read_str_list( string , to=float ):
    
    a = re.split( "\s+" , string )
    c = a.count( "" )
    
    for i in range(c):
        a.remove("")
        
    r = []
    for i in a :
        r.append( to(i) )
    
    return tuple(r)
        
        
        
        
        
        
        
        
        
