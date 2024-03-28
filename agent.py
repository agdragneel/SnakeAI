import torch
import random
import numpy as np
from game import SnakeGameAI,Direction,Point
from collections import deque
'''
State: 11 Values [danger_straight,danger_right, danger left,
                    direction_up,direction_down,direction_right,direction_left
                    food_up,food_down,food_right,food_left]

Action: 3 values No change: [1,0,0]
                Right Turn: [0,1,0]
                Left Turn: [0,0,1]
'''
MAX_MEMORY=100_000
BATCH_SIZE=1000
LR= 0.001                      #   Learning Rate

class Agent:

    def __init__(self):
        self.n_games=0
        self.epsilon=0          #  Parameter to control randomness (Exploration vs Exploitation Tradeoff)
        self.gamma=0            #  Discount Rate
        self.memory=deque(maxlen=MAX_MEMORY)       # Deques automatically remove element if memory size is exceeded.and
        
        self.model=None #TODO
        self.trainer=None #TODO
        



    def get_state(self,game):

        head=game.snake[0]

        point_l=Point(head.x-20,head.y)
        point_r=Point(head.x+20,head.y)
        point_u=Point(head.x,head.y-20)
        point_d=Point(head.x,head.y+20)

        dir_l= game.direction==Direction.LEFT
        dir_r= game.direction==Direction.RIGHT
        dir_u= game.direction==Direction.UP
        dir_d= game.direction==Direction.DOWN
        
        state=[

            #Danger Straight

            ((dir_r and game._is_collision(point_r)) or
            (dir_l and game._is_collision(point_l)) or
            (dir_d and game._is_collision(point_d)) or
            (dir_u and game._is_collision(point_u))),

            #Danger Right
            ((dir_r and game._is_collision(point_d)) or
            (dir_l and game._is_collision(point_u)) or
            (dir_d and game._is_collision(point_l)) or
            (dir_u and game._is_collision(point_r))),


            #Danger Left

            ((dir_r and game._is_collision(point_u)) or
            (dir_l and game._is_collision(point_d)) or
            (dir_d and game._is_collision(point_r)) or
            (dir_u and game._is_collision(point_l))),

            #Move Directions

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            #Food Locations

            game.food.x<game.head.x,
            game.food.x>game.head.x,
            game.food.y<game.head.y,
            game.food.y>game.head.y
        ]

        return np.array(state,dtype=int)


    def remember(self,state,action,reward,next_state,done):
        self.memory.append(state,action,reward,next_state,done)
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample=random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample=self.memory
            
        states,actions,rewards,next_states,dones=zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)

    def get_action(self,state):
        pass

def train():
    plot_scores=[]
    plot_mean_scores=[]
    total_score=0
    record=0
    agent=Agent()
    game=SnakeGameAI()

    while True:
        # Get Old State
        state_old=agent.get_state(game)

        #Get Move
        final_move=agent.get_action(state_old)

        #Perform Move and get new state
        reward,done,score=game.play_step(final_move)
        state_new=agent.get_state(game)

        #train_short_memory
        agent.train_short_memory(state_old,final_move,reward,state_new,done)

        #remember

        agent.remember(state_old,final_move,reward,state_new,done)

        if done:
            #train_long_memory

            game.reset()
            agent.n_games+=1
            agent.train_long_memory()

            if score > record:
                record=score
                #agent.model.save()
            
            print('Game',agent.n_games,'Score:',score,'Record',record)

            #TODO: plot
                



if __name__ == "__main__":
    train()


