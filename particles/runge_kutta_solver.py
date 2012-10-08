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
import particles.ode_solver as os

class RungeKuttaSolver( os.OdeSolver ) :
    def __init__( self , force , p_set , dt ):
        
        super(RungeKuttaSolver,self).__init__( force , p_set , dt )
        
        self.__K1 = np.zeros( self.force.A.shape )
        self.__K2 = np.zeros( self.force.A.shape )
        self.__K3 = np.zeros( self.force.A.shape )
        self.__K4 = np.zeros( self.force.A.shape )
    
    
    def __step__( self , dt ):
    
        self.__K1[:] = dt*self.force.A
        self.__K2[:] = dt*( 0.5*self.__K1 + 0.5*self.force.A )
        self.__K3[:] = dt*( 0.5*self.__K2 + 0.5*self.force.A )
        self.__K4[:] = dt*( self.__K3 + self.force.A )
        
        
        self.pset.V[:] = self.pset.V[:] + 1.0/6.0 * ( self.__K1 + 2.0*self.__K2 + 2.0*self.__K3 + self.__K4 )
        
        self.pset.X[:] = self.pset.X[:] + dt * self.pset.V
        
        self.force.update_force( self.pset )
        self.pset.update_boundary() 
