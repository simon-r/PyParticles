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



import pyparticles.animation.animation as pan

import numpy as np
import sys 


import pyparticles.ogl.trackball as trk
import pyparticles.ogl.axis_ogl as axgl
import pyparticles.ogl.translate_scene as tran
import pyparticles.ogl.draw_vector_field as dvf
import pyparticles.utils.time_formatter as tf
import pyparticles.ogl.draw_particles_ogl as drp

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

if sys.platform.startswith("win") :
    from OpenGL.WGL import *
    
if sys.platform.startswith("linux") :
    from OpenGL.GLX import *
 

def InitGL( Width , Height , ReSizeFun ):
    """
    Initialize OpenGl 
    """
    
    glClearColor(0.0, 0.0, 0.0, 0.0)    
    glClearDepth(1.0)                   
    glDepthFunc(GL_LESS)                
    glEnable(GL_DEPTH_TEST)             
    glShadeModel(GL_SMOOTH)        
    glEnable(GL_TEXTURE_2D)
    
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glAlphaFunc(GL_GREATER,0.1)
    glEnable(GL_ALPHA_TEST)
    
    glEnable (GL_LINE_SMOOTH)
    glHint( GL_LINE_SMOOTH_HINT , GL_NICEST )
    
    ReSizeFun(Width, Height)
    
    
    
    InitLight()



def InitLight() :
    light_ambient = np.array( [  0.0 , 0.0 , 0.0 , 1.0  ] )
    light_diffuse = np.array( [  1.0 , 1.0 , 1.0 , 1.0  ] )
    light_specular = np.array( [  1.0 , 1.0 , 1.0 , 1.0  ] )
    light_position = np.array( [  2.0 , 5.0 , 5.0 , 10.0  ] )
     
    mat_ambient = np.array( [  0.7 , 0.7 , 0.7 , 1.0  ] )
    mat_diffuse = np.array( [  0.8 , 0.8 , 0.8 , 1.0  ] )
    mat_specular = np.array( [  1.0 , 1.0 , 1.0 , 1.0  ] )
    high_shininess = np.array( [  100.0  ] )
    
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    #glEnable(GL_LIGHTING)
    
    glLightfv(GL_LIGHT0, GL_AMBIENT,  light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position) 
    
    glMaterialfv(GL_FRONT, GL_AMBIENT,   mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE,   mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR,  mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)    

def enableLight():
    glEnable(GL_LIGHTING)
    
def disableLight():
    glDisable(GL_LIGHTING)    
    

def DrawGLScene():
    """
    Draw the current particle scene.
    """
    
    # Simulation step
    DrawGLScene.stream()
    
    tr = DrawGLScene.animation.translation
    
    sim_time = DrawGLScene.animation.ode_solver.time
        
    fm = tf.MyTimeFormatter()
        
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    
    Set2DMode( )
        
    glut_print( 0.02 , 0.02 , GLUT_BITMAP_9_BY_15 , fm.to_str( sim_time ) , 1.0 , 1.0 , 1.0 , 1.0 )
    
    if DrawGLScene.animation.measures_cnt() > 0 :
        print_measures()
    
    if DrawGLScene.animation.print_help :
        print_help()
    
    if DrawGLScene.animation.fps_print :
        print_fps( DrawGLScene.animation.fps )
    
    SetPerspective( DrawGLScene.animation )

    glPushMatrix()
    
    glEnable (GL_FOG)
    glFogf (GL_FOG_DENSITY, 0.05)
    
    glLoadIdentity()  
    
    if DrawGLScene.animation.state == "trackball_down" and DrawGLScene.animation.motion or joystick_func.animation.joy_state == "joy_on":
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

    if DrawGLScene.animation.light :
        enableLight()

    DrawGLScene.animation.draw_particles.draw()
    
    if DrawGLScene.animation.light :
        disableLight()
    
    if DrawGLScene.animation.view_axis :
        DrawGLScene.animation.axis.draw_axis()    
        
    if DrawGLScene.animation.draw_vector_field :
        DrawGLScene.animation.vector_field.draw()
        
    glPopMatrix()
    glutSwapBuffers()


