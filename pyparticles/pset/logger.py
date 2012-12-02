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

class logger ( object ):
    def __init__( self , pset , log_max_size , log_X=True , log_V=False ):
        
        self.__pset = pset
        
        self.__log_max_size = log_max_size
        self.__size = 0
        
        self.__log_cnt = 0
        
        self.__La = 0 
        self.__Lb = 0
        
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
        
        self.__log_cnt += 1
        
        if self.__log_X != None :
            self.__log_X[ self.__Lb , : , : ] = self.__pset.X

        if self.__log_V != None :
            self.__log_V[ self.__Lb , : , : ] = self.__pset.V
        
        if self.__state == 0 :
            self.__size +=1
            self.__Lb += 1

        if self.__state in [ 1 , 2 ] :
            self.__La += 1
            self.__Lb += 1
            
            if self.__La > self.__log_max_size :
                self.__La = 0
                
            if self.__Lb > self.__log_max_size :
                self.__Lb = 0

        if self.__state != 0 and self.__La > self.__Lb :
            self.__state = 1

        if self.__state != 0 and self.__La < self.__Lb :
            self.__state = 2

        if self.__state == 0 and self.__size > self.__log_max_size :
            self.__size = self.__log_max_size
            self.__state = 1 
            


    def get_log_max_size( self ):
        return self.__log_max_size
    
    def set_log_max_size( self , log_max_size ):
        self.__log_max_size = log_max_size
        
    log_max_size = property( get_log_max_size , set_log_max_size , doc="set and get the max allowed size of the log")
    
    
    def get_log_size(self):
        return self.__log_len
    
    log_size = property( get_log_size )
    
 
    def get_log_X_enabled(self):
        return ( self.__log_X != None )
    
    def get_log_V_enabled(self):
        return ( self.__log_V != None )


    log_V_enabled = property( get_log_V_enabled , doc="return true if the logging of the position is enabled")
    log_X_enabled = property( get_log_X_enabled , doc="return true if the logging of the velocity is enabled")
             