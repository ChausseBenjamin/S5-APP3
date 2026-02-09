from code.guitar import execute_guitar
from code.rawSignals import plot_raw_signals

# from code.sandbox import sandbox
from datetime import datetime


def main():
    print(datetime.now())
    plot_raw_signals()
    # sandbox()
    execute_guitar()


if __name__ == "__main__":
    main()
