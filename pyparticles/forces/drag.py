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

import pyparticles.pset.opencl_context as occ 

try:
    import pyopencl as cl
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
        
        self.__A =  self.__F[:] / self.__M
        
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

    Constructor:
        
    :param    size:        the number of particles in the system
    :param    dim:         the dimension of the system
    :param    m:           a vector containig the masses
    :param    Const:       the drag factor K
    """

    def __init__(self , size , dim=3 , m=None , Consts=1.0 , ocl_context=None ):
        
        self.__dim = np.int32( dim )
        self.__size = np.int32( size )
        
        if ocl_context == None :
            self.__occ = occ.OpenCLcontext( size , dim , ( occ.OCLC_V | occ.OCLC_A | occ.OCLC_M )  )
        else :
            self.__occ = ocl_context        
        
        self.__dtype = self.__occ.dtype
        
        self.__K = self.__occ.dtype( Consts )
        
        self.__A = np.zeros( ( size , dim ) , dtype=self.__occ.dtype )
        self.__F = np.zeros( ( size , dim ) , dtype=self.__occ.dtype )
                        
        if m != None :
            self.set_masses( m )
        
        self.__init_prog_cl()
    
    
    def __init_prog_cl(self):
        self.__drag_prg = """
        __kernel void drag(__global const float *V , 
                           __global const float *M ,
                                          float  K , 
                           __global       float *A )
        {
            int i = get_global_id(0) ;
            float mod ;
            
            mod = sqrt( pown( V[3*i] , 2 ) + pown( V[3*i+1] , 2 )  + pown( V[3*i+2] , 2 ) ) ;
                        
            A[3*i]   = ( -0.5f * K * mod * V[3*i] )  / M[i] ;
            A[3*i+1] = ( -0.5f * K * mod * V[3*i+1] )  / M[i] ;
            A[3*i+2] = ( -0.5f * K * mod * V[3*i+2] )  / M[i] ;
            
        }
        """
        
        self.__cl_program = cl.Program( self.__occ.CL_context , self.__drag_prg ).build()
    
    def set_masses( self , m ):
        self.__occ.M_cla.set( self.__dtype( m ) , queue=self.__occ.CL_queue )
    
    
    def update_force( self , pset ):
        
        self.__occ.V_cla.set( self.__dtype( pset.V ) , queue=self.__occ.CL_queue )
        
        self.__cl_program.drag( self.__occ.CL_queue , ( self.__size , ) , None , 
                                self.__occ.V_cla.data ,
                                self.__occ.M_cla.data , 
                                self.__K , 
                                self.__occ.A_cla.data )
    
        self.__occ.A_cla.get( self.__occ.CL_queue , self.__A )
        
        return self.__A
    

    def getA(self):
        return self.__A
    
    A = property( getA )

    def getF(self):
        return self.__A * self.__M[:]
    
    F = property( getF )
    
    

