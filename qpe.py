"""
qpe.py: Quantum phase estimation.
"""

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_multivector
from numpy import pi, sqrt
import matplotlib as plt

n = 4

a = QuantumRegister(n + 1, 'qreg')
b = QuantumRegister(1, 'anc')
c = ClassicalRegister(n, 'creg')

qc = QuantumCircuit(a, b, c)

# Using the last qubit for psi, the first four as counting qubits
# Creating psi
qc.x(a[n])

#Pushing into superposition
for i in range(n):
    qc.h(a[i])

#Applying controlled U's
for i in range(n):
    qc.cu1(pi*(2**(i))/4, a[i], a[n])

# Inverse QFT
for i in range((n) // 2):
    qc.swap(a[i], a[n - i - 1])

for i in range(n):
    for j in range(i):
        qc.cu1(-pi/(2**(i-j)), a[j], a[i])
    qc.h(a[i])

for i in range(n):
    qc.measure(a[i], c[i])

backend = Aer.get_backend('qasm_simulator')

shots = 4096
job = execute(qc, backend=backend, shots=shots)

print("""##################################""")
print('Shots:', shots)
print('Results:', job.result().get_counts())
print("""##################################""")
