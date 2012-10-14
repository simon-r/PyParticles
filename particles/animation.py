

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

import particles.particles_set as ps
import particles.rand_cluster as clu
import particles.gravity as gr
import particles.euler_solver as els
import particles.leapfrog_solver as lps
import particles.runge_kutta_solver as rks

import matplotlib.animation as animation

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import particles.periodic_boundary as pb
import particles.rebound_boundary as rb
import particles.const_force as cf
import particles.vector_field_force as vf
import particles.linear_spring as ls


class Animation(object):
    def __init__(self):
        self.__ode_solver = None
        self.__pset = None
        self.__steps = 10000
        
        self.__xl = (-1,1)
        self.__yl = (-1,1)
        self.__zl = (-1,1)
        
        self.__trajectory = False
        self.__trajectory_step = 1
        
        
    def set_ode_solver( self , solver ):
        self.__ode_solver = solver
    
    def get_ode_solver( self ):
        return self.__ode_solver     
        
    ode_solver = property( get_ode_solver , set_ode_solver )
    
    
    def get_pset(self):
        return self.__pset
    
    def set_pset( self , pset ):
        self.__pset = pset
        
    pset = property( get_pset , set_pset )
    
    
    def get_steps( self ):
        return self.__steps
    
    def set_steps( self , steps ):
        self.__steps = steps
    
    steps = property( get_steps , set_steps )
    
    
    def set_xlim( self , xl ):
        self.__xl = xl
        
    def get_xlim( self ):
        return self.__xl
 
    def set_ylim( self , yl ):
        self.__yl = yl
        
    def get_ylim( self ):
        return self.__yl    
           
    def set_zlim( self , zl ):
        self.__zl = zl
        
    def get_zlim( self ):
        return self.__zl
           
    xlim = property( get_xlim , set_xlim )
    ylim = property( get_ylim , set_ylim )
    zlim = property( get_zlim , set_zlim )
     
     
    def get_trajectory( self ) :
        return self.__trajectory
    
    def set_trajectory( self , tr ):
        self.__trajectory = tr
        
    trajectory = property( get_trajectory , set_trajectory , doc="enable or disable the trajectory" )
    
    
    def get_trajectory_step( self ) :
        return self.__trajectory_step
    
    def set_trajectory_step( self , trs ):
        self.__trajectory_step = trs
        
    trajectory_step = property( get_trajectory_step , set_trajectory_step , doc="set or get the step for drawing the trajectory" )

     
    def build_animation(self):
        pass
    
    def data_stream(self):
        pass
        
    def start(self):
        pass
        

        
    