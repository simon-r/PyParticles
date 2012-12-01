Programming examples I
======================

The Solar System
-----------------

Below I describe step by step how to build the simulation of the solar system included as example in the main application.


First you need to import numpy, since PyParticle is completely based on the arrays of numpy
::
    
    import numpy as np

Particle_set is the main container to be used with the systems of particles, then must always be imported.
::
    
    import pyparticles.pset.particles_set as ps
  
Import the force model used in this simulation, the gravity:
::
    
    import pyparticles.forces.gravity as gr

You must then import the module of the numerical procedure for solving the equation of motion. In this case I import them all.
::

    import pyparticles.ode.euler_solver as els
    import pyparticles.ode.leapfrog_solver as lps
    import pyparticles.ode.runge_kutta_solver as rks
    import pyparticles.ode.stormer_verlet_solver as svs
    import pyparticles.ode.midpoint_solver as mds
    
    
Import the 'animation' to control the simulation and the visualization: animation_ogl uses OpenGL as the graphics engine.
::

    import pyparticles.animation.animated_ogl as aogl
    
Let's start
    
Setup the main parameter of the simulation.

A *dt* of 6h is reasonable for the solar system simulation.
::
  
        dt = 6*3600
        steps = 1000000
        
        G = 6.67384e-11
        
        FLOOR = -10
        CEILING = 10

Create an instance of the class "ParticlesSet" that will contain the positions of all the planets. In this example enables the possibility to assign names to the particles, with the option 'label = True'
::
  
        pset = ps.ParticlesSet( 12 , 3 , label=True )
        
        pset.label[0] = "Sun"
        pset.label[1] = "Earth"
        pset.label[2] = "Jupiter"
        pset.label[3] = "Mars"
        pset.label[4] = "Mercury"
        pset.label[5] = "Neptune"
        pset.label[6] = "Pluto"
        pset.label[7] = "Saturn"
        pset.label[8] = "Uranus"
        pset.label[9] = "Venus"
        pset.label[10] = "Ceres"
        pset.label[11] = "Moon"
        

