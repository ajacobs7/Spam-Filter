'''
    File name: vectorize.py
    Author: Austin Jacobs
    Date created: 9/8/16
    Date last modified: 9/8/16
    Python Version: 2.7
'''

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import pandas as pd

def vectorize(emails, training=False):
	''' Vectorizes each part of the data, combines and returns. '''

	vec = load_vectorize
	if training:
		vec = train_vectorize

	data = pd.DataFrame(emails, columns = ['Subject', 'Body', 'Feature'])
	v_sub = vec(data['Subject'])
	v_body = vec(data['Body'])
	v_feat = vec(data['Feature'])
	return pd.concat([v_sub, v_body, v_feat], axis = 1, ignore_index=True)

def train_vectorize(emails):
	''' Creates a vectorizer, fits the email data, saves the model, returns vectorized data. '''

	vec = CountVectorizer(stop_words = 'english', ngram_range=(1,2), max_df = 0.5) #min_df=2
	dtm = pd.DataFrame(vec.fit_transform(emails).toarray())
	joblib.dump(vec, 'Models/' + emails.name + '_Vectorizer.pkl', compress=1)
	return dtm

def load_vectorize(emails):
	''' Loads the correct vectorizer, fits the email data, returns vectorized data. '''

	sub_vec = joblib.load('Models/' + emails.name + '_Vectorizer.pkl')
	dtm = sub_vec.transform(emails).toarray()
	return pd.DataFrame(dtm)