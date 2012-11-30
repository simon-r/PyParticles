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


class SimTime( object ):
    """
    Class used for storing the current simulation time:
    
    Constructor
    
    :param controller: a reference to the object that control the simulation time
    
    """
    def __init__( self , controller ):
        self.__time = 0.0
        self.__controller = controller
    
    def get_time( self ):
        """
        get the current time
        """
        return self.__time
    
    def set_time( self , t ):
        """
        set the current time
        """
        self.__time = t
        
    time = property( get_time , set_time , doc="get and set the current simulation time" )
    
    
    def get_controller( self ):
        r"""
        Get a reference to the simulation time controller, normally an ODE solver
        
        :returns the reference to the ODE solver object
        """
        return self.__controller
    
    controller = property( get_controller , doc="get the reference to the time controller" )
    
    