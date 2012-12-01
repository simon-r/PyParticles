Programming examples II
=======================

250K Particles Fountain
-----------------------

Bellow I describe how to build the 250'000 particles fountain demo included as example in the main application. 

The demo can be executed with the command: ::

    pyparticles_app -d fountain
	

First, you must import the libraries: numpy and particles set. ::

    import numpy as np
    import pyparticles.pset.particles_set as ps

For this demo I've chosen the midpoint method as ode numerical integration, but you can try with another one. :: 

    import pyparticles.ode.midpoint_solver as mds

The force is a combination between the constant gravity and the drag of the atmosphere, so I import the 'const_force' and 'drag'; and the multiple force for building the full scenario ::

    import pyparticles.forces.const_force as cf
    import pyparticles.forces.drag as dr
    import pyparticles.forces.multiple_force as mf

The 'animation' that control the simulation and the visualization is animation_ogl. ::

    import pyparticles.animation.animated_ogl as aogl


And I use the default_boundary model to control the jet. ::

    import pyparticles.pset.default_boundary as db


Let's start
+++++++++++
    
As first I've defined the function for modeling the jet. This function will be used by the boundary controller. 

This is a time-dependent function. And for convenience time is defined as variable internal to the function. As rule, the time must be based on a reference to an object of type **SimTime**. 	
::

    def default_pos( pset , indx ):
    
        t = default_pos.sim_time.time
    
        pset.X[indx,:] = 0.01 * np.random.rand( len(indx) , pset.dim )
    
        fs = 1.0 / ( 1.0 + np.exp( -( t - 2.0 ) ) ) 
   
        alpha = 2.0 * np.pi * np.random.rand( len(indx) ) 
    
        vel_x = 2.0 * fs * np.cos( alpha )
        vel_y = 2.0 * fs * np.sin( alpha )
       
        pset.V[indx,0] = vel_x  
        pset.V[indx,1] = vel_y 
        pset.V[indx,2] = 10.0 * fs + 1.0 * fs * ( np.random.rand( len(indx)) )

the main function
+++++++++++++++++

And finally you can start with the main function: 
    As first I've defined the number of steps the *dt* (step time), the size of the particle set and the **particles set** pset   
::

    def fountain():
    
        steps = 10000000
        dt = 0.01
   
        pcnt = 250000
        
        pset = ps.ParticlesSet( pcnt )
    
Initial position
++++++++++++++++
    
As a second point define the initial positions of the particles, in order to generate a continuous stream.
::    

        pset.M[:] = 0.1
        pset.X[:,2] = 0.7 * np.random.rand( pset.size )
    
Forces model
++++++++++++
    
The force model is based on a combination between a constant force, for simulating the gravity, and the drag for simulating the friction of the air. 

The two forces must be stored in an object of type  MultipleForce.
:: 

        grav = cf.ConstForce( pset.size , dim=pset.dim , u_force=( 0.0 , 0.0 , -10.0 ) )
        drag = dr.Drag( pset.size , dim=pset.dim , Consts=0.01 )
    
        multi = mf.MultipleForce( pset.size , dim=pset.dim )
    
        multi.append_force( grav )
        multi.append_force( drag )
    
        multi.set_masses( pset.M )
   
ODE integration
+++++++++++++++ 
   
As a ODE numerical integration method I've used the mid point algorithm. 
::
   
        solver = mds.MidpointSolver( multi , pset , dt )
        solver.update_force()
    
Simulation time
+++++++++++++++
    
Set up the simulation time in the *default_pos* function, used for modeling the jet.
::
 
        default_pos.sim_time = solver.get_sim_time()
        
        
Build the boundary model
++++++++++++++++++++++++

The tuples bd represents the size of the box closed domain: :math:`( min_x , max_x , min_y , max_y , min_z , max_z )`

.. note::
    The class DefaultBoundary positions the particles exited from the limits of the domain according to the function defualt_pos
::    

        bd = ( -100.0 , 100.0 , -100.0 , 100.0 , 0.0 , 100.0 )
        bound = db.DefaultBoundary( bd , dim=3 , defualt_pos=default_pos )
    
        pset.set_boundary( bound )
    
Build the 'animation' class and start
+++++++++++++++++++++++++++++++++++++

.. note::
    a.init_rotation( -80 , [ 0.7 , 0.05 , 0 ]  )
        setup an initial rotation where parameters are ( rot angle , axis of rotation )
    
    a.draw_particles.set_draw_model( 1 )
        enable the vectorized rendering, that is fundamental for drawing 250'000 particles
::

        a = aogl.AnimatedGl()
    
        a.ode_solver = solver
        a.pset = pset
        a.steps = steps
    
        a.draw_particles.set_draw_model( 1 )
    
        a.init_rotation( -80 , [ 0.7 , 0.05 , 0 ]  )
    
        a.build_animation()
        a.start()
    
        return

