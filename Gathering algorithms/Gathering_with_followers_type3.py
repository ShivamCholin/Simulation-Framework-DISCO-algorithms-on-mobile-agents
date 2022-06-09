from numpy import poly
from scipy import rand
from pick_point_polygon import random_points_within, check_within
from visibility_polygon import visibility_poly
from shapely.geometry import Polygon, Point
from ViewController import ViewController
from slowed_simulation import slowed_simu3
import random

class agent:
    def __init__(self,ID:int):
        self.ID=ID
        self.mov=[]
        self.gathered=False
        self.mov_next_set=False
        self.follower=False
        self.round_number=0
        self.followers=set()
        self.followers.add(ID)
        self.train_ID=[]
        self.train_ID.append(ID)
        self.stop_moving=False
        self.following_agent_ID=ID
        self.following_agent_ID_buffer_set=False
        
    def set_environment(self,poly:list,other_agents:list):
        self.poly_tuple=[tuple(j) for j in poly]
        self.poly=poly
        self.current_pos=random_points_within(self.poly_tuple,self.poly_tuple,1)[0]
        self.mov.append(self.current_pos)
        self.other_agents=other_agents
        self.agent_count=len(other_agents)

    def scan(self):
        self.visible_agents=[]
        self.visibility_polygon=visibility_poly(self.poly,self.current_pos.x,self.current_pos.y)
        for agent1 in self.other_agents:
            if not agent1.ID == self.ID and  check_within(agent1.current_pos,self.visibility_polygon):
                self.visible_agents.append(agent1)
        self.visible_agents.sort(key=lambda x: x.ID)

    def process(self):
        if self.following_agent_ID_buffer_set:
            self.following_agent_ID=self.following_agent_ID_buffer
            self.following_agent_ID_buffer_set=False
        if self.gathered==False:
            agents_on_same_spot=0
            temp=self.current_pos
            for ag in self.other_agents:
                if ag.current_pos==temp:
                    agents_on_same_spot+=1
            if agents_on_same_spot==self.agent_count:
                self.gathered=True
        
        if len(self.followers)==self.agent_count:
            self.stop_moving=True
        if self.stop_moving:
            self.round_number+=1
            self.mov_next=self.current_pos
            self.mov_next_set=True
            self.round_number+=1
            return
        if not self.follower:
            self.visible_agents.sort(key=lambda x: x.following_agent_ID)
            if self.visible_agents and self.visible_agents[0].following_agent_ID<self.ID:
                self.follower=True
                candidate_agents=[]
                for ag in self.visible_agents:
                    if ag.following_agent_ID<self.ID:
                        candidate_agents.append(ag)
                self.following_agent=random.choice(candidate_agents)
                self.mov_next=self.following_agent.current_pos
                self.mov_next_set=True
            else:
                next_mov=random_points_within(self.visibility_polygon,self.poly_tuple,1)[0]
                self.mov_next=next_mov
                self.mov_next_set=True
        else:
            self.mov_next=self.following_agent.current_pos
            self.mov_next_set=True
        self.round_number+=1
    
    def communicate(self):
        if self.follower:
            self.following_agent.followers=self.following_agent.followers.union(self.followers)
            self.following_agent_ID_buffer=self.following_agent.following_agent_ID
            self.following_agent_ID_buffer_set=True
        
    def move(self):
        if self.mov_next_set and self.gathered==False:
            self.mov_next_set=False
            self.current_pos=self.mov_next
            self.mov.append(self.current_pos)


def simulate(poly,agent_count=5, visualise=False, round_cap=True, round_cap_no=10,sim_slow_index=10,record=False):
    agent_array=[]
    for i in range(agent_count):
        agent_array.append(agent(i))
    for i in range(agent_count):
        agent_array[i].set_environment(poly,agent_array)
    flag1=1
    round_no=0
    while(flag1):
        flag1=0
        for ag in agent_array:
            ag.scan()
        for ag in agent_array:
            ag.process()
        for ag in agent_array:
            ag.communicate()
        for ag in agent_array:
            ag.move()
        for ag in agent_array:
            if ag.gathered==False:
                flag1=1
        round_no+=1
        if round_cap:
            if round_cap_no==round_no:
                break

    mov12=[[[p2.x,p2.y] for p2 in ag.mov] for ag in agent_array]
    mov13=slowed_simu3(mov12,sim_slow_index)
    if visualise:
        mov15=[]
        for i in range(len(mov13[0])):
            temp6=[]
            for j in range(len(mov13)):
                temp6.append([mov13[j][i][0]*50,mov13[j][i][1]*50])
            mov15.append(temp6)
        printpoly=[[j*50 for j in i] for i in poly]+[[poly[0][0]*50,poly[0][1]*50]]
        vc=ViewController(mov15,printpoly,record)
        vc.start_simulation()
    return round_no


if __name__ == "__main__":
    #poly=[[0,4],[0,7],[2,9],[4,8],[2,6],[2,1],[6,2],[4,5],[6,9],[8,6],[9,2],[9,-3],[6,-1],[4,-3],[6,-6],[9,-6],[6,-9],[2,-9],[4,-8],[3,-5],[2,-7],[-1,-9],[-9,-9],[-9,9],[-7,6],[-7,-3],[-3,-7],[-3,-3],[-6,-1],[-3,4]]
    poly=[[-6, 1], [-6, -2], [-3, -2], [-3, 2], [-9, 2], [-9, 9], [-7, 9], [-7, 4], [-5, 4], [-5, 5], [-6, 5], [-6, 9], [-5, 9], [-5, 7], [-4, 7], [-4, 9], [0, 9], [0, 5], [-2, 5], [-2, 1], [1, 1], [1, 10], [6, 10], [6, 8], [3, 8], [3, 2], [6, 2], [6, 4], [5, 4], [5, 7], [8, 7], [8, 9], [10, 9], [10, 3], [8, 3], [8, 0], [9, 0], [9, -3], [6, -3], [6, -1], [0, -1], [0, -2], [5, -2], [5, -4], [9, -4], [9, -6], [5, -6], [5, -7], [7, -7], [7, -9], [3, -9], [3, -4], [2, -4], [2, -9], [-1, -9], [-1, -4], [-6, -4], [-6, -7], [-4, -7], [-4, -5], [-2, -5], [-2, -9], [-9, -9], [-9, -4], [-8, -4], [-8, -1], [-9, -1], [-9, 1]]
    #simulate(poly,agent_count=5, visualise=False, round_cap=True, round_cap_no=10,sim_slow_index=10,record=False)
    simulate(poly,50,True,False,20,20)