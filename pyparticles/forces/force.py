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

class Force(object):
    """
    The main abstract class used as interface for the forces classes

    Constructor

    :param        size:        the number of particles in the system
    :param        dim:         the dimension of the system (3D, 2D..)
    :param        m:           a vector containig the masses
    :param        Const:       the force constants (Like G, K ...)
    """

    def __init__(self , size , dim , m=None , Conts=1.0 ):
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )

    def set_masses( self , m ):
        """
        Set the masses used for computing the forces.

        :param    m:         An array containig the masses
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )

    def update_force( self , p_set ):
        """
        Computes the forces of the current status ad return the accelerations of the particles
    
        :param    p_set:     Particles set obj.
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )

    def getA(self):
        """
        return the array of the acclerations
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )

    A = property( getA , doc="(property) return the array of the acclerations")

    def getF(self):
        """
        returns the array of the forces
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )

    F = property( getF , doc="(property) returns the array of the forces" )


    def get_const( self ):
        """
        returns the force contants
        """
        NotImplementedError(" %s : is virtual and must be overridden." % sys._getframe().f_code.co_name )        

    const = property( get_const , doc="(property) returns the force contants")


