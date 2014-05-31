#!/usr/bin/env python

import sys
import base64
import cPickle as pickle
#from mrjob.job import MRJob
import numpy as np

def main():
	#f1 = open("/home/aditi/Downloads/SVM_MR/Snabler-master/psvm/testdata.txt")
	f = open('SVMvalues.txt', 'r')
	f2 = open('cases.txt', 'r')
	omatrixList = []
	gammaList =[]

	pos_class_list = []
	neg_class_list = []
	count =0
	
	cases = f2.readlines()
		
	for line in f:
		current_case = cases[count]
		count+=1
		line = line.strip()
				
		line = line.replace('[', '')
		line = line.replace(']', '')		
		svm = line.split('$')
		#print svm
		
		
		current_case = current_case.strip()
		
		class_t = current_case.split('\t',1)
		class_t[0]=class_t[0].rstrip(',')
        	class_t[1]=class_t[1].rstrip(',')
       		#print class_t
        	class_1 = str(class_t[0]).split(',',1000)
        	class_2 = str(class_t[1]).split(',',1000)			
		#print "line_in",line_in
		pos_class_list.append(class_1)
		neg_class_list.append(class_2)
		
		omega = svm[:-1]
		omegalist=[]
		for o in omega:
			o=float(o)
			omegalist.append(o)
			#print "omegalist ", omegalist
	
		O = np.matrix(np.reshape(np.array(omegalist),(1, len(omegalist))))
		omatrixList.append(O)
		#print "Omega", O
		gamma = svm[-1]
		gamma=float(gamma)
		gammaList.append(gamma)
		tp=0
		tn=0
		fp=0
		fn=0
		#G = np.matrix(np.reshape(np.array(gamma),(1, len(gamma))))
	
	#print "count", count
	classifyList = []
	tplist = [0] * count 
	fplist = [0] * count
	fnlist = [0] * count
	tnlist = [0] * count
	
	for line in sys.stdin:
	


		#print "A", A
		for i in range(len(omatrixList)):
			
			flag = check_if_belongs_to_category(line, pos_class_list[i], neg_class_list[i])
			
			if flag>0:
						
				category,features = transform_input(line,pos_class_list[i],neg_class_list[i])

				num_training_features = len(features)
				#print num_training_features
		   		A = np.matrix(np.reshape(np.array(features),(1, num_training_features)))
				
				classify = A * omatrixList[i].T - gammaList[i]
				classifyList.append(classify)

				for c in classify:
					if(float(c)>0 and category > 0):
						#tp+=1
						tplist[i]+=1
					if(float(c)>0 and category < 0):
						#fp+=1
						fplist[i]+=1
					if(float(c)<0 and category > 0):
						#fn+=1
						fnlist[i]+=1	
					if(float(c)<0 and category < 0):
						#tn+=1
						tnlist[i]+=1 
			else:
				continue
		
	#print classifyList	
	for x in range(len(tplist)):
		print x,"$", pos_class_list[x],"$", neg_class_list[x],"$", tplist[x],"$",fplist[x],"$", fnlist[x],"$", tnlist[x], "$", "#".join(str(omatrixList[x].tolist()).split(',')), "$", gammaList[x]
	
	
		
def check_if_belongs_to_category(line, neg, pos):
	array = line.split(',')
	categ = array[-1].strip()
	category = map_category(categ)
	if category in pos or category in neg:
		#print category
		return category
	else:
		#print 0
		return 0


def map_category(category):
	if (category == 'Iris-setosa'):
		return '1'
	elif (category == 'Iris-versicolor'):
		return '2'
	else:
		return '3'
		
		
def numerify_feature(feature):
    if feature == '?':
        feature = 0.0
    return float(feature)

def extract_features(array):
    features = array[0:-1]
    return [numerify_feature(f) for f in features]

def extract_category(array, neg, pos):
    categ = array[-1].strip()
    category = map_category(categ)
    if category in neg: 
	return -1.0 
    elif category in pos:  
	return 1.0
    else: 
	return 0

def transform_input(value,pos,neg):
    array = value.split(',')
    features = extract_features(array)
    category = extract_category(array, neg, pos)
    return(category, features)
		
		
main()
