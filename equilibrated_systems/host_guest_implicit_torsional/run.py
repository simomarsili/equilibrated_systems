# -*- coding: utf-8 -*-
"""Run/restart a simulation from checkpoint."""
# pylint: disable=no-member
import logging

import app

from equilibrated_systems.utils import (get_variables, initialize_sampler,
                                        parse_command_line_args)

prms = get_variables(app)

if prms.verbose_module:
    logging.getLogger(prms.verbose_module).setLevel(logging.DEBUG)

if __name__ == '__main__':
    try:
        sampler = prms.sampler_class.from_storage(
            storage=str(prms.ms_container))
    except FileNotFoundError:
        sampler = initialize_sampler(prms)
        sampler.metadata.update(app.metadata)

    args = parse_command_line_args()
    n_iterations = args['n_iterations']
    n_equilibration = args['equilibration']
    if n_equilibration > 0:
        sampler.equilibrate(n_equilibration)
    if n_iterations > 0:
        sampler.extend(n_iterations)
