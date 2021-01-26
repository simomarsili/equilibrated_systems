# -*- coding: utf-8 -*-
"""Prepare input for alchemical transformations."""
import logging

import app

if app.verbose_module:
    logging.getLogger(app.verbose_module).setLevel(logging.DEBUG)

if __name__ == '__main__':

    _ = app.extract()
    app.gromacs_input_files()
