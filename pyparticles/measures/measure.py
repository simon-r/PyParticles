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

class Measure( object ):
    """
    Main abstract class for defining the measurement procedures of the system, for example the total kinetic energy.
    """
    def __init__( self , pset=None , force=None ):
        """
        Constructor
          
        :param pset:    The particles set
        :param force:   The model of the used force
        """
        self.__pset  = pset
        self.__force = force
        self.__par   = dict()
        
        self.__str_f = "%f"
    
    def get_pset( self ):
        return self.__pset
    
    def set_pset( self , pset ):
        self.__pset = pset
    
    pset = property( get_pset , set_pset , doc="set and get the current measured particle set" )
    
    
    def get_force( self ):
        return self.__force
    
    def set_force( self , force ):
        self.__force = force
    
    force = property( get_force , set_force , doc="set and get the current force model" )
    
    
    def get_parameter( self , name , val ):
        """
        return the reference to the dict of the used parameter
            A parameter  should be the volume, some constant ....
        """
        return self.__par
    
    parameter = property( get_parameter , doc="return the reference to the dict of the used paramenter" )
    
    
    def update_measure( self ):
        """
        compute and return the value of the measured quantity
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
    
    
    def value( self ):
        """
        Return the value of the current measure
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )
    
    def set_str_format( self , f="%5.3f" ):
        self.__str_f = f
        
    def get_str_format( self ):
        return self.__str_f
    
    str_format = property( get_str_format , set_str_format , doc="get ad set the string format for representing the value" )
    
    def value_str( self ):
        """
        return a string containig the value of the current neasure formmatted according to the format defined with the str_property format. By default if uses the simple floaf format
        """
        return self.str_format % ( self.value() )
    
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
        
        
        
        
        
class MeasureParticles( Measure ):
    """
    Abstract class used fopr measuring a subset of partiles or a set of singles particles.
    """
    def __init__( self , pset=None , force=None , subset=None , model="part_by_part" ):
        """
        Constructor:
          
        :param pset:    The particles set
        :param force:   The model of the used force
        :param subset:  a numpy 1D array containing the indicies of the measured particles
        :param model:   a strung describing the model for the measure: "part_by_part" or "subsystem"
          
        """
        self.__subset = np.copy(subset)
        
        self.__model = None
        
        self.model = model
        
        super( MeasureParticles , self ).__init__( pset=pset , force=force )

    
    def set_subset( self , subset ):
        self.__subset = np.copy(subset)    
    
    def get_subset( self ):
        return self.__subset
    
    
    subset = property( get_subset , set_subset , doc="get and set the subset of particles to be measured" )
    
    
    def get_model ( self ):
        return self.__model

    def set_model ( self , model ):
        if model not in [ "part_by_part" , "subsystem" ] :
            ValueError
            
        self.__model = model
    
    model = property( get_model , set_model , doc="set and get the measurement model: \"part_by_part\" or \"subsystem\" ")
        