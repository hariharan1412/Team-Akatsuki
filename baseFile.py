#OUR IMPORTS    
from enum import Flag
from queue import PriorityQueue
from operator import itemgetter
import numpy as np
import random
from collections import deque

class player:

    def __init__(self , grid , Gameboard , agent_id , unit_id , hp):
        
        self.row = 0
        self.col = 0

        self.id = self.col + self.row * 15
        
        self.grid = grid
        self.gameBoard = Gameboard

        self.agent_id = agent_id 
        self.unit_id = unit_id

        self.bombs = None
        self.hp = hp 
        self.blast_diameter = None
        self.invulnerability = 0
        self.stunned = 0
        
        self.evade_loc = False
        
        self.next_node_pos = None

        self.target_ammo = []

        # self.goto = [7]
        self.goto = [None , 112]


    def next_node(self , action ,  unit=None):
        
        if action == 'left':
            self.next_node_pos = self.id - 1
        
        elif action == 'right':
            self.next_node_pos = self.id + 1 
        
        elif action == 'up':
            self.next_node_pos = self.id - 15

        elif action == 'down':
            self.next_node_pos = self.id + 15
        
        elif action == 'bomb':
            
            self.can_i_place_bomb_here(unit)
            self.next_node_pos = self.id

        elif action == None or action == 'detonate':

            self.next_node_pos = self.id
        
        # elif action == 'bomb':
            # self.next_node_pos = self.id

    def can_i_place_bomb_here(self , unit):
        
        straight = True


    def move_on(self , start , to_node=None , told_by=None , single_Step=False):
        
        if not single_Step:

            print(" FUCNTION CALLED " , self.unit_id)
            self.grid[self.id].add_neibour(self.grid)
            
            neibour = self.grid[self.id].neibours

            neibour.remove(start)
            neibour.remove(to_node)

            least_Weight = float("inf")
            for i in neibour:
                if i.weight < least_Weight:
                    least_Weight = i.weight
                    to_ = i
            
            print(" CHOOSING TYPE : ", to_.obj_type , " LOC : " , to_.id)
            # to_ = random.choice(neibour)

            print("UNIT NAME : " , self.unit_id)
            return self.gameBoard.path_finding(unit=self.unit_id , end_point=to_.id , check=True)

        else:

            self.grid[self.id].add_neibour(self.grid)
            neibour = self.grid[self.id].neibours
            neibour.remove(start)

            least_Weight = float("inf")
            for i in neibour:
                if i.weight < least_Weight:
                    least_Weight = i.weight
                    to_ = i
            
            print(" CHOOSING TYPE : ", to_.obj_type , " LOC : " , to_.id)
            # to_ = random.choice(neibour)

            print("UNIT NAME : " , self.unit_id)
            return self.gameBoard.path_finding(unit=self.unit_id , end_point=to_.id , check=True)


    #HELP TEAM MATES TO OPEN A PATH OR SOMETHING
    # def help_me(self , unit , pos):
        
    #     print("BEFORE INSIDE HELP ME FUNCTION : " , unit)
    #     action , unit = self.gameBoard.path_finding(unit=unit , end_point=pos , bomb=10 ,help=True)
    #     print("AFTER INSIDE HELP ME FUNCTION : " , action , unit)
    #     return action , unit


