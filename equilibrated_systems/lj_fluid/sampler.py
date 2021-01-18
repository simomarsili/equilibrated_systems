# -*- coding: utf-8 -*-
"""Functions for sampling."""
# pylint: disable=protected-access, no-member
from math import ceil
from pathlib import Path

from mmdemux import extract_trajectory_to_file
from mmlite.gromacs import generate_gromacs_input
from mmlite.multistate import SAMSSampler, propagator
from mmlite.systems import LennardJonesFluid
from simtk import unit

test = LennardJonesFluid(nparticles=100, reduced_density=0.01)  # test system
temperatures = 298 * unit.kelvin
pressure = 1.0 * unit.atmosphere
# production_iterations = 1000  # total number of sampler iterations (state updates)
production_iterations = 100  # total number of sampler iterations (state updates)
burnin_iterations = 100  # number of burnin iterations (#iterations)
timestep = 1.0 * unit.femtoseconds
state_update_steps = 1000  # stride in steps between state update (#steps)
checkpoint_iterations = 10  # checkpoint_interval (#iterations)

ms_container = Path('frames/trj.nc')  # trajectory filepath
target_container = Path('frames/trj.0.nc')  # trajectory filepath


def initialize_sampler():
    """Initialize a multistate sampler."""

    # initialize sampler
    n_iterations = production_iterations + burnin_iterations

    smp = SAMSSampler(number_of_iterations=n_iterations,
                      mcmc_moves=propagator(timestep=timestep,
                                            n_steps=state_update_steps),
                      online_analysis_interval=None)

    # set sampler states and positions
    smp.from_testsystem(test,
                        temperatures=temperatures,
                        pressure=pressure,
                        stride=checkpoint_iterations,
                        storage=ms_container)
    return smp


if __name__ == '__main__':

    burnin_iterations += 1  # discard starting configuration from trajectory

    start_frame = ceil(burnin_iterations / checkpoint_iterations)

    # initialize sampler
    sampler = initialize_sampler()

    # run the simulation
    sampler.run()

    # save the sampled configurations at the target thermodynamic state
    extract_trajectory_to_file(nc_path=ms_container,
                               out_path=target_container,
                               state_index=0,
                               start_frame=start_frame)

    # start_frame = 10
    # create gromacs .top and .gro files in the target directory
    generate_gromacs_input(target_container,
                           topology=test.topology,
                           system=test.system,
                           split='.gro')
