# -*- coding: utf-8 -*-
"""Setup simulation parameters."""
# pylint: disable=no-member

from pathlib import Path
from types import SimpleNamespace

import numpy as np
from mmlite import systems
from mmlite.multistate import SAMSSampler
from simtk import unit

prms = SimpleNamespace(**dict(
    # test = systems.HostGuestImplicit(constraints=None)  # test system
    test=systems.HostGuestImplicit(),  # test system
    ref_state_index=0,
    temperatures=list(np.logspace(np.log10(298), np.log10(600), num=20)),
    # temperatures=298 * unit.kelvin
    # pressure=1.0 * unit.atmosphere
    pressure=None,
    # timesteps
    timestep=1.0 * unit.femtoseconds,
    state_update_steps=1000,  # stride in steps between state update (#steps)
    # iterations
    checkpoint_iterations=1,  # checkpoint_interval (#iterations)
    ms_container=Path('frames/trj.nc'),  # trajectory filepath
    verbose_module='openmmtools.multistate',
    sampler_class=SAMSSampler,
))
