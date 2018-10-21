import sys
import re

def locate(file_name):
	loc = []
	with open(file_name) as f:
		for line in f:
			tmp = line.strip()
			loc.append(tmp)
	return loc

arg_len = len(sys.argv)
arg_list = []
for a in range(4, arg_len, 1):
	arg_list.append(sys.argv[a])

lab = ["O","B-PER","I-PER","B-LOC","I-LOC","B-ORG","I-ORG"]
num = ["0","1","2","3","4","5","6"]
label=dict(zip(lab,num))

train_word = []
train_pos = []
training_corpus = []
with open(sys.argv[1]) as f:
	for line in f:
		tmp = line.strip()
		if (tmp):
			tmp1 = tmp.split()
			train_pos.append(tmp1[1])
			train_word.append(tmp1[2])
			training_corpus.append(tmp1)

train_word_uq = set(train_word)
train_word_uq.add('UNK')

train_pos_uq = set(train_pos)
train_pos_uq.add('UNKPOS')

def create_feature(file_name):	 
	feature = {}
	index = 1
	for word in train_word_uq:
		feature["word-"+word] = index
		index += 1
		feature["prev-word-"+word] = index
		index += 1
		feature["next-word-"+word] = index
		index += 1

	feature["prev-word-PHI"] = index
	index += 1
	feature["next-word-OMEGA"] = index
	index += 1

	for pos in train_pos_uq:
		feature["pos-"+pos] = index
		index += 1
		feature["prev-pos-"+pos] = index
		index += 1
		feature["next-pos-"+pos] = index
		index += 1

	feature["prev-pos-PHIPOS"] = index
	index += 1
	feature["next-pos-OMEGAPOS"] = index
	index += 1
	feature["ABBR"] = index
	index += 1
	feature["CAP"] = index
	index += 1
	feature["LOCATION"] = index

	return feature


def abbr(word):
	if (len(word) <= 4):
		if (re.search('[0-9]',word)):
			return 'no'
		elif (re.search('[a-zA-Z]',word)) or (re.search('.',word)):
			if (word.strip()[-1] == '.'):
				return 'yes'
	return 'no'


def cap(word):
	if ((word[0].isupper() == True)):
		return 'yes'
	else:
		return 'no'

def location(loc, word):
	if word in loc:
		return 'yes'
	else:
		return 'no'


def feature_extract_test(stce,loc,feature,readable,vector):
	length = len(stce)
	for i in range(length):
		
		tmp = []	
		cur_word = cur_word1 = stce[i][2]
		cur_pos = stce[i][1]
	
		if cur_word not in train_word_uq:
			cur_word = 'UNK'
		if cur_pos not in train_pos_uq:
			cur_pos = 'UNKPOS'

		if i == 0:
			prev_word = 'PHI'
			prev_pos = 'PHIPOS'
		else:
			prev_word = stce[i-1][2]
			prev_pos = stce[i-1][1]

			if prev_word not in train_word_uq:
				prev_word = 'UNK'
			if prev_pos not in train_pos_uq:
				prev_pos = 'UNKPOS'
		
		if (i == length-1):
			nxt_word = 'OMEGA'
			nxt_pos = 'OMEGAPOS'
		else:
			nxt_word = stce[i+1][2]
			nxt_pos = stce[i+1][1]

			if nxt_word not in train_word_uq:
				nxt_word = 'UNK'
			if nxt_pos not in train_pos_uq:
				nxt_pos = 'UNKPOS'
		
		if 'WORD' in arg_list:
			vector.write("{} ".format(label[stce[i][0]]))
			tmp.append(feature["word-"+cur_word])
			readable.write("WORD: {}\n".format(cur_word))
		else:
			readable.write("WORD: n/a\n")

		if 'WORDCON' in arg_list:
			tmp.append(feature["prev-word-"+prev_word])
			tmp.append(feature["next-word-"+nxt_word])
			readable.write("WORDCON: {} {}\n".format(prev_word, nxt_word))
		else:
			readable.write("WORDCON: n/a\n")
		
		if 'POS' in arg_list:
			tmp.append(feature["pos-"+cur_pos])
			readable.write("POS: {}\n".format(cur_pos))
		else:
			readable.write("POS: n/a\n")
		
		if 'POSCON' in arg_list:
			tmp.append(feature["prev-pos-"+prev_pos])
			tmp.append(feature["next-pos-"+nxt_pos])
			readable.write("POSCON: {} {}\n".format(prev_pos, nxt_pos))
		else:
			readable.write("POSCON: n/a\n")
		
		if 'ABBR' in arg_list:
			if ((abbr(cur_word1)) == "yes"):
				tmp.append(feature["ABBR"])

			readable.write("ABBR: {}\n".format(abbr(cur_word1)))
		else:
			readable.write("ABBR: n/a\n")
		
		if 'CAP' in arg_list:
			if ((cap(cur_word1)) == "yes"):
				tmp.append(feature["CAP"])

			readable.write("CAP: {}\n".format(cap(cur_word1)))
		else:
			readable.write("CAP: n/a\n")
		
		if 'LOCATION' in arg_list:
			if ((location(loc,cur_word1)) == "yes"):
				tmp.append(feature["LOCATION"])

			readable.write("LOCATION: {}\n\n".format(location(loc,cur_word1)))
		else:
			readable.write("LOCATION: n/a\n\n")

		tmp.sort()
		for w in tmp:
			vector.write("{}:{} ".format(w,"1"))

		vector.write("\n")


