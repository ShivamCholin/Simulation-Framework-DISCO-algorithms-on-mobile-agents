from asyncio import gather
from numpy import poly
from scipy import rand
from pick_point_polygon import random_points_within, check_within
from visibility_polygon import visibility_poly
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import numpy as np
class agent:
    
    def __init__(self,ID):
        self.ID=ID
        self.mov=[]
        self.gathered=False
        self.mov_next_set=False

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
        if self.gathered:
            return
        if self.visible_agents:
            self.gathered=True
            self.mov_next_set=True
            self.mov_next=Point([(self.visible_agents[0].current_pos.x + self.current_pos.x)/2,(self.visible_agents[0].current_pos.y + self.current_pos.y)/2])
        else:
            next_mov=random_points_within(self.visibility_polygon,self.poly_tuple,1)[0]
            self.mov_next=next_mov
            self.mov_next_set=True

    def communicate(self):
        return

    def move(self):
        if self.mov_next_set:
            self.mov_next_set=False
            self.current_pos=self.mov_next
            self.mov.append(self.current_pos)

def simulate(poly,agent_count=2, round_cap=True, round_cap_no=50):
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
    #print(len(mov12[0]))
    x1=[i[0] for i in poly]+[poly[0][0]]
    y1=[i[1] for i in poly]+[poly[0][1]]
    x2=[i[0] for i in mov12[0]]
    y2=[i[1] for i in mov12[0]]
    x3=[i[0] for i in mov12[1]]
    y3=[i[1] for i in mov12[1]]
    plt.plot(x2, y2, color='green', linestyle='dashed', linewidth = 1,
            marker='o', markerfacecolor='blue', markersize=5)
    plt.plot(x3, y3, color='red', linestyle='dashed', linewidth = 1,
            marker='o', markerfacecolor='orange', markersize=5)
    plt.plot(x1, y1, label = "line 1")
    plt.show()
    return  len(mov12[0])
if __name__ == "__main__":
    poly=[[0,4],[0,7],[2,9],[4,8],[2,6],[2,1],[6,2],[4,5],[6,9],[8,6],[9,2],[9,-3],[6,-1],[4,-3],[6,-6],[9,-6],[6,-9],[2,-9],[4,-8],[3,-5],[2,-7],[-1,-9],[-9,-9],[-9,9],[-7,6],[-7,-3],[-3,-7],[-3,-3],[-6,-1],[-3,4]]
    poly=[[-6, 1], [-6, -2], [-3, -2], [-3, 2], [-9, 2], [-9, 9], [-7, 9], [-7, 4], [-5, 4], [-5, 5], [-6, 5], [-6, 9], [-5, 9], [-5, 7], [-4, 7], [-4, 9], [0, 9], [0, 5], [-2, 5], [-2, 1], [1, 1], [1, 10], [6, 10], [6, 8], [3, 8], [3, 2], [6, 2], [6, 4], [5, 4], [5, 7], [8, 7], [8, 9], [10, 9], [10, 3], [8, 3], [8, 0], [9, 0], [9, -3], [6, -3], [6, -1], [0, -1], [0, -2], [5, -2], [5, -4], [9, -4], [9, -6], [5, -6], [5, -7], [7, -7], [7, -9], [3, -9], [3, -4], [2, -4], [2, -9], [-1, -9], [-1, -4], [-6, -4], [-6, -7], [-4, -7], [-4, -5], [-2, -5], [-2, -9], [-9, -9], [-9, -4], [-8, -4], [-8, -1], [-9, -1], [-9, 1]]
    #simulate(poly,agent_count=2, round_cap=True, round_cap_no=50)
    simulate(poly)