#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 09:42:06 2018

@author: jdavidmartinezg
"""

# Master simulator

'''
Parameters:
    
    Size of intake class
    Desired average for each section
    Number of possible group distribution
    
    
    Number of spots x possible GRE values (41 for Q and V and 13 for AWA)
'''

import itertools as it
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def frange(start, stop, step):
     i = start
     while i < stop:
         yield i
         i += step

def gre_average_simulator(n_sim = 1000000, class_size = 65, quant_avg = 167, verbal_avg = 158, awa_avg = 4, quant_range = [163,170], verbal_range = [149,163], awa_range = [2,5]):
    
    '''
    n_sim        = 1000000
    class_size   = 65
    quant_avg    = 167
    verbal_avg   = 158
    awa_avg      = 4
    quant_range  = [163,170]
    verbal_range = [149,163]
    awa_range    = [2,5]
    '''
    
    # Array with n_sim rows and class_size columns
    
    # QUANT
    
    quant_array_sim       = np.random.randint(quant_range[0], quant_range[1] + 1, size = n_sim*class_size)
    
    quant_matrix_sim      = np.reshape(quant_array_sim, (n_sim, class_size))
    
    quant_desired_row_sum = class_size*quant_avg*0.999
    
    quant_row_sums        = quant_matrix_sim.sum(axis = 1)
    
    quant_matrix_sim      = quant_matrix_sim[np.where(quant_row_sums > quant_desired_row_sum)]
    
    n_sim_pos_quant       = len(quant_matrix_sim)
    
    freq_my_quant         = np.count_nonzero(quant_matrix_sim == quant_range[0], axis = 1)
    
    probability_quant     = 1 - (np.count_nonzero(freq_my_quant == 0)/n_sim_pos_quant)
    
    quant_mean_n_students       = np.mean(freq_my_quant)
    
    quant_max_n_students        = np.max(freq_my_quant)
    
    quant_min_n_students        = np.min(freq_my_quant)
    
    plt.hist(freq_my_quant, alpha = .75, rwidth = .9, color = "C0")
    
    plt.title("Distribution of Number of students with score " + str(quant_range[0]) + " in the quant section, given an average score of " + str(quant_avg) + " in the group of admitted") 
    
    plt.xlabel("Number of students with a score of " + str(quant_range[0]) + " in Quant section")
    
    plt.ylabel("Frequency")
    
    ###########################################################################
    
    
    # Verbal
    
    verbal_array_sim       = np.random.randint(verbal_range[0], verbal_range[1] + 1, size = n_sim*class_size)
    
    verbal_matrix_sim      = np.reshape(verbal_array_sim, (n_sim, class_size))
    
    verbal_desired_row_sum = class_size*verbal_avg*0.999
    
    verbal_row_sums        = verbal_matrix_sim.sum(axis = 1)
    
    verbal_matrix_sim      = verbal_matrix_sim[np.where(verbal_row_sums > verbal_desired_row_sum)]
    
    n_sim_pos_verbal       = len(verbal_matrix_sim)
    
    freq_my_verbal         = np.count_nonzero(verbal_matrix_sim == verbal_range[0], axis = 1)
    
    probability_verbal     = 1 - (np.count_nonzero(freq_my_verbal == 0)/n_sim_pos_verbal)
    
    verbal_mean_n_students       = np.mean(freq_my_verbal)
    
    verbal_max_n_students        = np.max(freq_my_verbal)
    
    verbal_min_n_students        = np.min(freq_my_verbal)
    
    plt.hist(freq_my_verbal, alpha = .75, rwidth = .9, color = "C0")
    
    plt.title("Distribution of Number of students with score " + str(verbal_range[0]) + " in the verbal section, given an average score of " + str(verbal_avg) + " in the group of admitted") 
    
    plt.xlabel("Number of students with a score of " + str(verbal_range[0]) + " in verbal section")
    
    plt.ylabel("Frequency")  
    
    
    # AWA --- Experimental
    
    awa_array           = np.arange(awa_range[0], awa_range[1] + 0.5, 0.5)
    
    if (n_sim*class_size)%len(awa_array) != 0:
        x = (n_sim*class_size) - ((n_sim*class_size)%len(awa_array)) 
    else:
        x = (n_sim*class_size)

    mult                = x/len(awa_array)

    awa_array_sim       = np.repeat(awa_array, repeats = mult)
    
    awa_array_fix       = np.repeat(awa_array, repeats = 100)
    
    np.random.shuffle(awa_array_fix)
    
    awa_array_sim       = np.append(awa_array_sim, awa_array_fix[0:((n_sim*class_size)%len(awa_array))])
    
    np.random.shuffle(awa_array_sim)
    
    awa_matrix_sim      = np.reshape(awa_array_sim, (n_sim, class_size))
    
    awa_desired_row_sum = class_size*awa_avg*0.999
    
    awa_row_sums        = awa_matrix_sim.sum(axis = 1)
    
    awa_matrix_sim      = awa_matrix_sim[np.where(awa_row_sums > awa_desired_row_sum)]
    
    n_sim_pos_awa       = len(awa_matrix_sim)
    
    freq_my_awa         = np.count_nonzero(awa_matrix_sim == awa_range[0], axis = 1)
    
    probability_awa     = 1 - (np.count_nonzero(freq_my_awa == 0)/n_sim_pos_awa)
    
    awa_mean_n_students       = np.mean(freq_my_awa)
    
    awa_max_n_students        = np.max(freq_my_awa)
    
    awa_min_n_students        = np.min(freq_my_awa)
    
    plt.hist(freq_my_awa, alpha = .75, rwidth = .9, color = "C0")
    
    plt.title("Distribution of Number of students with score " + str(awa_range[0]) + " in the awa section, given an average score of " + str(awa_avg) + " in the group of admitted") 
    
    plt.xlabel("Number of students with a score of " + str(awa_range[0]) + " in awa section")
    
    plt.ylabel("Frequency")      

    
    ###########################################################################
    
    
    report = '''
    
GENERAL PARAMETERS \n\n    
    
NUMBER OF SIMULATIONS       = {num_sim} \n
CLASS SIZE                  = {class_} \n
QUANT AVERAGE FOR ADMITTED  = {quantav} \n
VERBAL AVERAGE FOR ADMITTED = {verbalav} \n
AWA AVERAGE FOR ADMITTED    = {awaav} \n\n

-------------------------------------------------------------- \n\n

YOUR SCORES: \n\n

QUANT  = {my_quant} \n
VERBAL = {my_verbal} \n
AWA    = {my_awa} \n\n

-------------------------------------------------------------- \n\n

REPORT \n\n

Quant \n\n

Probability of being part of the incoming group given your Quant score and the average of the University: {quant_prob}% \n\n
Max number of students with your Quant scores in the simulations: {max_quant} \n\n
Mean number of students with your Quant scores in the simulations: {min_quant} \n\n\n

Verbal \n\n

Probability of being part of the incoming group given your Verbal score and the average of the University: {verbal_prob}% \n\n
Max number of students with your Verbal scores in the simulations: {max_verbal} \n\n
Mean number of students with your Verbal scores in the simulations: {min_verbal} \n\n\n

AWA (EXPERIMENTAL)\n\n

Probability of being part of the incoming group given your AWA score and the average of the University: {awa_prob}% \n\n
Max number of students with your AWA scores in the simulations: {max_awa} \n\n
Mean number of students with your AWA scores in the simulations: {min_awa} \n\n\n
    '''.format(num_sim = n_sim, class_ = class_size, quantav = quant_avg, verbalav = verbal_avg, awaav = awa_avg,
    quant_prob = round(probability_quant,2)*100, max_quant = quant_max_n_students, min_quant = round(quant_mean_n_students, 2), verbal_prob = round(probability_verbal,2)*100,
    max_verbal = verbal_max_n_students, min_verbal = round(verbal_mean_n_students,2), awa_prob = round(probability_awa,2)*100, max_awa = awa_max_n_students,
    min_awa = round(awa_mean_n_students,2), my_quant = str(quant_range[0]), my_verbal = str(verbal_range[0]), my_awa = str(awa_range[0]))
    
    
    return report