Set up the coordinates velocity and mass of the planets: That's the real (or realistic) data in meter Kg and m/s.
The data should be assigned in the property X, V, M of the container of particles **pset**, note that the size of X, V and M is constant and one must always use the method as shown below.
These property can not be reassigned by the user.
::
        
        # Coordinates
        pset.X[:] = np.array(  [
                                [  0.00000000e+00 ,  0.00000000e+00  , 0.00000000e+00],    # Sun
                                [  1.49597871e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Earth
                                [  7.78357721e+11 ,  0.00000000e+00 ,  0.00000000e+00],    # Jupiter
                                [  2.27987155e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Mars
                                [  5.83431696e+10 ,  0.00000000e+00  , 0.00000000e+00],    # Mercury
                                [  4.49691199e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Neptune
                                [  5.91360383e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Pluto
                                [  1.42701409e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Saturn
                                [  2.86928716e+12 ,  0.00000000e+00  , 0.00000000e+00],    # Uranus
                                [  1.04718509e+11 ,  0.00000000e+00  , 0.00000000e+00],    # Venus
                                [  4.138325875e+11,  0.00000000e+00  , 0.00000000e+00],    # Ceres
                                [  1.499604410e+11,  0.00000000e+00  , 0.00000000e+00]     # Moon
                                ]) 
        
        
        # Mass
        pset.M[:] = np.array(  [
                                [  1.98910000e+30] ,
                                [  5.98000000e+24] ,
                                [  1.90000000e+27] ,
                                [  6.42000000e+23] ,
                                [  3.30000000e+23] ,
                                [  1.02000000e+26] ,
                                [  1.29000000e+22] ,
                                [  5.69000000e+26] ,
                                [  8.68000000e+25] ,
                                [  4.87000000e+24] ,
                                [  9.43000000e+20] ,
                                [  7.34770000e+22]
                                ] )
    
        # Speed
        pset.V[:] = np.array( [ [ 0. ,   0.    ,    0.] ,
                                [ 0. , 29800.  ,    0.] ,
                                [ 0. , 13100.  ,    0.] ,
                                [ 0. , 24100.  ,    0.] ,
                                [ 0. , 47900.  ,    0.] ,
                                [ 0. ,  5400.  ,    0.] ,
                                [ 0. ,  4700.  ,    0.] ,
                                [ 0. ,  9600.  ,    0.] ,
                                [ 0. ,  6800.  ,    0.] ,
                                [ 0. , 35000.  ,    0.] ,
                                [ 0  , 17882.  ,    0.] ,
                                [ 0  , 30822.  ,    0.] 
                                ] )
  
To be more realistic we use also the 'Inclination' and the 'Longitude of the ascending node' of the orbits
::
    
        # Inclination
        incl = np.array([ 0.0 ,
                          0.0 ,
                          1.305 ,
                          1.850 ,
                          7.005 ,
                          1.767975,
                          17.151 ,
                          2.485 ,
                          0.772 ,
                          3.394 ,
                          10.587 ,
                          0.0 ,
                          ])
        
        # Longitude of the ascending node
        lan = np.array([ 0.0 ,
                         348.73936 ,
                         100.492 ,
                         49.562 ,
                         48.331 ,
                         131.794310 ,
                         110.286 ,
                         113.642 ,
                         73.989 ,
                         76.678 ,
                         80.3932 ,
                         348.73936 
                        ])
    
 
Rotate and correct the main coordinated to produce a more realistic scenario
::
    
        incl[:] = incl * 2.0*np.pi / 360.0
        
        lan[:]  = lan * 2.0*np.pi / 360.0
        
        pset.V[:,2] = np.sin( incl ) * pset.V[:,1]
        pset.V[:,1] = np.cos( incl ) * pset.V[:,1]
        
        for i in range ( pset.V.shape[0] ) :
            x = pset.V[i,0]
            y = pset.V[i,1]
            
            pset.V[i,0] = x * np.cos( lan[i] ) - y * np.sin( lan[i] )
            pset.V[i,1] = x * np.sin( lan[i] ) + y * np.cos( lan[i] )
            
    
        for i in range ( pset.X.shape[0] ) :
            x = pset.X[i,0]
            y = pset.X[i,1]
            
            pset.X[i,0] = x * np.cos( lan[i] ) - y * np.sin( lan[i] )
            pset.X[i,1] = x * np.sin( lan[i] ) + y * np.cos( lan[i] )
    
        
Define the len unit to the 1 UA ant the mass unit to the Earth mass
::

        pset.unit = 149597870700.0
        pset.mass_unit = 5.9736e24

Build the force model, the gravity and setup G as gravity constant.
::
        
        grav = gr.Gravity( pset.size , Consts=G )
        grav.set_masses( pset.M )

That's a model with open boundary:
::
      
        bound = None      
        pset.set_boundary( bound )
        
Enable the positions log, useful for drawing the trajectory or for analizing the data.
::
        
        pset.enable_log( True , log_max_size=1000 )

Compute the forces for the initial condition, **don't forget this step!**
::
        
        grav.update_force( pset )
        
We use Runge kutta as integration method, or at you option, another one
::

        solver = rks.RungeKuttaSolver( grav , pset , dt )    
        
        #solver = mds.MidpointSolver( grav , pset , dt )    
        #solver = els.EulerSolver( grav , pset , dt )
        #solver = lps.LeapfrogSolver( grav , pset , dt )
        #solver = svs.StormerVerletSolver( grav , pset , dt )

Create the controller of the simulation, in our case the one based on OpenGL
::
        
        a = aogl.AnimatedGl()
       # a = anim.AnimatedScatter()
       
Plot the trajectory with 1 as a step.
::
       
        a.trajectory = True
        a.trajectory_step = 1

Setup the integration method (solver) and the particles set (pset) in the controller
::

        a.ode_solver = solver
        a.pset = pset
        
Set the maximal number of steps, and call the build procedure.
::
        
        a.steps = steps
        
        a.build_animation()
        
That's all, we can start the simulation!
::        
        a.start()
        

It's easy? ... I think yes!


