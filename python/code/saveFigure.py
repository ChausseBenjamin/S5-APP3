from pathlib import Path

import matplotlib.pyplot as plt

DIRECTORY_PATH = Path("./graphs")


def save_plot(name: str):
    """
    Does the annoying bit of saving matplotlib figures.
    Automatically creates the output path if it doesn't
    exist. Includes the file format for you.

    :param name: Name for the figure, don't include any file extension.
    :type name: str
    """
    DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
    plt.savefig(DIRECTORY_PATH / f"{name}.svg", bbox_inches="tight")
