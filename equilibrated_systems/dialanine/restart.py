# -*- coding: utf-8 -*-
"""Extende a simulation from checkpoint."""
# pylint: disable=no-member
import logging

import app

if app.verbose_module:
    logging.getLogger(app.verbose_module).setLevel(logging.DEBUG)

if __name__ == '__main__':
    sampler = app.sampler_class.from_storage(storage=str(app.ms_container))
    sampler.extend(1000)
