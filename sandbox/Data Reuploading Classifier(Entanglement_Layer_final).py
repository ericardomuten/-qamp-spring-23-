#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_machine_learning.algorithms import VQC


from qiskit_machine_learning.connectors import TorchConnector
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import TwoLocal
from qiskit.circuit.library.n_local import RealAmplitudes
from qiskit.circuit.library import ZZFeatureMap
from qiskit.quantum_info import Pauli


# Necessary imports

import numpy as np
import matplotlib.pyplot as plt

from torch import Tensor
from torch.nn import Linear, CrossEntropyLoss, MSELoss
from torch.optim import LBFGS

from qiskit import QuantumCircuit
from qiskit.utils import algorithm_globals
from qiskit.circuit import Parameter
from qiskit.circuit.library import RealAmplitudes, ZZFeatureMap
from qiskit_machine_learning.neural_networks import SamplerQNN, EstimatorQNN
from qiskit_machine_learning.connectors import TorchConnector

# Set seed for random generators
algorithm_globals.random_seed = 42


# In[2]:


from qiskit import QuantumCircuit

class DataReuploading():
    """
    Create the Data Reuploading Classifier ansatz.
    """

    def __init__(
        self,
        num_qubits: int = None,
        num_features: int = None,
        num_layers: int = None
    ):
        """
        Args:
            num_qubits: The number of qubits.
            num_features: The number of input features (the dimension of the input data).
            num_layers: The number of layers (N).
        Returns:
            ansatz: A QuantumCircuit object.
        """
        self._num_qubits = num_qubits
        self._num_features = num_features
        self._num_layers = num_layers

    def rotational_gate_layer(
        self,
        num_qubits: int = None,
        num_features: int = None
    ):
        """
          This is the L layer.
          Args:
              num_qubits: The number of qubits.
              num_features: The number of input features (the dimension of the input data).
          Returns:
              circuit_block: A QuantumCircuit object with ParameterVector as gate's arguments.
        """
        # Implement the rotational gate layer logic here
        pass

    def entanglement_layer(
        self,
        num_qubits: int = None
    ):
        """
          This is the E layer for even and odd number of qubits.
          Args:
              num_qubits: The number of qubits.
          Returns:
              circuit_block: A QuantumCircuit object consists of only CZ gates.
        """
        circuit_block = QuantumCircuit(num_qubits)

        # For even number of qubits
        if num_qubits % 2 == 0:
            # Divide the qubits into two sets
            set_size = num_qubits // 2
            set1 = range(set_size)
            set2 = range(set_size, num_qubits)

            # Apply CZ gates within each set
            for i in range(set_size - 1):
                circuit_block.cz(set1[i], set1[i+1])
                circuit_block.cz(set2[i], set2[i+1])

            # Apply CZ gates between the sets
            circuit_block.cz(set1[-1], set2[0])
            circuit_block.cz(set2[-1], set1[0])
        
        # For odd number of qubits
        else:
            # Apply CZ gates between adjacent qubits
            for i in range(num_qubits - 1):
                circuit_block.cz(i, i + 1)

            

        return circuit_block

    @property
    def num_qubits(self) -> int:
        """Returns the number of qubits used by the ansatz."""
        return self._num_qubits

    @property
    def num_features(self) -> int:
        """Returns the number of features of the input data accepted by the ansatz."""
        return self._num_features

    @property
    def num_layers(self) -> int:
        """Returns the number of layers used by the ansatz."""
        return self._num_layers










