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
import pyparticles.pset.particles_set as ps

class StormerVerletSolver( os.OdeSolver ) :
    def __init__( self , force , p_set , dt ):
        super(StormerVerletSolver,self).__init__( force , p_set , dt )
        self.__pset_m1 = ps.ParticlesSet( p_set.size , p_set.dim , mass=False , velocity=False )
        self.__pset_tmp = ps.ParticlesSet( p_set.size , p_set.dim , mass=False , velocity=False )
        
    
    def __step__( self , dt ):

        self.force.update_force( self.pset )
        
        if self.steps_cnt == 1 :
            
            # for the firse step we use the Euler method
            self.__pset_m1.X[:] = self.pset.X[:]
            self.pset.V[:] = self.pset.V + self.force.A * dt
            self.pset.X[:] = self.pset.X + self.pset.V * dt    
            
        else :
        
            self.__pset_tmp.X[:] = self.pset.X
            
            self.pset.X[:] = 2.0*self.pset.X[:] - self.__pset_m1.X[:] + self.force.A[:] * dt**2.0
            self.pset.V[:] = ( self.__pset_tmp.X[:] - self.__pset_m1.X[:] ) / dt
            
            self.__pset_m1.X[:] = self.__pset_tmp.X[:]
            
        
        self.pset.update_boundary() 
