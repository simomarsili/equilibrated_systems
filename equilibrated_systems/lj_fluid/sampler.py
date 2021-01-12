# -*- coding: utf-8 -*-
"""Functions for sampling."""
# pylint: disable=protected-access, no-member
from math import ceil
from pathlib import Path

from mmlite.systems import LennardJonesFluid
from simtk import unit
from TestPipelines.sampler import SAMSSampler, propagator
from TestPipelines.utils import generate_gromacs_input

test = LennardJonesFluid(nparticles=100, reduced_density=0.01)  # test system
temperatures = 298 * unit.kelvin
pressure = None
# pressure = 298 * unit.atmosphere
production_iterations = 1000  # total number of sampler iterations (state updates)
burnin_iterations = 100  # number of burnin iterations (#iterations)
timestep = 1.0 * unit.femtoseconds
state_update_steps = 1000  # stride in steps between state update (#steps)
checkpoint_iterations = 10  # checkpoint_interval (#iterations)
container = Path('frames/trj.nc')  # trajectory filepath

if __name__ == '__main__':

    n_iterations = production_iterations + burnin_iterations

    burnin_iterations += 1  # discard starting configuration from trajectory

    # initialize sampler
    sampler = SAMSSampler(number_of_iterations=n_iterations,
                          mcmc_moves=propagator(timestep=timestep,
                                                n_steps=state_update_steps),
                          online_analysis_interval=None)

    start_frame = ceil(burnin_iterations / checkpoint_iterations)

    print('''
        temperatures: %r,
        n_iterations: %r,
        burnin: %r,
        state_update_interval: %r,
        checkpoint_interval: %r,
        start_frame: %r
        ''' % (temperatures, n_iterations, burnin_iterations,
               state_update_steps, checkpoint_iterations, start_frame))

    # set sampler states and positions
    sampler.from_testsystem(test,
                            temperatures=temperatures,
                            pressure=pressure,
                            stride=checkpoint_iterations)

    # run the simulation
    sampler.run()

    # save the sampled configurations at the target thermodynamic state
    sampler.demux(0, to_file=container, start_frame=start_frame)

    # start_frame = 10
    # create gromacs .top and .gro files in the target directory
    generate_gromacs_input(container, sampler)
