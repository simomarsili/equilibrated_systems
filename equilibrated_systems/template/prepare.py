# -*- coding: utf-8 -*-
"""Prepare input for alchemical transformations."""
import logging
from pathlib import Path

import app
from mmlite.gromacs import generate_gromacs_input
from mmlite.utils import multistate_reporter_metadata

if app.verbose_module:
    logging.getLogger(app.verbose_module).setLevel(logging.DEBUG)

burnin_iterations = 100  # number of burnin iterations (#iterations)
target_container = Path('frames/trj.0.pdb')  # trajectory filepath


def gromacs_input_files():
    """Create gromacs .top and .gro files in the target directory."""
    reference_system, topology = multistate_reporter_metadata(
        app.ms_container, 'reference_state.system topography.topology'.split())

    # create gromacs .top and .gro files in the target directory
    generate_gromacs_input(target_container,
                           topology=topology,
                           system=reference_system,
                           split='.gro')


if __name__ == '__main__':

    _ = app.extract(ms=app.ms_container,
                    target=target_container,
                    state_index=app.ref_state_index,
                    discard=burnin_iterations)
    gromacs_input_files()
