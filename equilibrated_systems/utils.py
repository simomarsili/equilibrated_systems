# -*- coding: utf-8 -*-
"""Setup simulation parameters."""
# pylint: disable=no-member

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from types import SimpleNamespace

from mmdemux import extract_trajectory
from mmlite.multistate import propagator


def initialize_sampler(prms):
    """Initialize a multistate sampler.

    Parameters
    ----------
    prms : SimpleNamespace

    Returns
    -------
    sampler

    """

    # initialize sampler
    smp = prms.sampler_class(number_of_iterations=0,
                             mcmc_moves=propagator(
                                 timestep=prms.timestep,
                                 n_steps=prms.state_update_steps),
                             online_analysis_interval=None)

    # set sampler states and positions
    smp.from_testsystem(prms.test,
                        thermodynamic_states=prms.thermodynamic_states,
                        pressure=prms.pressure,
                        stride=prms.checkpoint_iterations,
                        storage=prms.ms_container)

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
