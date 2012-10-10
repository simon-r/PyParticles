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

import particles.particles_set as ps

import particles.animation as pan

import particles.rand_cluster as clu
import particles.gravity as gr
import particles.euler_solver as els
import particles.leapfrog_solver as lps
import particles.runge_kutta_solver as rks

import matplotlib.animation as animation

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import particles.periodic_boundary as pb
import particles.rebound_boundary as rb
import particles.const_force as cf
import particles.vector_field_force as vf
import particles.linear_spring as ls
import particles.trackball as trk
import particles.axis_ogl as axgl
import particles.translate_scene as tran

import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    _____foo = None

    
    
def InitGL( Width , Height , ReSizeFun ):                # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
    
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glEnable (GL_LINE_SMOOTH)
    glHint( GL_LINE_SMOOTH_HINT , GL_NICEST )
    
    ReSizeFun(Width, Height)
    

def DrawGLScene():
    
    j = next(DrawGLScene.stream)
    
    tr = DrawGLScene.animation.translation
    unit = DrawGLScene.animation.pset.unit
    
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    
    glEnable (GL_FOG)
    glFogf (GL_FOG_DENSITY, 0.05)
    
    glLoadIdentity()  
    
    if DrawGLScene.animation.state == "trackball_down" and DrawGLScene.animation.motion:
        ( ax , ay , az ) = DrawGLScene.animation.rotatation_axis
        angle = DrawGLScene.animation.rotation_angle
        glRotatef( angle , ax , ay , az )
        DrawGLScene.animation.motion = False
        
    glMultMatrixf( DrawGLScene.animation.rot_matrix )
    # save the rot matrix
    DrawGLScene.animation.rot_matrix = glGetFloatv( GL_MODELVIEW_MATRIX )
    
    glLoadIdentity()
    
    glTranslatef( tr[0] , tr[1] , -15.0 )          
    glMultMatrixf( DrawGLScene.animation.rot_matrix )

    glEnable(GL_POINT_SMOOTH)
        
    DrawGLScene.animation.axis.draw_axis()
    
    glPointParameterf( GL_POINT_SIZE_MAX , 10.0 )
    glPointParameterf( GL_POINT_SIZE_MIN , 0.1 )    
    
    for i in range( DrawGLScene.animation.pset.size() ):
        glPointSize( DrawGLScene.animation.pset.M[i] )
        glBegin(GL_POINTS)
        glColor3f( 1.0 , 1.0 , 1.0 )    
        #glPointSize( DrawGLScene.animation.pset.M[i] )
        glVertex3f( DrawGLScene.animation.pset.X[i,0] / unit ,
                    DrawGLScene.animation.pset.X[i,1] / unit ,
                    DrawGLScene.animation.pset.X[i,2] / unit )

        glEnd()
    
    glutSwapBuffers()


def ReSizeGLScene(Width, Height):
    
    if Height == 0:                        
        Height = 1

    per = ReSizeGLScene.animation.perspective
    
    MousePressed.animation.win_size = ( Width , Height )

    glViewport(0, 0, Width, Height)        
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective( per[0] , float(Width)/float(Height), per[1] , per[2] )
    glMatrixMode(GL_MODELVIEW)

   
def KeyPressed():
    pass

def MousePressed(  button , state , x , y ):
    #print ("--------------------")
    #print ( "click" )
    #print ( "  butt  " + str( button ) )
    #print ( "  state " + str(state ) )
    #print ( "  x     " + str(x) )
    #print ( "  y     " + str(y) )
    
    if state == GLUT_DOWN and button == GLUT_LEFT_BUTTON :
        MousePressed.animation.trackball.track_ball_mapping( np.array( [ x , y ] ) )
        MousePressed.animation.state = "trackball_down"
    elif state == GLUT_UP and button == GLUT_LEFT_BUTTON :
        MousePressed.animation.state = "trackball_up"
    
        
    if state == GLUT_DOWN and button == GLUT_RIGHT_BUTTON :
        MousePressed.animation.translate_scene.translate_mapping( np.array( [ x , y ] ) )
        MousePressed.animation.state = "translate_down" 
    elif state == GLUT_UP and button == GLUT_RIGHT_BUTTON :
        MousePressed.animation.state = "translate_up" 
    
    
    if state == GLUT_DOWN and button == 3 :
        MousePressed.animation.zoom_scene( +1 )
        
    if state == GLUT_DOWN and button == 4 :
        MousePressed.animation.zoom_scene( -1 )
    

def MouseMotion( x , y ) :
    #print ("--------------------")
    #print ( "move" )
    #print ( "  x     " + str(x) )
    #print ( "  y     " + str(y) )
    
    if MousePressed.animation.state == "trackball_down" :
        ( axis , angle ) = MousePressed.animation.trackball.on_move( np.array( [ x , y ] ) )
    
        MousePressed.animation.rotation_angle = angle 
        MousePressed.animation.rotatation_axis = ( axis[0] , axis[1] , axis[2] )
    
        MousePressed.animation.motion = True
    
    elif MousePressed.animation.state == "translate_down" :
        ( dx , dy ) = MousePressed.animation.translate_scene.on_move( np.array( [ x , y ] ) )
        ( tx , ty ) = MousePressed.animation.translation
        MousePressed.animation.translation = ( tx + dx , ty + dy )
        
        MousePressed.animation.motion = True
        
    #print( axis )
    #print( angle )
    


