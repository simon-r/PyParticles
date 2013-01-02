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

class MidpointSolver( os.OdeSolver ) :
    def __init__( self , force , p_set , dt ):
        
        super(MidpointSolver,self).__init__( force , p_set , dt )
        
        self.__mid_pset = ps.ParticlesSet( p_set.size , p_set.dim )
    
    
    def __step__( self , dt ):
    
        self.__mid_pset.X[:] = self.pset.X[:] + dt/2.0 * self.pset.V
        
        self.force.update_force( self.__mid_pset )
        
        self.__mid_pset.V[:] = self.pset.V[:] + dt/2.0 * self.force.A
        
        self.pset.V[:] = self.pset.V[:] + dt * self.force.A
        self.pset.X[:] = self.pset.X[:] + dt * self.__mid_pset.V[:]
        
        self.pset.update_boundary() 
        self.force.update_force( self.pset )
        
        
class MidpointSolverConstrained( os.OdeSolverConstrained ) :
    
    def __init__( self , force , p_set , dt , x_constraint=None , v_constraint=None ):
        super(MidpointSolverConstrained,self).__init__( force , p_set , dt , x_constraint=None , v_constraint=None )
        
        self.__mid_pset = ps.ParticlesSet( p_set.size , p_set.dim )
 
        if x_constraint != None :
            self.x_constraint = x_constraint
    
    
    def get_x_constraint(self):
        return super(MidpointSolverConstrained,self).get_x_constraint()
    
    def set_x_constraint(self ,  xc ):
        super(MidpointSolverConstrained,self).set_x_constraint( xc )
        self.__free_inx = self.x_constraint.get_cx_free_indicies()
        self.__csrt_inx = self.x_constraint.get_cx_indicies()
    
    x_constraint = property( get_x_constraint , set_x_constraint , doc="get and set the current positionals constraints" )
 


    def __step__( self , dt ):
    
        
        self.__mid_pset.X[self.__free_inx,:] = self.pset.X[self.__free_inx,:] + dt/2.0 * self.pset.V[self.__free_inx,:]
        self.__mid_pset.X[self.__csrt_inx,:] = self.pset.X[self.__csrt_inx,:]
        
        self.force.update_force( self.__mid_pset )
        
        self.__mid_pset.V[self.__free_inx,:] = self.pset.V[self.__free_inx,:] + dt/2.0 * self.force.A[self.__free_inx,:]
        
        self.pset.V[self.__free_inx,:] = self.pset.V[self.__free_inx,:] + dt * self.force.A[self.__free_inx,:]
        self.pset.X[self.__free_inx,:] = self.pset.X[self.__free_inx,:] + dt * self.__mid_pset.V[self.__free_inx,:]
        
        self.pset.update_boundary() 
        self.force.update_force( self.pset )

