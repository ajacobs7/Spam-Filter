from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, confusion_matrix, roc_auc_score, precision_score, recall_score
from math import sqrt
import pandas as pd
from ExtractContent import ExtractDir


def downloadData():
	emails = ExtractDir("CSDMC2010_SPAM/TRAINING")
	labels = pd.read_table("CSDMC2010_SPAM/SPAMTrain.label", delim_whitespace=True, names=["labels", "files"])["labels"]
	labels = [0 if x==1 else 1 for x in labels] #reverse so that SPAM = 1, HAM = 0
	return emails, labels

def train(emails, labels):
	model = GaussianNB() #LogisticRegression() #PassiveAggressiveClassifier() #SGDClassifier() #GaussianNB() #MultinomialNB()
	model.fit(emails, labels)
	return model

def evaluate(model, test_emails, test_labels):
	pred_labels = model.predict(test_emails)

	accuracy = accuracy_score(test_labels, pred_labels)
	rmse = sqrt(mean_squared_error(test_labels, pred_labels))
	conf_mat = confusion_matrix(test_labels, pred_labels)
	precision = precision_score(test_labels, pred_labels)
	recall = recall_score(test_labels, pred_labels)
	roc_score = roc_auc_score(test_labels, pred_labels)

	print("Accuracy: %f" % accuracy)
	print("ROC: %f" % roc_score)
	print("RMSE: %f" % rmse)
	print("Confusion Matrix:")
	print(conf_mat)
	print("Precision: %f" % precision)
	print("Recall: %f" % recall)

print('Downloading')
emails, labels = downloadData()
print('Splitting')
X_train, X_test, y_train, y_test = train_test_split(emails, labels, test_size=0.33, random_state=42)
print('Training')
model = train(X_train, y_train)
evaluate(model, X_test, y_test)