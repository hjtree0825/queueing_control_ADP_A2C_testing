# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:13:29 2020

@author: J
"""


from keras import backend as K
from keras.layers import Dense, Input
from keras.models import Model
from keras.optimizers import Adam
import numpy as np

class Agent(object):
    def __init__(self, alpha, beta, gamma = 0.99, n_actions = 2, layer1_size = 1024, layer2_size = 512,
                 input_dims = 2):
        self.gamma = gamma
        self.alpha = alpha
        self.beta = beta
        self.input_dims = input_dims
        self.fc1_dims = layer1_size
        self.fc2_dims = layer2_size
        self.n_actions = n_actions
        
        self.actor, self.critic, self.policy = self.build_actor_critic_network()
        self.action_space = [i for i in range(self.n_actions)]
        
    def build_actor_critic_network(self):
        inputt = Input(shape=(self.input_dims,))
        # calculation of loss function
        delta = Input(shape=[1])
        dense1 = Dense(self.fc1_dims, activation = 'relu')(inputt)
        dense2 = Dense(self.fc2_dims, activation = 'relu')(dense1)
        
        # actor
        probs = Dense(self.n_actions, activation = 'softmax')(dense2)
        
        # critic
        values = Dense(1, activation = 'linear')(dense2)
        
        def custom_loss(y_true, y_pred):
            out = K.clip(y_pred, 1e-8, 1-1e-8) # making sure that we do not get identically 0 or 1 (we will take log)
            log_lik = y_true*K.log(out)
            
            return(K.sum(-log_lik*delta))
        
        actor = Model([inputt, delta], [probs])
        actor.compile(optimizer = Adam(lr = self.alpha), loss = custom_loss)
        
        critic = Model([inputt], [values])        
        critic.compile(optimizer = Adam(lr = self.beta), loss = 'mean_squared_error')
        
        policy = Model([inputt], [probs])
        
        return(actor, critic, policy)
    
    def choose_action(self, observation):
        state = observation
        probabilities = self.policy.predict(state)[0]
        action = np.random.choice(self.action_space, p = probabilities) + 1
        
        return(action)
    
    def learn(self, state, action ,reward, state_, done):
        # I know this is redundant but wanted to just leave it while debugging
        state = state
        state_ = state_
        
        critic_value_ = self.critic.predict(state_)
        critic_value = self.critic.predict(state)
        
        target = reward + self.gamma * critic_value_*(1-int(done))
        delta = target - critic_value
        
        actions = np.zeros([1, self.n_actions])
        actions[np.arange(1), action - 1] = 1.0
        actions = actions + 1.0
        
        self.actor.fit([state, delta], actions, verbose = 0)
        self.critic.fit(state, target, verbose = 0)
        
        
    
        
