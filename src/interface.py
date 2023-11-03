import curses
import codecs
import time
import random
import datetime
from src.func_keys import FunctionalKeys
from src.stat_keys import Statistics

class Interface:
    """
       Основной интерфейс клавиатурного тренажера.
    """
    def __init__(self, win):
        """
        Инициализация интерфейса.
        Args:
            win: Основное окно curses.
        """
        self.win = win
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.win.keypad(True)
        self.text = []
        self.max_y, self.max_x = self.win.getmaxyx()
        self.fk = FunctionalKeys()
        self.stat = Statistics()

    def clear(self):
        """
        Очистка экрана.
        """
        self.win.clear()

    def insert_string(self, string, x, y):
        """
        Вставка строки на экране на определенные координаты.

        Args:
            string: Текст для вывода.
            x, y: Координаты на экране.
        """
        self.win.addstr(x, y, string)
        self.refresh()

    def read_data(self, path):
        """
        Чтение данных из файла.

        Args:
            path: Путь к файлу для чтения.
        """
        f = codecs.open(path, "r", 'utf-8')
        for line in f:
            self.text.append(
                line.replace("”", '')
                .replace("’", '')
                .replace("“", '')
                .replace("‘", '')
            )
        f.close()

    def get_text(self):
        """
        Получить случайный текст из сохраненного списка.

        Returns:
            Строка с текстом.
        """
        return random.choice(self.text)

    def insert_colored(self, string, x, y, color):
        """
        Вставка строки определенного цвета на экране на определенные координаты.

        Args:
            string: Текст для вывода.
            x, y: Координаты на экране.
            color: Индекс цвета.
        """
        self.win.attron(curses.color_pair(color))
        self.insert_string(string, x, y)
        self.win.attroff(curses.color_pair(color))
        self.refresh()

    def refresh(self):
        self.win.refresh()

    def move(self, x, y):
        self.win.move(x, y)
        self.refresh()

    def refresh_wrong_count(self, wrong_count):
        tmp_x, tmp_y = self.win.getyx()
        self.insert_colored(str(wrong_count), self.max_y - 2, 19, 3)
        self.move(tmp_x, tmp_y)

    def refresh_time(self, start, i):
        time.sleep(.0000001)
        delta = time.time() - start
        tmp_x, tmp_y = self.win.getyx()
        self.insert_string(str(round(i / delta, 3)), self.max_y - 1, 22)
        self.move(tmp_x, tmp_y)
        return round(i / delta, 3)

    def start_program(self):
        """
        Начало работы программы: главное меню.
        """
        self.clear()
        self.read_data("data/texts.txt")
        self.insert_colored(
            "{0}Добро пожаловать в KeyOut!\n\n\nДля того, чтобы начать игру, нажмите Enter.\n\n\n"
            "Для просмотра статистики нажмите букву s, чтобы открыть тепловую карту, нажмите n\n\n\n".format(' ' * int((self.max_x / 3))),
            0,
            0,
            3,
        )
        self.insert_colored('Нажмите ESC чтобы выйти', self.max_y - 3, 0, 2)
        self.move(0,0)
        self.refresh()
        c = self.win.getch()
        if c == self.fk.ENTER_CODE:
            self.clear()
            self.insert_string(
                "Игра начинается! Не забудьте нажать Enter в конце!!", 0, 0
            )
            self.refresh()
            time.sleep(4)
            self.run_level()
        elif c == ord("s"):
            self.show_statistic()
        elif c == self.fk.ESC_CODE:
            quit()
        elif c == ord('n'):
            self.stat.show_heatmap()
            self.start_program()
        else:
            self.start_program()

    def run_level(self):
        """
        Запуск уровня тренажера.
        """
        text = [self.get_text()]
        self.insert_colored(text[0], 0, 0, 0)
        self.insert_colored("Количество ошибок: 0", self.max_y - 2, 0, 3)
        self.insert_colored("Скорость (буква/сек): 0", self.max_y - 1, 0, 3)
        self.insert_colored("Для выхода нажмите ESC, чтобы поменять текст нажите TAB", self.max_y - 3, 0, 3)
        self.move(0, 0)
        x, y = 0, 0
        wrong_count = 0
        click_count = 0
        start = time.time()
        delta_time = 0
        for word in text:
            for i in range(len(word)):
                while True:
                    delta_time = self.refresh_time(start, i)
                    pressed = self.win.getch()
                    click_count += 1
                    if pressed == ord(word[i]):
                        self.insert_colored(word[i], x, y, 1)
                        y += 1
                        if y >= self.max_x:
                            y = 0
                            x += 1
                        self.move(x, y)
                        break
                    elif pressed == self.fk.ESC_CODE:
                        self.start_program()
                    elif pressed == self.fk.TAB_CODE:
                        self.clear()
                        self.run_level()
                    else:
                        self.insert_colored(word[i], x, y, 2)
                        self.move(x, y)
                        wrong_count += 1
                        try:
                            self.stat.add_wrong(word[i].upper())
                        except:
                            pass
                        self.refresh_wrong_count(wrong_count)

        end = time.time()
        time.sleep(2)
        self.show_round_statistics(
            [
                delta_time,
                wrong_count,
                round(1 - (wrong_count / click_count), 3) * 100,
            ]
        )

    def show_round_statistics(self, statistics):
        """
        Показ статистики после завершения раунда.

        Args:
            statistics: Список со статистикой раунда.
        """
        self.clear()
        self.insert_colored(
            "Игра окончена!\nВаша статистика:\nскорость печати - {0}\nколичество ошибок - {1},\nпроцент"
            " правильных попаданий - {2} ".format(
                statistics[0], statistics[1], statistics[2]
            ),
            0,
            0,
            1,
        )
        self.insert_colored("Хотите сохранить статистику? [Y/n]", 5, 0, 1)
        while True:
            pressed = self.win.getch()
            if pressed == ord("Y"):
                self.save_statistics(statistics)
                self.stat.refresh_wrong_count()
                self.start_program()
            else:
                self.start_program()

    def save_statistics(self, statistics):
        """
        Сохранение статистики в файл.
        Args:
            statistics: Список со статистикой раунда.
        """
        f = open("data/stats.txt", "a")
        statistics.append(datetime.datetime.now().strftime("%H:%M;%D"))
        f.write(";".join(map(str, statistics)))
        f.write("\n")
        f.close()

    def show_statistic(self):
        """
        Отображение сохраненной статистики.
        """
        self.clear()
        self.refresh()
        self.insert_colored(
            "Ваша сохраненная статистика:",
            0,
            0,
            1,
        )
        x, y = 1, 0
        index = 0
        stat_file = open("data/stats.txt", "r")
        lines = stat_file.readlines()
        can_include, quit_msg_rows = self.calculate_space()
        for line in lines:
            if index >= can_include:
                self.insert_colored(
                    "Для перехода на следующую страницу нажмите Enter, "
                    "для выхода в главное меню нажмите q",
                    self.max_y - 1 - quit_msg_rows,
                    y,
                    1,
                )
                while True:
                    c = self.win.getch()
                    if c == self.fk.ENTER_CODE:
                        self.clear()
                        self.refresh()
                        x = 0
                        index = 0
                        break

            row = line.split(";")
            self.insert_colored(
                "Дата: {0}, {4}\nскорость печати - {1}\nколичество ошибок - {2}\n"
                "процент правильных попаданий - {3}".format(
                    row[3], row[0], row[1], row[2], row[4].strip()
                ),
                x,
                y,
                1,
            )
            index += 1
            x += 5
        stat_file.close()
        self.insert_colored(
            "Для выхода в главное меню нажмите q", self.max_y - 1 - quit_msg_rows, y, 1
        )
        while True:
            c = self.win.getch()
            if c == ord("q"):
                self.start_program()
            else:
                continue

    def calculate_space(self):
        """
        Расчет доступного пространства на экране.
        Returns:
            Количество доступных строк, количество строк, необходимых для вывода сообщения о выходе.
        """
        quit_message_len = 85
        for_quit_message_needs = quit_message_len // self.max_x
        available = (self.max_y - 1) - for_quit_message_needs - 1
        return available // 5 - 1, for_quit_message_needs

