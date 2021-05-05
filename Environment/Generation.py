from godot import exposed, export
from godot import *
import numpy as np
import json 
import os
import shutil
import random

GENERATIONS_DIR = os.path.join(os.getcwd(), "Generations")
if os.path.exists(GENERATIONS_DIR):
	shutil.rmtree(GENERATIONS_DIR)
os.mkdir(GENERATIONS_DIR)

@exposed
class Generation(Node):
	generation = 0
	def _ready(self):
		self.parent = self.get_parent()
		
	def create_generation(self, pop_size, prev_birds=False):
		self.generation += 1
		new_generation_dir = os.path.join(GENERATIONS_DIR, f"generation-{self.generation}")
		os.mkdir(new_generation_dir)
		data_paths = PoolStringArray()
		if len(prev_birds) == 0:
			for i in range(pop_size):
				path = os.path.join(new_generation_dir, f"{i}.npy")
				data_paths.append(GDString(path))
		else:
			distribution, average_fitness = self.calc_distribution(prev_birds)
			for i in range(pop_size):
				parents = self.calc_parents(prev_birds, distribution)
				weights_1 = np.load(str(parents[0].get_brain().get_brain_data()), allow_pickle=True)
				weights_2 = np.load(str(parents[1].get_brain().get_brain_data()), allow_pickle=True)
				new_weights = self.crossover(weights_1, weights_2)
				self.mutate(new_weights)
				path = os.path.join(new_generation_dir, f"{i}.npy")
				np.save(path, new_weights)
				data_paths.append(GDString(path))
			self.parent.python_print(average_fitness)
			
		return data_paths
		
	def mutate(self, weights):
		self.mutate_weight(weights[0])
		self.mutate_weight(weights[1])
		self.mutate_weight(weights[2])
		self.mutate_weight(weights[3])

	def mutate_weight(self, weights):
		for weight in np.nditer(weights, op_flags=['readwrite']):
			if random.random() < 0.1:
				weight[...] = max(0, min(1, weight + (random.gauss(0,1) * 0.5)))
				
	def crossover(self, weights_1, weights_2):
		fully_new_weights = []
		for parent_1, parent_2 in zip(weights_1, weights_2):
			new_weights = np.zeros(parent_1.shape)
			parent_1_nditer = np.nditer(parent_1, op_flags=['readwrite'], flags=['multi_index'])
			parent_2_nditer = np.nditer(parent_2, op_flags=['readwrite'], flags=['multi_index'])
			for weight_1 in parent_1_nditer:
				index = parent_1_nditer.multi_index
				if random.random() > 0.5:
					new_weights[index] = weight_1
				else:
					new_weights[index] = parent_2[index]
	
			fully_new_weights.append(new_weights)
	
		return fully_new_weights
		
	def calc_parents(self, birds, distribution):
		parents = random.choices(birds, distribution, k=2)
		return parents
	
	def calc_distribution(self, birds):
		total_fitness, average_fitness = self.calc_total_fitness(birds)
		total_fitness = max(total_fitness, 1)
		distribution = []
		for bird in birds:
			distribution.append(max(bird.fitness, 0.001)/total_fitness)
		return distribution, average_fitness

	def calc_total_fitness(self, birds):
		total_fitness = 0
		for bird in birds:
			if bird.fitness > 0:
				total_fitness += bird.fitness
		return total_fitness, total_fitness/len(birds)
			
			
