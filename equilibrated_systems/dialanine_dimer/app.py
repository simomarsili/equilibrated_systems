# -*- coding: utf-8 -*-
"""Setup simulation parameters."""
# pylint: disable=no-member

import logging
from pathlib import Path

import numpy as np
import openmmtools as mmtools
import simtk.openmm as mm
from mmlite.multistate import ReplicaExchangeSampler, create_compound_states
from mmlite.system import SystemMixin
from openmmtools import testsystems
from simtk import unit

from equilibrated_systems.utils import (parse_command_line_args,
                                        parse_parameters, run)


class AlanineDipeptideDimer(SystemMixin, testsystems.TestSystem):
    """Alanine dipeptide + LJ particle."""
    def __init__(self, constraints=mm.app.HBonds, hydrogenMass=None, **kwargs):

        testsystems.TestSystem.__init__(self, **kwargs)

        pdb = mm.app.PDBFile(
            '/media/data/scr/equilibrated_systems/equilibrated_systems/'
            'bi_dialanine/input.pdb')
        topology = pdb.topology
        positions = pdb.positions

        forcefield = mm.app.ForceField('amber99sb.xml', 'tip3p.xml')
        system = forcefield.createSystem(pdb.topology,
                                         constraints=constraints,
                                         nonbondedCutoff=1 * unit.nanometer,
                                         hydrogenMass=hydrogenMass)
        '''
        prmtop_filename = testsystems.get_data_filename(
            "data/alanine-dipeptide-gbsa/alanine-dipeptide.prmtop")
        crd_filename = testsystems.get_data_filename(
            "data/alanine-dipeptide-gbsa/alanine-dipeptide.crd")
        prmtop = mm.app.AmberPrmtopFile(prmtop_filename)


        system = prmtop.createSystem(implicitSolvent=None,
                                     constraints=constraints,
                                     nonbondedCutoff=None,
                                     hydrogenMass=hydrogenMass)

        # Extract topology
        topology = prmtop.topology

        # Read positions.
        inpcrd = mm.app.AmberInpcrdFile(crd_filename)
        positions = inpcrd.getPositions(asNumpy=True)

        # add a LJ particle to the topology
        chain = topology.addChain()  # add a chain
        residue = topology.addResidue('Lig', chain)  # add a 'Ligand' residue
        element = mm.app.Element.getBySymbol('Ar')
        topology.addAtom('Ar', element, residue)  # add an atom

        # add particle coordinates to positions
        coord = np.array([0., 0., 0.]).reshape((1, 3))
        positions = np.append(positions._value, coord, axis=0) * positions.unit

        # add forces to system
        for k in range(system.getNumForces()):
            nbforce = system.getForce(k)
            if isinstance(nbforce, mm.openmm.NonbondedForce):
                break
        print(type(nbforce))
        mass = 39.9 * unit.amu
        charge = 0.0 * unit.elementary_charge
        sigma = 3.350 * unit.angstrom
        epsilon = 10.0 * unit.kilocalories_per_mole
        system.addParticle(mass)
        nbforce.addParticle(charge, sigma, epsilon)
        '''

        # print(type(system), type(nbforce))

        self.system, self.positions, self.topology = (system, positions,
                                                      topology)


test = AlanineDipeptideDimer()  # test system

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
    args = parse_command_line_args()
    parameters = parse_parameters(dict(**locals()))
    run(args, parameters)
