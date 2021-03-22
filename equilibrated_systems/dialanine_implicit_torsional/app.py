# -*- coding: utf-8 -*-
"""Setup simulation parameters."""
# pylint: disable=no-member

import logging
from pathlib import Path

import numpy as np
import openmmtools as mmtools
from mmlite import systems
from mmlite.multistate import ReplicaExchangeSampler, create_compound_states
from simtk import unit

from equilibrated_systems.utils import (parse_command_line_args,
                                        parse_parameters, run)

test = systems.AlanineDipeptideImplicit()  # test system
temperature = 298 * unit.kelvin
pressure = None

sampler_class = ReplicaExchangeSampler
timestep = 2.0 * unit.femtoseconds
state_update_steps = 1000  # stride in steps between state update (#steps)
checkpoint_iterations = 1  # checkpoint_interval (#iterations)

protocol = dict(  # define the scaling protocol as a dict
    lambda_torsions=list(np.logspace(0, -1, 4)))
ref_state_index = 0

reference_thermodynamic_state = mmtools.states.ThermodynamicState(
    system=test.system, temperature=temperature, pressure=pressure)
thermodynamic_states = create_compound_states(reference_thermodynamic_state,
                                              test.topology,
                                              protocol,
                                              region='default')
metadata = create_compound_states.metadata

ms_container = Path('frames/trj.nc')  # trajectory filepath
verbose_module = 'openmmtools.multistate'

if verbose_module:
    logging.getLogger(verbose_module).setLevel(logging.DEBUG)

if __name__ == '__main__':
    args = parse_command_line_args()
    parameters = parse_parameters(dict(**locals()))
    run(args, parameters)