class node:
    
    def __init__(self , row , col):

        self.row = row
        self.col = col
        self.id = self.col + self.row * 15


        # self.evade_neibours = []

    def board_reset(self , weight):
        
        self.obj_type = '.' #Type of This node i.e ENTITY type (Refer line : 53)

        self.bg = '.'

        self.player = None
        self.enemy  = False

        self.weight = weight

        self.is_visited = False
        
        self.bombs = None
        self.hp = None
        self.expires = None
        self.blast_diameter = None
        self.invulnerability = 0
    
        self.gonna_fire = False

        self.h_score = 0
        self.g_score = float("inf")
        self.f_score = float("inf")

    def add_neibour(self , grid , evade=False):

        if evade:
            
            self.evade_neibours = []

            if self.row > 0 and grid[self.id - 15].obj_type ==  '.' and not grid[self.id - 15].enemy: #UP
                self.evade_neibours.append(grid[self.id - 15])

            if self.row < 14 and grid[self.id + 15].obj_type ==  '.' and not grid[self.id + 15].enemy: #DOWN
                self.evade_neibours.append(grid[self.id + 15])

            if self.col > 0 and grid[self.id -1].obj_type ==  '.' and not grid[self.id - 1].enemy: #LEFT
                self.evade_neibours.append(grid[self.id - 1])
            
            if self.col < 14 and grid[self.id + 1].obj_type ==  '.' and not grid[self.id + 1].enemy: #RIGHT
                self.evade_neibours.append(grid[self.id + 1])        
        
        else:
            self.neibours = []

            if self.row > 0 and grid[self.id - 15].weight !=  float("inf"): #UP
                self.neibours.append(grid[self.id - 15])

            if self.row < 14 and grid[self.id + 15].weight !=  float("inf"): #DOWN
                self.neibours.append(grid[self.id + 15])

            if self.col > 0 and grid[self.id -1].weight !=  float("inf"): #LEFT
                self.neibours.append(grid[self.id - 1])
            
            if self.col < 14 and grid[self.id + 1].weight !=  float("inf"): #RIGHT
                self.neibours.append(grid[self.id + 1])        


