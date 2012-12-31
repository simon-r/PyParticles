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
import pyparticles.ode.ode_solver as os
import pyparticles.pset.opencl_context as occ 

try:
    import pyopencl as cl
except:
    ___foo = 0


class EulerSolver( os.OdeSolver ) :
    def __init__( self , force , p_set , dt ):
        super(EulerSolver,self).__init__( force , p_set , dt )
        
    
    def __step__( self , dt ):

        self.force.update_force( self.pset )
        
        self.pset.V[:] = self.pset.V + self.force.A * dt
        self.pset.X[:] = self.pset.X + self.pset.V * dt
        
        self.pset.update_boundary() 
        

class EulerSolverConstrained( os.OdeSolverConstrained ) :
    def __init__( self , force , p_set , dt , x_constraint=None , v_constraint=None ):
        super(EulerSolverConstrained,self).__init__( force , p_set , dt , x_constraint=None , v_constraint=None )
        
        if x_constraint != None :
            self.x_constraint = x_constraint
        

    def get_x_constraint(self):
        return super(EulerSolverConstrained,self).get_x_constraint()
    
    def set_x_constraint(self ,  xc ):
        super(EulerSolverConstrained,self).set_x_constraint( xc )
        self.__free_inx = self.x_constraint.get_cx_free_indicies()
        self.__csrt_inx = self.x_constraint.get_cx_indicies()
    
    x_constraint = property( get_x_constraint , set_x_constraint , doc="get and set the current positionals constraints" )
    
    
    def __step__( self , dt ):

        self.force.update_force( self.pset )
        
        self.pset.V[self.__free_inx,:] = self.pset.V[self.__free_inx,:] + self.force.A[self.__free_inx,:] * dt
        self.pset.X[self.__free_inx,:] = self.pset.X[self.__free_inx,:] + self.pset.V[self.__free_inx,:] * dt
        
        self.pset.V[self.__csrt_inx,:] = 0.0
        
        self.pset.update_boundary() 
        

class EulerSolverOCL( os.OdeSolver ) :
    def __init__( self , force , p_set , dt , ocl_context=None ):
        super(EulerSolverOCL,self).__init__( force , p_set , dt )
        
        if ocl_context == None :
            self.__occ = occ.OpenCLcontext( self.pset.size , self.pset.dim , ( occ.OCLC_X | occ.OCLC_V | occ.OCLC_A )  )
        else :
            self.__occ = ocl_context
            
        self.__init_prog_cl()
                    
    
    def __init_prog_cl(self):
        self.__euler_prg = """
        __kernel void euler( __global       float *V , 
                             __global const float *A , 
                             __global       float *X ,
                                            float  dt )
        {
            int i = get_global_id(0) ;
            
            V[3*i]   = V[3*i]   + A[3*i]*dt ;
            V[3*i+1] = V[3*i+1] + A[3*i+1]*dt ;
            V[3*i+2] = V[3*i+2] + A[3*i+2]*dt ;
            
            X[3*i]   = X[3*i]   + V[3*i]*dt ;
            X[3*i+1] = X[3*i+1] + V[3*i+1]*dt ;
            X[3*i+2] = X[3*i+2] + V[3*i+2]*dt ;       
        }
        """
        
        self.__cl_program = cl.Program( self.__occ.CL_context , self.__euler_prg ).build()
        
    
    def __step__( self , dt ):
        
        self.force.update_force( self.pset )
        
        dtype = self.__occ.dtype
        
        self.__occ.V_cla.set( dtype( self.pset.V ) , queue=self.__occ.CL_queue )
        self.__occ.A_cla.set( dtype( self.force.A ) , queue=self.__occ.CL_queue )
        self.__occ.X_cla.set( dtype( self.pset.X ) , queue=self.__occ.CL_queue )
        
        self.__cl_program.euler( self.__occ.CL_queue , ( self.pset.size , ) , None , 
                                 self.__occ.V_cla.data ,
                                 self.__occ.A_cla.data , 
                                 self.__occ.X_cla.data ,
                                 np.float32( dt ) )
        
        self.__occ.X_cla.get( self.__occ.CL_queue , self.pset.X )
        self.__occ.V_cla.get( self.__occ.CL_queue , self.pset.V )
                
        self.pset.update_boundary() 
        





