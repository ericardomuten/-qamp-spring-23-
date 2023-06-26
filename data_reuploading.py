from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit.circuit.library import TwoLocal

import numpy as np
from typing import Optional, Union, List, Callable


class DataReuploading():
    """
    Create the Data Reuploading Classifier ansatz.
    Based on the works of Perez-Salinas, et al.
      https://quantum-journal.org/papers/q-2020-02-06-226/pdf/
    """

    def __init__(
        self,
        num_qubits: int,
        num_features: int,
        num_layers: int,
        entanglement_blocks: Optional[
            Union[str, List[str], type, List[type], QuantumCircuit, List[QuantumCircuit]]
        ] = 'cz',
        entanglement: Union[str, List[List[int]], Callable[[int], List[int]]] = "linear",
        skip_final_entangling_layer: bool = True,
        insert_barriers: bool = False,
    ):
        """
        Args:
            num_qubits: The number of qubits.
            num_features: The number of input features (the dimension of the input data).
            num_layers: The number of layers (N).
            entanglement_blocks: The gates used in the entanglement layer. See the TwoLocal documentation
                https://qiskit.org/documentation/stubs/qiskit.circuit.library.TwoLocal.html. Defaults to ``cz``.
            entanglement: Specifies the entanglement structure. See the TwoLocal documentation
                https://qiskit.org/documentation/stubs/qiskit.circuit.library.TwoLocal.html. Defaults to ``linear``.
            skip_final_entangling_layer: If ``True``, the final layer will end with only rotational gate (no entangling layer). If ``False``,
                the final layer will end with entangling layer following the last rotational gate layer. Defaults to ``True``.
            insert_barriers: If ``True``, barriers are inserted in between each layer. If ``False``,
                no barriers are inserted. Defaults to ``False``.
        Returns:
            ansatz: A QuantumCircuit object.
        """

        self._num_qubits = num_qubits
        # rounding up the number of features to the nearest integer number that is multiples of 3
        self._num_features = int(np.ceil(num_features/3)*3)
        self._num_layers = num_layers

        self.parameters = ParameterVector(name="θ", length=2*self._num_qubits*self._num_features*self._num_layers)
        self.input_params = ParameterVector(name="x", length=self._num_features)

        qc = QuantumCircuit(self._num_qubits)

        for l in range(self._num_layers):
          for k in range(int(np.ceil(num_features/3))):
            for q in range(self._num_qubits):
              qc.compose(self.rotational_gate_layer(self._num_qubits, q,
                                                    self.parameters[l*self._num_qubits*int(np.ceil(num_features/3))*2*3 + q*int(np.ceil(num_features/3))*2*3 + k*2*3
                                                                    :l*self._num_qubits*int(np.ceil(num_features/3))*2*3 + q*int(np.ceil(num_features/3))*2*3 + k*2*3 + 2*3],
                                                    self.input_params[k*3 : k*3+3]), inplace=True)

          if insert_barriers:
            qc.barrier()

          # if it's not the last layer, add the entangling layer
          if (l+1) != self._num_layers and self._num_qubits != 1:
            qc.compose(self.entanglement_layer(self._num_qubits, entanglement_blocks=entanglement_blocks, entanglement=entanglement), inplace=True)
            if insert_barriers:
              qc.barrier()

          # add entangling layer on the last layer if set by the user
          if skip_final_entangling_layer == False and (l+1) == self._num_layers and self._num_qubits != 1:
            qc.compose(self.entanglement_layer(self._num_qubits, entanglement_blocks=entanglement_blocks, entanglement=entanglement), inplace=True)
            if insert_barriers:
              qc.barrier()


        self.circuit = qc

    def rotational_gate_layer(
        self,
        num_qubits: int,
        qubit_id: int,
        trainable_params : ParameterVector,
        input_params : ParameterVector,
    ):
        """
          This is the rotational gate layer.
          Args:
              num_qubits: The number of qubits.
              num_features: The number of input features (the dimension of the input data).
          Returns:
              circuit_block: A QuantumCircuit object with ParameterVector as gate's arguments.
        """

        circuit_block = QuantumCircuit(num_qubits)
        circuit_block.rx(trainable_params[0] + trainable_params[3]*input_params[0], qubit_id)
        circuit_block.ry(trainable_params[1] + trainable_params[4]*input_params[1], qubit_id)
        circuit_block.rz(trainable_params[2] + trainable_params[5]*input_params[2], qubit_id)

        return circuit_block



    def entanglement_layer(
        self,
        num_qubits: int,
        entanglement_blocks: Optional[
            Union[str, List[str], type, List[type], QuantumCircuit, List[QuantumCircuit]]
        ] = None,
        entanglement: Union[str, List[List[int]], Callable[[int], List[int]]] = "full",
    ):
        """
          This is the entangling layer.
          Args:
              num_qubits: The number of qubits.
          Returns:
              circuit_block: A QuantumCircuit object consists of entangling gates.
        """

        circuit_block = QuantumCircuit(num_qubits)

        # Build the engangling layer
        entangling_layer = TwoLocal(num_qubits=num_qubits, entanglement_blocks=entanglement_blocks, entanglement=entanglement, reps=1).decompose()
        circuit_block.compose(entangling_layer, inplace=True)

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