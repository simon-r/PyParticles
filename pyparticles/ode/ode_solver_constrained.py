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


#import numpy as np
#import pyparticles.ode.ode_solver

#class OdeSolverConstrained( os.OdeSolver ) :
#    def __init__(self , force , p_set , dt , x_constraint=None , v_constraint=None ):
#        
#        self.__x_constr = x_constraint
#        self.__v_constr = v_constraint
#        
#        super(OdeSolverConstrained,self).__init__( force , p_set , dt )
#        
#
#    def get_x_constraint(self):
#        """
#        returns a reference to the current positionals constraints
#        """
#        return self.__x_constr
#    
#    def set_x_constraint(self ,  xc ):
#        """
#        set the new positionals contraints
#        """
#        self.__x_constr = xc
#        self.__x_constr.pset = self.pset
#    
#    x_constraint = property( get_x_constraint , set_x_constraint , doc="get and set the current positionals constraints" )
#    
#    