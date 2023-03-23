# Blind Mouse Chasing Cheese
A mouse which has no ability needs to find the cheese using Q learning. Mouse is in the left upper corner and cheese is located in the right bottom corner. 
When mouse reaches the cheese the game ends and 100 points are rewarded. The grid is determined by the user input. Every time program is executed 
the learning progress take place. One last game is played and every step is displayed in the console.
## Q Learning
In this project I used Q Learning. Q learning is model free reinforcement learning algorithm to learn the value of an action in a particular state. 
It can handle problems with stochastic transitions and rewards without requiring adaptations.\
![alt text](https://i.stack.imgur.com/E1U4S.png)
### Parameters 
Change of action being random or `epsilon = 0.3`\
How much epsilon will be reduced or `eps_reduce_factor = 0.001`\
Reward is `0`\
Learning rate or `alpha is 0.3`\
Discount rate or `gamma is 0.9`\
How many times the game will be played or `max_iteration is 100000`
### Starting Q Table
### Ending Q Table
## Game
First state of the game\
Last state of the game
## Output
Every 5,000th Episode\
Every step of the last game\
How many moves have been made\
Last status of the Q table\
If the solution is optimal
