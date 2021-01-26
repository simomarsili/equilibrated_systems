# -*- coding: utf-8 -*-
"""Functions for sampling."""
# pylint: disable=protected-access, no-member, unused-import
import logging
from pathlib import Path

import numpy as np
from mmlite.multistate import SAMSSampler, propagator
from mmlite.systems import (AlanineDipeptideExplicit, AlanineDipeptideImplicit,
                            AlanineDipeptideVacuum, HostGuestExplicit)
from simtk import unit

test = AlanineDipeptideImplicit()  # test system
temperatures = list(np.logspace(np.log10(298), np.log10(600), num=4))
# temperatures = 298 * unit.kelvin
# pressure = 1.0 * unit.atmosphere
pressure = None
production_iterations = 1000  # total number of sampler iterations
burnin_iterations = 1000  # number of burnin iterations (#iterations)
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
