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

class OpenCLcontext( object ):
    """
    Create a working context for PyOpenCL.
        This class build a single opencl context and a command queue, that should be shared between the different method or algorithms. 
        We can also use this class for minimizing  the data transfer between the main RAM and the GPU RAM or for sharing some TMP array.
        
    The Array used in this class are the ones defined in the pyopencl package: http://documen.tician.de/pyopencl/array.html#the-array-class 
        
        Constructor
        
        :param size: the size of the particles set
        :param dim: The dimension of the system
        :param mask: ( OCLC_X | OCLC_V | OCLC_A | OCLC_M ) setup the indicated arrays 
            *. OCLC_X: Position array
            *. OCLC_V: Velocity array
            *. OCLC_A: Acceleration array
            *. OCLC_M: Mass array
        :param dtype: the floating point type (at the moment I support only np.float32 !! )
        
        Example: ::
            
            # Share the same context between gravity and the Euler Solver
            
            import pyparticles.ode.euler_solver as els
            import pyparticles.forces.gravity as gr
            import pyparticles.pset.opencl_context as occ 
            
            occx = occ.OpenCLcontext(  pset.size , pset.dim , (occ.OCLC_X|occ.OCLC_V|occ.OCLC_A|occ.OCLC_M) )
            grav = gr.GravityOCL( pset.size , Consts=G , ocl_context=occx  )
            solver = els.EulerSolverOCL( grav , pset , dt , ocl_context=occx )
    """
    def __init__( self , size , dim , mask=( OCLC_X | OCLC_V | OCLC_A | OCLC_M ) , dtype=np.float32 ):
        
        self.__dtype = dtype 
        
        self.__size = size
        self.__dim = dim  
        
        self.__opt_arrays = dict()
                
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
                                    

    def get_dtype(self):
        return self.__dtype
    
    dtype = property( get_dtype , doc="return the dtype of the context" )
    
    
    def add_array_by_name( self , key , size=None , dim=None , dtype=None ):
        """
        Add a new array by name.
        
        :param key: The key (or name) of the new array
        :param size: (Default: current) The size of the new array, if not specified by default it uses the current size
        :param dim: (Default: current) The dim of the new array, if not specified by default it uses the current dim 
        :param dtype: (Dafault: current) The dtype of the new array, if not specified by default it uses the context dtype
        """
        
        if dim == None :
            dim = self.__dim        
        
        if size == None :
            size = self.__size
            
        if dtype == None :
            dtype = self.dtype 
            
            
        self.__opt_arrays[key] = cla.Array( self.__cl_queue , ( size , dim ) , dtype=dtype )
    
        
    def get_by_name( self , key ):
        """
        Return the array named "key"
        """
        return self.__opt_arrays[key]
    
    
    def get_CL_context(self):
        return self.__cl_context
    
    CL_context = property( get_CL_context , doc="return the opencl context")
    
    
    def get_CL_queue(self):
        return self.__cl_queue
        
    CL_queue = property( get_CL_queue , doc="return the command queue" )
    
        
    def get_X_cla(self):
        return self.__X_cla
    
    X_cla = property( get_X_cla , doc="return the positions array" )
    
    
    def get_A_cla(self):
        return self.__A_cla
    
    A_cla = property( get_A_cla , doc="return the acceleration array" )
    
    
    def get_V_cla(self):
        return self.__V_cla
    
    V_cla = property( get_V_cla , doc="return the velocity array" )
    
    
    def get_M_cla(self):
        return self.__M_cla
        
    M_cla = property( get_M_cla , doc="return the masses array (this is a 1D array)" )
    
    