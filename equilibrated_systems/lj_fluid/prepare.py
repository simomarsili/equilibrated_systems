# -*- coding: utf-8 -*-
"""Prepare files for alchemical transformations."""
from math import ceil
from pathlib import Path

from mmdemux import extract_trajectory
from mmlite.gromacs import generate_gromacs_input
from mmlite.utils import multistate_reporter_metadata

burnin_iterations = 100  # number of burnin iterations (#iterations)
checkpoint_iterations = 10  # checkpoint_interval (#iterations)

ref_state_index = 0

ms_container = Path('frames/trj.nc')  # trajectory filepath
target_container = Path('frames/trj.0.nc')  # trajectory filepath

burnin_iterations += 1  # discard starting configuration from trajectory

start_frame = ceil(burnin_iterations / checkpoint_iterations)

reference_system, topology = multistate_reporter_metadata(
    ms_container, 'reference_state.system topography.topology'.split())

# save the sampled configurations at the target thermodynamic state
trj = extract_trajectory(nc_path=ms_container,
                         to_file=target_container,
                         state_index=ref_state_index,
                         start_frame=start_frame)

# create gromacs .top and .gro files in the target directory
generate_gromacs_input(target_container,
                       topology=topology,
                       system=reference_system,
                       split='.gro')
