#!/usr/bin/env python

import sys
import base64
import cPickle as pickle
#from mrjob.job import MRJob
import numpy as np

def main():

	tp=0
	tn=0
	fn=0
	fp=0
	count2 = 0
	old_key = 0
	classes_pos_list = []
	classes_neg_list = []
	accuracy_list = []
	omegalist = []
	gammalist = []

	for line in sys.stdin:
	
		line = line.strip()	
		line = line.replace('[', '')
		line = line.replace(']', '')	
		line = line.split('$')
		
		#print line
		
		key = int(line[0])
		#print key
		
		if(key == old_key):
		
			tp = tp + int(line[3])
			fp = fp + int(line[4])
			fn = fn + int(line[5])
			tn = tn + int(line[6])
			x =line[1]
			y=line[2]
			
			om = line[7]
			gam = line[8]
			old_key = key
			#print tp,fp,fn,tn
	
		else:
			omegalist.append(om)
			gammalist.append(gam)
			
			classes_pos_list.append(x)
			x = classes_pos_list[-1]		
			x = x.replace('\'', '')
			x = x.replace(' ', '')
			classes_pos_list[-1] = x
			classes_neg_list.append(y)
			x = classes_neg_list[-1]		
			x = x.replace('\'', '')
			x = x.replace(' ', '')
			classes_neg_list[-1] = x
			if (tp==0 and fp ==0):
				precision = 0.0
			else:
				precision = float(tp)/(tp+fp)
			if (tp==0 and fn ==0):
				recall = 0.0
			else:			
				recall = float(tp)/(tp+fn)

 			if (precision ==0.0 and recall ==0.0):
				f1measure = 0
			else:	
				f1measure = 2*precision*recall/(precision+recall)
			accuracy = float(tp+tn)/(tp+tn+fn+fp)
			
			accuracy_list.append(str(accuracy))
			#print line[1], line[2], precision, recall, f1measure, accuracy
			tp=0
			tn=0
			fn=0
			fp=0
			tp = tp + int(line[3])
			fp = fp + int(line[4])
			fn = fn + int(line[5])
			tn = tn + int(line[6])
			x = line[1]
			y=line[2]
			om = line[7]
			gam = line[8]
			#print tp,fp,fn,tn
			old_key = key			
			
			
		
	omegalist.append(om)
	gammalist.append(gam)
	classes_pos_list.append(x)
	x = classes_pos_list[-1]		
	x = x.replace('\'', '')
	x = x.replace(' ', '')
	classes_pos_list[-1] = x
	classes_neg_list.append(y)
	x = classes_neg_list[-1]		
	x = x.replace('\'', '')
	x = x.replace(' ', '')
	classes_neg_list[-1] = x
	if (tp==0 and fp ==0):
		precision = 0.0
	else:
		precision = float(tp)/(tp+fp)
	if (tp==0 and fn ==0):
		recall = 0.0
	else:			
		recall = float(tp)/(tp+fn)
	if (precision ==0.0 and recall ==0.0):
		f1measure = 0
	else:	
		f1measure = 2*precision*recall/(precision+recall)
	accuracy = float(tp+tn)/(tp+tn+fn+fp)

	accuracy_list.append(str(accuracy))
	#print accuracy_list, omegalist, gammalist
	max=0
	index = 0

	for i in range(len(accuracy_list)):
		accuracy_list[i] = float(accuracy_list[i])
		if(accuracy_list[i]>max):
			max=accuracy_list[i]
			index = i

	print classes_pos_list[index], classes_neg_list[index], accuracy_list[index], omegalist[index].split("#"), gammalist[index]		
	
	
	
	
main()