def feature_extract_train(stce,loc,feature,readable,vector):
	length = len(stce)
	for i in range(length):
		tmp = []		
		cur_word = stce[i][2]
		cur_pos = stce[i][1]
		
		if i == 0:
			prev_word = 'PHI'
			prev_pos = 'PHIPOS'
		else:
			prev_word = stce[i-1][2]
			prev_pos = stce[i-1][1]
		
		if (i == length-1):
			nxt_word = 'OMEGA'
			nxt_pos = 'OMEGAPOS'
		else:
			nxt_word = stce[i+1][2]
			nxt_pos = stce[i+1][1]

		if 'WORD' in arg_list:
			vector.write("{} ".format(label[stce[i][0]]))
			tmp.append(feature["word-"+cur_word])
			readable.write("WORD: {}\n".format(cur_word))
		else:
			readable.write("WORD: n/a\n")

		if 'WORDCON' in arg_list:
			tmp.append(feature["prev-word-"+prev_word])
			tmp.append(feature["next-word-"+nxt_word])
			readable.write("WORDCON: {} {}\n".format(prev_word, nxt_word))
		else:
			readable.write("WORDCON: n/a\n")
		
		if 'POS' in arg_list:
			tmp.append(feature["pos-"+cur_pos])
			readable.write("POS: {}\n".format(cur_pos))
		else:
			readable.write("POS: n/a\n")
		
		if 'POSCON' in arg_list:
			tmp.append(feature["prev-pos-"+prev_pos])
			tmp.append(feature["next-pos-"+nxt_pos])
			readable.write("POSCON: {} {}\n".format(prev_pos, nxt_pos))
		else:
			readable.write("POSCON: n/a\n")
		
		if 'ABBR' in arg_list:
			if ((abbr(cur_word)) == "yes"):
				tmp.append(feature["ABBR"])

			readable.write("ABBR: {}\n".format(abbr(cur_word)))
		else:
			readable.write("ABBR: n/a\n")
		
		if 'CAP' in arg_list:
			if ((cap(cur_word)) == "yes"):
				tmp.append(feature["CAP"])

			readable.write("CAP: {}\n".format(cap(cur_word)))
		else:
			readable.write("CAP: n/a\n")
		
		if 'LOCATION' in arg_list:
			if ((location(loc,cur_word)) == "yes"):
				tmp.append(feature["LOCATION"])

			readable.write("LOCATION: {}\n\n".format(location(loc,cur_word)))
		else:
			readable.write("LOCATION: n/a\n\n")
	
		tmp.sort()
		for w in tmp:
			vector.write("{}:{} ".format(w,"1"))

		vector.write("\n")


def train(file_name,loc,feature):
	with open(file_name) as f:
		sen = []
		read = file_name+".readable"
		f1 = open(read,"w")
		vector = file_name+".vector"
		f2 = open(vector,"w")

		for line in f:
			tmp = line.strip()
			if (len(tmp) != 0):
				new = tmp.split()
				sen.append(new)
			elif (sen):
				feature_extract_train(sen,loc,feature,f1,f2)
				sen = []
		if (sen):
			feature_extract_train(sen,loc,feature,f1,f2)
			sen = []

		f1.close()
		f2.close()


def test(file_name,loc,feature):
	with open(file_name) as f:
		sen = []
		read = file_name+".readable"
		f3 = open(read,"w")
		vector = file_name+".vector"
		f4 = open(vector,"w")

		for line in f:
			tmp = line.strip()
			if (len(tmp) != 0):
				new = tmp.split()
				sen.append(new)
			elif (sen):
				feature_extract_test(sen,loc,feature,f3,f4)
				sen = []
		if (sen):
			feature_extract_test(sen,loc,feature,f3,f4)
			sen = []

		f3.close()
		f4.close()


loc = locate(sys.argv[3])
feature = create_feature(sys.argv[1])
train(sys.argv[1],loc,feature)
test(sys.argv[2],loc,feature)
