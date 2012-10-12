# PyParticles #

PyParticles is a particle simulation toolbox entirely written in python

##Features##

Simulate a particle by particle model with the most popular integrations methods, and it represents the results on a OpenGL or Matplotlib plot.

###PyParticle includes:###

1. Euler method
2. Leap Frog method
3. Rung Kutta method
4. Stormer Verlet method

As a forces model it includes:

1. Gravity
2. Particle by Particle spring
3. Constant
4. User defined field

PyParticle offers an easy to use class structure with a fully interchangable integrations method or force model, it also implements the possibility to add some boudary model.

##Command line tool usage:##

In PyParticles a simulation model is entierly described in a config file that scholuld be edited by the user.

The following are the main command of the PyParticles application.

Start the demo simulation:

    pypaticle
    
Start a simulation described in a config file

    pyparticle <file_name>
    
Write out a model config file
    
    pyparticle -m
    
Write out some informations

    pyparticles --help
    pyparticles --version
    

Config file Example:

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
