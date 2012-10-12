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


import numpy as np
import particles.periodic_boundary as pb
import particles.rebound_boundary as rb
import particles.const_force as cf
import particles.vector_field_force as vf
import particles.linear_spring as ls
import particles.file_cluster as fc

import re
import ConfigParser
import sys

if sys.version_info[0] == 2:
    import particles.animated_ogl as aogl

    """
    Parse the config files used for generating the problems:
    
    Config file description:
    
    - Section: pset_origin
    -  Define the origin of the particles data set.
    -
    -  Varibles:
    -   media_origin = [file]   Where data the is stored
    -   file_name = <file>      the dataset file name
    [pset_origin]
    media_origin = file
    file_name = solar_sys.csv
    
    - Section: set_config
    -  Particles data set configauration
    -
    -  Varibles:
    -   len_unit  = <number>         - How many meters is a unit,
    -   mass_unit = <number>         - How many Kg is a unit
    -                                Note: len_unit & mass_unit are used only for drawing the particles
    -   boundary  = [open|periodic]  - The boundary model used in the simulation
    [set_config]
    len_unit = 149597870700.0
    mass_unit = 5.9736e24
    boundary = open
    
    - Section: model
    -  Simulation method and force model
    -
    -  Varibles:
    -   force = [gravity|linear_spring|constant_force]                     # Force type used
    -   ode_solver_name = [euler|runge_kutta|leap_frog|constant_force]     # Integration method
    -   time_step = <number>                                               # time step used for the integration
    -   force_const = <number>                                             # Force constant, like G
    -   force_vector= <number>                                             # Force vector, for the constant force
    [model]
    force = gravity
    ode_solver_name = euler
    time_step = 3600
    steps = 1000000
    force_const = 6.67384e-11
    force_vector = 0 0 0
    
    # Section: animation
    #  Simulation control & graphic wiew
    #  Variables:
    #   animation_type = [opengl|matplotlib]   # Setup the output interface
    #   xlim = <number> <number>    # define the limit of the picture (sometime unused)
    #   ylim = <number> <number> 
    #   zlim = <number> <number> 
    [animation]
    animation_type = opengl
    xlim = -5.0  5.0
    ylim = -5.0  5.0
    zlim = -5.0  5.0

    
    """


ConfigParser.ConfigParser.add_comment = lambda self, section, option, value: self.set(section, '# '+option, value)

