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
import scipy.spatial.distance as dist

import pyparticles.forces.force as fr

import random

class ElectromagneticField( fr.Force ) :
    r"""
    Compute the electromagnetic force of a system of charged and non-selfinteracting particles system immersed in an electromagnetic filed  according to the Lorenz formulation.
    
    .. math::
    
        \mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B})
    """
    
    def __init__( self , size , dim=3 , m=None , Consts=1.0 ):
        
        self.__dim = dim
        self.__size = size
        
        self.__Ke = Consts[0]
        self.__Km = Consts[1]

        self.__Am = np.zeros( ( size , dim ) )
        self.__Ae = np.zeros( ( size , dim ) )
        
        self.__Fe = np.zeros( ( size , dim ) )
        self.__Fm = np.zeros( ( size , dim ) )
        
        self.__V = np.zeros( ( size , size ) )
        self.__D = np.zeros( ( size , size ) )
        self.__Q = np.zeros( ( size , size ) )
        self.__M = np.zeros( ( size , 1 ) )
        
        self.__Cr = np.zeros( ( size , dim ) )
        
        if m != None :
            self.set_masses( m )
        
        self.__el_fields = dict()
        self.__ma_fields = dict()
    
    def set_masses( self , m ):
        self.__M[:] = m
        
    def set_charges( self , q ):
        self.__Q[:,:] = q
        self.__Q[:,:] = self.__Q * self.__Q.T
    
    def append_electric_field( self , ef , key=None ):
        r"""
        Append a vector field funcion to the list of electric field funtions.
        
        The field function must be in the form
        | E = ef( X )
        |
        | Where:
        |  E is a n by 3 numpy array of vectors
        |  X is a n by 3 numpy array of coordinates
        """
        if key == None :
            key = random.randint( 0 , 2**64 )
            
        self.__el_fields[key] = ef
        
        return key
    
    def append_magnetic_field( self , bf , key=None ):
        r"""
        Append a vector field funcion to the list of electric field funtions.
        
        It return the key used to identify the funtion, if key == None it uses a random number.
        
        The filed function must be in the form
        | B = bf( X )
        |
        | Where:
        |  B is a n by 3 numpy array of vectors
        |  X is a n by 3 numpy array of coordinates
        """
        if key == None :
            key = random.randint( 0 , 2**64 )
            
        self.__ma_fields[key] = bf
        
        return key
    
    
    def update_force( self , pset ):        
        self.__Fe[:] = 0.0
        
        for key in self.__el_fields.keys() :
            self.__Fe[:] = self.__Fe[:] + pset.Q[:] * pself.__el_fields[key]( pset.X[:] )
    
        for key in self.__el_fields.keys() :
            self.__Fm[:] = self.__Fm[:] + pset.Q[:] * np.cross( pset.V[:] , pself.__el_fields[key]( pset.X[:] ) )
            
        self.__Fe[:] += self.__Fm[:]
    
        self.__A = self.__Fe[:] / pset.M[:]
        
        return self.__A
    
    
    def getA(self):
        return self.__A
    
    A = property( getA )


    def getF(self):
        return self.__Fe
    
    F = property( getF )