class AnimatedGl( pan.Animation ):
    def __init__(self):
        super( AnimatedGl , self ).__init__()
        self.__window = None
        
        # perspective sutup
        self.__fovy = 40.0
        self.__near = 1.0
        self.__far  = 30.0
    
        self.__xrot_ax = 1.0
        self.__yrot_ax = 0.0
        self.__zrot_ax = 0.0

        self.__rot_angle = 0.0

        self.__trans_x = 0.0
        self.__trans_y = 0.0

        self.__win_width = 800
        self.__win_height = 600
        
        self.__trackb = trk.TrackBall( self.win_size )
        self.__tran   = tran.TranslateScene( self.win_size )
        
        self.rot_matrix = np.array( [ 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 ]  )
        
        self.state = "trackball_down"
        self.motion = False
        
        self.axis = axgl.AxisOgl()
    

    def get_rotation_axis( self ):
        return ( self.__xrot_ax , self.__yrot_ax , self.__zrot_ax ) 
    
    def set_rotation_axis( self , rot_xyz_ax ):
        self.__xrot_ax = rot_xyz_ax[0]
        self.__yrot_ax = rot_xyz_ax[1]
        self.__zrot_ax = rot_xyz_ax[2] 
    
    rotatation_axis = property( get_rotation_axis , set_rotation_axis )
    
    
    def get_rot_angle( self ):
        return self.__rot_angle
    
    def set_rot_angle( self , angle ):
        self.__rot_angle = angle
    
    rotation_angle = property( get_rot_angle , set_rot_angle )
    

    
    def get_trackball( self ):
        return self.__trackb
    
    trackball = property( get_trackball )
    
    
    def get_translate_scene(self):
        return self.__tran
    
    translate_scene = property( get_translate_scene )
    
    
    def get_rotation( self ):
        return ( self.__xrot , self.__yrot , self.__zrot ) 
    
    def set_rotation( self , rot_xyz ):
        self.__xrot = rot_xyz[0]
        self.__yrot = rot_xyz[1]
        self.__zrot = rot_xyz[2] 
    
    rotatation = property( get_rotation , set_rotation )
    
    
    def get_translation(self):
        return ( self.__trans_x , self.__trans_y )
    
    def set_translation( self , transl ):
        self.__trans_x = transl[0]
        self.__trans_y = transl[1]
        
    translation = property( get_translation , set_translation )
    
    
    def get_perspective( self ):
        return ( self.__fovy , self.__near , self.__far )
    
    def set_perspective( self , perspective ):
        self.__fovy = perspective[0]
        self.__near = perspective[1]
        self.__far  = perspective[2]
    
    perspective = property( get_perspective , set_perspective )
    
    
    def get_win_size( self ):
        return ( self.__win_width , self.__win_height )
    
    def set_win_size( self , w_size ):
        self.__win_width  = w_size[0]
        self.__win_height = w_size[1]
        
        self.trackball.win_size = w_size
        self.translate_scene.win_size = w_size
        
    win_size = property( get_win_size , set_win_size )
    

    
    def zoom_scene( self , f ):
        
        (w,h) = MousePressed.animation.win_size
        
        ( fovy , near , far ) = MousePressed.animation.perspective
        
        if fovy <= 2 and f < 0 :
            f = 0.0
        
        MousePressed.animation.perspective = ( fovy+f*2 , near , far )
        ReSizeGLScene( w , h )
        
    
    def build_animation(self):
        self.__window = None
        
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize( self.win_size[0] , self.win_size[1] )
        glutInitWindowPosition(20, 20)
        
        self.__window = glutCreateWindow("Particles")
        
        DGLS = DrawGLScene
        
        DGLS.stream = self.data_stream()
        DGLS.animation = self
        
        glutDisplayFunc(DGLS)
        glutIdleFunc(DGLS)
        
        
        ReSizeFun = ReSizeGLScene
        ReSizeFun.animation = self
        
        glutReshapeFunc( ReSizeFun )
        glutKeyboardFunc( KeyPressed )
        
        pressed = MousePressed
        pressed.animation = self
        
        m_move = MouseMotion
        m_move.animation = self
        
        glutMouseFunc( pressed )
        glutMotionFunc( m_move )
        
        InitGL( self.win_size[0] , self.win_size[1]  , ReSizeFun )   
        
        
    def data_stream(self):
        self.ode_solver.update_force()
        
        for j in range(self.steps):
            self.ode_solver.step()            
            yield j
        
    def start(self):
        glutMainLoop()
    



