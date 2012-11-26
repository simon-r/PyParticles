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

import sys

class Transformations( object ):
    """
    Class used for administrate 3D transformations matrix using an OpenGl like method with a push_matrix & pop_matrix model. This method is very confortable if we want to create articulated geometric structures with a lot of subobjects and relative coordinates.
    
    Example: ::
        
            t = tr.Transformations() # init transfomation
    
            t.set_points_tuple_size(2) # Pairwise points in the queue
            
            t.rotY( np.radians(90) )  # Apply some transoformations matricies
            t.rotX( np.radians(90) )  
            t.rotZ( np.radians(90) )
            # Now the current matrix is: Ry(90) * Rx(90) * Rz(90)
            
            t.append_point( list( [1,0,0] ) )      # Append some poits. It accept every Indexable type 
            t.append_point( np.array( [1,1,0] ) )  # The preview transoformations are applied on these points
            t.append_point( np.array( [1,1,1] ) )
            t.append_point( np.array( [0,1,1] ) )    
            
            t.push_matrix() # push the current matrix
            
            t.translation( 10 , 2 , 2 ) # Apply a translation
            # Now the current matrix is: Ry(90) * Rx(90) * Rz(90) * Tr( [ 10 , 2 , 2 ]  )
            
            t.append_point( [1,1,1] )
            t.append_point( np.matrix( [0,1,1] ).T ) # Only vertical matrix
            
            t.pop_matrix() # Back to the old matrix
            # Now the current matrix is newly: Ry(90) * Rx(90) * Rz(90)
            
            t.append_point( np.array( [1,0,0] ) )
            t.append_point( [1,1,0] )
            t.append_point( np.array( [1,1,1] ) )
            t.append_point( [0,1,1] )
            
            # Print the resulting points (in a paiwise tuple)
            # Attention: the points are removed from the queue during the iteration.
            for p in t :
                # p is a tuple ( p1 , p2 ) see the function: t.set_points_tuple_size(2)
                print( p[0] )
                print( p[1] )
                
    
    """
    def __init__(self):
        self.__cmatrix = np.matrix( np.eye( 4 ) )
        self.__stack = list( [] )
        self.__points = deque( [] )
        
        self.__p = np.matrix( np.zeros( ( 4,1 ) ) )
        self.__nr = 1
        
    def __iter__(self):
        return self

    if sys.version_info[0] == 3:    
        def __next__(self):
            """
            iterate over the points in the queue, it pop and returns the transformed points.
            The popped points in the queue are cancelled during the itarations.
            """
            if len( self.__points ) == 0 :
                raise StopIteration
            else :
                p = self.pop_points()
                
            return p
    else:
        def next(self):
            """
            iterate over the points in the queue, it pop and returns the transformed points.
            The popped points in the queue are cancelled during the itarations.
            """
            if len( self.__points ) == 0 :
                raise StopIteration
            else :
                p = self.pop_points()
                
            return p

    def identity(self):
        """
        Set the current matrix to the identity 
        """
        self.__cmatrix = np.matrix( np.eye( 4 ) )
    
    def push_matrix(self):
        """
        Push in the stack a copy of the current matrix
        """
        self.__stack.append( np.copy( self.__cmatrix ) )
    
    def pop_matrix(self):
        """
        Pop and copy in the current matrix the last matrix in the stack 
        """
        m = self.__stack.pop()
        self.__cmatrix[:] = m[:]
      
    def clear(self):
        """
        Clear the stack, the points in the queue and set to the identity the current matrix
        """
        del self.__stack
        self.__stack = list( [] )
        
        del self.__points
        self.__points = deque( [] )
        
        self.__cmatrix[:] = np.matrix( np.eye( 4 ) )
    
    
    def set_points_tuple_size( self , nr ):
        """
        The points are organized by tuples of size nr. That's useful if you want to draw triangles squares or lines,
        where the size of the tupre are respectively 3, 4 and 2.
        """
        if nr < 1 :
            raise ValueError
        
        self.__nr = int( nr )
        
    def append_point( self , pt ):
        """
        Transforms and append a new point in the points queue
        
        Argument:
            pt : point coord: [ x , y , z ]
        """
        nwp = np.matrix( np.zeros( ( 4 , 1 ) ) )
        
        nwp[0] = pt[0]
        nwp[1] = pt[1]
        nwp[2] = pt[2]
        nwp[3] = 1.0
        
        self.__points.append( self.transformv( nwp ) )
    
    def pop_points( self ):
        """
        Returns the firsts #nr of points in the point queue, the returned points are organized in a tuple
        """
        if len( self.__points ) == 0 :
            return None
        
        l = list()
        
        for i in range(self.__nr) :
            p = self.__points.popleft()
            l.append( p )
        
        return tuple(l)
        
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
        Transform the point ( x , y , z ) according to the current matrix and returns a 3 by 1 matrix containig the resulting point
        """
        self.__p[0] = x
        self.__p[1] = y
        self.__p[2] = z
        self.__p[3] = 1.0
      
        return (self.__cmatrix[:] * self.__p)[:3]
    
    def transformv( self , pt ):
        """
        Transform the point pt: [ x , y , z ] according to the current matrix and returns a 3 by 1 matrix containig the resulting point
        """
        self.__p[0] = pt[0]
        self.__p[1] = pt[1]
        self.__p[2] = pt[2]
        self.__p[3] = 1.0
      
        return (self.__cmatrix[:] * self.__p)[:3] 
    
    
    def rotate( self , angle , x , y , z ):
        """
        Apply the rotation matrix around the axis [ x , y , z ] of the angle: *angle*
        """
        n = np.array( [ x , y , z ] )
        
        n = n / np.linalg.norm( n )
        
        ux = n[0]
        uy = n[1]
        uz = n[2]
        
        sa = np.sin( angle )
        ca = np.cos( angle )
        
        m = np.matrix ( [
                        [ ux**2 + ca*(1. - ux**2)   , ux*uy*(1.-ca)-uz*sa     , uz*ux*(1.-ca) + uy*sa  , 0.0 ] ,
                        [ ux*uy * (1. - ca) + uz*sa , uy**2 + ca*(1.-uy**2)   , uy*uz*(1.-ca) - ux*sa  , 0.0 ] ,
                        [ uz*ux*(1.-ca)-uy*sa       , uy*uz*(1.-ca)+ux*sa     , uz**2+ca*(1.-uz**2)    , 0.0 ] ,
                        [ 0.0                       , 0.0                     , 0.0                    , 1.0 ] 
                        ] )
    
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
    
      
    def rotX( self , angle ):
        """
        Apply the rotation around the x axis
        """
        m = np.matrix( np.eye( 4 ) )
        
        m[1,1] =  np.cos( angle )
        m[2,2] =  np.cos( angle )
        
        m[2,1] =  np.sin( angle )
        m[1,2] = -np.sin( angle )
        
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]

        
    def rotY( self , angle ):
        """
        Apply the rotation around the y axis 
        """
        m = np.matrix( np.eye( 4 ) )
        
        m[0,0] =  np.cos( angle )
        m[2,2] =  np.cos( angle )
        
        m[0,2] =  np.sin( angle )
        m[2,0] = -np.sin( angle )
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
    
    
    def rotZ( self , angle ):
        """
        Apply the rotation around the z axis 
        """        
        
        m = np.matrix( np.eye( 4 ) )
        
        m[0,0] =  np.cos( angle )
        m[1,1] =  np.cos( angle )
        
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
        
    def shearX( self , a , b ):
        """
        Apply the shearing along X axis using the values a b
        ::
          SH_X(a,b) = [ 1 0 0 0 
                        a 1 0 0 
                        b 0 1 0 
                        0 0 0 1 ]
        
        """        
        m = np.matrix( np.eye( 4 ) )
        
        m[1,0] = a
        m[2,0] = b
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
        
    
    def shearY( self , a , b ):
        """
        Apply the shearing along Y axis using the values a b
        ::
        
          SH_Y(a,b) = [ 1 a 0 0 
                        0 1 0 0 
                        0 b 1 0 
                        0 0 0 1 ]
        
        """        
        m = np.matrix( np.eye( 4 ) )
        
        m[0,1] = a
        m[2,1] = b
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
        
    def shearZ( self , a , b ):
        """
        Apply the shearing along Z axis using the values a b
        ::
        
         SH_Z(a,b) = [ 1 0 a 0 
                       0 1 b 0 
                       0 0 1 0 
                       0 0 0 1 ]        
        
        """        
        m = np.matrix( np.eye( 4 ) )
        
        m[0,2] = a
        m[1,2] = b
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
        

    def reflection( self , a , b , c  ) :
        """
        Apply the reflection through the plane: ax + by + cz = 0
        """
        m = np.matrix ( [
                        [  1.0 - 2.0*a**2 , -2.0*a*b       , -2.0*a*c         , 0.0 ] ,
                        [ -2.0*a*b        , 1.0 - 2.0*b**2 , -2.0*b*c         , 0.0 ] ,
                        [ -2.0*a*b        , -2.0*b*c       , 1.0 - 2.0*c**2   , 0.0 ] ,
                        [ 0.0             , 0.0            , 0.0              , 1.0 ] 
                        ] )
        
        self.__cmatrix[:] = self.__cmatrix[:] * m[:]
        
        
        
        
        
        
    
    