def Set2DMode(  ):
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    

def SetPerspective( animation ):
    
    per = animation.perspective
    
    ( w , h ) = animation.win_size
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective( per[0] , float(w)/float(h), per[1] , per[2] )
    
    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    
    if Height == 0:                        
        Height = 1
    
    MousePressed.animation.win_size = ( Width , Height )
    glViewport(0, 0, Width, Height)
    
    SetPerspective( MousePressed.animation )
    
   
def KeyPressed( c , x , y ):    
    if c == 'a' :
        KeyPressed.animation.view_axis = not KeyPressed.animation.view_axis
        
    if c == 'h' :
        KeyPressed.animation.print_help = not KeyPressed.animation.print_help
        
    if c == 't' :
        KeyPressed.animation.trajectory = not KeyPressed.animation.trajectory
        
    if c == 'f' :
        KeyPressed.animation.fps_print = not KeyPressed.animation.fps_print        
        
    if c == 'p' :
        KeyPressed.animation.draw_particles.set_particle_model( model="point" )
        
    if c == 's' :
        KeyPressed.animation.draw_particles.set_particle_model( model="sphere" )
    
    if c == 'o' :
        KeyPressed.animation.draw_particles.set_particle_model( model="teapot" )
        
    if c == 'L' :
        KeyPressed.animation.light = True
        
    if c == 'l' :
        KeyPressed.animation.light = False
        
    if c == 'v' :
        KeyPressed.animation.draw_vector_field = ( not KeyPressed.animation.draw_vector_field ) and ( KeyPressed.animation.vector_field != None )
        
        


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

def joystick_func( button_mask, x, y, z ):
    #print( "------------------ "  )
    #print( "butt %d: " % button_mask )
    #print( "x %d " % x )
    #print( "y %d " % y )
    #print( "z %d " % z )
    
    if x == 0 and y == 0 :
        joystick_func.animation.joy_state = "joy_off"
        return
        
    ( axis , angle ) = joystick_func.animation.trackball.on_joystick( ( x , y ) )
    
    joystick_func.animation.rotation_angle = angle 
    joystick_func.animation.rotatation_axis = ( axis[0] , axis[1] , axis[2] )
    joystick_func.animation.joy_state = "joy_on"
    
    

def print_help():
    
    y = 0.9
    glut_print( 0.1 , y , GLUT_BITMAP_9_BY_15 , "a: Axis ON/OFF" , 1 , 1 , 1 , 1 )
    
    y -= 0.05
    glut_print( 0.1 , y , GLUT_BITMAP_9_BY_15 , "t: Trajectory ON/OFF" , 1 , 1 , 1 , 1 )
    
    y -= 0.05
    glut_print( 0.1 , y , GLUT_BITMAP_9_BY_15 , "Point model - p: point | s: sphere | o: teapot " , 1 , 1 , 1 , 1 )
    
    y -= 0.05
    glut_print( 0.1 , y , GLUT_BITMAP_9_BY_15 , "Lighting - L: On  l: OFF " , 1 , 1 , 1 , 1 )
    
    y -= 0.05
    glut_print( 0.1 , y , GLUT_BITMAP_9_BY_15 , "v: Toggle vector field " , 1 , 1 , 1 , 1 )
    
    y -= 0.05
    glut_print( 0.1 , y , GLUT_BITMAP_9_BY_15 , "f: Toggle FPS " , 1 , 1 , 1 , 1 )
    
    y -= 0.1    
    glut_print( 0.1 , y , GLUT_BITMAP_9_BY_15 , "h: Toggle help message" , 1 , 1 , 1 , 1 )
    
    
