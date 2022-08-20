#I'M TOO FAR YOUNG TO WORRY ABOUT MY FAILURES.

from typing import Union
from game_state import GameState
import asyncio
import random
import os
import time
from queue import PriorityQueue
import numpy as np 

uri = os.environ.get(
    'GAME_CONNECTION_STRING') or "ws://127.0.0.1:3000/?role=agent&agentId=agentId&name=defaultName"

actions = ["up", "down", "left", "right", "bomb", "detonate"]

class player:

    def __init__(self , grid , agent_id , unit_id):
        
        self.row = 0
        self.col = 0

        self.id = self.col + self.row * 15
        
        self.grid = grid

        self.agent_id = agent_id 
        self.unit_id = unit_id

        self.bombs = None
        self.hp = None
        self.blast_diameter = None
        self.invulnerability = 0
        

class node:
    
    def __init__(self , row , col):

        self.row = row
        self.col = col
        self.id = self.col + self.row * 15

        self.neibours = []

    def board_reset(self):
        
        self.obj_type = '.' #Type of This node i.e ENTITY type (Refer line : 53)
        self.weight = 0.1
        
        # self.bomb_is_here = False

        self.bombs = None
        self.hp = None
        self.expires = None
        self.blast_diameter = None
        self.invulnerability = 0
    
        self.h_score = 0
        self.g_score = float("inf")
        self.f_score = float("inf")

    def add_neibour(self , grid ):
         
        if self.row > 0 and (grid[self.id - 15].obj_type == '.' or grid[self.id - 15].obj_type == 'w' or grid[self.id - 15].obj_type == 'o' or grid[self.id - 15].obj_type == 'a'): #UP
            self.neibours.append(grid[self.id - 15])

        if self.row < 14 and (grid[self.id + 15].obj_type == '.' or grid[self.id + 15].obj_type == 'w' or  grid[self.id + 15].obj_type == 'o' or grid[self.id + 15].obj_type == 'a' ): #DOWN
            self.neibours.append(grid[self.id + 15])

        if self.col > 0 and (grid[self.id -1].obj_type == '.' or grid[self.id -1].obj_type == 'w' or grid[self.id -1].obj_type == 'o' or grid[self.id -1].obj_type == 'a' ): #LEFT
            self.neibours.append(grid[self.id - 1])
        
        if self.col < 14 and (grid[self.id + 1].obj_type == '.' or grid[self.id + 1].obj_type == 'w' or grid[self.id + 1].obj_type == 'o' or grid[self.id + 1].obj_type == 'a' ): #RIGHT
            self.neibours.append(grid[self.id + 1])

class Gameboard:

    def __init__(self): 

        g = []
        for i in range(15):
            for j in range(15):
                g.append(node(i , j))
        
        self.grid = np.array(g)

        self.p = {
                'c' : player(grid=self.grid , agent_id='a' , unit_id='c'),
                'd' : player(grid=self.grid , agent_id='b' , unit_id='d'),
                'e' : player(grid=self.grid , agent_id='a' , unit_id='e'),
                'f' : player(grid=self.grid , agent_id='b' , unit_id='f'),
                'g' : player(grid=self.grid , agent_id='a' , unit_id='g'),
                'h' : player(grid=self.grid , agent_id='b' , unit_id='h')
            }


        self.maja = lambda x : [14-x[1] , x[0]] #MAJA FUNCTION i.e is convert col , row to row , col (want to know reason call us :)

        self.h = lambda start , end : abs(start.row - end.row) + abs(start.col - end.col) #Herustic function

        self.linear_fucn = lambda l : l[1] + l[0] * 15 


    def update_board(self , gameState): #Everytime the board get updated with current values 

        self.gameState = gameState 

        for i in range(225):
            self.grid[i].board_reset()

        #ENTITIES i.e WOOD , STONE , METAL , BOMB , AMMO , FIRE , POWERUP => w , o , m , b , a , x , bp
        for i in self.gameState['entities']:

            x_ = self.maja([i['x'] , i['y']])
            l_ = self.linear_fucn(x_)   

            self.grid[l_].obj_type = i['type']
            
            if i['type']   == 'w':
                self.grid[l_].weight = i['hp']

            elif i['type'] == 'o':
                self.grid[l_].weight = i['hp']
            
            elif i['type'] == 'm':
                self.grid[l_].weight = float("inf")
            
            elif i['type'] == 'b':

                self.grid[l_].blast_diameter = i['blast_diameter']
                self.grid[l_].expires = i['expires']

                # self.grid[l_].weight = float("inf")
                # self.grid[l_].bomb_is_here = True
        
        # BOTs
        # OPPONENT TEAM => c , e , g 
        # OUR TEAM      => d , f , h 
        for i in 'cdefgh':
            
            x_ = self.maja(self.gameState['unit_state'][i]['coordinates'])
            
            self.p[i].row = x_[0]
            self.p[i].col = x_[1]

            self.p[i].id  = self.linear_fucn(x_)
            
            self.p[i].hp = self.gameState['unit_state'][i]['hp']
            self.p[i].bombs = self.gameState['unit_state'][i]['inventory']['bombs']
            self.p[i].blast_diameter = self.gameState['unit_state'][i]['blast_diameter']
            self.p[i].invulnerability = self.gameState['unit_state'][i]['invulnerability']

        for i in range(225):
            if i % 15 == 0:
                print()
            
            for j in self.p:

                if self.p[j].id == i:
                    self.grid[i].obj_type = j
         
            print(self.grid[i].obj_type , end=' ')


    def take_action(self , came_from , current):
        
        path = []
        while current in came_from:
            current = came_from[current]
    
            if current != self.start:
                path.append(current)
        
        path.insert(0 , self.end)
        n = path[len(path)-1]
        
        
        # actions = ["up", "down", "left", "right", "bomb", "detonate"]
        
        try:
            print(n.row , n.col)
    
            if n.obj_type == 'w':

                return actions[4]
            
            else:    

                if n.col > self.start.col: 
                    print("RIGTH")
                    return actions[3]

                elif n.col < self.start.col:
                    print("LEFT")
                    return actions[2]

                elif n.row > self.start.row: 
                    print("DOWN")
                    return actions[1]

                elif n.row < self.start.row: 
                    print("UP")
                    return actions[0]

        except Exception as e:
            print("ERROR IS : " , e)

    def path_finding(self , unit , end , priority=None): 

        # self.start = self.grid[self.linear_fucn(self.maja(self.gameState['unit_state'][unit]['coordinates']))]#UNIT postion
        self.start = self.grid[self.p[unit].id]#UNIT postion

        self.end = self.grid[end]

        self.path = {}

        count = 0
        self.open_set = PriorityQueue()

        self.open_set.put((count , self.start))

        self.start.f_score = self.h(self.start , self.end)
        self.start.g_score = 0

        open_set_hash = {self.start}
        while not self.open_set.empty():

            current = self.open_set.get()[1]
            open_set_hash.remove(current)

            current.add_neibour(self.grid) 

            if current == self.end:
                action = self.take_action(self.path, current)
                print(" REACHED ")
                return action

            for neibour in current.neibours:
                
                temp_g_score = current.g_score + neibour.weight
                
                if temp_g_score < neibour.g_score:
                    
                    self.path[neibour] = current
                    neibour.g_score = temp_g_score
                    neibour.f_score = temp_g_score + self.h(neibour , self.end)
                    
                    if neibour not in open_set_hash:
                        count += 1 
                        self.open_set.put((count , neibour))
                        open_set_hash.add(neibour)
        
        print("CAN'T REACH")
        return False

