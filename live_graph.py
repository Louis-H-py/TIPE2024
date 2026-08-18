import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd

matplotlib.use("tkagg")

fig, axs = plt.subplots(2, 2)

axs2 = axs[0][0].twinx()
axs3 = axs[0][1].twinx()

MA_LEN: int = 25


def moving_average(x, length):
    r = []

    for i in range(0, len(x)):
        a = x[max(0, i - length):i]
        r.append(np.sum(a) / min(i, length))

    return r


def plot(data):
    axs[0][0].clear()
    axs[1][0].clear()
    axs[0][1].clear()
    axs[1][1].clear()

    x = data["game played"].values

    # ax 1
    axs[0][0].clear()
    axs2.clear()

    l1 = axs[0][0].plot(x, data["model accuracy"].values, c="tab:blue", label="Accuracy")
    axs[0][0].plot(x, moving_average(data["model accuracy"].values, MA_LEN), c="black", alpha=0.25)

    l2 = axs2.plot(x, data["model loss"].values, c="tab:orange", label="Loss")
    axs2.plot(x, moving_average(data["model loss"].values, MA_LEN), c="black", alpha=0.25)

    axs[0][0].set_title("Neural network accuracy/loss")
    lt = l1 + l2
    labs = [lab.get_label() for lab in lt]
    axs[0][0].legend(lt, labs)
    axs[0][0].set_ylim(0, 1.1)

    # ax 2
    axs[0][1].clear()
    axs3.clear()

    l1 = axs[0][1].plot(x, data["model accuracy"].values, c="tab:blue", label="Accuracy")
    axs[0][1].plot(x, moving_average(data["model accuracy"].values, MA_LEN), c="black", alpha=0.25)

    l2 = axs3.plot(x, data["model loss"].values, c="tab:orange", label="Loss")
    axs3.plot(x, moving_average(data["model loss"].values, MA_LEN), c="black", alpha=0.25)

    axs[0][1].set_title("Neural network accuracy/loss")
    lt = l1 + l2
    labs = [lab.get_label() for lab in lt]
    axs[0][1].legend(lt, labs)

    # ax 3
    axs[1][0].clear()
    d = data["elo rating"].values
    d[702:] += 220
    axs[1][0].step(x, d, c="tab:blue")
    axs[1][0].set_title("Model Elo rating")

    # ax 4
    y = (data["score"].values * 64)

    axs[1][1].clear()
    axs[1][1].plot(x, [max(32, v) for v in y], c="tab:green", alpha=0.5)
    axs[1][1].plot(x, [min(32, v) for v in y], c="tab:red", alpha=0.5)

    axs[1][1].plot(x, moving_average(y, MA_LEN), c="black", alpha=0.75)

    axs[1][1].plot(x, [32 for _ in x], c="black", alpha=0.75)
    axs[1][1].set_title("Model score")
    axs[1][1].set_ylim(0, 64)


def animate(i):
    data = pd.read_csv("train_history.txt", encoding="utf-8", sep=";")
    plot(data)


if __name__ == '__main__':
    plot(pd.read_csv("train_history.txt", encoding="utf-8", sep=";", ))
    ani = animation.FuncAnimation(fig, animate, interval=5000)
    plt.show()
