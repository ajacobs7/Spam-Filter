
# 
# Adapted from Version 1.0 by Tao Ban, 2010.5.26 found on: http://csmining.org/index.php/spam-email-datasets-.html
#
# 
# and store it in a new file with the same name in the dst dir. 

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib

import pandas as pd
import email.parser 
import os, stat
import shutil

# From a .eml file, xtracts the email contents (subject, body, virus scanning info...)
def ExtractFile(filename):
	''' Extract the subject and payload from the .eml file. '''

	if not os.path.exists(filename): # dest path doesnot exist
		print "ERROR: input file does not exist:", filename
		os.exit(1)
	fp = open(filename)
	msg = email.message_from_file(fp)
	#fp.close()

	payload = msg.get_payload(decode=True)
	if type(payload) == type(list()) :
		payload = payload[0] # only use the first part of payload
	if type(payload) != type('') :
		payload = str(payload)
	payload = unicode(payload, errors='replace')
	
	sub = unicode(str(msg.get('subject')), errors='replace')
	virus = str(msg.get('X-Virus-Scanned'))
	recieved = str(msg.get('Received'))	
	returnPath = str(msg.get('Return-Path'))
	to = str(msg.get('To'))


	#return sub, unicode(payload + virus + recieved + returnpath + to, errors='replace') # or 'ignore'
	return sub, payload, unicode(virus + recieved + returnPath + to, errors='replace')


# Extracts info from all .eml files in the specified directory
def ExtractDirHelper(srcdir, df):
	'''Extract the body information from all .eml files in the srcdir and store in an array.'''

	files = os.listdir(srcdir)
	for file in files:
		srcpath = os.path.join(srcdir, file)
		src_info = os.stat(srcpath)
		if stat.S_ISDIR(src_info.st_mode): # for subfolders, recurse
			df = ExtractDirHelper(srcpath, df)
		else:  # copy the file
			sub, body, features = ExtractFile(srcpath)
			df.append([sub, body, features])
	return df


def vectorize(emails):
	vec = CountVectorizer(stop_words = 'english', ngram_range=(1,2), max_df = 0.5) #min_df=2
	dtm = vec.fit_transform(emails).toarray() #, columns=vec.get_feature_names())
	#joblib.dump(vec, 'Vectorizer.pkl')
	return dtm

def ExtractDir(srcdir):
	data = pd.DataFrame(ExtractDirHelper(srcdir, []), columns = ['subject', 'body', 'features'])
	v_sub = pd.DataFrame(vectorize(data['subject']))
	v_body = pd.DataFrame(vectorize(data['body']))
	v_feat = pd.DataFrame(vectorize(data['features']))
	return pd.concat([v_sub, v_body, v_feat], axis = 1, ignore_index=True) #.values.tolist()