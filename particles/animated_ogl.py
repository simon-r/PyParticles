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

import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except:
    _____foo = None

FLOOR = -10
CEILING = 10
    
    
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    gluLookAt( 10 , 10 , 10 , 0, 0, 0, 0, 0, 0);
    glMatrixMode(GL_MODELVIEW)
    

def DrawGLScene():
    
    j = next(DrawGLScene.stream)
    
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()                    # Reset The View
    glTranslatef(-1.5,0.0,-6.0)                # Move Left And Into The Screen

    glRotatef(0.0,0.0,1.0,0.0)                # Rotate The Pyramid On It's Y Axis
    
    glEnable(GL_POINT_SMOOTH)
    
    glPointParameterf( GL_POINT_SIZE_MAX , 10.0 )
    glPointParameterf( GL_POINT_SIZE_MIN , 0.1 )
    #glBegin(GL_POINTS)
    
    for i in range( DrawGLScene.animation.pset.size() ):
        glPointSize( DrawGLScene.animation.pset.M[i] )
        glBegin(GL_POINTS)
        glColor3f( 1.0 , 1.0 , 1.0 )    
        #glPointSize( DrawGLScene.animation.pset.M[i] )
        glVertex3f( DrawGLScene.animation.pset.X[i,0] ,
                    DrawGLScene.animation.pset.X[i,1] ,
                    DrawGLScene.animation.pset.X[i,2] )

        glEnd()
    
    glutSwapBuffers()


def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
   
def KeyPressed():
    pass

class AnimatedGl( pan.Animation ):
    def __init__(self):
        super( AnimatedGl , self ).__init__()
        self.__window = None
    
        
    def build_animation(self):
        self.__window = None
        
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(20, 20)
        
        self.__window = glutCreateWindow("Particles")
        
        DGLS = DrawGLScene
        
        DGLS.stream = self.data_stream()
        DGLS.animation = self
        
        glutDisplayFunc(DGLS)
        glutIdleFunc(DGLS)
        
        glutReshapeFunc(ReSizeGLScene)
        glutKeyboardFunc(KeyPressed)
        
        InitGL(640, 480)   
        
        
    def data_stream(self):
        self.ode_solver.update_force()
        
        for j in range(self.steps):
            self.ode_solver.step()            
            yield j
    
    def update(self,i):
        pass
    
    def start(self):
        glutMainLoop()
    



