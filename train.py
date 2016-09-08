from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score, mean_squared_error, roc_auc_score, precision_score, recall_score

from math import sqrt
import pandas as pd
from ExtractContent import ExtractDir


print('Extracting Data...')
emails = ExtractDir("CSDMC2010_SPAM/TRAINING")
labels = pd.read_table("CSDMC2010_SPAM/SPAMTrain.label", delim_whitespace=True, names=["labels", "files"])["labels"] #SPAM = 0, HAM = 1

print('Splitting...')
X_train, X_test, y_train, y_test = train_test_split(emails, labels, test_size=0.33, random_state=42)

print('Training...')
model = LogisticRegression()
model.fit(X_train, y_train)

print('Saving...')
joblib.dump(model, 'Models/Filter_Model.pkl', compress=1)

print('\nModel Evaluation:')
pred_labels = model.predict(X_test)

accuracy = accuracy_score(y_test, pred_labels)
rmse = sqrt(mean_squared_error(y_test, pred_labels))
precision = precision_score(y_test, pred_labels)
recall = recall_score(y_test, pred_labels)
roc_score = roc_auc_score(y_test, pred_labels)

print("   RMSE: %f" % rmse)
print("   Accuracy: %f" % accuracy)
print("   ROC: %f" % roc_score)
print("   Precision: %f" % precision)
print("   Recall: %f" % recall)
