import math
import collections


def readFile(filename):
	data = []
	labels = []
	with open(filename) as data_file:
		lines = data_file.readlines()
		num_features = int(lines[0])
		num_data_points = int(lines[1])
		for index in range(2,len(lines)):
			parts = lines[index].split(': ')
			label = int(parts[1][0])
			labels.append(label)
			features = [int(x) for x in parts[0].split(' ')]
			data.append(features)
	return labels, data

def z(data_instance, Beta):
	return sum(x[0] * x[1] for x in zip(data_instance, Beta)) #dot product basically

def batchGradient(num_vars, Beta, data, labels):
	gradient = [0 for x in range(num_vars)]
	for index,data_instance in enumerate(data):
		data_instance = [1] + data_instance
		label = labels[index]
		logfxn = 1 / (1 + pow(math.e, -z(data_instance,Beta)))	
		for j in range(num_vars):
			gradient[j] += (data_instance[j] * (label - logfxn))

	return gradient

def regress(data, labels):
	num_vars = len(data[0]) + 1 #add 1 for first data point
	Beta = [0 for x in range(num_vars)] # 1 for each var
	epochs = 10000
	learning_rate = 0.0000002#0.0001
	
	for i in range(epochs):
		gradient = batchGradient(num_vars, Beta, data, labels)
		for j in range(num_vars):
			Beta[j] += (learning_rate * gradient[j])
	return Beta

def classify(data_instance, Beta):
	data_instance = [1] + data_instance
	p = 1 / (1 + pow(math.e, -z(data_instance,Beta)))	
	return 1 if p > 0.5 else 0

def test(Beta, data, labels):
	n_correct = 0
	klass_correct_counts = collections.defaultdict(lambda: 0)
	test_klass_counts = collections.defaultdict(lambda: 0)
	for i,pt in enumerate(data):
		klass = classify(pt, Beta)
		test_klass_counts[labels[i]] += 1
		if labels[i] == klass:
			n_correct += 1
			klass_correct_counts[klass] += 1

	for klass in test_klass_counts:
		tested = str(test_klass_counts[klass])
		correct = str(klass_correct_counts[klass])
		print('Class ' + str(klass) + ': tested ' + tested + ', correctly classified ' + correct)

	accuracy = float(n_correct) / len(labels)
	print('accuracy = ' + str(accuracy) + '\n')



for file in ['heart']: #'simple','vote',
	train_labels, train_data = readFile('datasets/'+ file +'-train.txt')
	Beta = regress(train_data, train_labels)
	test_labels, test_data = readFile('datasets/'+ file +'-test.txt')
	print(file + ':')
	test(Beta, test_data, test_labels)







