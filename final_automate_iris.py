import os


########################## first time run  ##########################################

print ("*** FIRST TIME RUN STARTING . . . ")

os.system("python /home/aditi/SVM_iris/cases.py 3 1 2 3")
os.system("rm -rf posneg_queue")
os.system("rm -rf final_result")

os.system("hadoop fs -rmr /user/hduser/iris_training.data")


# ^^^^^^^^^^^^^ path change required here^^^^^^^^^^^^^^^^^^^^^^^
# %%%%%%%%%%%%% input dataset can be changed here %%%%%%%%%%%%%%%%%%%%
os.system("hadoop fs -copyFromLocal /home/aditi/SVM_iris/iris_training2.data /user/hduser/iris_training.data")

print ("### TEST DATA COPIED")
#copying cases and data file to hdfs
os.system("hadoop fs -rmr /user/hduser/cases.txt")

# ^^^^^^^^^^^^^ path change required here^^^^^^^^^^^^^^^^^^^^^^^
os.system("hadoop fs -copyFromLocal /home/aditi/SVM_iris/cases.txt /user/hduser/")
print ("*** CASES.TXT COPIED TO HDFS")

print ("*** removing previous output directories")
os.system("hadoop fs -rmr /user/hduser/multi_output")
os.system("hadoop fs -rmr /user/hduser/multi_acc8")


print ("### TRAINING PART 1 RUNNING . . .")

# ^^^^^^^^^^^^^ 4 path changes required here^^^^^^^^^^^^^^^^^^^^^^^
# @@@@@@@@@@@@@ For multinode cluster, change 'localhost' to name of Master node here @@@@@@@@@@@@@@@@@@
os.system("bin/hadoop jar contrib/streaming/hadoop-*streaming*.jar -file /home/aditi/SVM_iris/test.py    -mapper /home/aditi/SVM_iris/test.py -file /home/aditi/SVM_iris/test_reducer.py    -reducer /home/aditi/SVM_iris/test_reducer.py -cacheFile 'hdfs://localhost:54310/user/hduser/cases.txt#cases.txt' -input /user/hduser/iris_training.data -output /user/hduser/multi_output")



print ("*** TRAINING PART 2 RUNNING . . .")

# ^^^^^^^^^^^^^ 4 path changes required here^^^^^^^^^^^^^^^^^^^^^^^
# @@@@@@@@@@@@@ For multinode cluster, change 'localhost' to name of Master node here (2 changes) @@@@@@@@@@@@@@@@@@
os.system("bin/hadoop jar contrib/streaming/hadoop-*streaming*.jar -file /home/aditi/SVM_iris/svm_test.py    -mapper /home/aditi/SVM_iris/svm_test.py -file /home/aditi/SVM_iris/svm_test_reducer.py    -reducer /home/aditi/SVM_iris/svm_test_reducer.py -cacheFile 'hdfs://localhost:54310/user/hduser/multi_output/part-00000#SVMvalues.txt' -cacheFile 'hdfs://localhost:54310/user/hduser/cases.txt#cases.txt' -input /user/hduser/iris_training.data -output /user/hduser/multi_acc8")


os.system("rm -rf part-00000")
os.system("bin/hadoop fs -copyToLocal /user/hduser/multi_acc8/part-00000 /usr/local/hadoop")



f = open("part-00000", "r")
words = f.read()
words = words.strip()
words = words.replace("[", "")
words = words.replace("]", "")
words = words.replace("'", "")
words = words.split()
posclass = words[0].split(",")

negclass = words[1].split(",")

index = 1

print ("### First Enqueue operation to pos neg file queue ")

#writing to posneg queue file ----------------------------------
f1 = open("posneg_queue","a")
if (len(posclass) > 1):
	
	f1.write(str(index)+","+"p")
	for x in posclass:
		f1.write(","+x)
	f1.write(",\n")


if (len(negclass) > 1):
	f1.write(str(index)+","+"n")
	for x in negclass:
		f1.write(","+x)
	f1.write(",\n")


#os.system("cat posneg_queue")

print ("Appending Content to Final_result")

#final result --------------------------------------------------- appending
f2 = open("final_result","a")
f2.write(str(index)+","+"p")
for x in posclass:
	f2.write(","+x)
f2.write("$")


f2.write(str(index)+","+"n")
for x in negclass:
	f2.write(","+x)
f2.write("$")

f2.write(words[2].replace(",", "")+"$"+words[3].replace(",", "")+"$"+words[4].replace(",", "")+"$"+words[5].replace(",", "")+"$"+words[6].replace(",", "")+"$"+words[7].replace(",", "")+"\n")

f.close()
f1.close()
f2.close()
#---------------------------------------

print ("******************** FIRST RUN OVER *********************************")

############################# first time run end ####################################


print ("@@@@@@@@@@@@@@@ WHILE RUN STARTS @@@@@@@@@@@@@@@@@@@@@@@")

