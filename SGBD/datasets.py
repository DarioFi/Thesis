"""This file contains the functions to load the datasets."""

import torch
from torchvision import datasets, transforms


def get_mnist(train_kwargs, test_kwargs):
    """
    This function loads the MNIST dataset.
    :param train_kwargs: kwargs to pass to torch.utils.data.DataLoader
    :param test_kwargs: kwargs to pass to torch.utils.data.DataLoader
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    dataset1 = datasets.MNIST('../data', train=True, download=True,
                              transform=transform)
    dataset2 = datasets.MNIST('../data', train=False,
                              transform=transform)
    train_loader = torch.utils.data.DataLoader(dataset1, **train_kwargs)
    test_loader = torch.utils.data.DataLoader(dataset2, **test_kwargs)

    return train_loader, test_loader


def get_cifar10(train_kwargs, test_kwargs):
    """
    This function loads the CIFAR10 dataset.
    :param train_kwargs: kwargs to pass to torch.utils.data.DataLoader
    :param test_kwargs: kwargs to pass to torch.utils.data.DataLoader
    """
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    dataset1 = datasets.CIFAR10(root='../data', train=True,
                                download=True, transform=transform)

    dataset2 = datasets.CIFAR10(root='../data', train=False, transform=transform)

    trainloader = torch.utils.data.DataLoader(dataset1, **train_kwargs)
    testloader = torch.utils.data.DataLoader(dataset2, **test_kwargs)

    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    return trainloader, testloader
