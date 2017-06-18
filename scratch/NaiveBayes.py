import math
import collections


class NaiveBayesClassifier:

	def __init__(self, laplace):
		self.laplace = laplace
		self.num_features = 0
		self.num_data_points = 0

		value = 1 if laplace else 0
		self.counts = collections.defaultdict(lambda: value)
		self.klass_counts = collections.defaultdict(lambda: 0)

	def readFile(self, filename, training):
		data = []
		labels = []
		with open(filename) as data_file:
			lines = data_file.readlines()

			if training:
				self.num_features = int(lines[0])
				self.num_data_points = int(lines[1])

			for line in lines[2:]:
				parts = line.split(': ')
				label = int(parts[1][0])
				labels.append(label)
				if training:
					self.klass_counts[label] += 1
				features = [int(x) for x in parts[0].split(' ')]
				data.append(features)


		return data, labels

	def train(self, filename):
		data, labels = self.readFile(filename, True)
		for i in range(len(labels)):
			features = data[i]
			label = labels[i]
			for j,feat in enumerate(features):
				self.counts[feat, label, j] += 1


	def klassProbability(self, features, klass):
		#probability of klass
		numKlass = self.klass_counts[klass]
		p = float(numKlass)/self.num_data_points
		#conditional probabilities
		for i,feat in enumerate(features):
			numerator = self.counts[feat, klass, i]
			denom = numKlass
			if self.laplace:
				denom += (self.num_features*2)
			p *= (float(numerator)/denom) #num of feature in klass/num in klass
		return p

	def classify(self, data_instance, labels):
		one_Prob = self.klassProbability(data_instance, 1)
		zero_Prob = self.klassProbability(data_instance, 0)
		return 1 if one_Prob > zero_Prob else 0
		
	def test(self, file):
		data, labels = self.readFile(file, False)
		n_correct = 0
		klass_correct_counts = collections.defaultdict(lambda: 0)
		test_klass_counts = collections.defaultdict(lambda: 0)
		for i,pt in enumerate(data):
			klass = self.classify(pt, labels)
			test_klass_counts[labels[i]] += 1
			if labels[i] == klass:
				n_correct += 1
				klass_correct_counts[klass] += 1

		for klass in self.klass_counts:
			tested = str(test_klass_counts[klass])
			correct = str(klass_correct_counts[klass])
			print('Class ' + str(klass) + ': tested ' + tested + ', correctly classified ' + correct)

		accuracy = float(n_correct) / len(labels)
		print('accuracy = ' + str(accuracy) + '\n')


for file in ['simple', 'vote','heart']:
	for laplace in [False, True]:
		print(file + ', laplace = ' + str(laplace) + ':')
		classifier = NaiveBayesClassifier(laplace)
		classifier.train('datasets/'+ file +'-train.txt')
		classifier.test('datasets/'+ file +'-test.txt')

