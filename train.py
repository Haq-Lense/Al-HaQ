import sys
import torch

# Importing custom dataset and batching functions
from src.preprocessing import FakeTweetsDataset, create_mini_batch
from torch.utils.data import DataLoader
from torch import nn

# Importing the quantum neural network models
import models.qnn as qnn

# Importing utilities for tokenization and model loading
from transformers import AutoTokenizer, XLNetForSequenceClassification
from IPython.display import display, clear_output
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import os

# Disabling SSL certificate verification for outgoing requests
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""

# Setting the batch size for training
BATCH_SIZE = 24

# Configuring proxy settings for network requests
proxy = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}

# Model name for tokenization and classification
MODEL_NAME = "xlnet-base-cased"

# Initializing the tokenizer with the pre-trained model name
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Loading the XLNet model for sequence classification with two output labels
cla_model = XLNetForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

# Initializing the quantum convolutional neural network model
qcnn = qnn.QCNN(20)

# Setting the path to the dataset
data_path = "datasets/twitter_dataset"

# Loading the dataset for training
trainset = FakeTweetsDataset("train", tokenizer=tokenizer, path=data_path)

# Creating a DataLoader for batching operations
trainloader = DataLoader(trainset, batch_size=BATCH_SIZE, collate_fn=create_mini_batch)

# Setting the device to GPU if available, else CPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Sending models to the device
cla_model.to(device)
qcnn.to(device)

# Setting models to training mode
cla_model.train()
qcnn.train()

# Initializing the optimizer with parameters from both models
optimizer = torch.optim.AdamW(
    [{"params": cla_model.parameters()}, {"params": qcnn.parameters()}], lr=1e-3
)

# Defining the loss function for training
loss_func = nn.CrossEntropyLoss()

# Number of training epochs
NUM_EPOCHS = 50

# Training loop
for epoch in range(NUM_EPOCHS):
    train_loss = 0.0
    train_acc = 0.0

    # Printing the epoch number
    print(f"Epoch [{epoch + 1}/{NUM_EPOCHS}]")

    # Iterating over batches of data
    for batch_idx, data in enumerate(trainloader):

        # Moving data to the device
        tokens_tensors, segments_tensors, masks_tensors, labels = [
            t.to(device) for t in data
        ]

        # Resetting gradients
        optimizer.zero_grad()

        # Generating inputs for the QCNN from the XLNet model
        q_input = cla_model(
            input_ids=tokens_tensors,
            token_type_ids=segments_tensors,
            attention_mask=masks_tensors,
        )[0].to(device)

        # Getting predictions from QCNN
        outputs = qcnn(q_input)

        # Calculating loss
        loss = loss_func(outputs, labels)

        # Backpropagation
        loss.backward()
        optimizer.step()

        # Calculating accuracy
        pred = torch.argmax(outputs, dim=1)
        train_acc = accuracy_score(pred.cpu().tolist(), labels.cpu().tolist())

        # Accumulating the loss
        train_loss += loss.item()

    # Printing the accuracy and loss for the epoch
    print(f"acc={train_acc}, loss={train_loss / (batch_idx + 1):.2f}")

    # Saving models after each epoch
    torch.save(cla_model, "results/xlnet_twitter.pth")
    torch.save(qcnn.state_dict(), "results/qcnn_twitter_tx.pth")


# Saving models at the end of training
torch.save(cla_model, "results/xlnet_twitter_tx.pth")
torch.save(qcnn.state_dict(), "results/qcnn_twitter_tx.pth")
