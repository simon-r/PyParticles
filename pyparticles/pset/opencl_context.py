# PyParticles : Particles simulation in python
# Copyright (C) 2012  Simone Riva simone.rva {at} gmail {dot} com
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


try:
    import pyopencl as cl
    import pyopencl.array as cla
except:
    ___foo = 0
    

OCLC_X = np.uint8( 0b10000000 )
OCLC_V = np.uint8( 0b01000000 )
OCLC_A = np.uint8( 0b00100000 ) 
OCLC_M = np.uint8( 0b00010000 )

class OpneCLcontext( object ):
    def __init__( self , size , dim , mask=( OCLC_X | OCLC_V | OCLC_A | OCLC_M ) , dtype=np.float32 ):
                
        self.__cl_context = cl.create_some_context()
        self.__cl_queue = cl.CommandQueue(self.__cl_context, properties=cl.command_queue_properties.PROFILING_ENABLE )
        
        
        if mask & OCLC_V :
            self.__V_cla = cla.Array( self.__cl_queue , ( size , dim ) , dtype )
        else :
            self.__V_cla = None


        if mask & OCLC_X :
            self.__X_cla = cla.Array( self.__cl_queue , ( size , dim ) , dtype )
        else :
            self.__X_cla = None

            
        if mask & OCLC_A :
            self.__A_cla = cla.Array( self.__cl_queue , ( size , dim ) , dtype )
        else :
            self.__A_cla = None

            
        if mask & OCLC_M :
            self.__M_cla = cla.Array( self.__cl_queue , ( size , 1 ) , dtype )
        else :
            self.__M_cla = None
                                    
    
    
    def get_CL_context(self):
        return self.__cl_context
    
    CL_context = property( get_CL_context )
    
    
    def get_CL_queue(self):
        return self.__cl_queue
        
    CL_queue = property( get_CL_queue )
    
        
    def get_X_cla(self):
        return self.__X_cla
    
    X_cla = property( get_X_cla )
    
    
    def get_A_cla(self):
        return self.__A_cla
    
    A_cla = property( get_A_cla )
    
    
    def get_V_cla(self):
        return self.__V_cla
    
    V_cla = property( get_V_cla )
    
    
    def get_M_cla(self):
        return self.__M_cla
        
    M_cla = property( get_M_cla )
    
    