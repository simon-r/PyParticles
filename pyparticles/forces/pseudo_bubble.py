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

import scipy.spatial.distance as dist

import pyparticles.pset.opencl_context as occ 

try:
    import pyopencl as cl
except:
    ___foo = 0


class PseudoBubble( fr.Force ) :
    r"""
    Pseudo Bubble is a **fake force** that produce the effect of the bubbles in a fluid.
    
    .. math::
    
        \begin{cases}
         & \text{ if } d_{i,j} < R \,\,\, \text{then} \,\,\,F_{i,j}= -\frac{B}{R}d_{i,j}+\frac{B}{d_{i,j}} \\ 
         & \text{ if } d_{i,j} \geqslant  R \,\,\, \text{then} \,\,\,F_{i,j}= 0
        \end{cases}
    """
    def __init__(self , size , dim=3 , m=None , Consts=( 0.3 , 2.0 ) ):
        self.__dim = dim
        self.__size = size
        
        self.__R = Consts[0]
        self.__B = Consts[1]
        
        self.__A = np.zeros( ( size , dim ) )
        self.__M = np.zeros( ( size , 1 ) )
        
        self.__F = np.zeros( ( size , size ) )
        self.__D = np.zeros( ( size , size ) )
        #self.__bool = np.zeros( ( size , size ) , dtype=np.bool )
        
        self.__V = np.zeros( ( size , size ) )
        
        if m != None :
            self.set_messes( m )
        
    
    def set_masses( self , m ):
        self.__M[:] = m
        
    
    def update_force( self , pset ):
        
        D = self.__D
        
        D[:] = dist.squareform( dist.pdist( pset.X ) )
        ( n , m ) = np.where( np.logical_and( D <= self.__R , D != 0.0 ) )
        
        #print(np.where(b))
        
        self.__F[:] = 0.0
        
        self.__F[n,m] = ( -( self.__B / self.__R ) * D[n,m] + self.__B ) / D[n,m]
        
        for i in range( pset.dim ) :
            self.__V[:,:] = pset.X[:,i]
            self.__V[:,:] = ( self.__V[:,:].T - pset.X[:,i] ).T
            
            self.__A[:,i] = np.sum( self.__F * self.__V[:,:] / self.__M.T , 0 )
        
        return self.__A
    
    def getA(self):
        return self.__A
    
    A = property( getA )
    
    def getF(self):
        return self.__A * self.__M

    F = property( getF )
    
    
class PseudoBubbleOCL( fr.Force ) :
    r"""
    Pseudo Bubble is a **fake force** that produce the effect of the bubbles in a fluid.
        OpenCL version.
    """
    def __init__(self , size , dim=3 , m=None , Consts=( 0.3 , 2.0 ) , ocl_context=None ):
        
        self.__dim = np.int( dim )
        self.__size = np.int( size )
        
        if ocl_context == None :
            self.__occ = occ.OpenCLcontext( size , dim , ( occ.OCLC_X | occ.OCLC_A | occ.OCLC_M )  )
        else :
            self.__occ = ocl_context    
        
        self.__R = self.__occ.dtype( Consts[0] )
        self.__B = self.__occ.dtype( Consts[1] )
        
        self.__A = np.zeros( ( size , dim ) , dtype=self.__occ.dtype )
        
        if m != None :
            self.__occ.M_cla.set( self.__dtype( m ) , queue=self.__occ.CL_queue )
            
        self.__init_prog_cl()
            
        
    def __init_prog_cl(self):
        self.__pseudo_bubble_prg = """
        __kernel void pseudo_bubble( __global const float *X , 
                                     __global const float *M ,
                                                    float  R ,
                                                    float  B , 
                                     __global       float *A )
        {
            int i = get_global_id(0) ;
            int sz = get_global_size(0) ;
            
            float4 at , u ;
            
            u.w = 0.0 ;            
            
            int i0 = 3*i ;
            int i1 = 3*i+1 ;
            int i2 = 3*i+2 ;            
            
            at.x = 0.0 ;
            at.y = 0.0 ;
            at.z = 0.0 ;
            at.w = 0.0 ;            
            
            int n ;
            
            float d , f , dist ;
            
            for( n = 0 ; n < sz ; n++ )
            {
                if ( n == i ) continue ;
                
                u.x = X[i0] - X[3*n] ;
                u.y = X[i1] - X[3*n+1] ;
                u.z = X[i2] - X[3*n+2] ;
                
                dist = length( u ) ;                
                
                if ( dist >= R ) continue ;
                 
                f = ( -1.0 * B/R * dist + B ) / dist  ;
                
                at.x = at.x + u.x * f / M[i] ;
                at.y = at.y + u.y * f / M[i] ;
                at.z = at.z + u.z * f / M[i] ;
            }
            
            A[i0] = at.x ;
            A[i1] = at.y ;
            A[i2] = at.z ;
        }
        """
        
        self.__cl_program = cl.Program( self.__occ.CL_context , self.__pseudo_bubble_prg ).build()        
        
    
    def set_masses( self , m ):
        self.__occ.M_cla.set( self.__occ.dtype( m ) , queue=self.__occ.CL_queue )
        
    
    def update_force( self , pset ):

        self.__occ.X_cla.set( self.__occ.dtype( pset.X ) , queue=self.__occ.CL_queue )
        
        self.__cl_program.pseudo_bubble( self.__occ.CL_queue , ( self.__size , ) , None ,
                                         self.__occ.X_cla.data ,
                                         self.__occ.M_cla.data ,
                                         self.__R ,
                                         self.__B ,
                                         self.__occ.A_cla.data )

        self.__occ.A_cla.get( self.__occ.CL_queue , self.__A )
                
        return self.__A
    
    def getA(self):
        return self.__A
    
    A = property( getA )
    
    def getF(self):
        return self.__A * self.__M

    F = property( getF )
    
    
    
