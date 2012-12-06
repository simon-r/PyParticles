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

import pyparticles.animation.animation as pan
import pyparticles.utils.time_formatter as tf

import numpy as np
import sys


class AnimatedCLI( pan.Animation ):
    def __init__(self):
        super( AnimatedCLI , self ).__init__()
        
    def build_animation(self):
        print( "Build ... " )
    
    def data_stream(self):
        
        self.pset.log()
        self.ode_solver.step()
        
        self.perform_measurement()
        
        self.update_fps()
        
        return self.ode_solver.steps_cnt
        
    def closing_procedure(self):
        pass
        
    def start(self):
        tfrmt =   tf.MyTimeFormatter()
        for i in range( self.steps ):
            self.data_stream()
            
            if np.mod( self.ode_solver.steps_cnt , 100 ):
                print( "time: %s " % ( tfrmt.to_str( self.ode_solver.time ) ) ) 
            
        self.closing_procedure()