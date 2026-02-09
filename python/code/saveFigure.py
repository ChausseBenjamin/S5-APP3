from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

# mpl.rcParams["font.family"] = "CMU Serif"
mpl.rcParams["mathtext.fontset"] = "cm"

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
    plt.tight_layout()
    plt.rcParams["figure.figsize"] = (16, 9)
    plt.savefig(DIRECTORY_PATH / f"{name}.pdf", pad_inches=0.1)
