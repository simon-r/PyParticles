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


class Measure( object ):
    """
    Main abstract class for defining the measurments procedures of the system, for example the kinetic energy.
    """
    def __init__( self , pset=None , force=None ):
        self.__pset  = pset
        self.__force = force
        self.__par   = dict()
    
    def get_pset( self ):
        return self.__pset
    
    def set_pset( self , pset ):
        self.__pset = pset
    
    pset = property( get_pset , set_pset , doc="set and get the current measured particle set" )
    
    
    def get_force( self ):
        return self.__force
    
    def set_force( self , force ):
        self.__force = force
    
    pset = property( get_force , set_force , doc="set and get the current force model" )
    
    
    def get_parameter( self , name , val ):
        """
        return the reference to the dict of the used paramenter
        
        A paramenter shold be the volume, some constant ....
        """
        return self.__par
    
    parameter = property( get_parameter , doc="return the reference to the dict of the used paramenter" )
    
    def value( self ):
        """
        The value of the current measure
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
    
    def shape(self ):
        """
        return a tuple containing the shape of the measures dataset
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
    
    def dim( self ):
        """
        return the dimension of the measure, for the dimensionless measure it must return 1 (like kinetic energy or mass)
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
        
    def name(self):
        """
        return a string containig the name of the measure
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
        