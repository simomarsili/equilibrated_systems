# -*- coding: utf-8 -*-
"""Setup simulation parameters."""
# pylint: disable=no-member
from math import ceil
from pathlib import Path

import numpy as np
from mmdemux import extract_trajectory
from mmlite.gromacs import generate_gromacs_input
from mmlite.multistate import SAMSSampler, propagator
from mmlite.systems import HostGuestExplicit
from mmlite.utils import multistate_reporter_metadata
from simtk import unit

test = HostGuestExplicit()  # test system
ref_state_index = 0
temperatures = list(np.logspace(np.log10(298), np.log10(600), num=20))
# temperatures = 298 * unit.kelvin
pressure = 1.0 * unit.atmosphere
# pressure = None

# timesteps
timestep = 1.0 * unit.femtoseconds
state_update_steps = 1000  # stride in steps between state update (#steps)

# iterations
burnin_iterations = 1000  # number of burnin iterations (#iterations)
checkpoint_iterations = 10  # checkpoint_interval (#iterations)

ms_container = Path('frames/trj.nc')  # trajectory filepath
target_container = Path('frames/trj.0.pdb')  # trajectory filepath

verbose_module = 'openmmtools.multistate'

sampler_class = SAMSSampler


def initialize_sampler():
    """Initialize a multistate sampler."""

    # initialize sampler
    smp = SAMSSampler(number_of_iterations=burnin_iterations,
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


def extract():
    """Extract configurations at the target thermodynamic state."""
    # discard starting configuration from trajectory
    burnin = burnin_iterations + 1
    start_frame = ceil(burnin / checkpoint_iterations)
    trj = extract_trajectory(nc_path=ms_container,
                             to_file=target_container,
                             state_index=ref_state_index,
                             start_frame=start_frame)
    return trj


def gromacs_input_files():
    """Create gromacs .top and .gro files in the target directory."""
    reference_system, topology = multistate_reporter_metadata(
        ms_container, 'reference_state.system topography.topology'.split())

    # create gromacs .top and .gro files in the target directory
    generate_gromacs_input(target_container,
                           topology=topology,
                           system=reference_system,
                           split='.gro')
