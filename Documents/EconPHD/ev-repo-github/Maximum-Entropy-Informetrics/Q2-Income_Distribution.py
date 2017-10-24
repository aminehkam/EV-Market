import numpy as np
from scipy.optimize import minimize
from itertools import product, permutations
import matplotlib.pyplot as plt

def entropy(probs):
    return -sum([prob * np.log(prob +1e-8) for prob in probs])

def objective_func(probs, sign=1.0):
    '''
    The objective function to be used in numpy minimze.
    '''
    return sign * entropy(probs)

def compute_probabilities(cons, size):


    # scipy requires a starting position to compute the values.
    # We can start from a fair dice
    start_pos = ptrues #np.ones(6)*(1/6.)

    # we want to make sure all the solutions are in the range of [0, 1]
    bnds = tuple((0,1) for x in range(0, size))

    # call scipy minimize to find the solution and return all the information
    # - the args = (-1.0) passes the sign to the objective function
    # - we are going to use the Sequential Least Square Programming
    # - we would like to see the detailed information about number of iterations
    return minimize(objective_func, start_pos, args=(-1.0,),
                    constraints=cons, method='SLSQP', bounds=bnds, options={'disp': True})




def expected_value(probs, values):
    s = 0
    for i in range(0, len(probs)):
        s += probs[i] * values[i]
    return s


ptrues = [0.271, 0.418, 0.237, 0.046, 0.018, 0.002, 0.008]
x1 = [(0 +  9225)/2, (9225+37450)/2, (37450+90750)/2, (90750+189300)/2, (189300+411500)/2, (411500+413200)/2, 413200]
x2 = [(0 + 18450)/2, (18450+74900)/2, (74900+151200)/2, (151200+230450)/2, (230450+411500)/2, (411500+464850)/2, 464850]
x3 = [(0 + 13150)/2, (13150+50200)/2, (50200+129600)/2, (129600+209850)/2, (209850+411500)/2, (411500+439000)/2, 439000]


#we construct the means of each one of the constraints using the true distribution.

expected_x1 = expected_value(ptrues, x1)
expected_x2 = expected_value(ptrues, x2)
expected_x3 = expected_value(ptrues, x3)

print expected_x1
print expected_x2
print expected_x3

print x1
print x2
print x3




# cons1 = ({'type': 'eq', 'fun': lambda p:  1 - sum(p)},
#        {'type': 'eq', 'fun': lambda p: sum([p[i] * x1[i] for i in range(0, len(x1))]) - expected_x1})


# cons2 = ({'type': 'eq', 'fun': lambda p:  1 - sum(p)},
#        {'type': 'eq', 'fun': lambda p: sum([p[i] * x1[i] for i in range(0, len(x1))]) - expected_x2})

cons3 = ({'type': 'eq', 'fun': lambda p:  1 - sum(p)},
        {'type': 'eq', 'fun': lambda p: sum([p[i] * x1[i] for i in range(0, len(x1))]) - expected_x1},
         {'type': 'eq', 'fun': lambda p: sum([p[i] * x2[i] for i in range(0, len(x2))]) - expected_x2},
         {'type': 'eq', 'fun': lambda p: sum([p[i] * x3[i] for i in range(0, len(x3))]) - expected_x3})


probs = compute_probabilities(cons3, len(x1)).x
for prob in probs:
    print '{0:.3f}'.format(prob)


x = np.array(sorted(x1))
y = np.array(ptrues)

bar_width = 10000
plt.bar(x, y, bar_width, alpha=1.0, color='b')
plt.xlabel("Income Groups")
plt.ylabel("Probability")

plt.show()


