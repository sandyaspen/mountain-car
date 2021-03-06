import numpy as np
import random
import gym
import sys
import pickle
from os import path


EPISODES = 500
LEARNING_RATE = 0.2
DISCOUNT = 0.9
EPSILON = 1
EPSILON_DECAY = 0.97

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "load":
        if path.exists("mc_q_matrix.pickle"):
            with open("mc_q_matrix.pickle", "rb") as f:
                q = pickle.load(f)
    else:
        q = np.zeros((18,15,3), dtype=float)
        # q table (columns: car position (-1.2 to 0.6), car velocity (-0.07 to 0.07), action (0,1,2))

    env = gym.make('MountainCar-v0')
    total_episode_rewards = []
    epsilon = EPSILON
    alpha = LEARNING_RATE
    gamma = DISCOUNT
    for episode in range(EPISODES):
        state = env.reset()
        state = (int(round(state[0] - env.observation_space.low[0], 1) * 10), int(round(state[1] - env.observation_space.low[1], 2) * 100))
        done = False
        episode_rewards = 0

        while not done:
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q[state])
            #PERFORM ACTION  
            #COLLECT NEW STATE, REWARD, and DONE
            next_state, reward, done, info = env.step(action)
            
            #ADJUST AND ROUND NEW STATE
            next_state = (int(round(next_state[0] - env.observation_space.low[0], 1) * 10), int(round(next_state[1] - env.observation_space.low[1], 2) * 100))
            
            #UPDATE
            Gt = reward # todo: calculate the discounted reward using gamma
            if not done:
                q[state][action] = q[state][action] + alpha * (Gt - q[state][action])
            else:
                q[state][action] = q[state][action] + alpha * (reward - q[state][action])
            
            #ADD REWARD TO EPISODE_REWARDS
            episode_rewards += reward
            
            #set state to next_state
            state = next_state
        
        #Lower epsilon some amount
        epsilon *= EPSILON_DECAY
        
        #ADD EPISODE REWARD TO TOTAL_EPISODE_REWARDS
        total_episode_rewards.append(episode_rewards)
        print("EPISODE: {}    REWARD: {}    EPSILON: {}".format(episode, episode_rewards, epsilon))


    #Save the trained q matrix 
    with open("mc_q_matrix.pickle", "wb") as f:
        pickle.dump(q, f)


    #Plot results with matplot lib
    print(total_episode_rewards)
