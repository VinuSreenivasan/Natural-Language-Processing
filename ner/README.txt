Language:
------------------
Programming language used - python2


File details:
------------------
1. 'ner-input-files/ner.py' is the python program file for named entity recognition.

2. 'eval-program-files/eval.py' is the python program file for evaluation.

3. 'liblinear-1.93' directory has the compiled ML software.

4. 'ner-trace-files' directory has the given trace files.

5. 'my-trace-files' directory contains the sample trace files generated for all the features "WORD WORDCON POS POSCON ABBR CAP LOCATION"



Running Method
-----------------

a) For named entity recognition, please run in following format inside 'ner-input-files' directory.

	python ner.py train.txt test.txt locs.txt WORD WORDCON POS POSCON ABBR CAP LOCATION
	
	../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier

	../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy.txt

The above comments will generate following files,

	train.txt.readable
	test.txt.readable
	train.txt.vector
	test.txt.vector
	classifier
	predictions.txt
	accuracy.txt

b) For evaluation, please run in following format inside 'eval-program-files' directory.

	python eval.py prediction.txt gold.txt

The above comment will generate the following file,

	eval.txt



Machine used:
--------------
CADE machine used for testing 'lab1-1.eng.utah.edu'
