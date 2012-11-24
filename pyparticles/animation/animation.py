

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


import sys


class Animation(object):
    """
    Base abstract class used for controling the simulation.
        This class should be used as a base class for building and runnig a simulation problem.
        The class animation contains all foudamental element for working with a PyParticles in an easy way.
    The user must overide the methods:
            build_animation: For setting up averithing
            data_stream: for performing a simulation step or runnig the main loop
            start: start the smulation
    
    In a few word you must follow this procedure:
    ::
    
        # Construct a new object
        a = MyAnimation()
        
        # setup the particles set
        a.pset = pset
        
        # setup the numeric integration 
        a.ode_solver = solver
        
        # max number of steps
        a.steps = steps
        
        # set up everythings 
        a.build_animation()
        
        # start!
        a.start()
    """
    def __init__(self):
        self.__ode_solver = None
        self.__pset = None
        self.__steps = 10000
        
        self.__xl = (-1,1)
        self.__yl = (-1,1)
        self.__zl = (-1,1)
        
        self.__trajectory = False
        self.__trajectory_step = 1
        
        self.__measures = dict()
        self.__measures_names = []
        
        
    def set_ode_solver( self , solver ):
        self.__ode_solver = solver
    
    def get_ode_solver( self ):
        return self.__ode_solver     
        
    ode_solver = property( get_ode_solver , set_ode_solver )
    
    
    def add_measure( self , measure ):
        """
        Add a class delegeted for performing a measure
        """
        self.__measures[measure.name()] = measure
        self.__measures_names.append( measure.name() )
        
    def perform_measurement( self ):
        """
        Execute all listed measures
        """
        for m in self.__measures_names :
            self.__measures[m].pset = self.pset
            self.__measures[m].update_measure()
            
    def get_measure_value( self , name ):
        """
        get the value of the measure named 'name'
        """
        return self.__measures[name].value()
    
    
    def get_measure_value_str( self , name ):
        """
        return a string containig the value of the measure
        """
        return self.__measures[name].value_str()
    
    
    def get_measure( self , name ):
        """
        return the measure named 'name'
        """
        return self.__measures[name]
    
    def get_measures_names( self ):
        """
        Return a list containg the names of the executed measured.
        """
        return self.__measures_names
    
    def measures_cnt( self ):
        return len( self.__measures )
        
    
    def get_pset(self):
        return self.__pset
    
    def set_pset( self , pset ):
        self.__pset = pset
        
    pset = property( get_pset , set_pset )
    
    
    def get_steps( self ):
        return self.__steps
    
    def set_steps( self , steps ):
        self.__steps = steps
    
    steps = property( get_steps , set_steps )
    
    
    def set_xlim( self , xl ):
        self.__xl = xl
        
    def get_xlim( self ):
        return self.__xl
 
    def set_ylim( self , yl ):
        self.__yl = yl
        
    def get_ylim( self ):
        return self.__yl    
           
    def set_zlim( self , zl ):
        self.__zl = zl
        
    def get_zlim( self ):
        return self.__zl
           
    xlim = property( get_xlim , set_xlim )
    ylim = property( get_ylim , set_ylim )
    zlim = property( get_zlim , set_zlim )
     
     
    def get_trajectory( self ) :
        return self.__trajectory
    
    def set_trajectory( self , tr ):
        self.__trajectory = tr
        
    trajectory = property( get_trajectory , set_trajectory , doc="enable or disable the trajectory" )
    
    
    def get_trajectory_step( self ) :
        return self.__trajectory_step
    
    def set_trajectory_step( self , trs ):
        self.__trajectory_step = trs
        
    trajectory_step = property( get_trajectory_step , set_trajectory_step , doc="set or get the step for drawing the trajectory" )

     
    def build_animation(self):
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
    
    def data_stream(self):
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
        
    def start(self):
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
        

        
    