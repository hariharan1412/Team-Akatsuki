
    def bomb_evade(self , unit=None , end_node=None , teamCheck=False) -> int: #IF RADIUS IS EQUAL TO 2 


        start = self.grid[self.p[unit].id]#UNIT postion

        if end_node != None:
            
            b_ = self.grid[end_node]
            self.bombs.append(b_)
            self.grid[end_node].blast_diameter = self.p[unit].blast_diameter
            
    
        visited = []

        safe_spot = None

        self.attack_spot = set() #MAY BE I CAN GET THIS INFO FROM BOMB_DETONATE


        for b in self.bombs:
            
            # for j in visited:
            #     j.is_visited = False


            bomb = b
            if 2*self.h(b , self.p[unit]) - 3 < b.blast_diameter:
                
                print(" CHECK BOMB " , b.id)

                bomb_blast = bomb.add_neibour(self.grid , directed=True , diameter=bomb.blast_diameter) #RETURN LIST 

                self.attack_spot.update(bomb_blast)

        if [2*self.h(b , self.p[unit]) - 3 < b.blast_diameter for b in self.bombs]:

            q = deque()
            q.append(start)

            start.is_visited = True
            # visited.append(start)

            while q:

                a = q.popleft()

                if a in self.attack_spot: 

                    neibours = a.add_neibour(self.grid , evade=True) #NEED TO CHECK WETHER ALL ARE INFINITY  

                    # self.attack_spot.add(a.id)
                
                    for i in neibours: 
                        
                        # 135 -> 120, 136
                        if i.is_visited == False:
                            
                            q.append(i)
                                
                            i.is_visited = True
                            visited.append(i)

                            print(i.id)

                else:
                    #2 CASES => HE MAY BE IN THE START POSITION ITSELF OR OTHER SPOT  
                    # safe_spot = a.id #MAY BE THE START POSITION OF THE UNIT #if start.id == a.id => None
                    print(" WHILE SAFE SPOT &&&&&&&&& ", safe_spot)
                    safe_spot = a #MAY BE THE START POSITION OF THE UNIT #if start.id == a.id => None
                    break

                            # return None

            start.is_visited = False
            for i in visited:
                i.is_visited = False

            self.safe_spot = safe_spot

            
            for i in self.attack_spot:
                print(" ATTACK SPOT " , i.id)


            if safe_spot in self.attack_spot:

                print(" SAFE SPOT " , safe_spot.id)
                return None

            if safe_spot == None:
                print(" SAFE SPOT " , safe_spot)
                return None

            safe_spot = safe_spot.id
            return safe_spot
     



    if evade == self.p[unit_id].id:
        print(" ##### ANGAYE NILLU DAWW ##### ")
        action , unit_id = self.path_finding(unit=unit_id , end_point=self.p[unit_id].id)

        # if evade not in self.p[unit_id].goto:

        #     self.p[unit_id].goto.append(evade)

        # else:

        #     self.p[unit_id].remove(evade)


        # self.p[unit_id].goto.append(evade)
        # print(" SAFE SPOT " , self.safe_spot , " TICK NUMBER " , self.tick_number)

        if evade != self.p[unit_id].id:
            print("**********", self.p[unit_id].goto[-1], "**********")
            action , unit_id = self.path_finding(unit=unit_id , end_point=evade)
