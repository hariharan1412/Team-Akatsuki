import json

class GameBoard:
    def __init__(self, path):
        self.gameJson = self.getJson(path)
        self.Board = self.initialBoard()
        self.makeBoard()

    def getJson(self, p):
        with open(p, 'r') as file:
            return json.load(file)

    def initialBoard(self):
        board = list()
        for _ in range(15):
            a = list('.' * 15)
            board.append(a)
        return board
    
    def display(self):
        for x in self.Board:
            for j in x:
                print(f'| {j} ', end='')
            print()

    def fillUnits(self):
        for i in self.gameJson['units']:
            x, y = i['coordinates']
            self.Board[x][y] = i['unit_id']

    def fillObs(self):
        for i in self.gameJson['entities']:
            x, y = i['x'], i['y']
            self.Board[x][y] = i['type']

    def makeBoard(self):
        self.fillUnits()
        self.fillObs()
        self.display()

    def getBoard(self):
        return self.Board


newGame = GameBoard('found0.json')
