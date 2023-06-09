"""Collection of utilities for training and defining models"""
import torch
from torch import nn
import torch.nn.functional as f


class CnnMedium(nn.Module):
    def __init__(self, use_cifar=False):
        super().__init__()
        if use_cifar:
            self.conv1 = nn.Conv2d(3, 16, 3, 1)
        else:
            self.conv1 = nn.Conv2d(1, 16, 3, 1)

        self.conv2 = nn.Conv2d(16, 16, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        if use_cifar:
            self.fc1 = nn.Linear(1568 * 2, 64)
        else:
            self.fc1 = nn.Linear(1152 * 2, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = f.relu(x)
        x = self.conv2(x)
        x = f.relu(x)
        x = f.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = f.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        # x = f.log_softmax(x, dim=1)
        return x


class DenseModel(nn.Module):
    def __init__(self, cifar=False):
        super().__init__()
        if cifar:
            self.lin = nn.Linear(32 * 32 * 3, 256)
        else:
            self.lin = nn.Linear(28 * 28, 256)

        self.ff = nn.Sequential(
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            # nn.Dropout(.25),
            nn.Linear(256, 256),
            nn.ReLU(),
            # nn.Dropout(.25),
            nn.Linear(256, 10))

    def forward(self, x):
        x = torch.flatten(x, 1)
        x = self.lin(x)
        x = self.ff(x)
        # x = f.log_softmax(x, dim=1)
        return x


class LargeModel(nn.Module):
    def __init__(self, use_cifar=False):
        super().__init__()
        if use_cifar:
            self.conv1 = nn.Conv2d(3, 64, 3, 1)
        else:
            self.conv1 = nn.Conv2d(1, 64, 3, 1)

        self.conv2 = nn.Conv2d(64, 128, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.25)
        self.dropout3 = nn.Dropout(0.25)
        self.fc1 = nn.Linear(3136 * 8, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = f.relu(x)
        x = self.conv2(x)
        x = f.relu(x)
        x = f.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = f.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        x = self.dropout3(x)
        x = self.fc3(x)
        # x = f.log_softmax(x, dim=1)
        return x


class LogisticReg(nn.Module):
    def __init__(self, cifar=False):
        super().__init__()
        if cifar:
            self.lin = nn.Linear(32 * 32 * 3, 10)
        else:
            self.lin = nn.Linear(28 ** 2, 10)

    def forward(self, x):
        x = torch.flatten(x, 1)
        x = self.lin(x)
        # x = f.log_softmax(x, dim=1)
        return x


Default_Net = CnnMedium


def hot_loader(path, cl):
    def lod(use_cifar):
        model = cl(use_cifar)
        model.load_state_dict(torch.load(path))
        model.eval()
        return model

    return lod


if __name__ == '__main__':
    # create the graph of the model, used as image in the thesis

    model = CnnMedium(use_cifar=True)
    from torchview import draw_graph

    model_graph = draw_graph(CnnMedium(use_cifar=True), input_size=(1, 3, 32, 32),
                             expand_nested=False,
                             hide_inner_tensors=True,
                             hide_module_functions=True,
                             )
    model_graph.visual_graph.render(format='png', filename='model_graph')

