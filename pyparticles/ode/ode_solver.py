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
import sys


import pyparticles.ode.sim_time as st

class OdeSolver(object) :
    """
    Base abstract class for defining the integration method of the ordinary differential equation like Runge Kutta or Euler method,
    the user must overide the method **__step__**
    
    Example (Euler method):
    ::
    
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
    
    Constructor:
    
    :param force:      the force model
    :param p_set:      the particle set
    :param dt:         delta time
    """
    def __init__( self , force , p_set , dt ):
        self.__force = force
        self.__p_set = p_set
        self.__dt = dt
        
        self.__sim_time = st.SimTime( self )
        
        self.__steps_cnt = 0        
    
    def get_dt( self ):
        return self.__dt

    def set_dt( self , dt ):
        self.__dt = dt

    dt = property( get_dt , set_dt , doc="get and set the delta time of the step")
    
    
    def get_steps(self):
        return self.__steps_cnt
    
    def del_steps(self):
        self.__steps_cnt = 0
    
    steps_cnt = property( get_steps , fdel=del_steps , doc="return the count of the performed steps")
    
    
    def get_time(self):
        return self.__sim_time.time
    
    def set_time( self , t0 ):
        self.__sim_time.time = t0
        
    time = property( get_time , set_time , doc="get and set the current simulation time" )
    
    
    def get_sim_time( self ):
        return self.__sim_time
    
    sim_time = property( get_sim_time , doc="get the reference to the SimTime object, used for storing and sharing the current simulation time" )
    
    
    def get_force( self ):
        return self.__force
    
    def set_force( self , force ):
        self.__force = force
        
    force = property( get_force , set_force , doc="get and set the used force model")
    
    
    def update_force( self ):
        self.__force.update_force( self.pset )
    
    def get_pset( self ):
        return self.__p_set
    
    def set_pset( self , p_set ):
        self.__p_set = p_set
        
    pset = property( get_pset , set_pset , "get and set the used particles set")
    
    
    def step( self , dt=None ):
        """
        Perform an integration step. If the dt is not given (reccomended) it uses the stored *dt*.
        You must alway use this method for executing a step.
        """
        if dt == None:
            dt = self.dt
        
        self.__sim_time.time += dt
        
        self.__steps_cnt += 1
        
        self.__step__( dt )
        
    def __step__( self , dt ):
        """
        Abstract methos that contain the code for computing the new status of the particles system. This methos must be overidden by the user.
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )



class OdeSolverConstrained( OdeSolver ) :
    def __init__(self , force , p_set , dt , x_constraint=None , v_constraint=None ):
        
        self.__x_constr = x_constraint
        self.__v_constr = v_constraint
        
        super(OdeSolverConstrained,self).__init__( force , p_set , dt )
        

    def get_x_constraint(self):
        """
        returns a reference to the current positionals constraints
        """
        return self.__x_constr
    
    def set_x_constraint(self ,  xc ):
        """
        set the new positionals contraints
        """
        self.__x_constr = xc
        self.__x_constr.pset = self.pset
    
    x_constraint = property( get_x_constraint , set_x_constraint , doc="get and set the current positionals constraints" )