class Gameboard:

    def __init__(self): 

        g = []
        for i in range(15):
            for j in range(15):
                g.append(node(i , j))
        
        self.grid = np.array(g)

        self.p = {
                'c' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='c' , hp=3),
                'd' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='d' , hp=3),
                'e' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='e' , hp=3),
                'f' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='f' , hp=3),
                'g' : player(grid=self.grid , Gameboard=self , agent_id='a' , unit_id='g' , hp=3),
                'h' : player(grid=self.grid , Gameboard=self , agent_id='b' , unit_id='h' , hp=3)
            }
            
        self.actions = ["up", "down", "left", "right", "bomb", "detonate"]

        self.weight = 0.1

        self.myTeam = []
        
        self.maja = lambda x : [14-x[1] , x[0]] #MAJA FUNCTION i.e is convert col , row to row , col (want to know reason call us :)

        self.h = lambda start , end : abs(start.row - end.row) + abs(start.col - end.col) #Herustic function

        self.linear_fucn = lambda l : l[1] + l[0] * 15         

        # self.attack_spot = set()

        # self.bomb_is_here = lambda x : True if self.grid[self.p[x].id].obj_type == 'b' else False

    def render(self, game=False):

        print()

        for i in range(225):
            if i % 15 == 0:
                print()

            if game:
                self.grid[i].bg = self.grid[i].obj_type 
            else:
                self.grid[i].bg = self.grid[i].g_score 

            for j in self.p:

                if self.p[j].id == i:
                    self.grid[i].bg = j
         
            print(self.grid[i].bg , end=' ')
        
        print()

    def update_board(self , gameState , tick_number=None): #Everytime the board get updated with current values 

        self.tick_number = tick_number

        self.ammo_found = False
        self.ammos = []

        self.power_up_found = False

        self.gameState = gameState 
        # print(self.gameState)
        
        self.bombs = []

        for i in range(225):
            self.grid[i].board_reset(self.weight)

        #ENTITIES i.e WOOD , STONE , METAL , BOMB , AMMO , FIRE , POWERUP => w , o , m , b , a , x , bp
        for i in self.gameState['entities']:

            x_ = self.maja([i['x'] , i['y']])
            l_ = self.linear_fucn(x_)   

            self.grid[l_].obj_type = i['type']


            
            if i['type']   == 'w':
                # self.grid[l_].weight = i['hp'] * 10
                self.grid[l_].weight = 10

            elif i['type'] == 'o':
                self.grid[l_].weight = i['hp'] * 30

            
            elif i['type'] == 'm':
                self.grid[l_].weight = float("inf")
            

            elif i['type'] == 'bp':

                self.grid[l_].weight = self.weight
                self.ammos.append(self.grid[l_])

                self.power_up_found = True
                self.power_up = l_
                self.grid[l_].expires = i['expires']

            elif i['type'] == 'fp':

                self.grid[l_].weight = self.weight
                self.ammos.append(self.grid[l_])

                self.power_up_found = True
                self.power_up = l_
                self.grid[l_].expires = i['expires']

            elif i['type'] == 'b':

                self.grid[l_].weight = float("inf")
                self.grid[l_].blast_diameter = i['blast_diameter']
                self.grid[l_].expires = i['expires']

                self.bombs.append(self.grid[l_])

                
            elif i['type'] == 'x':

                self.grid[l_].weight = 90

        # BOTs
        # OPPONENT TEAM => c , e , g 
        # OUR TEAM      => d , f , h 
        # for i in self.total_players:
        for i in 'cdefgh':
            
            x_ = self.maja(self.gameState['unit_state'][i]['coordinates'])
            l_ = self.linear_fucn(x_)
            
            self.p[i].row = x_[0]
            self.p[i].col = x_[1]

            self.p[i].id  = l_

            # self.grid[i].player = True

            self.p[i].hp = self.gameState['unit_state'][i]['hp']
            self.p[i].bombs = self.gameState['unit_state'][i]['inventory']['bombs']
            self.p[i].blast_diameter = self.gameState['unit_state'][i]['blast_diameter']
            self.p[i].invulnerability = self.gameState['unit_state'][i]['invulnerable']
            self.p[i].stunned = self.gameState['unit_state'][i]['stunned']

            if i in self.myTeam:
    
                if self.p[i].hp > 0:
                    self.grid[l_].weight = self.weight

                else:
                    self.grid[l_].weight = float("inf")
                
                # print("UNIT IN UPDATE : " , i)
                # print(self.p[i].goto)

            else:
                self.grid[l_].weight = float("inf")
                self.grid[l_].enemy = True
            
        self.render(game=True)

    # def active_agents(self, my_units):
        
    #     self.myTeam = []
    #     self.total_players = ['c','d','e','f','g','h']

    #     for i in my_units:

    #         if self.p[i].hp > 0:
    #             self.myTeam.append(i)
            
    #         else:
    #             self.total_players.remove(i)
                
    #     return self.myTeam
    
    def sort_ammo(self , unit):

        prior_list = [self.h(self.p[unit] , i) for i in self.ammos]
        ele = self.ammos.pop(prior_list.index(min(prior_list)))
    
        return ele.id
        
    def catch_spans(self , unit_id):
        
        if self.power_up_found:
            
            bp = self.sort_ammo(unit_id)
            print("POWERUP PRESENT SIR !!! " , bp)

            if bp != None:
                action , unit_id = self.path_finding(unit_id , bp)
            else:
                action = None

        else:
            action = None
        
        return action , unit_id

    # def take_action(self , came_from , current , start , end , unit , once_check=False):
    def take_action(self , came_from , current , start , end , unit ):
        
        print(" INSIDE TAKE ACTION ", unit)
        path = []

        tot_cost = 0
        
        while current in came_from:
            current = came_from[current]
    
            if current != start:
                path.append(current)
                tot_cost += current.weight

        path.insert(0 , end)
        n = path[len(path)-1]
        # print("UNIT LETS SEE : " , unit , " PATH LEN : " , len(path))
        
        try:
            print(" TOTAL WEIGHT ", tot_cost , len(path))

            if len(path) > 0:

                print("UNIT ", unit , start.id)

                # if not self.p[unit].evade_loc:

                # if start.obj_type == 'b':
                    
                #     print(" BOMB IS HERE, RUN RA PANDA ") 
                #     id_ = self.bomb_evade(unit=unit , bomb=self.grid[self.p[unit].id])
                #     self.p[unit].goto.append(id_)

                #     # self.p[unit].evade_loc = True
                #     # self.p[unit].target_ammo.append(start)

                #     print(" ID " , id_)

                #     # action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True , once_check=True)
                #     action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True)
                    # return action , unit
                        
                    
                # self.actions = ["up", "down", "left", "right", "bomb", "detonate"]
                if n.obj_type == 'x':
                    # print(unit , " => BOMB NEXT MOVE ")
                    # # self.p[unit].next_node(unit , self.actions[4])
                    # id_ = self.bomb_evade(unit=unit , bomb=n)
                    # self.p[unit].goto.append(id_)
                    # # return self.actions[3] , unit
                    # print(" ID " , id_)

                    # action , unit = self.path_finding(unit=unit , end_point=self.p[unit].goto[-1] , check=True)
                    action = None
                    return action , unit

                # elif n.player in self.myTeam:

                #     if len(path) > 1:
                #         # print(" CALLED BY " , unit)
                #         n2 = path[len(path)-2]
                #         action , unit = self.p[n.player].move_on(start , to_node=n2)
                #         return action , unit

                #     else:
                #         action , unit = self.p[n.player].move_on(start , to_node=None , told_by=n.player , single_Step=True)
                #         self.this_player = 'd'
                #         return action , unit
                # elif n.id in self.attack_spot:
                #     return None , unit

                elif n.obj_type == 'w':
                    print(unit , " => BOMB" , "END NODE : " , self.p[unit].id)

                    evade = self.bomb_evade( unit=unit , end_node=self.p[unit].id)

                    print( " EVADE END NODE : " , evade)

                    if evade != None:

                        self.p[unit].next_node(unit , self.actions[4])
                        return self.actions[4] , unit

                    else:
                        action = None

                        self.p[unit].next_node(unit ,action)
                        return action , unit

                    # evade = self.bomb_evade(unit=unit , fake_bomb=True)

                    # if evade != None:
                    #     self.p[unit].next_node(unit , self.actions[4])
                    #     self.p[unit].goto.append(evade)

                    #     return self.actions[4] , unit
                    # else:
                    #     return None, unit

                    # return self.actions[4] , unit

                
                elif n.obj_type == 'o':
                    print(unit , " => BOMB" , "END NODE : " , self.p[unit].id)

                    evade = self.bomb_evade(unit=unit , end_node=self.p[unit].id)

                    if evade != None:

                        self.p[unit].next_node(unit , self.actions[4])
                        return self.actions[4] , unit

                    else:
                        action = None

                        self.p[unit].next_node(unit ,action)
                        return action , unit
    

                elif n.id == start.id:
                    print(unit , " => SAME SPOT")
                    self.p[unit].next_node(None)
                    return None , unit

                elif n.col > start.col: 
                    print(unit , " => RIGTH  ", n.id)
                    self.p[unit].next_node(self.actions[3])
                    return self.actions[3] , unit

                elif n.col < start.col:
                    print(unit , " => LEFT ", n.id)
                    self.p[unit].next_node(self.actions[2])
                    return self.actions[2] , unit

                elif n.row > start.row: 
                    print(unit , " => DOWN ", n.id)
                    self.p[unit].next_node(self.actions[1])
                    return self.actions[1] , unit

                elif n.row < start.row: 
                    print(unit , " => UP ", n.id)
                    self.p[unit].next_node(self.actions[0])
                    return self.actions[0] , unit
                
                else:
                    action = None
                    return action , unit
            else:

                print("CAN'T REACH , Weight exceed priority")
                print(" CALLING HELP ")

                return None , unit

        except Exception as e:

            print("ERROR IS : " , e)
            return None , unit

    # def bomb_place(self, unit):
    # def bomb_evade(self , unit , fake_bomb=False , end_node=None):
    def bomb_evade(self , unit=None , end_node=None):

        print( "END NODE : " , end_node)

        start = self.grid[self.p[unit].id]#UNIT postion

        if end_node != None:
            self.bombs.append(self.grid[end_node])
            self.grid[end_node].blast_diameter = self.p[unit].blast_diameter
            # self.grid[end_node].blast_diameter = 5
        
        print( " BOMBS : " , self.bombs)
        
        self.need_to_check = [i for i in self.bombs if 2*self.h(i , self.p[unit]) -1 < i.blast_diameter] 

        print( " NODE CHECK : " , self.need_to_check)

        safe_spot = None
        self.attack_spot = set()

        # self.p[unit_player].target_ammo = []

        for b in self.need_to_check:
            
            for j in self.attack_spot:
                self.grid[j].is_visited = False

            bomb = b
            
            q = deque()
            q.append(start)

            start.is_visited = True

            while q:
                
                a = q.popleft()

                if a.row == bomb.row or a.col == bomb.col : 

                    if 2*self.h(a , bomb) -1 < bomb.blast_diameter or a.id in self.attack_spot: #NOT SAFE 
                        a.add_neibour(self.grid , evade=True) #NEED TO CHECK WETHER ALL ARE INFINITY  

                        self.attack_spot.add(a.id)
                        
                        for i in a.evade_neibours:
                            if i.is_visited == False:
                                q.append(i)
                                i.is_visited = True

                                print(i.id)

                    else:
                        safe_spot = a.id
                        # return a.id
                else:
                    safe_spot = a.id
                    # return None
        
        self.safe_spot = safe_spot

        print(" SAFE SPOT " , safe_spot)
        print(" ATTACK SPOT " , self.attack_spot)

        if safe_spot in self.attack_spot:
            
                print("IN")
                return None

        print("OUT")
        return safe_spot
     

    # def path_finding(self , unit , end_point , check=False , once_check=False): 
    def path_finding(self , unit , end_point , check=False): 
        
        print("UNIT " , unit , end_point)
        # if check:
        #     self.update_board(self.gameState)
                
        start = self.grid[self.p[unit].id]#UNIT postion

        if end_point == None:
            print(" LIST EMPTY ")
            return None , unit


        if type(end_point) == list:
            end_point = self.linear_fucn(end_point)

        end = self.grid[end_point]
            
        path = {}

        count = 0

        start.f_score = self.h(start , end)
        start.g_score = 0

        open_set = PriorityQueue()
        open_set.put((start.f_score , count , start))
        open_set_hash = {start}

        while not open_set.empty():

            current = open_set.get()[2]
            # current = open_set.get()[2]

            if current == end:

                action , unit_player = self.take_action(came_from=path, current=current , start=start ,end=end ,unit=unit)

                # if self.p[unit].id == self.safe_spot:

                    # if self.p[unit].next_node_pos in self.attack_spot:
                    
                    # action = None 
                    # return action , unit 

                return action , unit_player

            open_set_hash.remove(current)

            current.add_neibour(self.grid) 

            for neibour in current.neibours:
                
                temp_g_score = current.g_score + neibour.weight
                
                if temp_g_score < neibour.g_score:
                    
                    path[neibour] = current
                    neibour.g_score = temp_g_score
                    neibour.f_score = temp_g_score + self.h(neibour , end)
                    
                    if neibour not in open_set_hash:
                        count += 1 
                        open_set.put((neibour.f_score , count ,  neibour))
                        open_set_hash.add(neibour)
        
        # print("CAN'T REACH" , unit)
        # print(" UNIT " , unit , " ACTION " , action)
        return None , unit

    def AI(self , unit_id):
        # self.actions = ["up", "down", "left", "right", "bomb", "detonate"]

          
        # unit_id = 'h'
        # unit_id = 'f'
        # unit_id = 'h'

        evade = self.bomb_evade(unit=unit_id)

        if evade != None:
            
            if evade not in self.p[unit_id].goto:
                self.p[unit_id].goto.append(evade)
            # self.p[unit_id].goto.append(evade)
            print(" SAFE SPOT " , self.safe_spot , " TICK NUMBER " , self.tick_number)
            action , unit_id = self.path_finding(unit=unit_id , end_point=self.p[unit_id].goto[-1])

        elif self.power_up_found:
            action , unit_id = self.catch_spans(unit_id=unit_id)
        
        else:        
            if len(self.p[unit_id].goto) > 2:
                action = self.actions[5]
                self.p[unit_id].goto.pop()
                self.p[unit_id].next_node(self.actions[5])


            else:
                action , unit_id = self.path_finding(unit=unit_id , end_point=self.p[unit_id].goto[-1])

        
        for i in self.myTeam:
            if self.p[unit_id].next_node_pos == self.p[i].next_node_pos and i != unit_id:
                self.p[unit_id].next_node(None)

                action = None

        print("ACTION : " , action , "UNIT : " , unit_id)

        return action , unit_id
        