def print_measures():
    
    mnames = print_measures.animation.get_measures_names()
    
    y = 0.9
    
    for na in mnames:
        m = print_measures.animation.get_measure_value_str( na )
        glut_print( 0.7 , y , GLUT_BITMAP_9_BY_15 , " %s:  %s " % ( na , m ) , 1 , 1 , 1 , 1 )
        y -= 0.05
        
        
def print_fps( fps ):
    glut_print( 0.9 , 0.05 , GLUT_BITMAP_9_BY_15 , "FPS: %.2f" % fps , 1 , 1 , 1 , 1 )
    
        
def glut_print( x,  y,  font,  text, r,  g , b , a):
        
    blending = False 
    if glIsEnabled(GL_BLEND) :
        blending = True
        
    glPushMatrix()
    glColor3f(1,1,1)
    glRasterPos2f(x,y)
        
    text = bytes( text.encode("ascii") ) 
    
    glutBitmapString( font , text ) 
    glPopMatrix()

    if not blending :
        glDisable(GL_BLEND) 


if sys.platform.startswith("win"):
    def SwapIntervalEXT( value ):   
        import ctypes
        # Open the opengl32.dll
        gldll = ctypes.windll.opengl32
        # define a function pointer prototype of *(GLuint program, GLenum pname, GLint value)
        prototype = ctypes.WINFUNCTYPE( ctypes.c_int , ctypes.c_uint )
        # Get the win gl func adress
        fptr = gldll.wglGetProcAddress( 'wglSwapIntervalEXT' )
        if fptr==0:
            raise Exception( "wglSwapIntervalEXT ('wglSwapIntervalEXT ') returned a zero adress, which will result in a nullpointer error if used.")
        _wglSwapIntervalEXT = prototype( fptr )
        
        _wglSwapIntervalEXT( value )
        
elif sys.platform.startswith("linux"):
    def SwapIntervalEXT( value ):
        pass
else :
    def SwapIntervalEXT( value ):
        pass




