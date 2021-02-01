# -*- coding: utf-8 -*-
"""Prepare input for alchemical transformations."""
import logging
from pathlib import Path

import app
from mmlite.gromacs import generate_gromacs_input
from mmlite.utils import multistate_reporter_metadata

from equilibrated_systems.utils import extract

if app.prms.verbose_module:
    logging.getLogger(app.prms.verbose_module).setLevel(logging.DEBUG)

# burnin_iterations = 100  # number of burnin iterations (#iterations)
burnin_iterations = 0  # number of burnin iterations (#iterations)
target_container = Path('frames/trj.0.pdb')  # trajectory filepath


def gromacs_input_files():
    """Create gromacs .top and .gro files in the target directory."""
    reference_system, topology = multistate_reporter_metadata(
        app.prms.ms_container,
        'reference_state.system topography.topology'.split())

    # create gromacs .top and .gro files in the target directory
    generate_gromacs_input(target_container,
                           topology=topology,
                           system=reference_system,
                           split='.gro')


if __name__ == '__main__':

    _ = extract(ms=app.prms.ms_container,
                target=target_container,
                state_index=app.prms.ref_state_index,
                discard=burnin_iterations)
    gromacs_input_files()
