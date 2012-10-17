
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
import pyparticles.pset.particles_set as ps

class ElectricallyChargeedParticlesSet ( ps.ParticlesSet ):
    """
    Deprecated !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    def __init__( self , size=1 , dim=3 , boundary=None ,
                  label=False , mass=True  , charge=True , velocity=True ,
                  log_X=False , log_V=False , log_max_size=0
                  ):
        
        super(ElectricChargeParticlesSet,self).__init__( size , dim , boundary ,
                                                        label , mass , velocity ,
                                                        log_X , log_V , log_max_size )
        
        if charge :
            self.__Q = np.zeros(( size , 1 ))
        else:
            self.__Q = None
            
    
    def realloc( self , size , dim , boundary=None ,
                 label=False , mass=True , charge=True , velocity=True ,
                 log_X=False , log_V=False , log_max_size=0 ):
        """
        Realloc the particle set, it uses the same args of the constructor
        """
        del self.__Q
        
        self.__init__( size , dim , boundary , label , mass , charge , velocity , log_X , log_V , log_max_size )
    
        
    
    def getQ(self):
        return self.__mass
    
    Q = property( getQ , doc="return the reference to the array of the charges" )
    
    