i=0
while (1):
	i = i+1
	print ("----------------- Loop Run No ------"+ str(i) +"-----------")
	#dequeue business --------------------------------

	print ("************** Deque Operation performing . . . *******************")
	with open('posneg_queue', 'r') as fin:
	    data = fin.read().splitlines(True)
	if(not data):
		print ("!!!!!!!!!!! Nothing to Dequeue , Voila Process Done ! !!!!!!!!!!!!")
		break
	

	with open('posneg_queue', 'w') as fout:
	    if(len(data)==1 ):
	    	fout.truncate()
	    else:
	    	fout.writelines(data[1:])

	tocases = data[0].split(",")
	tocases1 = tocases[2:-1]
	argument = ""
	for k in tocases1:
		argument += " "+ k

	#-------------------------------------
	print ("$$$$$$$$$$$$$ Calculating Node Number $$$$$$$$$$$$$$$")
	#set index
	if (tocases[1]=='p'):
		index = int(tocases[0])*2
	if (tocases[1]=='n'):
		index = (int(tocases[0])*2)+1

	print ("______________ Running Cases .py _________________________")
	
	# ^^^^^^^^^^^^^ path change required here^^^^^^^^^^^^^^^^^^^^^^^
	os.system ("python /home/aditi/SVM_iris/cases.py "+ str(len(tocases1)) + argument )

	os.system("hadoop fs -rmr /user/hduser/cases.txt")
	
	# ^^^^^^^^^^^^^ path change required here^^^^^^^^^^^^^^^^^^^^^^^
	os.system("hadoop fs -copyFromLocal /home/aditi/SVM_iris/cases.txt /user/hduser/")
	print ("*** CASES.TXT COPIED TO HDFS")

	print ("*** removing previous output directories")
	os.system("hadoop fs -rmr /user/hduser/multi_output")
	os.system("hadoop fs -rmr /user/hduser/multi_acc8")



	print ("### TRAINING PART 1 RUNNING . . .")


	# ^^^^^^^^^^^^^ 4 path changes required here^^^^^^^^^^^^^^^^^^^^^^^
	# @@@@@@@@@@@@@ For multinode cluster, change 'localhost' to name of Master node here @@@@@@@@@@@@@@@@@@
	os.system("bin/hadoop jar contrib/streaming/hadoop-*streaming*.jar -file /home/aditi/SVM_iris/test.py    -mapper /home/aditi/SVM_iris/test.py -file /home/aditi/SVM_iris/test_reducer.py    -reducer /home/aditi/SVM_iris/test_reducer.py -cacheFile 'hdfs://localhost:54310/user/hduser/cases.txt#cases.txt' -input /user/hduser/iris_training.data -output /user/hduser/multi_output")


	print ("### TRAINING PART 2 RUNNING . . .")

	
	# ^^^^^^^^^^^^^ 4 path changes required here^^^^^^^^^^^^^^^^^^^^^^^
	# @@@@@@@@@@@@@ For multinode cluster, change 'localhost' to name of Master node here (2 changes) @@@@@@@@@@@@@@@@@@
	os.system("bin/hadoop jar contrib/streaming/hadoop-*streaming*.jar -file /home/aditi/SVM_iris/svm_test.py    -mapper /home/aditi/SVM_iris/svm_test.py -file /home/aditi/SVM_iris/svm_test_reducer.py    -reducer /home/aditi/SVM_iris/svm_test_reducer.py -cacheFile 'hdfs://localhost:54310/user/hduser/multi_output/part-00000#SVMvalues.txt' -cacheFile 'hdfs://localhost:54310/user/hduser/cases.txt#cases.txt' -input /user/hduser/iris_training.data -output /user/hduser/multi_acc8")
	

	os.system("rm -rf part-00000")
	os.system("bin/hadoop fs -copyToLocal /user/hduser/multi_acc8/part-00000 /usr/local/hadoop")

	f = open("part-00000", "r")
	words = f.read()
	words = words.strip()
	words = words.replace("[", "")
	words = words.replace("]", "")
	words = words.replace("'", "")
	words = words.split()
	posclass = words[0].split(",")
	
	negclass = words[1].split(",")

	#writing to posneg queue file ----------------------------------
	f1 = open("posneg_queue","a")
	if (len(posclass) > 1):
		print ("### Pos Class Enqueue operation")
		
		f1.write(str(index)+","+"p")
		for x in posclass:
			f1.write(","+x)
		f1.write(",\n")

	if (len(negclass) > 1):
		print ("### Neg Class Enqueue operation")
		f1.write(str(index)+","+"n")
		for x in negclass:
			f1.write(","+x)
		f1.write(",\n")


	#os.system("cat posneg_queue")


	print ("^^^^^^^^^^^^ Appending Result to final_result ^^^^^^^^^^^^^^^^^^^^^^")
	#final result --------------------------------------------------- appending
	f2 = open("final_result","a")
	f2.write(str(index)+","+"p")
	for x in posclass:
		f2.write(","+x)
	f2.write("$")


	f2.write(str(index)+","+"n")
	for x in negclass:
		f2.write(","+x)
	f2.write("$")

	f2.write(words[2].replace(",", "")+"$"+words[3].replace(",", "")+"$"+words[4].replace(",", "")+"$"+words[5].replace(",", "")+"$"+words[6].replace(",", "")+"$"+words[7].replace(",", "")+"\n")

	f.close()
	f1.close()
	f2.close()
	print (" ---------------------- While Lopp No -----------"+ str(i) +"------------- ENDS") 
	

os.system("python testing_automation_iris.py")
