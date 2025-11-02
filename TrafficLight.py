import numpy as np
#import time
import sys
import matplotlib.pyplot as plt

N_road1_MAX = 40
N_road2_MAX = 25


actions = [0,1]
car_arrive = [(i,j) for i in range(6) for j in range(4)]
prob_car_arrive = 1.0/len(car_arrive)

v_state = np.zeros((N_road1_MAX+1, N_road2_MAX+1))
# we have 40+1 * 25+1 states .. meaning about 1066 states

def reward_from_counts(n_road1_s_dash, n_road2_s_dash):
    Np = n_road1_s_dash + n_road2_s_dash
    if Np < 15:
        return 1.0
    elif Np < 30:
        return 0.0
    else:
        return -1.0


def next_state_and_reward(n_road1, n_road2, a, arriv_road1_road2):
    i, j = arriv_road1_road2
    if a == 0:
        passed1 = min(n_road1, 3)
        n_road1_s_dash = n_road1 - passed1 + i
        n_road2_s_dash = n_road2 + j
    else:
        passed2 = min(n_road2, 4)
        n_road1_s_dash = n_road1 + i
        n_road2_s_dash = n_road2 - passed2 + j

    n_road1_s_dash = min(n_road1_s_dash, N_road1_MAX)
    n_road2_s_dash = min(n_road2_s_dash, N_road2_MAX)

    reward = reward_from_counts(n_road1_s_dash, n_road2_s_dash)
    return n_road1_s_dash, n_road2_s_dash, reward


def value_iteration():

    cur_itr = 0
    gamma = 0.9
    delta_0 = 0.001
    max_itr = 10000

    global v_state

    
    policy = np.zeros_like(v_state, dtype=int)
    delta_itr = 10000 #Any big number

    while delta_itr > delta_0 :
        delta_itr = 0.0
        cur_itr += 1
        for n_road1 in range(N_road1_MAX+1):
            for n_road2 in range(N_road2_MAX+1):
                temp = v_state[n_road1,n_road2]
                q_values = []
                for a in actions:
                    q = 0.0
                    for arriv_road1_road2 in car_arrive:
                        #This loop is going through all possible next state .. which are all possible cars can arrive in one time slot
                        #In the other project, we made that loop in the next_state() itself
                        n_road1_s_dash, n_road2_s_dash, reward = next_state_and_reward(n_road1, n_road2, a, arriv_road1_road2)
                        q += prob_car_arrive * (reward + gamma * v_state[n_road1_s_dash, n_road2_s_dash])

                    q_values.append(q)

                #After finishing the 2 actions, we choose the best action with best reward
                best_q = max(q_values)
                v_state[n_road1,n_road2] = best_q

                policy[n_road1,n_road2] = int(np.argmax(q_values))

                delta_itr = max(delta_itr, abs(temp - v_state[n_road1,n_road2]))

        print(f"delta_iteration = {delta_itr}")
        print(f"cur_itr = {cur_itr}")
        if cur_itr >= max_itr:
            print("Value iteration doesn't converge")
            sys.exit(-1)

    #ending the value iteration function
    print(f"Value iteration converged after {cur_itr}")
    print()
    return v_state, policy, cur_itr
    

v_state, policy, cur_itr = value_iteration()



# --------------------------------------
# plotting the v_state points
for m in range(0, N_road2_MAX+1, 5):
    n = range(N_road1_MAX+1)        
    label_str = "road2_cars =" + str(m) 
    plt.plot( n, v_state[n,m], label = label_str)
    #print("Road2_cars = ", m, " v_state = ", v_state[n,m])

# naming the x axis
plt.xlabel('x is road1_cars')
# naming the y axis
plt.ylabel('y is v_state')

# giving a title to my graph
plt.title('Value State Graph')

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()


# --------------------------------------
# plotting the policy points
# for m in range(0, N_road2_MAX+1, 5):
#     str_print = []
#     for n in range(N_road1_MAX+1):
#         # we want to convert 0 --> TL1 Green TL2 Red
#         # And 1 --> TL2 Green TL1 Red
#         str_print.append("TL1 Green") if policy[n,m] == 0 else str_print.append("TL2 Green")

#     print("Road2_cars = ", m, " policy = ", str_print)
#     print()

#The past print is not good at all, we will keep it 0, 1
print()
print("0 --> TL1 is Green & TL2 is Red")
print("1 --> TL2 is Green & TL1 is Red")

road2_car_gr = [] # that is to store the road2_car groups for plotting
values_TL1_g = []
values_TL2_g = []

for m in range(0, N_road2_MAX+1, 3):
    n = range(N_road1_MAX+1)
    print("Road2_cars = ", m, " policy = ", policy[n,m])
    print()

    road2_car_gr.append("Road2_cars= " + str(m))
    # print(f"Length of the road2_car_gr = {len(road2_car_gr)}")
    index = len(road2_car_gr) - 1
    values_TL1_g.append(0)
    values_TL2_g.append(0)

    # plotting policy data
    for n in range(N_road1_MAX):
        if policy[n,m] == 0:
            values_TL1_g[index] += 1 
        else:
            values_TL2_g[index] += 1


fig, ax = plt.subplots()

# Stacked bar chart
ax.bar(road2_car_gr, values_TL1_g, bottom = values_TL2_g, width = 0.25, label = "TL1 Green", color = "lightgreen")
ax.bar(road2_car_gr, values_TL2_g, width = 0.25, label = "TL2 Green", color = "lightcoral")

for bar in ax.patches:
  ax.text(bar.get_x() + bar.get_width() / 2,
          bar.get_height() / 2 + bar.get_y(),
          round(bar.get_height()), ha = 'center',
          color = 'w', weight = 'bold', size = 10)

ax.legend()
ax.set_ylabel('Road1_cars')

plt.show()