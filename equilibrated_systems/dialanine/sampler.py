# -*- coding: utf-8 -*-
"""Functions for sampling."""
# pylint: disable=protected-access, no-member, unused-import
import logging

import app

if app.verbose_module:
    logging.getLogger(app.verbose_module).setLevel(logging.DEBUG)

if __name__ == '__main__':

    # initialize sampler
    sampler = app.initialize_sampler()

    # run the simulation
    sampler.run()
