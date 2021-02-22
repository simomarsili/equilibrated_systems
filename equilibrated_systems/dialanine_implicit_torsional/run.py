# -*- coding: utf-8 -*-
"""Run/restart a simulation from checkpoint."""
# pylint: disable=no-member
import logging
from argparse import ArgumentParser, RawDescriptionHelpFormatter

import app

from equilibrated_systems.utils import get_variables, initialize_sampler

N_ITERATIONS = 1000  # default
prms = get_variables(app)

if prms.verbose_module:
    logging.getLogger(prms.verbose_module).setLevel(logging.DEBUG)


def parse_command_line_args():
    """Parse command line options."""
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__)
    parser.add_argument('-n', '--n_iterations', type=int, default=N_ITERATIONS)
    return vars(parser.parse_args())


if __name__ == '__main__':
    try:
        sampler = prms.sampler_class.from_storage(
            storage=str(prms.ms_container))
    except FileNotFoundError:
        sampler = initialize_sampler(prms)

    args = parse_command_line_args()
    n_iterations = args['n_iterations']
    sampler.extend(n_iterations)
