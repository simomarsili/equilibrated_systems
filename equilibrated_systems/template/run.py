# -*- coding: utf-8 -*-
"""Run/restart a simulation from checkpoint."""
# pylint: disable=no-member
import logging
from argparse import ArgumentParser, RawDescriptionHelpFormatter

import app

if app.verbose_module:
    logging.getLogger(app.verbose_module).setLevel(logging.DEBUG)

N_ITERATIONS = 1000  # default


def parse_command_line_args():
    """Parse command line options."""
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__)
    parser.add_argument('-n', '--n_iterations', type=int, default=N_ITERATIONS)
    return vars(parser.parse_args())


if __name__ == '__main__':
    try:
        sampler = app.sampler_class.from_storage(storage=str(app.ms_container))
    except FileNotFoundError:
        sampler = app.initialize_sampler()

    args = parse_command_line_args()
    n_iterations = args['n_iterations']
    sampler.extend(n_iterations)
