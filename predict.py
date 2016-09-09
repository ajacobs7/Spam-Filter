'''
    File name: predict.py
    Author: Austin Jacobs
    Date created: 9/8/16
    Date last modified: 9/8/16
    Python Version: 2.7
'''

from sklearn.externals import joblib
from extract import extract_file
from vectorize import vectorize

filename = input('Email File Name: ')

print("Extracting Data...")
email = vectorize([extract_file(filename)])

print("Predicting...")
model = joblib.load('Models/Filter_Model.pkl')
pred = model.predict(email)


if pred[0] == 0:
	print('SPAM')
else:
	print('HAM')
