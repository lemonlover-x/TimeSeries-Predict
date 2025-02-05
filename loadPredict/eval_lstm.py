"""

"""


import torch
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt


from model.lstm import LSTMModel
from dataset import LoadDatasetTS
import config





if __name__ == '__main__':

    # load the model
    model = LSTMModel(input_size=3, hidden_size=64, num_layers=1).to(config.DEVICE)
    checkpoints = torch.load('./logs/lstm/minloss.tar')
    model.load_state_dict(checkpoints)

    # load the dataset
    dataset = LoadDatasetTS(train=False, label_in_feature=True)
    dataloader = DataLoader(
        dataset=dataset,
        batch_size=24,
        shuffle=False,
        pin_memory=True
    )

    for features, y in dataloader:
        features = features.to(config.DEVICE)
        y = y.to(config.DEVICE)
        features = features.permute(1, 0, 2)
        y_hat = model(features)

        # plot
        plt.figure()
        x = np.arange(24)
        y = y.reshape((y.shape[0],)).detach().numpy()
        y_hat = y_hat.reshape((y_hat.shape[0],)).detach().numpy()
        plt.plot(x, y, label='real')
        plt.plot(x, y_hat, label='prediction')
        plt.legend()

        plt.show()

        break