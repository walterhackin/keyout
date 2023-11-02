import curses
from interface import Interface


def main(win):
    interface = Interface(win)
    interface.start_program()


if __name__ == "__main__":
    curses.wrapper(main)
