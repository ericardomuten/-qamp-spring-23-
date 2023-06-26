#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

