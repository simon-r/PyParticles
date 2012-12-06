PyParticles 
===========

PyParticles is a particle simulation toolbox entirely written in python. 

The main objective of PyParticles is to provide a system API simple and fast to use.
Furthermore is to provide a basic application for the implementation of simple models.

| Blog: http://pyparticles.wordpress.com/
| GitHub:  https://github.com/simon-r/PyParticles

Index
-----

.. toctree::
   :maxdepth: 2

   Programming Example
   Programming Example II
   Config File
   Testing
   Packages Descriptions
   pyparticles


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
#. Lennard Jones
#. Drag
#. Damping
#. Electromagnetic fields

We have also the possibility of modeling the forces with user-defined constraints (See demo *cat_spri*).

PyParticle offers an easy to use class structure with a fully *interchangeable* integrations method or force model, it also implements the possibility to add some boundary model.


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

**Start the demo simulation:**

::

    pyparticles_app
    

**Start a simulation described in a config file**
::

    pyparticle_app <file_name>
    

**Start the specified demo simulation**

============= ========================================================
Demos
============= ========================================================
springs       3 body springs
solar_system  Simulation of the solar system with realistic magnitudes
bubble        Bubbles. With a non realistic force
cat_spri      Vibrating string with gravity and air drag
gas_lj        Lennard jones gas model (should be improved)
elmag_field   Electromagnetic field 
fountain      250'000 particles fountain
============= ========================================================
::

    pyparticles_app --demo springs
    pyparticles_app --demo solar_system
    pyparticles_app --demo bubble
    pyparticles_app --demo cat_spri
    pyparticles_app --demo gas_lj
    pyparticles_app --demo elmag_field
    pyparticles_app --demo fountain

**Start a testing procedure**
Execute the specified test: ::

    pyparticles_app --test harmonic
    pyparticles_app --test fall
    


**Write out a model config file**
::
    
    pyparticle_app -m
    

**Print out the help and version**
::

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