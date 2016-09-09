# 
# Adapted from Version 1.0 by Tao Ban, 2010.5.26 found on: http://csmining.org/index.php/spam-email-datasets-.html
#

from sklearn.externals import joblib
import email.parser 
import os, stat
import shutil

def ExtractFile(filename):
	''' Extract the email contents (subject, body, virus scanning info...)  from the .eml file. '''

	if not os.path.exists(filename): # dest path doesnot exist
		print "ERROR: input file does not exist:", filename
		os.exit(1)
	fp = open(filename)
	msg = email.message_from_file(fp)

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

	return sub, payload, unicode(virus + recieved + returnPath + to, errors='replace')


def ExtractDirHelper(srcdir, df):
	'''Uses recursion to extract info from all .eml files in the specified directory.'''

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


def ExtractDir(srcdir):
	'''Extracts info from all .eml files in the specified directory.'''

	return ExtractDirHelper(srcdir, [])
	