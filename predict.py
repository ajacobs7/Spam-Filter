'''
    File name: predict.py
    Author: Austin Jacobs
    Date created: 9/8/16
    Date last modified: 9/8/16
    Python Version: 2.7
'''

from sklearn.externals import joblib
from extract import extract_file, extract_dir
from vectorize import vectorize

scale = raw_input('(1) File (2) Directory : ')

if scale == '1': 
	filename = raw_input('File Name: ')
	email = [extract_file(filename)]
elif scale == '2':
	direc = raw_input('Directory: ')
	email = extract_dir(direc)
else:
	print('Invalid')
	exit()


email = vectorize(email)
model = joblib.load('Models/Filter_Model.pkl')
pred = model.predict(email)

print ['SPAM' if x == 0 else 'HAM' for x in pred]

