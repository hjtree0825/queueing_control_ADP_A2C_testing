# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:33:28 2020

@author: J
"""

import gym
from A2C_keras import Agent
from QC_env import QCEnv
#from utils import plotLearning
import numpy as np


if __name__ == '__main__':
    agent = Agent(alpha = 0.0001, beta = 0.0005)
    
    #env = gym.make('LunarLander-v2')
    
    arr_rate1 = 20
    arr_rate2 = 10
    serv_rate1 = 100
    serv_rate2 = 90
    cost1 = 10
    cost2 = 30
    
    
    env = QCEnv(arr_rate1, arr_rate2)
    
    score_history = []
    num_episodes = 100
    
    for i in range(num_episodes):
        done = False
        score = 0
        observation = env.reset(arr_rate1, arr_rate2)
        
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action, arr_rate1, arr_rate2, serv_rate1, serv_rate2, cost1, cost2)
            agent.learn(observation, action, reward, observation_, done)
            observation = observation_
            score += reward
            print(score)
            
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])
        print('episode ', i, 'score %.2f average score %.2f' %\
              (score, avg_score))
        
    
