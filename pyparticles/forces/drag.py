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
import pyparticles.forces.force as fr

try:
    import pyopencl as cl
    import pyopencl.array as cla
except:
    ___foo = 0


class Drag( fr.Force ) :
    r"""
    Calculate the forces of resistance. Drag is a force that reacts to the movement with respect to a square law speed. It's commonly used for describing the resistance  of a fluid

    The force is given the equation:

    .. math::

        F_i=-\frac{1}{2}K\dot{X}^2

    Constructor:
        
    :param    size:        the number of particles in the system
    :param    dim:         the dimension of the system
    :param    m:           a vector containig the masses
    :param    Const:       the drag factor K
    """

    def __init__(self , size , dim=3 , m=None , Consts=1.0 ):
        
        self.__dim = dim
        self.__size = size
        
        self.__G = np.zeros( ( size , 1 ) )
        self.__G[:] = Consts
        
        self.__A = np.zeros( ( size , dim ) )
        self.__F = np.zeros( ( size , dim ) )
        
        self.__V = np.zeros( ( size , 1 ) )
        
        self.__M = np.zeros( ( size , 1 ) )
        if m != None :
            self.set_masses( m )
        
        
    
    def set_masses( self , m ):
        self.__M[:] = m
    
    
    def update_force( self , pset ):
        
        self.__V.T[:] = np.sqrt( np.sum( pset.V[:]**2 , 1 )  )
        
        #print( self.__V[:] )
        #print( pset.V[:] )
        
        self.__F[:] =  -1./2. * self.__V[:] * pset.V[:] * self.__G[:]
        
        self.__A = self.__F[:] / self.__M
        
        return self.__A
    

    def getA(self):
        return self.__A
    
    A = property( getA )


    def getF(self):
        return self.__A * self.__M[:]
    
    F = property( getF )
    

    
########################
# OpenCL based 
########################    
class DragOCL( fr.Force ) :
    r"""
    Calculate the forces of resistance. Drag is a force that reacts to the movement with respect to a square law speed. It's commonly used for describing the resistance  of a fluid
    
    this class is based on openCL

    The force is given the equation:

    .. math::

        F_i=-\frac{1}{2}K\dot{X}^2

    Constructor:
        
    :param    size:        the number of particles in the system
    :param    dim:         the dimension of the system
    :param    m:           a vector containig the masses
    :param    Const:       the drag factor K
    """

    def __init__(self , size , dim=3 , m=None , Consts=1.0 , np_type=np.float32):
        
        self.__dim = dim
        self.__size = size
        
        self.__G = np_type( Consts )
        
        self.__A = np.zeros( ( size , dim ) )
        self.__F = np.zeros( ( size , dim ) )
        
        self.__V = np.zeros( ( size , 1 ) )
        
        self.__M = np.zeros( ( size , 1 ) )
        
        self.__cl_context = cl.create_some_context()
        self.__cl_queue = cl.CommandQueue(self.__cl_context, properties=cl.command_queue_properties.PROFILING_ENABLE )
        
        self.__V_cla = cla.to_device( self.__cl_queue , self.__V )
        self.__A_cla = cla.Array( self.__cl_queue , ( self.__size , self.__dim ) , np_type )
        
        if m != None :
            self.set_masses( m )
        
        self.__init_prog_cl()
    
    
    def __init_prog_cl(self):
        self.__drag_prg = """
        __kernel void drag(__global const float *V , 
                           __global const float *M ,
                                          float  G , 
                           __global       float *A ,
                                          uint    dim  )
        {
            i = get_global_id(0);
            j = get_global_id(1);
            
            A[3*i+j] = ( -0.5f * V[3*i+j]*V[3*i+j] * G ) / M[i]
        }
        """
        
        self.__cl_program = cl.Program( self.__cl_context , self.__drag_prg ).build()
    
    def set_masses( self , m ):
        self.__M[:] = m
        self.__M_cla = cla.to_device( self.__cl_queue , self.__M )
    
    def update_force( self , pset ):
        
        self.__V_cla.set( pset.V , queue=self.__cl_queue )
        
        self.__cl_program.drag( self.__cl_queue , ( self.__size , self.__dim ) , None , 
                                self.__V_cla.data ,
                                self.__M_cla.data , 
                                self.__G , 
                                self.__A_cla.data ,
                                self.__dim )
    
        self.__A_cla.get( self.__cl_queue , self.__A )
    

    def getA(self):
        return self.__A
    
    A = property( getA )


    def get_A_ocl(self):
        return self.__A_cla
    
    A_ocl = property( get_A_ocl )

    def getF(self):
        return self.__A * self.__M[:]
    
    F = property( getF )
    
    

