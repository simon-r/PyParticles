PyParticles 
===========

PyParticles is a particle simulation toolbox entirely written in python

Visit: http://pyparticles.wordpress.com/
Docs:  http://simon-r.github.com/PyParticles/index.html


Features
--------

Simulate a particle by particle model with the most popular integrations methods, and it represents the results on a OpenGL or Matplotlib plot.

**PyParticle includes** the followings integrations methods 

#. Euler method
#. Leap Frog method
#. Rung Kutta method
#. Midpoint
#. Stormer Verlet method

**As a forces model** it includes:

#. Gravity
#. Particle by Particle spring
#. Constant
#. User defined field

PyParticle offers an easy to use class structure with a fully * interchangeable* integrations method or force model, it also implements the possibility to add some boundary model.


Requirements
------------
| PyParticles require the following packages:

| **numpy** : http://scipy.org/Download
| **scipy** : http://scipy.org/Download
| **pyopengl** : http://pyopengl.sourceforge.net/
| **matplotlib** : http://matplotlib.org/

For more details about the installation visit the Blog: http://pyparticles.wordpress.com/installation/


Command line tool usage:
------------------------

In PyParticles a simulation model is entirely described in a config file that should be edited by the user.

The following are the main command of the PyParticles application.

Start the demo simulation: ::

    pypaticle_app
    

Start a simulation described in a config file ::

    pyparticle_app <file_name>
    

Start the specified demo simulation ::

    pypaticle_app --demo springs
    pypaticle_app --demo solar_system

Write out a model config file ::
    
    pyparticle_app -m
    

Print out the help and version ::

    pyparticles_app --help
    pyparticles_app --version
    

During the simulation you can toggle the help message by pressing **h**


Config file Example: ::

    [pset_origin]
    media_origin = from_file
    file_name = solar_sys.csv
    
    [set_config]
    len_unit = 149597870700.0
    mass_unit = 5.9736e24
    boundary = open
    
    [model]
    force = gravity
    ode_solver_name = euler
    time_step = 3600
    steps = 1000000
    force_const = 6.67384e-11
    force_vector = 0 0 0
    
    [animation]
    animation_type = opengl
    xlim = -5.0  5.0
    ylim = -5.0  5.0
    zlim = -5.0  5.0


