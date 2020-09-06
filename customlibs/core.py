import random
import numpy as np
import pandas as pd
import scipy.stats
import scipy.optimize
from simanneal import Annealer


class OptSim(Annealer):

	def __init__(self, ent_array):
		self.ent_array = ent_array
		state = np.zeros(len(ent_array[2]))
		super(OptSim, self).__init__(state)

	def move(self):
		i = random.randint(0, len(self.state) - 1)
		if self.state[i] == 0:
			self.state[i] = 1
		else:
			self.state[i] = 0

	def energy(self):
		return 0 - calc_util(np.vstack((self.ent_array[0:2], self.state)))


def calc_util(ent_array):
	util = 0
	n_ent = sum(ent_array[2])
	for i in range(ent_array.shape[1]):
		if ent_array[2][i]:
			util += ent_array[0][i]
			util -= ent_array[1][i] * (n_ent - 1)
	return util


def rat_sim(ent_array):
	util = calc_util(ent_array)
	bin_vector = ent_array[2]
	while True:
		prev_bin_vector = bin_vector
		prev_util = util
		n_ent = sum(bin_vector)
		for i, x in enumerate(bin_vector):
			if x == 0 and ent_array[0][i] > ent_array[1][i] * n_ent:
				bin_vector[i] = 1
			if x == 1 and ent_array[0][i] < ent_array[1][i] * (n_ent - 1):
				bin_vector[i] = 0
		temp_array = ent_array
		temp_array[2] = bin_vector
		util = calc_util(temp_array)
		if util == prev_util:
			return bin_vector
		if util < prev_util:
			return prev_bin_vector


def alt_sim(ent_array):
	util = calc_util(ent_array)
	bin_vector = ent_array[2]
	while True:
		prev_bin_vector = bin_vector
		prev_util = util
		n_ent = sum(bin_vector)
		for i, x in enumerate(bin_vector):
			if x == 0:
				p_b = ent_array[0][i]
				p_c = ent_array[1][i] * n_ent
				e_c = sum([x[1] for x in ent_array.transpose() if x[2] == 1])
				if p_b > p_c + e_c:
					bin_vector[i] = 1
			if x == 1:
				p_b = ent_array[0][i]
				p_c = ent_array[1][i] * (n_ent - 1)
				e_c = sum([x[1] for j, x in enumerate(ent_array.transpose()) if x[2] == 1 and i != j])
				if p_b < p_c + e_c:
					bin_vector[i] = 0
		temp_array = ent_array
		temp_array[2] = bin_vector
		util = calc_util(temp_array)
		if util == prev_util:
			return bin_vector
		if util < prev_util:
			return prev_bin_vector



def opt_sim(ent_array):
	os = OptSim(ent_array)
	os.set_schedule(os.auto(minutes=3))
	state, e = os.anneal()
	return state


'''
 def opt_sim(ent_array):
	init = ent_array[2]
	# func_1 = lambda x: len([y for y in x if y != 0 and y != 1])
	# con_1 = scipy.optimize.NonlinearConstraint(func_1, 0, 0)
	bound = scipy.optimize.Bounds(0, 1)
	func_2 = lambda x: 1 - calc_util(np.vstack((ent_array[0:2], x)))
	# result = scipy.optimize.minimize(func_2, init, constraints=con_1)
	result = scipy.optimize.minimize(func_2, init, bounds=bound)
	return np.array([round(x) for x in result["x"]])


class Step(object):

	def __init__(self):
		return

	def __call__(self, x):
		while True:
			index = random.randint(0, len(x) - 1)
			if x[index] == 0:
				x[index] = 1
			else:
				x[index] = 0
			if all([y == 0 or y == 1 for y in x]):
				break
		return x


def opt_sim(ent_array):
	init = np.zeros(len(ent_array[2]))
	func = lambda x: -calc_util(np.vstack((ent_array[0:2], x)))
	step=Step()
	result = scipy.optimize.basinhopping(func, init, take_step=step)
	return result
'''