class Agent():
    def __init__(self):
        self._client = GameState(uri)

        # any initialization code can go here
        self._client.set_game_tick_callback(self._on_game_tick)
        self.board = Gameboard()
        print(" CHECK ")

        loop = asyncio.get_event_loop()
        connection = loop.run_until_complete(self._client.connect())
        tasks = [
            asyncio.ensure_future(self._client._handle_messages(connection)),
        ]
        loop.run_until_complete(asyncio.wait(tasks))


    # returns coordinates of the first bomb placed by a unit
    def _get_bomb_to_detonate(self, unit) -> Union[int, int] or None:
        entities = self._client._state.get("entities")
        bombs = list(filter(lambda entity: entity.get(
            "unit_id") == unit and entity.get("type") == "b", entities))
        bomb = next(iter(bombs or []), None)
        if bomb != None:
            return [bomb.get("x"), bomb.get("y")]
        else:
            return None

    async def _on_game_tick(self, tick_number, game_state):

        # get my units
        my_agent_id = game_state.get("connection").get("agent_id")
        my_units = game_state.get("agents").get(my_agent_id).get("unit_ids")


        for unit_id in my_units:
            # unit_id = 'f'
            
            self.board.update_board(self._client._state)       
            # action = self.board.path_finding(unit_id , 220)
            ammo = None
            bp   = None

            for i in range(225):
                if self.board.grid[i].obj_type == 'a':
                    ammo = i
                    ammo = None

                if self.board.grid[i].obj_type == 'bp':
                    bp = i
                    bp = None

            if ammo:

                print("AMMO PRESENT SIR !!! " , ammo)
                action = self.board.path_finding(unit_id , ammo)

            elif bp:
                
                print("POWER PRESENT SIR !!! " , bp)
                action = self.board.path_finding(unit_id , bp)

            else:
                end = random.randint(0 , 225-1)
                # end = 220
                print("END SIR !!! " , end)
                action = self.board.path_finding(unit_id , end)


            if action in ["up", "left", "right", "down"]:
                await self._client.send_move(action, unit_id)

            elif action == "bomb":
                await self._client.send_bomb(unit_id)

            elif action == "detonate":
                bomb_coordinates = self._get_bomb_to_detonate(unit_id)
                if bomb_coordinates != None:
                    x, y = bomb_coordinates
                    await self._client.send_detonate(x, y, unit_id)
            else:
                print(f"Unhandled action: {action} for unit {unit_id}")


def main():
    for i in range(0,10):
        while True:
            try:
                Agent()
            except:
                time.sleep(5)
                continue
            break


if __name__ == "__main__":
    main()

