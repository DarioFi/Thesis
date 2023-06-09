"""This file is used to plot the results of the training. It is intended to be modified to plot different combinations of results.
It uses the logs saved in the json file."""

import json

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

with open("logs.json", "r") as file:
    data = json.load(file)

# allowed_models = ["resnet non", ]
allowed_models = ["resnet pre", ]
allowed_algs = ["*"]
# allowed_algs = ["sgbd"]
lower_bound_epochs = 12
upper_bound_epochs = 17
corrected = (True, False)
# corrected = (False,)
print(len(data))


data.sort(key=lambda x: (x["algorithm"],-x["stepsize"]))
fig, ax = plt.subplots(2, 2, figsize=(12, 12))

# fig.tight_layout()

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.25)

i = 0

# le run erano 0.1, 0.01, e 0.001
# second round era 1, 0.1, 0.01

plot_epochs = 10 ** 10
lrs = [0, 1, .1, .01]
for obs in data[:]:

    if not (obs['corrected'] in corrected):
        continue

    if "*" not in allowed_models:
        # print("large" not in obs["model"].lower())
        if any(x not in obs["model"].lower() for x in allowed_models):
            continue

    if not (lower_bound_epochs <= obs["epochs"] <= upper_bound_epochs):
        continue

    if "*" not in allowed_algs:
        if any(x not in obs["algorithm"].lower() for x in allowed_algs):
            continue

    if i > 3: continue
    ax1 = ax[i // 2][i % 2]
    # ax1 = ax[i]
    # fig, ax1 = plt.subplots()
    i += 1
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Loss")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Accuracy")

    ax1.plot(obs["train_losses"][:plot_epochs], label="Train", color="red")

    ax1.plot(obs["test_losses"][:plot_epochs], label="Test loss", color="tab:blue")
    # ax1.plot(obs["test_losses_ensemble"], color="tab:green", label="Loss ensemble")
    ax2.plot(obs["test_accuracies"][:plot_epochs], label="Test accuracy", color="tab:orange")
    # ax2.plot(obs["test_accuracies_ensemble"], color="tab:purple", label="Accuracy ensemble")

    if "Adam" in obs['algorithm']:
        plt.title(f"{obs['algorithm']}\n stepsize=0.001")
    else:
        plt.title(
            f"{obs['algorithm']}\nalpha*={obs['alfa_target']} stepsize={obs['stepsize']}")

    # plt.title(f"SGDB - lr={lrs[i - 1]}")
    # plt.title(f"{obs['model']}\nExtreme={obs['extreme']} alpha*={obs['alfa_target']}")
    ax1.legend()
    ax2.legend(loc="upper left")

    # if i == 0:
    #     ax1.set_ylim(0.0, 4)
    # else:
    #     ax1.set_ylim(0.0, 3)

    ax2.set_ylim(0, 100)

    ax1.set_ylim(0, 5)
    # ax1.set_yscale("log")
    # plt.ylim(bottom=1e-10)

    ax1.grid()
plt.savefig("temp.png",bbox_inches='tight')
# plt.show()
