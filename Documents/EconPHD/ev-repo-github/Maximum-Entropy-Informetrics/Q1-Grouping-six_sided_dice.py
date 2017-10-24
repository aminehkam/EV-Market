import numpy as np
from scipy.optimize import minimize
from itertools import product, permutations
import matplotlib.pyplot as plt

def entropy(probs):
    return -sum([prob * np.log(prob) for prob in probs])

def objective_func(probs, sign):
    '''
    The objective function to be used in numpy minimze.
    '''
    return sign * entropy(probs) #-sum([prob * np.log(prob) for prob in probs])

def compute_probabilities(average_value):
    '''
    Given an average value for a die, returns the probabilities
    of each outcome.

    To do so, this function tries to maximize the following function
      -sum(p[i] * log(p[i]))
    In other words it is trying to minimize the negation of this function.

    The contraints for this computations are:
        1. sum(p[i]) = 1 for i in [1, 6]
        2. sum(p[i]*x[i]) = y (for a given y)
    '''

    # define the constraints
    cons = ({'type': 'eq', 'fun': lambda p:  1 - sum(p)},
            {'type': 'eq', 'fun': lambda p: sum([p[i] * (i+1) for i in range(0, 6)]) - average_value})

    # scipy requires a starting position to compute the values.
    # We can start from a fair dice
    start_pos = np.ones(6)*(1/6.)

    # we want to make sure all the solutions are in the range of [0, 1]
    bnds = tuple((0,1) for x in range(0,6))

    # call scipy minimize to find the solution and return all the information
    # - the args = (-1.0) passes the sign to the objective function
    # - we are going to use the Sequential Least Square Programming
    # - we would like to see the detailed information about number of iterations
    return minimize(objective_func, start_pos, args=(-1.0,),
                    constraints=cons, method='SLSQP', bounds=bnds)


def find_permutations(number_of_dice, dice_values=range(1,7)):
    '''
    Given number of dice, return the possible permutations of
    the elementary outcomes(i) and store them as a dictionary of their
    potential sums. In other words, group them as disjoint set of k=2,...,12
    '''

    # this dictionary uses sums of possible dice outcomes as the key and
    # a list of the permutations that results in that sum as the values
    perms = {}
    for i in product(dice_values, repeat=number_of_dice):
        k = sum(i)
        # print i
        # print k
        # if it is the first time create an empty list (setdefault)
        # otherwise append the current permutation.
        if k not in perms:
            perms[k] = []
        perms[k].append(i)
        #print perms


    print perms
    return perms

def find_probability_per_sum(sums_permutations, num_of_dice, p_elementary_outcomes):
    '''
    Given a set of sums_permutations for dice and their associated
    probability compute the probability for each sum to occur.
    '''
    # print sums_permutations
    # print p_elementary_outcomes
    p_k = {}

    # for each given sum permutation
    for k in sums_permutations:
        # for each permutaiton that its sum is equal to k:
        # - multiply the probability of each dice occurence to
        #   compute the probability of the outcome and add it to
        #   the final dictionary of probability per sum.
        p_k[k] = 0
        for each_perm in sums_permutations[k]:
            cur_prob = 1
            # for as many dices we have compute the sum of their probabilities
            #[[1/6, 1/6, 1/6, 1/6, 1/6, 1/6], [1/3, 1/3, 1/12, 1/12, 1/12, 1/12]]
            # consider (2,2) as a permutaiton with k = 4
            # probability of this outcome is 1/6*1/3
            # now consider (1,3) with k = 4
            # probability of this outcome is 1/6*1/12
            # and for (3,1)
            # probability of this outcome is 1/6*1/3
            # so the probability of p_k[4]= 1/6*1/3 + 1/6*1/12 + 1/6*1/3

            # number_of_dice = len(p_elementary_outcomes)
            for i in range(0, num_of_dice):
                cur_die_elementary_outcome = p_elementary_outcomes[i]
                cur_die_value = each_perm[i]
                cur_prob = cur_prob * cur_die_elementary_outcome[cur_die_value-1]
            p_k[k] += cur_prob

    # print p_k
    return p_k

#def find_pk_for_k(single_die_prob, num_dice):
def find_pk_for_k(dice_probs, num_of_dice):
    '''
    Given the expected sum for a die, and the number of dice
    compute the pk values (probability of each sum).
    '''
    #assume all dice have same probability
    #dice_probs = [single_die_prob for i in range(0, num_of_dice)]
    # find permutations of two dice
    dice_perms = find_permutations(num_of_dice)

    return find_probability_per_sum(dice_perms, num_of_dice, dice_probs)


def plot_all(max_num_dice, average_values):
    for num_dice in range(2, max_num_dice+1):
        i_probs = [compute_probabilities(average_value).x for average_value in average_values]
        # i_prob = compute_probabilities(average_value1).x
        # i_prob = compute_probabilities(average_value2).x
        pks = find_pk_for_k(i_probs, num_dice)

        pks_probs = [pks[key] for key in pks]

        print 'probability of pks = {}'.format(pks_probs)
        print 'probability of die outcomes = {}'.format(i_probs)
        print 'entropy of pks = {}'.format(entropy(pks_probs))
        for i_prob in i_probs:
            print 'entropy of p[i]s for {} dice = {}'.format(num_dice, entropy(i_prob) * num_dice)

        x = np.array(sorted(pks))
        y = np.array(pks_probs)
        plt.plot(x, y)

    plt.xlabel("Possible sums")
    plt.ylabel("Probability")
    plt.show()

plot_all(2,[3.5,3.5])
#plot_all(5,[5,5,5,5,5])
#plot_all(5, [2,2,2,5,5])
