		
# Traffic Light Control		
		
## Introduction		
This project models a **two-road intersection** with independent car arrivals and a shared traffic light system.		
The objective is to control the traffic lights intelligently to **minimize congestion** or in the coding formulation **maximize reward**.		
The problem is formulated as a **Markov Decision Process (MDP)** and solved using the **Value Iteration algorithm** from Reinforcement Learning.		
		
---		
		
## System Overview / Objective		
### Goal		
To determine an **optimal traffic light switching policy** that minimizes the total number of cars (traffic load) on both roads.		
		
### System Components		
- **State (s):** The number of cars on each road and the current light configuration,		
\( s = (n_1, n_2, TL1, TL2) \), where TL1/TL2 ∈ {green, red}.		
- **Action (a):** Two possible actions:		
1. `a=0` → TL1 green, TL2 red		
2. `a=1` → TL1 red, TL2 green		
- **Transition:** Cars leave and arrive according to probabilistic rules.		
- **Reward:** Based on the total traffic after action:		
- +1 → Low traffic (<15 cars total)		
-  0 → Medium traffic (15–30 cars)		
- -1 → High traffic (≥30 cars)		
		
The MDP iteratively updates the value of each state until convergence, producing an optimal policy.		
		
---		
		
## 🧱 Code Structure		
TrafficLight.py	

├── value_iteration() # Select best action & Core algorithm computing value and policy tables (0=TL1 green, 1=TL2 green).
	
├── next_state_and_reward() # Computes transitions given current state and action

├── reward_from_counts() # Defines reward based on total car count	

├── Visualization Section: # Optional Matplotlib charts for policy/value

├── main() # Runs computation and saves results				
		
		
---		
		
## Algorithm Description		
The **Value Iteration Algorithm** is used to solve for the optimal policy.

At each iteration, the value of every state \( s \) is updated using:

$$
V(s) \leftarrow \max_a \sum_{s'} P(s' \mid s, a)
\left[ R(s, a, s') + \gamma V(s') \right]
$$

where:

- \( V(s) \): value of being in state \( s \)
- \( a \): action (which light is green)
- \( gamma \): discount factor (0.9 used here)
- \( P(s' \mid s, a) \): probability of transitioning to next state \( s' \) given action \( a \)
- \( R(s, a, s') \): immediate reward from the resulting traffic condition

The algorithm repeats these updates until the change in value between iterations, Delta falls below a small threshold \( theta = 0.001 \) denoted: 

$$ 
Delta = |V_{\text{new}}(s) - V_{\text{old}}(s)| 
$$

Once the values converge, the **optimal policy**  \( pi^*(s) \) is derived as:

$$
pi^*(s) = \arg\max_a Q(s, a)
$$

where

$$
Q(s, a) = \sum_{s'} P(s' \mid s, a)
\left[ R(s, a, s') + \gamma V(s') \right]
$$		
		
---		
		
## 📊 Input / Output Description		
**Inputs**		
- Initial state: `(n_road1, n_road2)` number of cars on both roads.		
- Transition probabilities:		
- New cars entering road 1: uniform {0…5}		
- New cars entering road 2: uniform {0…3}		
- Constraints:		
- Max cars: 40 on road 1, 25 on road 2.		
		
**Outputs**		
- `policy matrix` → Optimal action for each state (matrix of size 41×26).		
- `v_state matrix` → Computed value function for each state.		
- Optional visualization:	
- Showing the v_state in Line-Graph view for road2_cars = 0, 5, 10, 15, 20, 25 	
- Showing part of optimal action matrix in bar view (`lightgreen` = TL1 green, `lightcoral` = TL2 green).		
		
---		
		
## Summary		
The model demonstrates how **reinforcement learning principles** can optimize urban traffic control.		
The value iteration algorithm successfully learns when to prioritize road 1 or road 2, minimizing congestion in the long run.		
This framework can be extended to multiple intersections, stochastic arrivals, or adaptive traffic systems.		