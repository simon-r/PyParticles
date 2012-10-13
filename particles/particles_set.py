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
from collections import deque

class ParticlesSet(object):
    """
    The main class for storing the particles data set.
    Constructor arguments:
        ============= =============== =======================================================
        size:         (default 0)     Number of particles
        dim :         (default 3)     dimensions of the system 2 or 3 ... 2D 3D
        mass:         (dafault True)  if True the particles have a mass, a charge ...
        label:        (default False) if true it's possible to set a name for each particle
        velocity:     (dafault True)  if true the particles has a velocity
        log_X:        (default False) if true it's possible to logging the position
        log_V:        (default False) if true it's possible to logging the velocity
        log_max_size: (default 0) set the maximal size of the log queue
        ============= =============== =======================================================
    """
    def __init__( self , size=1 , dim=3 , boundary=None ,
                 label=False , mass=True , velocity=True ,
                 log_X=False , log_V=False , log_max_size=0 ):
        
        if size < 0 :
            raise
        
        self.__X = np.zeros((size,dim))
        
        if velocity:
            self.__V = np.zeros((size,dim))
        else:
            self.__V = None
        
        if mass :
            self.__mass = np.zeros((size,1))
        else:
            self.__mass = None
        
        if not label :
            self.__label = None
        else:
            self.__label = list( "" for i in range(size) )
        
        self.__size = int( size )
        self.__dim  = int( dim )
        self.__centre_mass = None
        
        self.__bound = boundary
        
        self.__unit = 1.0
        self.__mass_unit = 1.0
        
        if log_X == True :
            self.__log_X = deque([])
        else :
            self.__log_X = None
            
        if log_V == True :
            self.__log_V = deque([])
        else :
            self.__log_V = None
            
        self.__log_max_size = log_max_size
        self.__log_len = 0
        
        
    def realloc( self , size , dim , boundary=None ,
                 label=False , mass=True , velocity=True ,
                 log_X=False , log_V=False , log_max_size=0 ):
        
        del self.__X
        del self.__V
        del self.__mass
        del self.__label
        del self.__log_X
        del self.__log_V
        
        self.__init__( size , dim , boundary , label , mass , velocity , log_X , log_V , log_max_size )
        
        

    def getX(self):
        return self.__X
    
    X = property( getX , doc="return the reference to the array of the positions" )
    
    def getM(self):
        return self.__mass
    
    M = property( getM , doc="return the reference to the array of the masses" )
    
    def getV(self):
        return self.__V
    
    V = property( getV , doc="return the reference to the velocities array" )

    def update_boundary( self ):
        """ Update the particle set according to the boudary rule"""
        if self.__bound != None :
            self.__bound.boundary( self )
        
    def get_boundary( self ):
        return self.__bound
    
    def set_boundary( self , boundary):
        self.__bound = boundary

    boundary = property( get_boundary , set_boundary , "return the reference to the boudary, None if the boudary are not set or open")

    
    def get_log_max_size( self ):
        return self.__log_max_size
    
    def set_log_max_size( self , log_max_size ):
        self.__log_max_size = log_max_size
    
    log_max_size = property( get_log_max_size , set_log_max_size , "set and get the max allowed size of the log")
    
    
    def enable_log( self , log_X=True , log_V=False , log_max_size=0 ):
        if ( not self.log_X_enabled ) and log_X :
            self.__log_X = deque([])
            
        if ( not self.log_V_enabled ) and log_V :
            self.__log_V = deque([])
            
        self.log_max_size = log_max_size
            
    
    def get_log_size(self):
        return self.__log_len
    
    log_size = property( get_log_size )

    def get_log_X_enabled(self):
        return ( self.__log_X != None )
    
    def get_log_V_enabled(self):
        return ( self.__log_V != None )

    def get_log_enabled(self):
        return ( self.log_V_enabled or self.log_X_enabled )

    log_V_enabled = property( get_log_V_enabled , doc="return true if the logging of the position is enabled")
    log_X_enabled = property( get_log_X_enabled , doc="return true if the logging of the velocity is enabled")
    
    log_enabled = property( get_log_enabled , doc="return true if the logging of position or velocity is enabled")

    

    def log(self):
        """
        if the log is enable, save the current satus in the log queue.
        The last element of the queue will be removed if we reach the max allowed size
        """
        delta_x = 0
        delta_v = 0
        
        if self.__log_X != None :
            lX = np.zeros(( self.size , self.dim ))
            lX[:] = self.X
            
            #print(lX)
            
            if self.log_size > self.log_max_size :
                self.__log_X.popleft()
                delta_x -= 1
            
            self.__log_X.append( lX )
            delta_x += 1
        
        if self.__log_V != None :
            lV = np.zeros(( self.size , self.dim ))
            lV[:] = self.V
            
            if self.log_size > self.log_max_size :
                self.__log_V.popleft()
                delta_v -= 1
            
            self.__log_V.append( lV )
            delta_v+=1
            
        #print( self.__log_X )
        self.__log_len += max( [ delta_x , delta_v ]  )
        
            

    def get_logX( self ):
        return self.__log_X
        
    def get_logV( self , i ):
        return self.__log_V
    
    logX = property( get_logX , doc="return the log queue X: position" )
    logV = property( get_logV , doc="return the log queue V: velocity" )
    

    def set_unit( self , u ):
        self.__unit = u
        
    def get_unit(self):
        return self.__unit
    
    unit = property( get_unit , set_unit )
    
    def set_mass_unit( self , u ):
        self.__mass_unit = u
        
    def get_mass_unit(self):
        return self.__mass_unit
    
    mass_unit = property( get_mass_unit , set_mass_unit )
    
    
    def update_centre_of_mass(self):
        self.__centre_mass = np.sum( self.__X * self.__mass , axis=0 ) / np.float( self.__size )
        return self.__centre_mass
        
    def centre_of_mass(self):
        return self.__centre_mass
    
    def get_dim(self):
        return self.__dim
    
    def get_size( self ):
        return self.__size
    
    dim = property( get_dim )
    size = property( get_size )
    
    def add_clusters( self , Cs , n ):
        i = 0
        for c in Cs:
            self.__X[n[i]:n[i]+C.shape[0]] = c
            i = i + 1
            
    