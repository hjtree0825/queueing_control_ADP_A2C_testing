# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 19:48:22 2020

@author: J
"""

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random as r
import math as m

g = r.Random(1234)
np.random.seed(1234)


class QCEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, rate1, rate2):        
        # Initialize the staet according to the arrival rates \lambda_{i}'s
        self.state = np.array([np.random.poisson(rate1), np.random.poisson(rate2)])[None,:]
        
        # Thera are two actions, 1 and 2 (i.e., the action set is {1,2})
        self.action_space = spaces.Discrete(2)
        
        self.counter = 0
        self.done = 0
        self.add = 0
        self.reward = 0
    
    def check(self):
        if self.state[0][0] == 0 and self.state[0][1] == 0:
            return(1)
    
    def cost_fun(self, x1, x2, arrival1, arrival2, t, cost1, cost2):
        cost = cost1*t*(x1 + arrival1/2.) + cost2*t*(x2 + arrival2/2.)
        return(cost)
        
    
    #def take_action(self, action): # Is this function necessary? We are taking care of it in "step" function
    #    if action == 1:
            
    
    def step(self, action, arr_rate1, arr_rate2, serv_rate1, serv_rate2, cost1, cost2):
        
        #self.take_action(action) # Redundant?
        
        # self.current_step += 1 # Do we nee this?
        
        
        if self.done == 1:
            return(self.state, self.reward, self.done, self.add)
        else:
            if action == 1: # If the next customer is class 1, then the service rate follows class_1_service_rate, and queue 1 reduces by 1
                rate = serv_rate1
                self.state[0][0] = self.state[0][0] - 1
            elif action == 2: # If the next customer is class 2, then the service rate follows class_2_service_rate, and queue 2 reduces by 1
                rate = serv_rate2
                self.state[0][1] = self.state[0][1] - 1
            U = g.uniform(0,1)
            t = -1./rate * m.log(U) # Sampled service time
            
            # Arrivals follow Poisson distributions with rate \lambda_{i}*t
            arrival1 = np.random.poisson(arr_rate1*t)
            arrival2 = np.random.poisson(arr_rate2*t)
            
            cost = self.cost_fun(self.state[0][0], self.state[0][1], arrival1, arrival2, t, cost1, cost2)
            
            # Update state (current state = next state = current state + arrivals)
            self.state[0][0] += arrival1
            self.state[0][1] += arrival2
            
            self.reward -= cost # Update cumulative rewards (-costs)

                
        check = self.check()
        if (check):
            self.done = 1;
            print("System emptied")
        return(self.state, self.reward, self.done, self.add)
            
   
    def reset(self, rate1, rate2):
        self.state = np.array([np.random.poisson(rate1), np.random.poisson(rate2)])[None,:]
        
        self.counter = 0
        self.done = 0
        self.add = 0
        self.reward = 0
        
        return(self.state)
        
    def render(self, mode = 'human', close = False):
        print(f'States: {self.state}')
        print(f'Costs: {-1.*self.reward}')
    

# =============================================================================
# Test Section
# =============================================================================

# =============================================================================
# cost1 = 30
# cost2 = 20
# 
# arr_rate1 = 0
# arr_rate2 = 0
# 
# serv_rate1 = 100
# serv_rate2 = 50
# 
# a = QCEnv(100, 10)
# print(a.state)
# a.step(2, arr_rate1, arr_rate2, serv_rate1, serv_rate2, cost1, cost2)
# print(a.state)
# a.render()
# 
# a.reset(0,0)
# print(a.state)
# print(a.counter)
# print(a.done)
# print(a.add)
# print(a.reward)
# a.render()
# =============================================================================


