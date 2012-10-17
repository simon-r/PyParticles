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

import pyparticles.pset.particles_set as ps

import pyparticles.animation as pan

import pyparticles.rand_cluster as clu
import pyparticles.forces.gravity as gr
import pyparticles.euler_solver as els
import pyparticles.leapfrog_solver as lps
import pyparticles.runge_kutta_solver as rks

import matplotlib.animation as animation

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pyparticles.periodic_boundary as pb
import pyparticles.rebound_boundary as rb
import pyparticles.const_force as cf
import pyparticles.vector_field_force as vf
import pyparticles.linear_spring as ls



class TestAnimation( pan.Animation ):
    
    def __init__(self):
        super( AnimatedScatter , self ).__init__()

 
    def build_animation(self):       
        pass
        
    def data_stream(self):
        pass
            

    def update(self, i):
        pass

    def start(self):
        pass
