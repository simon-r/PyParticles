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
import scipy.spatial.distance as dist

import pyparticles.measures.measure as me

class MomentumSystem( me.Measure ):
    """
    'Measure' for computing the total momentum of the particle system
    """
    def __init__( self , pset=None ):
        
        if pset != None :
            self.__P = np.zeros(( pset.dim ))
        else :
            self.__P = None
        
        super( MomentumSystem , self ).__init__( pset=pset , force=None )
        
        
    def value(self):
        """
        return the current value of the total momentum
        """
        return self.__P
    
    
    def update_measure( self ):
        """
        Compute and return the total momentum of the system 
        """
        
        self.__P = np.sum( self.pset.V * self.pset.M , 0 )
        
        return self.__P
        
    
    def shape( self ):
        """
        return a tuple containing the shape of the measures dataset
        """
        return ( self.pset.dim )
    
    def dim( self ):
        """
        return the dimension of the measure: Dim  for the momentum
        """
        return self.pset.dim
    
    def name(self):
        """
        Return the string: "momentum"
        """
        return "momentum"
    
    
    
class MomentumParticles( me.MeasureParticles ):
    """
    'Measure' for computing the momentum particle by particle or of a subsystem
    Example: ::
    
        P = MomentumParticles( pset , subset=np.array([1,4,5]) , model="part_by_part")
        P.update_measure()
        print( P.value )
        >    [[ 1.1 , 2.3 , 3.2 ],
        >     [ 1.7 , 5.2 , 6.9 ],
        >     [ 1.8 , 2.3 , 1.7 ]
        >    ]
     
    Constructor:
      
    :param pset      The particles set
    :param force     The model of the used force
    :param subset    a numpy 1D array containing the indicies of the measured particles
    :param model     a strung describing the model for the measure: "part_by_part" or "subsystem"
    """
    def __init__( self , pset=None , force=None , subset=None , model="part_by_part" ):
      
        if pset != None and model == "subsystem" :
            self.__P = np.zeros(( pset.dim ))
        elif pset != None and model == "part_by_part" and subset != None :
            self.__P = np.zeros(( len(subset) , pset.dim ))
        else :
            self.__P = None
        
        super( MomentumParticles , self ).__init__( pset , force , subset , model )
        
        
    def value(self):
        """
        return the current value of the momentum
        """
        return self.__P
    
    
    def update_measure( self ):
        """
        Compute and return the total momentum of the specified particles 
        """
        
        if self.model == "part_by_part" :
            self.__P = self.pset.V[self.subset] * self.pset.M[self.subset]
        else :
            self.__P = np.sum( self.pset.V[self.subset] * self.pset.M[self.subset] , 0 )
        
        return self.__P
        
    
    def shape( self ):
        """
        return a tuple containing the shape of the measures dataset
        """
        if self.model == "part_by_part" :
            return ( len( self.subset ) , pset.dim  )
        else :
            return ( 1 , pset.dim )
    
    def dim( self ):
        """
        return the dimension of the measure: Dim: (2D or 3D) for the momentum
        """
        return self.pset.dim
    
    def name(self):
        """
        Return the string: "momentum"
        """
        return "momentum" 