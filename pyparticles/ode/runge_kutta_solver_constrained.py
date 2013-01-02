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
#import pyparticles.pset.particles_set as ps
#
#import pyparticles.ode.ode_solver as ods

#class RungeKuttaSolverConstrained( ods.OdeSolverConstrained ) :
#    def __init__( self , force , p_set , dt , x_constraint=None , v_constraint=None ):
#        super(RungeKuttaSolverConstrained,self).__init__( force , p_set , dt , x_constraint=None , v_constraint=None )
#        
#        if x_constraint != None :
#            self.x_constraint = x_constraint
#            
#        self.__Kv1 = np.zeros( self.force.A.shape )
#        self.__Kv2 = np.zeros( self.force.A.shape )
#        self.__Kv3 = np.zeros( self.force.A.shape )
#        self.__Kv4 = np.zeros( self.force.A.shape )
#        
#        self.__Kx1 = np.zeros( self.force.A.shape )
#        self.__Kx2 = np.zeros( self.force.A.shape )
#        self.__Kx3 = np.zeros( self.force.A.shape )
#        self.__Kx4 = np.zeros( self.force.A.shape )
#        
#        self.__tmp_pset = ps.ParticlesSet( p_set.size , p_set.dim )
#        
#    
#    def get_x_constraint(self):
#        return super(RungeKuttaSolverConstrained,self).get_x_constraint()
#    
#    def set_x_constraint(self ,  xc ):
#        super(RungeKuttaSolverConstrained,self).set_x_constraint( xc )
#        self.__fi = self.x_constraint.get_cx_free_indicies()
#        self.__ci = self.x_constraint.get_cx_indicies()
#    
#    x_constraint = property( get_x_constraint , set_x_constraint , doc="get and set the current positionals constraints" )
#        
#        
#    def __step__( self , dt ):
#    
#        self.__tmp_pset.V[:] = self.pset.V[:]  
#        
#        # K1
#        self.__Kv1[self.__fi,:] = self.force.A[self.__fi,:]
#        self.__Kx1[self.__fi,:] = self.pset.V[self.__fi,:]
#        
#        # K2
#        self.__tmp_pset.X[self.__fi,:] = self.pset.X[self.__fi,:] + dt/2.0*self.__Kx1[self.__fi,:]
#        self.__tmp_pset.X[self.__ci,:] = self.pset.X[self.__ci,:]
#        self.force.update_force( self.__tmp_pset )
#        
#        self.__Kv2[self.__fi,:] = self.force.A[self.__fi,:]
#        self.__Kx2[self.__fi,:] = self.pset.V[self.__fi,:] + dt/2.0*self.__Kv1[self.__fi,:]
#        
#        #K3
#        self.__tmp_pset.X[self.__fi,:] = self.pset.X[self.__fi,:] + dt/2.0*self.__Kx2[self.__fi,:]
#        self.__tmp_pset.X[self.__ci,:] = self.pset.X[self.__ci,:]
#        self.force.update_force( self.__tmp_pset )
#        
#        self.__Kv3[self.__fi,:] = self.force.A[self.__fi,:]
#        self.__Kx3[self.__fi,:] = self.pset.V[self.__fi,:] + dt/2.0*self.__Kv2[self.__fi,:]
#        
#        #K4
#        self.__tmp_pset.X[self.__fi,:] = self.pset.X[self.__fi,:] + dt*self.__Kx3[self.__fi,:]
#        self.__tmp_pset.X[self.__ci,:] = self.pset.X[self.__ci,:]
#        self.force.update_force( self.__tmp_pset )
#        
#        self.__Kv4[self.__fi,:] = self.force.A[self.__fi,:]
#        self.__Kx4[self.__fi,:] = self.pset.V[self.__fi,:] + dt*self.__Kv3[self.__fi,:]
#        
#
#        
#        self.pset.V[self.__fi,:] = self.pset.V[self.__fi,:] + dt/6.0 * ( self.__Kv1[self.__fi,:] + 2.0*self.__Kv2[self.__fi,:] + 2.0*self.__Kv3[self.__fi,:] + self.__Kv4[self.__fi,:] )
#        self.pset.X[self.__fi,:] = self.pset.X[self.__fi,:] + dt/6.0 * ( self.__Kx1[self.__fi,:] + 2.0*self.__Kx2[self.__fi,:] + 2.0*self.__Kx3[self.__fi,:] + self.__Kx4[self.__fi,:] )
#        
#        self.pset.V[self.__ci,:] = 0.0
#        
#        self.pset.update_boundary() 
#        self.force.update_force( self.pset )
#        
        
    