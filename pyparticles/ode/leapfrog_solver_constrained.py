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
##import pyparticles.ode.ode_solver_constrained as osc
#import pyparticles.ode.ode_solver as ods

#class LeapfrogSolverConstrained( ods.OdeSolverConstrained ) :
#    def __init__( self , force , p_set , dt , x_constraint=None , v_constraint=None ):
#        super(LeapfrogSolverConstrained,self).__init__( force , p_set , dt , x_constraint=None , v_constraint=None )
#        self.__Ai = np.zeros( self.force.A.shape )
#        
#        if x_constraint != None :
#            self.x_constraint = x_constraint
#        
#    def get_x_constraint(self):
#        return super(LeapfrogSolverConstrained,self).get_x_constraint()
#    
#    def set_x_constraint(self ,  xc ):
#        super(LeapfrogSolverConstrained,self).set_x_constraint( xc )
#        self.__free_inx = self.x_constraint.get_cx_free_indicies()
#        self.__csrt_inx = self.x_constraint.get_cx_indicies()
#    
#    x_constraint = property( get_x_constraint , set_x_constraint , doc="get and set the current positionals constraints" )
#    
#    
#    def __step__( self , dt ):
#        
#        self.pset.X[self.__free_inx,:] = self.pset.X[self.__free_inx,:] + self.pset.V[self.__free_inx,:] * dt + 0.5*self.force.A[self.__free_inx,:] * dt**2.0
#        self.__Ai[self.__free_inx,:] = self.force.A[self.__free_inx,:]
#        
#        self.force.update_force( self.pset )
#        
#        self.pset.V[self.__free_inx,:] = self.pset.V[self.__free_inx,:] + 0.5 * ( self.__Ai[self.__free_inx,:] + self.force.A[self.__free_inx,:] ) * dt
#        
#        self.pset.V[self.__csrt_inx,:] = 0.0
#        
#        #print( self.pset.V )
#        
#        self.pset.update_boundary() 