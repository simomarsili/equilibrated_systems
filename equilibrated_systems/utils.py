# -*- coding: utf-8 -*-
"""Setup simulation parameters."""
# pylint: disable=no-member

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from types import SimpleNamespace

from mmdemux import extract_trajectory
from mmlite.multistate import propagator


def initialize_sampler(  # pylint: disable=too-many-arguments
        test, sampler_class, timestep, state_update_steps, reference_state,
        thermodynamic_states, pressure, checkpoint_iterations, ms_container):
    """Initialize a multistate sampler.

    Parameters
    ----------
    test : TestSystem object
    sampler_class : MultiStateSampler-derived class
    timestep : Quantity
        Simulation timestep
    state_update_steps : int
        Len of an iteration (in time steps).
        States are updated at each iteration.
    reference_state
    thermodynamic_states
    pressure : Quantity or None
    checkpoint_iterations : int
        Stride for checkpoint print (in iterations)
    ms_container : pathlib.Path
        Path to multistate trajectory container


    Returns
    -------
    sampler

    """

    # initialize sampler
    smp = sampler_class(number_of_iterations=0,
                        mcmc_moves=propagator(timestep=timestep,
                                              n_steps=state_update_steps),
                        online_analysis_interval=None)

    # set sampler states and positions
    smp.from_testsystem(test,
                        reference_state=reference_state,
                        thermodynamic_states=thermodynamic_states,
                        pressure=pressure,
                        stride=checkpoint_iterations,
                        storage=ms_container)

    smp.minimize()

    return smp


def extract(ms, target, state_index=0, discard=0):
    """Extract configurations at the target thermodynamic state."""
    # discard starting configuration from trajectory
    trj = extract_trajectory(nc_path=str(ms),
                             to_file=str(target),
                             state_index=state_index,
                             start_frame=discard)
    return trj


def get_variables(m):
    """
    Return a namespace of variables defined in module `m`.

    """
    vrs = {k: v for k, v in m.__dict__.items() if not k.startswith('__')}
    return SimpleNamespace(**vrs)


def parse_command_line_args():
    """Parse command line options."""
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__)
    parser.add_argument('-n', '--n_iterations', type=int, default=100)
    parser.add_argument('-e', '--equilibration', type=int, default=0)
    return vars(parser.parse_args())
