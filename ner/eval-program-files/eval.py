import sys
import numpy as np

def prediction(file_name):
	with open(file_name) as f:
		predict = f.read().splitlines()			

	return predict
			

def gold(file_name):
	with open(file_name) as f:
		gold = f.read().splitlines()			
	
	return gold 


def create_entity(data, label):
	entity = []
	t1 = label.split('-')
	nxt_label ="I-"+t1[1]

	for i in range(len(data)):
		tmp = data[i][1].split()
		tag = tmp[0]
		name = tmp[1]

		if tag == label:
			temp=[]
			flag=1
			temp.append(name)
			start = data[i][0]
			end = data[i][0]
			j = i+1

			while(flag == 1 and j < len(data)):
				tmp2 =data[j][1].split()
				tag1 = tmp2[0]

				if tag1 == nxt_label:
					temp.append(tmp2[1])
					end = data[j][0]
				else:
					flag=0
				j=j+1 

			word = " ".join(temp)
			index = "".join(['[',str(start),'-',str(end),']'])
			last = "".join([word,index])
			entity.append(last)	
	return entity 

numerator = []
pr_list = []
re_list = []
f = open("eval.txt","w")
def compare(predict, gold, label):
	final = []
	count = 0
		
	t1 = label.split('-')
	tag = t1[1]
	
	for item in predict:
		if item in gold:
			final.append(item)
			count += 1

	numerator.append(count)
	
	precision = len(predict)
	pr_list.append(precision) 
	
	recall = len(gold)
	re_list.append(recall) 
	
	if len(final)!=0:
		tmp = " | ".join(final)
		f.write("Correct {} = {}".format(tag, tmp))
		f.write('\n')
	else:
		f.write("Correct {} = {}".format(tag, "NONE"))
		f.write('\n')

	if recall !=0:
		tmp = "".join([str(count),'/',str(recall)])
		f.write("Recall {} = {}".format(tag, tmp))
		f.write('\n')
	else:
		f.write("Recall {} = {}".format(tag, "n/a"))
		f.write('\n')

	if precision !=0:
		tmp = "".join([str(count),'/',str(precision)])
		f.write("Precision {} = {}".format(tag, tmp))
		f.write('\n')
	else:
		f.write("Precision {} = {}".format(tag, "n/a"))
		f.write('\n')
		
	f.write('\n')	
	return(numerator, pr_list, re_list)	

		

label = ["B-PER","B-LOC","B-ORG"]

predict = prediction(sys.argv[1])
pre_list = list(enumerate(predict, 1))

gold = gold(sys.argv[2])
gold_list = list(enumerate(gold, 1))

for i in label:
	ret1 = create_entity(pre_list, i)
	ret2 = create_entity(gold_list, i)
	n, p, r = compare(ret1, ret2, i)


tmp = "".join([str(sum(n)),'/',str(sum(r))])
f.write("Average Recall = {}".format(tmp))
f.write('\n')

tmp = "".join([str(sum(n)),'/',str(sum(p))])
f.write("Average Precision = {}".format(tmp))
f.write('\n')

f.close()
