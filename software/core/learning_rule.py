from random import uniform

class Hebbian:
	def __init__(self, learningRate=0.1, apriori=0):
		self.learningRate = learningRate
		self.apriori = apriori

	def update(self, data):
		self.apriori += self.learningRate * data

	def output(self, data):
		return self.apriori * data


class Delta:
	def __init__(self, learningRate=0.1, apriori=uniform(-1, 1)):
		self.learningRate = learningRate
		self.apriori = apriori

	def update(self, data):
		self.apriori += self.learningRate * (data - self.output(data)) * self.apriori

	def output(self, data):
		return self.apriori * data
