import pennylane as qml
import torch
import torch.nn as nn


def state_prepare(input, qbits):
    """
    Prepares the initial state of the qubits using angle embedding.

    Args:
        input (Tensor): Input tensor containing the angles for the qubits.
        qbits (int): Number of qubits to prepare.
    """
    qml.AngleEmbedding(input, wires=range(qbits))


def conv(b1, b2, params):
    """
    Applies a convolution operation to the specified qubits using given parameters.

    Args:
        b1 (int): The first qubit index.
        b2 (int): The second qubit index.
        params (Tensor): A tensor containing three parameters for the RZ and RY gates.
    """
    qml.RZ(-torch.pi / 2, wires=b2)
    qml.CNOT([b2, b1])
    qml.RZ(params[0], wires=b1)
    qml.RY(params[1], wires=b2)
    qml.CNOT([b1, b2])
    qml.RY(params[2], wires=b2)
    qml.CNOT([b2, b1])
    qml.RZ(torch.pi / 2, wires=b1)


def pool(b1, b2, params):
    """
    Applies a pooling operation to the specified qubits using given parameters.

    Args:
        b1 (int): The first qubit index.
        b2 (int): The second qubit index.
        params (Tensor): A tensor containing three parameters for the RZ and RY gates.
    """
    qml.RZ(-torch.pi / 2, wires=b2)
    qml.CNOT([b2, b1])
    qml.RZ(params[0], wires=b1)
    qml.RY(params[1], wires=b2)
    qml.CNOT([b1, b2])
    qml.RY(params[2], wires=b2)


dev4 = qml.device("lightning.qubit", wires=4)


@qml.qnode(dev4, interface="torch")
def qcnn4(weights, inputs):
    state_prepare(inputs, 4)
    conv(0, 1, weights[0:3])
    conv(2, 3, weights[3:6])
    pool(0, 1, weights[6:9])
    pool(2, 3, weights[9:12])
    conv(1, 3, weights[12:15])
    pool(1, 3, weights[15:18])
    return qml.probs(wires=3)


dev8 = qml.device("lightning.qubit", wires=8)


@qml.qnode(dev8, interface="torch")
def qcnn8(weights, inputs):
    state_prepare(inputs, 8)
    conv(0, 1, weights[0:3])
    pool(0, 1, weights[3:6])
    conv(2, 3, weights[6:9])
    pool(2, 3, weights[9:12])
    conv(4, 5, weights[12:15])
    pool(4, 5, weights[15:18])
    conv(6, 7, weights[18:21])
    pool(6, 7, weights[21:24])
    conv(1, 3, weights[24:27])
    pool(1, 3, weights[27:30])
    conv(5, 7, weights[30:33])
    pool(5, 7, weights[33:36])
    conv(3, 7, weights[36:39])
    pool(3, 7, weights[39:42])
    return qml.probs(wires=7)


def draw(input, params, cir, name):
    qml.drawer.use_style("pennylane")
    fig, ax = qml.draw_mpl(cir)(params, input)
    fig.savefig("results/" + name + ".png")


class QCNN(nn.Module):
    """
    Defines a Quantum Convolutional Neural Network (QCNN) model for a specified number of qubits.

    Args:
        qbits (int): Number of qubits in the quantum circuit.

    Attributes:
        qcnn_layer (TorchLayer): The PyTorch layer representing the QCNN.
    """

    def __init__(self, qbits):
        super().__init__()
        self.qbits = qbits

        if qbits == 4:
            self.qcnn_layer = qml.qnn.TorchLayer(qcnn4, weight_shapes={"weights": 18})
        elif qbits == 8:
            self.qcnn_layer = qml.qnn.TorchLayer(qcnn8, weight_shapes={"weights": 42})
        else:
            self.qcnn_layer = qml.qnn.TorchLayer(qcnn8, weight_shapes={"weights": 84})

    def forward(self, x):
        """
        Defines the forward pass for the QCNN.

        Args:
            x (Tensor): Input tensor.

        Returns:
            Tensor: The output of the QCNN layer.
        """

        max = torch.max(x)
        min = torch.min(x)
        x = (x - min) / (max - min)
        x = 2 * x * torch.pi
        return self.qcnn_layer(x)