class ParticlesConfig(object):

    """
    Parse the config files used for generating the problems:
    
    Config file description:
    
    Section: pset_origin
    ====================
    B{Define the origin of the particles data set.}\n
    B{Varibles:}
        -   media_origin = [file]        Where data the is stored
        -   file_name = <file>           the dataset file name

    
    Section: set_config
    ===================
    B{Particles data set configauration}\n
    B{Varibles:}
        -   len_unit  = <number>         How many meters is a unit,
        -   mass_unit = <number>         How many Kg is a unit
            -                                   Note: len_unit & mass_unit are used only for drawing the particles
        -   boundary  = [open|periodic]  The boundary model used in the simulation

    
    Section: model
    ==============
    B{Simulation method and force model}\n
    B{Varibles:}
        -   force = [gravity|linear_spring|constant_force]                      Force type used
        -   ode_solver_name = [euler|runge_kutta|leap_frog|constant_force]      Integration method
        -   time_step = <number>                                                time step used for the integration
        -   force_const = <number>                                              Force constant, like G
        -   force_vector= <number>                                              Force vector, for the constant force

    
    Section: animation
    ==================
    B{Simulation control & graphic wiew}\n
    B{Variables:}\n
        -   animation_type = [opengl|matplotlib]   # Setup the output interface
        -   xlim = <number> <number>    # define the limit of the picture (sometime unused)
        -   ylim = <number> <number> 
        -   zlim = <number> <number>

    
    Example:
    ========
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
    def __init__(self):
        self.len_unit = 1.0
        self.mass_unit = 1.0
    
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
        
        config.add_section('model')
        config.set('model', 'force', 'gravity')
        config.set('model', 'ode_solver_name', 'euler')
        config.set('model', 'time_step', '3600')
        config.set('model', 'steps', '1000000')
        config.set('model', 'force_const', '6.67384e-11')
        config.set( 'model' , 'force_vector' , '0 0 0' )    
        
    
        config.add_section('animation')
        config.set('animation', 'animation_type', 'opengl')
        config.set('animation', 'xlim', '-5.0  5.0')
        config.set('animation', 'ylim', '-5.0  5.0')
        config.set('animation', 'zlim', '-5.0  5.0')
    
        # Writing our configuration file to 'example.cfg'
        with open( file_name , 'wb' ) as configfile:
            config.write(configfile)
        
        
        ###################################################################
        ## read and parse config file
        ###################################################################
    def read_config( self , file_name ):
        config = ConfigParser.ConfigParser()
        config.read( file_name )
        
        #########################################################
        ## Section pset_origin
        self.media_origin = config.get( 'pset_origin' , 'media_origin' ) 
        self.pset_file_name = config.get( 'pset_origin' , 'file_name' )
        
        #########################################################
        ## Section set_config
        self.len_unit  = config.getfloat( 'set_config' , 'len_unit' )
        self.mass_unit = config.getfloat( 'set_config' , 'mass_unit' )
        self.boudary = config.get( 'set_config' , 'boundary' )
        
        #########################################################
        ## Section model
        self.force_name = config.get( 'model' , 'force' )
        self.ode_solver_name = config.get( 'model' , 'ode_solver_name' )
        self.time_step = config.getfloat( 'model' , 'time_step' )
        self.steps = config.getint( 'model' , 'steps' )
        self.force_const = config.get( 'model' , 'force_const' )
        
        if self.force_name == "constant_force" :
            self.force_vector = config.get( 'model' , 'force_vector' , '-1 0 0' )
        
        ## Section animation
        self.animation_type = config.get( 'animation' , 'animation_type' )
        
    def build_problem( self ):
        self.get_particle_set()
        self.get_force()
        self.get_ode_solver()
        self.get_animation()
        
        return ( self.animation , self.pset , self.force , self.ode_solver )
    
    def get_particle_set( self ):
        
        print("")
        
        self.pset = ps.ParticlesSet()
        
        if self.media_origin == "from_file" :
            ff = fc.FileCluster()
            ff.open( self.pset_file_name )
            ff.insert3( self.pset )
            ff.close()
            print( " setup - particles set - file name: %s " % self.pset_file_name )
            
        self.pset.unit = self.len_unit
        self.pset.mass_unit = self.mass_unit
        
        if self.boudary == "open" :
            self.pset.boundary = None
        elif self.boudary == "periodic" :
            self.pset.boundary = pb.PeriodicBoundary( bound=(-10,10) , dim=pset.dim )
        
        
        #print( self.pset.X )
        #print( self.pset.M )
        #print( self.pset.V )
        
        print( " setup - particles set - size:      %d " % self.pset.size )
        print( " setup - particles set - dim:       %d " % self.pset.dim )
        print( " setup - particles set - len  unit: %e " % self.pset.unit )
        print( " setup - particles set - mass unit: %e " % self.pset.mass_unit )
        
        
        return self.pset
    
    
    def get_force(self):
        
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
            fv =re.split( r"\s+" , self.force_vector )
            
            self.force = cf.ConstForce( self.pset.size , self.pset.dim ,
                                        u_force=( float(fv[0]) , float(fv[1]) , float(fv[2]) ) )
            
            print( " setup - force - Type:  Constant " )
            print( " setup - force - Vect:  %e  %e  %e " % ( float(fv[0]) , float(fv[1]) , float(fv[2]) )  )
        
        self.force.set_masses( self.pset.M )
        
        return self.force
    
    def get_ode_solver(self):
        
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
        
        print( " setup - Integration method - time step: %e " %  self.time_step )   
        return self.ode_solver
    
    def get_animation(self):
        """ Build an Animation object and return the reference to the object """
        print("")
        
        self.animation = None
        
        if self.animation_type == "opengl" :
            self.animation = aogl.AnimatedGl()
            
            print(" setup - animation - type: OpenGL")

            
        elif self.animation_type == "matplotlib" :
            self.animation = anim.AnimatedScatter()
            
            print(" setup - animation - type: MatPlotlib")
            
        self.animation.ode_solver = self.ode_solver
        self.animation.pset       = self.pset
        self.animation.steps      = self.steps
        
            
        return self.animation
        
        
        
        
        
        
        
        
        
