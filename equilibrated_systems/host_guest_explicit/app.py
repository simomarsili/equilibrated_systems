# -*- coding: utf-8 -*-
"""Setup simulation parameters."""
# pylint: disable=no-member
from pathlib import Path

import numpy as np
from mmdemux import extract_trajectory
from mmlite import systems
from mmlite.multistate import SAMSSampler, propagator
from simtk import unit

test = systems.HostGuestExplicit()  # test system
ref_state_index = 0
temperatures = list(np.logspace(np.log10(298), np.log10(600), num=2))
# temperatures = 298 * unit.kelvin
pressure = 1.0 * unit.atmosphere
# pressure = None

# timesteps
timestep = 1.0 * unit.femtoseconds
state_update_steps = 1000  # stride in steps between state update (#steps)

# iterations
checkpoint_iterations = 1  # checkpoint_interval (#iterations)

ms_container = Path('frames/trj.nc')  # trajectory filepath

verbose_module = 'openmmtools.multistate'

sampler_class = SAMSSampler


def initialize_sampler():
    """Initialize a multistate sampler."""

    # initialize sampler
    smp = sampler_class(number_of_iterations=0,
                        mcmc_moves=propagator(timestep=timestep,
                                              n_steps=state_update_steps),
                        online_analysis_interval=None)

    # set sampler states and positions
    smp.from_testsystem(test,
                        temperatures=temperatures,
                        pressure=pressure,
                        stride=checkpoint_iterations,
                        storage=ms_container)

    smp.run()

    return smp


def extract(ms, target, state_index=0, discard=0):
    """Extract configurations at the target thermodynamic state."""
    # discard starting configuration from trajectory
    trj = extract_trajectory(nc_path=str(ms),
                             to_file=str(target),
                             state_index=state_index,
                             start_frame=discard)
    return trj
