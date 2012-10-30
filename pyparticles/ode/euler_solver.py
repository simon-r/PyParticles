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
import pyparticles.ode.ode_solver as os

class EulerSolver( os.OdeSolver ) :
    def __init__( self , force , p_set , dt ):
        super(EulerSolver,self).__init__( force , p_set , dt )
        
    
    def __step__( self , dt ):

        self.force.update_force( self.pset )
        
        self.pset.V[:] = self.pset.V + self.force.A * dt
        self.pset.X[:] = self.pset.X + self.pset.V * dt
        
        self.pset.update_boundary() 
