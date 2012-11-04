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

import pyparticles.geometry.transformations as tr

import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    _____foo = None
    
    
class AxisOgl(object):
    def __init__(self):
        self.__arrow_len = 5.0
        self.__dl_axis = None
    
    def ogl_init( self ):
        
        self.__dl_axis = glGenLists(1)
        
        glNewList( self.__dl_axis , GL_COMPILE );
        self.draw_axis_procedure()
        glEndList()
        
        
    def get_axis_len(self):
        return self.__arrow_len
    
    def set_axis_len( self , leng ):
        self.__arrow_len = leng
        
    axis_len = property( get_axis_len , set_axis_len )
    
    def draw_axis( self ):
        glCallList( self.__dl_axis )
    
       
    def draw_axis_procedure(self):
        self.draw_arrow( ( 1.0 , 0.0 , 0.0 ) , "x" )
        self.draw_arrow( ( 0.0 , 1.0 , 0.0 ) , "y" )
        self.draw_arrow( ( 0.0 , 0.0 , 1.0 ) , "z" )
    
        self.draw_arrow( ( 1.0 , 0.0 , 0.0 ) , "-x" )
        self.draw_arrow( ( 0.0 , 1.0 , 0.0 ) , "-y" )
        self.draw_arrow( ( 0.0 , 0.0 , 1.0 ) , "-z" )
            
        for pl in self.axis_planes_codes():
            self.draw_plane( pl )  
    
    def axis_planes_codes(self):
        return [ "xy" , "x-y" , "-xy" , "-x-y" , "xz" , "x-z" , "-xz" , "-x-z" , "yz" , "y-z" , "-yz" , "-y-z"  ]
    
    
    def draw_plane( self , plane="xy", color=( 0.7 , 0.7 , 0.7 , 0.3 ) , leng=None ):
        
        if leng == None :
            leng = self.axis_len
            
        
        t = tr.Transformations()
        
        if plane == "xy" :
            t.rotX( np.radians(0) )
        elif plane == "yz" :
            t.rotY( np.radians(90) )
        elif plane == "xz" :
            t.rotX( np.radians(90) )
        elif plane == "-yz" :
            t.rotX( np.radians(180) )
            t.rotY( np.radians(90) )
        elif plane == "-y-z" :
            t.rotX( np.radians(180) )
            t.rotY( np.radians(-90) )
        elif plane == "y-z" :
            t.rotY( np.radians(-90) )
        elif plane == "x-y" :
            t.rotX( np.radians(180) )
        elif plane == "-x-y" :
            t.rotX( np.radians(180) )
            t.rotY( np.radians(180) )
        elif plane == "x-z" :
            t.rotX( np.radians(-90) )
        elif plane == "-x-z" :
            t.rotX( np.radians(-90) )
            t.rotZ( np.radians(180) )
        elif plane == "-xz" :
            t.rotX( np.radians(90) )
            t.rotZ( np.radians(180) )
        elif plane == "-x-z" :
            t.rotX( np.radians(-90) )
            t.rotZ( np.radians(180) )
        elif plane == "-xy" :
            t.rotY( np.radians(180) )
        
        glColor4f( color[0] , color[1] , color[2] , color[3] )
        
        glBegin(GL_LINES)
        for i in range( 1 , int(leng) ):
            
            pt1 = np.matrix( [ float(i) ,  0.0 , 0.0 ] ).T
            pt2 = np.matrix( [ float(i) , leng , 0.0 ] ).T
            
            pt1[:] = t.transformv( pt1 )
            pt2[:] = t.transformv( pt2 )
            
            glVertex3fv( pt1 )
            glVertex3fv( pt2 )
            
            
            pt1 = np.matrix( [ 0.0  , float(i) , 0.0 ] ).T
            pt2 = np.matrix( [ leng , float(i) , 0.0 ] ).T            
            
            pt1[:] = t.transformv( pt1 )
            pt2[:] = t.transformv( pt2 )            
            
            glVertex3fv( pt1 )
            glVertex3fv( pt2 )
            
        glEnd()
        
        #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        #
        #glColor4f( color[0] , color[1] , color[2] , color[3]/0.5 )
        
        #glBegin( GL_TRIANGLES )
        #
        #glNormal3f( 0.0 , 0.0 , 1.0 )
        #glVertex3f( 0.0  , 0.0  , 0.0 )
        #glVertex3f( leng , 0.0  , 0.0 )
        #glVertex3f( leng , leng , 0.0 )
        #
        #glNormal3f( 0.0 , 0.0 , 1.0 )
        #glVertex3f( 0.0  , 0.0  , 0.0 )
        #glVertex3f( leng , leng , 0.0 )
        #glVertex3f( 0.0  , leng , 0.0 )
        #
        #glEnd()
        
                
        
    def draw_arrow( self , color , axis , leng=None ):
        
        if leng == None :
            leng = self.axis_len
            
        arrh = leng * 0.1
        arrp = leng - arrh
        
        dash = leng * 0.03
        
        t = tr.Transformations()
        t.set_points_tuple_size(2)
        
        if axis == "x" :
            t.rotX( np.radians(0) ) 
        elif axis == "y" :
            t.rotZ( np.radians(90) ) 
        elif axis == "z" :
            t.rotY( np.radians(-90) ) 
        if axis == "-x" :
            t.rotZ( np.radians(180) ) 
        elif axis == "-y" :
            t.rotZ( np.radians(-90) ) 
        elif axis == "-z" :
            t.rotY( np.radians(90) ) 
                
        t.append_point( np.array( [ 0.0  , 0.0 , 0.0 ] ) )
        t.append_point( np.array( [ leng , 0.0 , 0.0 ] ) )
        
        t.append_point( np.array( [ leng ,   0.0 , 0.0 ] ) )
        t.append_point( np.array( [ arrp , -arrh , 0.0 ] ) )
        
        t.append_point( np.array( [ leng ,  0.0 , 0.0 ] ) )
        t.append_point( np.array( [ arrp , arrh , 0.0 ] ) )        
        
        for i in range( 1 , int(leng) ):
            t.append_point( [ float(i) ,  dash , 0.0 ] )
            t.append_point( [ float(i) , -dash , 0.0 ] )
        
        glColor3f( color[0] , color[1] , color[2] )
        
        glBegin(GL_LINES)
        
        for pts in t :
            glVertex3fv( pts[0] )
            glVertex3fv( pts[1] )
        
            
        glEnd()
        
        
        
        