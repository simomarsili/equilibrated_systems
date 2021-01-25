# -*- coding: utf-8 -*-
"""Functions for sampling."""
# pylint: disable=protected-access, no-member
import logging
from pathlib import Path

from mmlite.multistate import SAMSSampler, propagator
from mmlite.systems import LennardJonesFluid
from simtk import unit

test = LennardJonesFluid(nparticles=100, reduced_density=0.01)  # test system
temperatures = 298 * unit.kelvin
pressure = 1.0 * unit.atmosphere
production_iterations = 100  # total number of sampler iterations (state updates)
burnin_iterations = 100  # number of burnin iterations (#iterations)
timestep = 1.0 * unit.femtoseconds
state_update_steps = 1000  # stride in steps between state update (#steps)
checkpoint_iterations = 10  # checkpoint_interval (#iterations)

ms_container = Path('frames/trj.nc')  # trajectory filepath
target_container = Path('frames/trj.0.nc')  # trajectory filepath

verbose_module = 'openmmtools.multistate'

if verbose_module:
    logging.getLogger(verbose_module).setLevel(logging.DEBUG)


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

    # initialize sampler
    sampler = initialize_sampler()

    # run the simulation
    sampler.run()
