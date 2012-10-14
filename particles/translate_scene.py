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

class TranslateScene(object):
    def __init__( self , w_size ):
        
        self.__v     = np.array( [ 0.0 , 0.0 , 0.0 ] )
        self.__v_old = np.array( [ 0.0 , 0.0 , 0.0 ] )
        
        self.__win_size = ( 800 , 600 )
        
        self.__win_width = 800
        self.__win_height = 600
        
        self.win_size = w_size
        
        self.factor = 100
        self.__fovy   = 2.0
    
    def get_V( self ):
        return self.__v 
    
    def set_V( self , v ):
        self.__v = v
        
    V = property( get_V , set_V )
    
    
    def get_fovy( self ):
        return self.__fovy 
    
    def set_fovy( self , fv ):
        if fv > 2.0 :
            fv = 2.0 
        self.__fovy = fv
        
    fovy = property( get_fovy , set_fovy )    
    
        
    def get_win_size( self ):
        return ( self.__win_width , self.__win_height )
    
    def set_win_size( self , w_size ):
        self.__win_width  = w_size[0]
        self.__win_height = w_size[1]
        
    win_size = property( get_win_size , set_win_size )


    def translate_mapping( self , point ):
        self.__v_old[:] = self.__v[:]
        
        self.__v[0] = ( 2.0 * point[0]   - self.win_size[0] ) / self.win_size[0]
        self.__v[1] = ( self.win_size[1] - 2.0 * point[1] )   / self.win_size[1]
        self.__v[2] = 1.0
        
        
    def on_move( self , point ):
        self.translate_mapping( point )
        
        direction = self.__v - self.__v_old
        
        velocity = np.linalg.norm( direction )
        
        delta = direction * velocity * self.factor * self.fovy
        
        return ( delta[0] , delta[1] )
        
        
        
        