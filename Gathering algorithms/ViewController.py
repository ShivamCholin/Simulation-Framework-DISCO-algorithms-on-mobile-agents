
BOUNDS_WIDTH: int = 1000
MAX_X: float = BOUNDS_WIDTH / 2
MIN_X: float = -MAX_X
VIEW_WIDTH: int = BOUNDS_WIDTH + 20

BOUNDS_HEIGHT: int = 1000
MAX_Y: float = BOUNDS_HEIGHT / 2
MIN_Y: float = -MAX_Y
VIEW_HEIGHT: int = BOUNDS_HEIGHT + 20

CELL_RADIUS: int = 15
CELL_COUNT: int = 1
CELL_SPEED: float = 5.0
from turtle import *
from turtle import Turtle, Screen, done
from typing import Any, List
from time import time_ns
from xmlrpc.client import Boolean

import tkinter as _
NS_TO_MS: int = 1000000
class ViewController:
    screen: Any
    pen: Turtle
    pen2: Turtle

    def __init__(self, agents: List, poly:List, record:Boolean=False):
        self.poly=poly
        self.agents=agents
        self.screen = Screen()
        self.screen.setup(VIEW_WIDTH, VIEW_HEIGHT)
        self.screen.tracer(0, 0)
        self.screen.delay(0)
        self.screen.title("polygon explore")
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen2 = Turtle()
        self.pen2.hideturtle()
        self.temp1=0
        self.pen2.color("blue")
        self.pen2.penup()
        self.pen2.goto(poly[0][0],poly[0][1])
        self.pen2.pendown()
        self.pen2.pensize(5)
        for point in self.poly:
            self.pen2.goto(point[0],point[1])
        self.record=record

    def start_simulation(self) -> None:
        self.tick()
        done()

    def tick(self) -> None:
        start_time = time_ns() // NS_TO_MS
        self.temp1+=1
        self.pen.clear()
        for cell in self.agents[self.temp1]:
            self.pen.penup()
            self.pen.goto(cell[0], cell[1])
            self.pen.pendown()
            self.pen.color("red")
            self.pen.dot(CELL_RADIUS)
        self.screen.update()

        if self.temp1==len(self.agents)-1:
            return
        else:
            end_time = time_ns() // NS_TO_MS
            next_tick = 30 - (end_time - start_time)
            if next_tick < 0:
                next_tick = 0
            self.screen.ontimer(self.tick, next_tick)
