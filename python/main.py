from code.guitar import execute_guitar
from code.rawSignals import plot_raw_signals
import matplotlib.pyplot as plt

# from code.sandbox import sandbox
from datetime import datetime

# Set font to CMU Serif for all plot elements
plt.rcParams["font.family"] = "CMU Serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rcParams["mathtext.fontset"] = "cm"  # Use Computer Modern for math text


def main():
    print(datetime.now())
    plot_raw_signals()
    # sandbox()
    execute_guitar()


if __name__ == "__main__":
    main()
