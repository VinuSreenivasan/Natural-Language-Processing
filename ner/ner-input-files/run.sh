#!/bin/bash

python ner.py train.txt test.txt locs.txt WORD
../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier
../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy1.txt
python ner.py train.txt test.txt locs.txt WORD WORDCON
../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier
../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy2.txt
python ner.py train.txt test.txt locs.txt WORD POS
../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier
../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy3.txt
python ner.py train.txt test.txt locs.txt WORD POSCON
../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier
../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy4.txt
python ner.py train.txt test.txt locs.txt WORD ABBR
../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier
../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy5.txt
python ner.py train.txt test.txt locs.txt WORD CAP
../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier
../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy6.txt
python ner.py train.txt test.txt locs.txt WORD LOCATION
../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier
../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy7.txt
python ner.py train.txt test.txt locs.txt WORD WORDCON POS POSCON ABBR CAP LOCATION
../liblinear-1.93/train -s 0 -e 0.0001 train.txt.vector classifier
../liblinear-1.93/predict test.txt.vector classifier predictions.txt > accuracy8.txt

echo "----------------WORD------------------"
cat accuracy1.txt
echo "--------------WORDCON-----------------"
cat accuracy2.txt
echo "----------------POS-------------------"
cat accuracy3.txt
echo "--------------POSCON------------------"
cat accuracy4.txt
echo "----------------ABBR------------------"
cat accuracy5.txt
echo "----------------CAP-------------------"
cat accuracy6.txt
echo "-------------LOCATION-----------------"
cat accuracy7.txt
echo "----------------ALL-------------------"
cat accuracy8.txt
