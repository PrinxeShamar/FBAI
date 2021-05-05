from godot import exposed, export
from godot import *
import numpy as np
import os
from scipy.special import expit

@exposed
class Brain(Node):
	def create_model(self):
		self.add(Layer_Dense(4, 16))
		self.add(Activation_ReLU())
		self.add(Layer_Dense(16, 1))
		self.add(Activation_Sigmoid())
		
	def create(self):
		self.weights = []
		self.layers = []
		self.create_model()
		
	def init(self, path):
		self.create()
		path = str(path)
		if os.path.exists(path):
			data = np.load(path, allow_pickle=True)
			self.set_weights(data)
		else:
			np.save(path, self.get_weights())
		self.brain_data = path
	
	def get_brain_data(self):
		return self.brain_data
			
	def add(self, layer):
		self.layers.append(layer)
		
	def predict(self, x):
		inputs = x
		for layer in self.layers:
			layer.forward(inputs)
			inputs = layer.output
		#return float(np.argmax(inputs))
		return float(inputs[0])

	def get_weights(self):
		weights = []
		for layer in self.layers:
			if layer.type == "layer":
				weights.append(np.copy(layer.weights))
				weights.append(np.copy(layer.biases))
		return weights
		
	def set_weights(self, weights):
		index = 0
		for layer in self.layers:
			if layer.type == "layer":
				layer.weights = weights[index]
				layer.biases = weights[index+1]
				index += 2
				
class Layer_Dense:
	type = "layer"
	def __init__(self, n_inputs, n_neurons):
		self.weights = np.random.randn(n_inputs, n_neurons)
		self.biases = np.random.randn(1, n_neurons)
	def forward(self, inputs):
		self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLU:
	type = "activation"
	def forward(self, inputs):
		self.output = np.maximum(0, inputs)

class Activation_Softmax:
	type = "activation"
	def forward(self, inputs):
		exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
		probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
		self.output = probabilities

class Activation_Sigmoid:
	type = "activation"
	def forward(self, inputs):
		self.output = expit(inputs)
		
 