class AnimatedGl( pan.Animation ):
    def __init__(self):
        super( AnimatedGl , self ).__init__()
        self.__window = None
        
        # perspective sutup
        self.__fovy = 40.0
        self.__near = 1.0
        self.__far  = 300.0
    

        self.__xrot_ax = 1.0
        self.__yrot_ax = 0.0
        self.__zrot_ax = 0.0

        self.__rot_angle = 0.0

        self.__trans_x = 0.0
        self.__trans_y = 0.0

        self.__win_width = 1000
        self.__win_height = 800
        
        self.__trackb = trk.TrackBall( self.win_size )
        self.__tran   = tran.TranslateScene( self.win_size )
        
        self.__light = False
        
        self.rot_matrix = np.array( [ 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 ]  )
        
        self.state = "trackball_down"
        self.joy_state = "joy_off"
        self.motion = False
        
        self.view_axis = True
        self.print_help = False
        
        self.axis = axgl.AxisOgl()
        self.draw_particles = drp.DrawParticlesGL()
        
        self.__draw_vector_field = False
        self.vector_field = None
    

    def get_pset(self):
        return super(AnimatedGl,self).get_pset()
        
    def set_pset( self , pset ):
        super(AnimatedGl,self).set_pset( pset )
        self.draw_particles.pset = pset
        
    pset = property( get_pset , set_pset )


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
    
    
    def set_light( self , sw ):
        self.__light = sw
        
    def get_light( self ):
        return self.__light
    
    light = property( get_light , set_light , doc="enable or disable (True or False) the opengl lighting"  )


    def init_rotation( self , angle , axis ):
        self.__init_rot = list( [ angle , axis ] )
        

    
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
        
    win_size = property( get_win_size , set_win_size , doc="get or set the size of the current window. The size is a tuple: (w,h)")
    
    
    def get_trajectory( self ) :
        return super(AnimatedGl,self).get_trajectory()
    
    def set_trajectory( self , tr ):
        super(AnimatedGl,self).set_trajectory( tr )
        self.draw_particles.trajectory = tr
        
    trajectory = property( get_trajectory , set_trajectory , doc="enable or disable (True or False) the trajectory" )
    
    
    def get_trajectory_step( self ) :
        return super(AnimatedGl,self).get_rajectory_step()
    
    def set_trajectory_step( self , trs ):
        super(AnimatedGl,self).set_trajectory_step( trs )
        self.draw_particles.set_trajectory_step( trs )
        
    trajectory_step = property( get_trajectory_step , set_trajectory_step , doc="set or get the step for drawing the trajectory" )

    
    def get_draw_vector_field(self):
        return self.__draw_vector_field
    
    def set_draw_vector_field( self , f ):
        self.__draw_vector_field = f
        
    draw_vector_field = property( get_draw_vector_field , set_draw_vector_field , doc="enable or disable (True of False) vector filed drawing (if available)" )
    
    
    def add_vector_field_fun( self , fun ,  unit , density=1.0 , color_fun=None ):
        
        if self.vector_field == None :
            
            lims = [ self.xlim[0] , self.xlim[1] , self.ylim[0] , self.ylim[1] , self.zlim[0] , self.zlim[1] ]
            
            self.vector_field = dvf.DrawVectorField( lims , density )
        
        self.vector_field.add_vector_fun( fun , unit , color_fun )
        
        
    def zoom_scene( self , f ):
        
        (w,h) = MousePressed.animation.win_size
        
        ( fovy , near , far ) = MousePressed.animation.perspective
        
        if fovy <= 2.0 and f < 0 :
            f = -0.04
        if fovy <= 0.2 and f < 0 :
            f = 0.0
        if fovy < 2.0 and f > 0 :
            f = 0.04
        if fovy > 179 and f > 0 :
            f = 0.0
            
        
        MousePressed.animation.perspective = ( fovy+f*2 , near , far )
        MousePressed.animation.translate_scene.fovy = fovy+f*2
        
        ReSizeGLScene( w , h )
        
    
    def build_animation(self):
        self.__window = None
        
        glutInit(sys.argv)
        
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE)
        glutInitWindowSize( self.win_size[0] , self.win_size[1] )
        glutInitWindowPosition(20, 20)
        
        self.__window = glutCreateWindow( ctypes.c_char_p( b"Particles" ) )
        
        DGLS = DrawGLScene
        
        self.ode_solver.update_force()
        
        DGLS.stream = self.data_stream
        
        DGLS.animation = self
        
        glutDisplayFunc(DGLS)
        glutIdleFunc(DGLS)
        
        ReSizeFun = ReSizeGLScene
        ReSizeFun.animation = self
        
        KeyPressed.animation = self
        
        glutReshapeFunc( ReSizeFun )
        glutKeyboardFunc( KeyPressed )
        
        pressed = MousePressed
        pressed.animation = self
        
        m_move = MouseMotion
        m_move.animation = self
        
        print_measures.animation = self
        joystick_func.animation = self
        
        
        glutJoystickFunc( joystick_func , 250 )
        glutMouseFunc( pressed )
        glutMotionFunc( m_move )
        
        InitGL( self.win_size[0] , self.win_size[1]  , ReSizeFun )
        
        self.draw_particles.ogl_init()
        self.axis.ogl_init()
        
        try:
            self.__init_rot
        except:
            pass
        else:
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            glRotatef( self.__init_rot[0] , self.__init_rot[1][0] , self.__init_rot[1][1] , self.__init_rot[1][2] )
            self.rot_matrix = glGetFloatv( GL_MODELVIEW_MATRIX )
            glPopMatrix()
            
        if self.vector_field != None :
            self.vector_field.ogl_init()
        
        try :            
            SwapIntervalEXT(0)
        except :
            print( "ERROR: VSYNC not disabled" )
            
        
    def data_stream(self):
        
        self.pset.log()
        
        self.ode_solver.step()
        self.perform_measurement()
        
        self.update_fps()
        
        return self.ode_solver.steps_cnt
        
    
    def start(self):
        glutMainLoop()
    