class PseudoBubbleFastOCL( fr.Force ) :
    r"""
    Pseudo Bubble is a **fake force** that produce the effect of the bubbles in a fluid.
        OpenCL version.
    """
    def __init__(self , size , dim=3 , m=None , Consts=( 0.3 , 2.0 ) , domain=( -5.5 , 5.5 ) , ocl_context=None ):
        
        self.__dim = np.int( dim )
        self.__size = np.int( size )
        
        if ocl_context == None :
            self.__occ = occ.OpenCLcontext( size , dim , ( occ.OCLC_X | occ.OCLC_A | occ.OCLC_M )  )
        else :
            self.__occ = ocl_context
            
        self.__R = self.__occ.dtype( Consts[0] )
        self.__B = self.__occ.dtype( Consts[1] )
        
        self.__A = np.zeros( ( size , dim ) , dtype=self.__occ.dtype )
        
        self.__Ix = np.zeros( size , dtype=np.uint32 )
        self.__occ.add_array_by_name( "Ix" , dtype=np.uint32 )
        
        self.__n_sub_dom = np.uint32( ( domain[1] - domain[0] ) / ( 2.0 * self.__R ) + 1.0 ) 
        self.__sub_d_vec = np.zeros( self.__n_sub_dom+1 , dtype=self.__occ.dtype )
        
        self.__sub_d_bd[:] = np.arange( self.__n_sub_dom + 1 ) * ( 2.0 * self.__R )
        self.__sub_d_ind = np.zeros( self.__n_sub_dom + 1 , dtype=np.uint32 )
        
        if m != None :
            self.__occ.M_cla.set( self.__dtype( m ) , queue=self.__occ.CL_queue )
            
        self.__init_prog_cl()
            
        
    def __init_prog_cl(self):
        
        self.__search_domain_bound_prg = """
        __kernel void search_domain_bound( __global const float *X ,
                                           __global const uint  *Ix ,
                                           __global const float *Bd ,
                                           __global       uint  *Ind ,
                                                          uint   inr )
        {
        
            int i = get_global_id(0) ;
            int gs = get_global_size(0) ;
            
            if ( i == 0 )
            {
                Ind[0] = 0 ;
                return ;
            }
            
            if ( i+1 => gs )
            {
                Ind[inr-1] = gs ;
                return ;
            }
                        
            ia = Ix[i] ;
            ib = Ix[i+1] ;
            
            int md =  i % inr ;
            
            if ( X[3*ia] < Bd[l] && X[3*ib] >= Bd[l] )
                Ind[md] = i+1 ;
        }
        """
        
        self.__pseudo_bubble_prg = """
        __kernel void pseudo_bubble( __global const float *X , 
                                     __global const float *M ,
                                     __global const  uint *Ix ,
                                     __global const  uint *Ind ,
                                                     unit  Insz ,
                                     __global const float *Bd ,
                                                    float  R ,
                                                    float  B , 
                                     __global       float *A )
        {
            int i = get_global_id(0) ;
            int sz = get_global_size(0) ;
            
            float4 at , u ;
            
            u.w = 0.0 ;            
            
            int i0 = 3*i ;
            int i1 = 3*i+1 ;
            int i2 = 3*i+2 ;            
            
            at.x = 0.0 ;
            at.y = 0.0 ;
            at.z = 0.0 ;
            at.w = 0.0 ;            
            
            int n , m ;
            int dom ;
            
            float d , f , dist ;
            
            for ( m = 0 ; m < Insz ; m++ ) 
            {
                if( X[i] >= Bd[m] && X[i] >= Bd[m+1] )
                {
                    dom = m ;
                    break ;
                }
            }
            
            for( n = Ind[dom] ; n < Ind[dom+1] ; n++ )
            {
                if ( n == i ) continue ;
                
                u.x = X[i0] - X[3*n] ;
                u.y = X[i1] - X[3*n+1] ;
                u.z = X[i2] - X[3*n+2] ;
                
                dist = length( u ) ;                
                
                if ( dist >= R ) continue ;
                 
                f = ( -1.0 * B/R * dist + B ) / dist  ;
                
                at.x = at.x + u.x * f / M[i] ;
                at.y = at.y + u.y * f / M[i] ;
                at.z = at.z + u.z * f / M[i] ;
            }
            
            A[i0] = at.x ;
            A[i1] = at.y ;
            A[i2] = at.z ;
        }
        """
        
        self.__cl_program = cl.Program( self.__occ.CL_context , self.__pseudo_bubble_prg ).build()        
        
    
    def set_masses( self , m ):
        self.__occ.M_cla.set( self.__occ.dtype( m ) , queue=self.__occ.CL_queue )
        
    
    def update_force( self , pset ):

        self.__Ix[:] = np.argsort( pset.X[:,0] )

        

        self.__occ.X_cla.set( self.__occ.dtype( pset.X ) , queue=self.__occ.CL_queue )
        self.__occ.get_by_name("Ix").set( self.__Ix , queue=self.__occ.CL_queue )
        
        self.__cl_program.pseudo_bubble( self.__occ.CL_queue , ( self.__size , ) , None ,
                                         self.__occ.X_cla.data ,
                                         self.__occ.M_cla.data ,
                                         self.__R ,
                                         self.__B ,
                                         self.__occ.A_cla.data )

        self.__occ.A_cla.get( self.__occ.CL_queue , self.__A )
                
        return self.__A
    
    def getA(self):
        return self.__A
    
    A = property( getA )
    
    def getF(self):
        return self.__A * self.__M

    F = property( getF )