import json
from tabulate import tabulate


def fg(text, color): return "\33[38;5;" + str(color) + "m" + text + "\33[0m"
def bg(text, color): return "\33[48;5;" + str(color) + "m" + text + "\33[0m"


class GameBoard:
    def __init__(self, path):
        self.gameJson = self.getJson(path)
        self.Board = self.initialBoard()
        self.colCode = {
            'w': bg('  ', 88),
            'o': bg('  ', 11),
            'm': bg('  ', 243),
            'a': 226,
            'b': 199
        }
        self.makeBoard()

    def getJson(self, p):
        with open(p, 'r') as file:
            return json.load(file)

    def initialBoard(self):
        board = list()
        for _ in range(15):
            a = ['  ' for i in range(15)]
            board.append(a)
        return board

    def display(self, g=False):
        if g:
            print(tabulate(self.Board, tablefmt='fancy_grid'))
        else:
            for x in self.Board:
                for y in x:
                    print(y, end='')
                print()

    def fillUnits(self):
        for i in self.gameJson['units']:
            x, y = i['coordinates']
            self.Board[x][y] = fg(' {}'.format(
                i['unit_id']), self.colCode[i['agent_id']])

    def fillObs(self):
        for i in self.gameJson['entities']:
            x, y = i['x'], i['y']
            self.Board[x][y] = self.colCode[i['type']]

    def makeBoard(self):
        self.fillUnits()
        self.fillObs()

    def getBoard(self):
        return self.Board


newGame = GameBoard('./found0.json')
newGame.display()
