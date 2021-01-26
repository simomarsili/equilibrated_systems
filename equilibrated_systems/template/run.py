# -*- coding: utf-8 -*-
"""Run/restart a simulation from checkpoint."""
# pylint: disable=no-member
import logging

import app

if app.verbose_module:
    logging.getLogger(app.verbose_module).setLevel(logging.DEBUG)

n_steps = 1000

if __name__ == '__main__':
    try:
        sampler = app.sampler_class.from_storage(storage=str(app.ms_container))
    except FileNotFoundError:
        sampler = app.initialize_sampler()

    sampler.extend(n_steps)
