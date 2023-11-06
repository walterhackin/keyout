import curses
from src.interface import Interface


def main(win):
    """
    Основная функция программы, которая инициализирует и запускает интерфейс.

    :param win: Окно curses, в котором будет отображаться интерфейс.
    """
    interface = Interface(win)
    interface.start_program()


if __name__ == "__main__":
    curses.wrapper(main)
