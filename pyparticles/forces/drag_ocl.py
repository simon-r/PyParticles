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
except:
    ___foo = 0


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
        if m != None :
            self.set_masses( m )
        
        
    
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
    
    def set_masses( self , m ):
        self.__M[:] = m
    
    
    def update_force( self , pset ):
        pass
    

    def getA(self):
        return self.__A
    
    A = property( getA )


    def getF(self):
        return self.__A * self.__M[:,0]
    
    F = property( getF )