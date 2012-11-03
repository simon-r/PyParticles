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

class Transformations( object ):
    """
    Class used for adiministrating 3D transformations matrix with an openGl like method with a push & pop model
    """
    def __init__(self):
        self.__cmatrix = np.matrix( np.eye( 4 ) )
        self.__stack = list( [] )

        self.__p = np.matrix( np.zeros( ( 4,1 ) ) )

    def identity(self):
        """
        Set the current matrix to the identity 
        """
        self.__cmatrix = np.matrix( np.eye((4,4)) )
    
    def push(self):
        """
        Push in the stack a copy of the current matrix
        """
        self.__stack.append( np.copy( self.__cmatrix ) )
    
    def pop(self):
        """
        Pop and copy in the current matrix the last matrix in the stack 
        """
        m = self.__stack.pop()
        self.__cmatrix[:] = m
      
    
    def get_matrix( self ):
        """
        Returns a copy of the current matrix
        """
        return np.copy( self.__cmatrix )
    
    def set_matrix( self , m ):
        """
        set the current matrix to m
        """
        self.__cmatrix[:] = m[:]
      
    matrix = property( get_matrix , set_matrix )
      
      
    def transform( self , x , y , z ):
        """
        Transform the point ( x , y , z ) according to the current matrix and returns a 4 by 1 matrix containig the resulting point
        """
        self.__p[0] = x
        self.__p[1] = y
        self.__p[2] = z
        self.__p[3] = 1.0
      
        return self.__cmatrix[:] * p
    
    def rotate( self , angle , x , y , z ):
        """
        Apply the rotation matrix around the axis [ x , y , z ] of the angle: *angle*
        """
        n = np.matrix( [[x],[y],[z],[1.0]] )
        
        n[:] = n / np.linalg.norm( a )
        
        sa = np.sin( angle )
        ca = np.cos( angle )
        
        m = np.matrix ( [
                        [ ca + n[0]**2.*(1.-ca) , 0 , 0 , 0 ] ,
                        [ 0 , 0 , 0 , 0 ] ,
                        [ 0 , 0 , 0 , 0 ] ,
                        [ 0 , 0 , 0 , 1.0 ] 
                        ] )
    
      
    def rotX( self , angle ):
        """
        Apply the rotation around the x axis
        """
        m = np.matrix( np.eye( 4 ) )
        
        m[0,0] =  np.cos( angle )
        m[1,1] = -np.cos( angle )
        
        m[1,2] = -np.sin( angle )
        m[2,1] =  np.sin( angle )
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]

        
    def rotY( self , angle ):
        """
        Apply the rotation around the y axis 
        """
        m = np.matrix( np.eye( 4 ) )
        
        m[1,1] =  np.cos( angle )
        m[2,2] = -np.cos( angle )
        
        m[0,2] =  np.sin( angle )
        m[2,0] = -np.sin( angle )
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
    
    
    def rotZ( self , angle ):
        """
        Apply the rotation around the z axis 
        """        
        
        m = np.matrix( np.eye( 4 ) )
        
        m[0,0] =  np.cos( angle )
        m[1,1] = -np.cos( angle )
        
        m[0,1] = -np.sin( angle )
        m[1,0] =  np.sin( angle )
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
        
        
    def translation( self , x , y , z ):
        """
        apply the translation with the vector [x y z]
        """
        
        m = np.matrix( np.eye( 4 ) )
        
        m[0,3] = x
        m[1,3] = y
        m[2,3] = z
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
        
        
    def scale( self , x , y , z ):
        """
        Apply the scale with values x y z
        """
        
        m = np.matrix( np.eye( 4 ) )
        
        m[0,0] = x
        m[1,1] = y
        m[2,2] = z
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]        

