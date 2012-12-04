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

class Logger ( object ):
    """
    Class used for logging the status of the particles system, this class will be used by the ParticlesSet class.
    This class uses a matrix of size [ log_size by pasrticles_size by dim ] for saving the status.
    
    Constructor
    
    :param  pset: A reference to the particles set to be logged.
    :param  log_max_size: The maximal size of the log
    :param  log_X: (default=True) log the positions
    :param  log_V: (default=False) log the velocities  
    """
    def __init__( self , pset , log_max_size , log_X=True , log_V=False ):
        
        self.__pset = pset
        
        self.__log_max_size = log_max_size
        self.__size = 0
        
        self.__log_cnt = 0
        
        self.__La = 0 
        self.__Lb = -1
        
        self.__state = 0
        
        if log_X :
            self.__log_X = np.zeros(( log_max_size , pset.size , pset.dim ))
        else :
            self.__log_X = None
            
        if log_V :
            self.__log_V = np.zeros(( log_max_size , pset.size , pset.dim ))
        else :
            self.__log_V = None
    
    def log( self ):
        """
        Save the current status of the particles-set in the log queue.
        If the log queue is filled it removes the oldest status
        """
        
        self.__log_cnt += 1
        
        if self.__state == 0 :
            self.__size +=1
            self.__Lb += 1

        if self.__state in [ 1 , 2 ] :
            self.__La += 1
            self.__Lb += 1
            
            if self.__La >= self.__log_max_size :
                self.__La = 0
                
            if self.__Lb >= self.__log_max_size :
                self.__Lb = 0

        if self.__state != 0 and self.__La > self.__Lb :
            self.__state = 1

        if self.__state != 0 and self.__La < self.__Lb :
            self.__state = 2

        if self.__state == 0 and self.__Lb >= self.__log_max_size :
            self.__size = self.__log_max_size
            self.__Lb = 0
            self.__La = 1
            self.__state = 1 
                    
        
        if self.__log_X != None :
            self.__log_X[ self.__Lb , : , : ] = self.__pset.X

        if self.__log_V != None :
            self.__log_V[ self.__Lb , : , : ] = self.__pset.V
                    

    def __get_log_indices( self ):
        if self.__state == 0 :
            ind = np.arange( self.__La , self.__Lb+1 , dtype=np.int32 )
            
        elif self.__state == 1 :
            ind = np.concatenate( ( np.arange( self.__La , self.log_max_size , dtype=np.int32 ) , 
                                     np.arange( 0 , self.__Lb+1 , dtype=np.int32 ) ) )
            
        elif self.__state == 2 :
            ind = np.concatenate( ( np.arange( self.__La , self.__Lb , dtype=np.int32 ) , 
                                     np.arange( self.__Lb , self.__log_max_size , dtype=np.int32 ) ) )
         

        return ind
        

    def get_log_array( self , i , log_X=True , log_V=False ):
        """
        Return an numpy array containing the log if the i-th particles 
        
        :param i: Index (or indices) of the particles
        :param log_X: (default=True) return the log of the positions
        :param log_V: (default=False) return the log of the velocities
        
        :returns: A tuple containing the log arrays ( log_x , [log_V] ) 
        """
        
        ind = self.__get_log_indices()
        
        l = list([])
        
        if log_X :
            l.append( self.__log_X[ind,i,:] )
        
        if log_V :
            l.append( self.__log_V[ind,i,:] )
        
        return tuple( l )


    def get_log_indices_segments(self):
        
        d = self.__size
        
        i = np.arange( d , dtype=np.uint )
        f = np.zeros( ( 2*d - 2 ) , dtype=np.uint )
        
        f[2:(2*d-2):2] = i[1:(d-1)]
        f[1:(2*d-2):2] = i[1:]
        
        return f
        
        

    def resize( self , log_max_size ):
        pass
    
    def jump( self ):
        pass

    def get_log_max_size( self ):
        return self.__log_max_size
            
    log_max_size = property( get_log_max_size , doc="get the max allowed size of the log")
    
    
    def get_log_size(self):
        return self.__size
    
    log_size = property( get_log_size )
    
 
    def get_log_X_enabled(self):
        return self.__log_X != None
    
    def get_log_V_enabled(self):
        return self.__log_V != None


    log_V_enabled = property( get_log_V_enabled , doc="return true if the logging of the position is enabled")
    log_X_enabled = property( get_log_X_enabled , doc="return true if the logging of the velocity is enabled")
             
             