"""
hhl.py: Implements the HHL linear systems solver using QISkit
Aqua.
"""

import qiskit
from qiskit.aqua import run_algorithm
from qiskit.aqua.input import LinearSystemInput
from qiskit.quantum_info import state_fidelity
from qiskit.aqua.algorithms.classical import ExactLSsolver
import numpy as np

# Set algo params
params = {
    'problem': {
        'name': 'linear_system'
    },
    'algorithm': {
        'name': 'HHL'
    },
    'eigs': {
        'expansion_mode': 'suzuki',
        'expansion_order': 1,
        'name': 'EigsQPE',
        'num_ancillae': 3, #Set to increase numerical accuracy
        'num_time_slices': 1
    },
    'reciprocal': {
        'name': 'Lookup'
    },
    'backend': {
        'provider': 'qiskit.BasicAer',
        'name': 'statevector_simulator'
    }
}

matrix = [[1, -1/3], [-1/3, 1]]
vector = [1, 0]
params['input'] = {
    'name': 'LinearSystemInput',
    'matrix': matrix,
    'vector': vector
}

# Get the quantum solution
result = run_algorithm(params)

# Get reference solution
result_ref = ExactLSsolver(matrix, vector).run()

print('##################################')
print('A:', matrix)
print('b:', vector)
print('Found x:', np.round(result['solution'], 5))
print('Reference Solution (Classical method):',  np.round(result_ref['solution'], 5))
print('Result fidelity:', fidelity(result['solution'], result_ref['solution'])) 
print('##################################')