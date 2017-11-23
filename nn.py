import math
import numpy as np 

class Connection:
	def __init__(self, connectedNeuron):
		self.connectedNeuron = connectedNeuron
		self.weight = np.random.normal()
		self.dweight = 0.0

class Neuron:
	eta = 0.001
	alpha = 0.01
	#takes the previous layer as input
	def __init__(self, layer):
		self.dendrons = [] #connections
		self.error = 0.0
		self.gradient = 0.0
		self.output = 0.0
		if layer is None:
			pass
		else:
			for neuron in layer:
				con = Connection(neuron)
				self.dendrons.append(con)

	def addError(self, err):
		self.error = self.error + err #accumulates error sent from all neurons in the next layer during backprop

	def sigmoid(self, x):
		return 1 / (1 + math.exp(-x * 1.0)) #activation

	def dsigmoid(self, x):
		return x * (1.0 - x) #derivation

	def setError(self, err):
		self.error = err

	def setOutput(self, output):
		self.output = output

	def getOutput(self):
		return self.output

	def feedForward(self):
		sumOutput = 0
		if len(self.dendrons) == 0:
			return
		for dendron in self.dendrons:
			sumOutput = sumOutput + dendron.connectedNeuron.getOutput() * dendron.weight
		self.output = self.sigmoid(sumOutput)

	def backProp(self):
		self.gradient = self.error * self.dsigmoid(self.output)
		for dendron in self.dendrons:
			dendron.dweight = Neuron.eta * (dendron.connectedNeuron.output * self.gradient) + self.alpha * dendron.dweight
			dendron.weight = dendron.weight + dendron.dweight
			dendron.connectedNeuron.addError(dendron.weight * self.gradient)

class Network:
	def __init__(self, topology):
		self.layers = []
		for numNeuron in topology:
			layer = []
			for i in range(numNeuron):
				if(len(self.layers) == 0):
					layer.append(Neuron(None))
				else:
					layer.append(Neuron(self.layers[-1]))
			layer.append(Neuron(None))#bias neuron
			layer[-1].setOutput(1)#setting output of bias neuron as 1
			self.layers.append(layer)

	def setInput(self, inputs):
		for i in range(len(inputs)):
			self.layers[0][i].setOutput(inputs[i])

	def getError(self, target):
		err = 0
		for i in range(len(target)):
			e = (target[i] - self.layers[-1][i].getOutput())
			err = err + e**2
		err = err / len(target)
		err = math.sqrt(err)
		return err

	def feedForwardNetwork(self):
		for layer in self.layers[1:]:
			for neuron in layer:
				neuron.feedForward()


	def backPropNetwork(self, target):
		for i in range(len(target)):
			self.layers[-1][i].setError(target[i] - self.layers[-1][i].getOutput())
		for layer in self.layers[::-1]:
			for neuron in layer:
				neuron.backProp()

	def getResults(self):
		output = []
		for neuron in self.layers[-1]:
			output.append(neuron.getOutput())
		output.pop()#remove bias
		return output
		
	# def getTheResults(self):
	# 	output = []
	# 	for neuron in self.layers[-1]:
	# 		x = neuron.getOutput()
	# 		if(x > 0.5):
	# 			x = 1
	# 		else:
	# 			x = 0
	# 		output.append(x)
	# 	output.pop()#remove bias
	# 	return output

def main():
	topology = []
	topology.append(2)
	topology.append(3)
	topology.append(2)
	net = Network(topology)
	Neuron.eta = 0.09
	Neuron.alpha = 0.015
	inputs = [[0,0],[0,1],[1,0],[1,1]]
	outputs = [[0,0],[1,0],[1,0],[0,1]]
	while True:
		err = 0
		for i in range(len(inputs)):
			net.setInput(inputs[i])
			net.feedForwardNetwork()
			net.backPropNetwork(outputs[i])
			err = err + net.getError(outputs[i])
		print("Error: ", err)
		if err < 0.01:
			break
	while True:
		a = input("Type 1st input: ")
		b = input("Type 2nd input: ")
		net.setInput([a,b])
		net.feedForward()
		print(net.getResults())

main()