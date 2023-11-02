import numpy as np
import matplotlib.pyplot as plt


class Statistics:
    def __init__(self):
        self.keyboard_layout = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '(', ')', '\\'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', "'"],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '?'],
            [' ']
        ]
        self.layout_size = sum([len(i) for i in self.keyboard_layout])
        data_file = open('wrong_key_data.txt', 'r')
        self.data = list(map(lambda x : int(x.replace('\n', '')), data_file.readlines()))
        data_file.close()
        self.wrong_statistics = {}
        index = 0
        for line in self.keyboard_layout:
            for letter in line:
                self.wrong_statistics[letter] = self.data[index]
                index += 1

    def get_index(self, letter):
        return list(self.wrong_statistics.keys()).index(letter)

    def add_wrong(self, letter):
        self.data[self.get_index(letter)] += 1

    def get_wrong_count(self, letter):
        return self.wrong_statistics[letter]

    def get_layout(self):
        return self.keyboard_layout

    def refresh_wrong_count(self):
        data_file = open('wrong_key_data.txt', 'w')
        for i in self.data:
            data_file.write(str(i) + '\n')

        data_file.close()

    def show_heatmap(self):
        layout = self.get_layout()
        heatmap_data = []
        max_length = max(len(row) for row in layout)

        for row in layout:
            heatmap_row = []
            for key in row:
                if key == ' ':
                    space_width = 6
                    space_padding = (max_length - space_width) // 2
                    heatmap_row.extend([0] * space_padding)
                    heatmap_row.extend([self.wrong_statistics.get(key, 0)] * space_width)
                    heatmap_row.extend([0] * space_padding)
                else:
                    heatmap_row.append(self.wrong_statistics.get(key, 0))
            heatmap_row.extend([0] * (max_length - len(heatmap_row)))
            heatmap_data.append(heatmap_row)

        heatmap_data = np.array(heatmap_data, dtype=float)

        fig, ax = plt.subplots()
        cax = ax.matshow(heatmap_data, cmap='inferno')
        fig.colorbar(cax, shrink=.3)

        ax.set_xticks(np.arange(len(layout[0])))
        ax.set_yticks(np.arange(len(layout)))
        ax.set_xticklabels('')
        ax.set_yticklabels('')
        for i, row in enumerate(layout):
            for j, key in enumerate(row):
                if key == ' ':
                    label = "SPACE"
                    ax.text(j + space_width / 2 + space_padding - .5, i, label, ha='center', va='center', color='green')
                else:
                    ax.text(j, i, key, ha='center', va='center', color='green')
        plt.show()
