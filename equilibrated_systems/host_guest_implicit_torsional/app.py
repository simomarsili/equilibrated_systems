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

from equilibrated_systems.utils import (initialize_sampler,
                                        parse_command_line_args)

test = systems.HostGuestImplicit()  # test system
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
    try:
        sampler = sampler_class.from_storage(storage=str(ms_container))
    except FileNotFoundError:
        # sampler = initialize_sampler(prms)

        sampler = initialize_sampler(test, sampler_class, timestep,
                                     state_update_steps,
                                     reference_thermodynamic_state,
                                     thermodynamic_states, pressure,
                                     checkpoint_iterations, ms_container)
        sampler.metadata.update(metadata)

    args = parse_command_line_args()
    n_iterations = args['n_iterations']
    n_equilibration = args['equilibration']
    if n_equilibration > 0:
        sampler.equilibrate(n_equilibration)
    if n_iterations > 0:
        sampler.extend(n_iterations)
