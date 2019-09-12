# -*- coding: utf-8 -*-
"""
Spyder Editor
Author: Sammed Mandape
Purpose: This python code will find UMIs given primers, read1(fastq)
and read2(fastq) as inputs. 
This is a temporary script file.
"""

import os
import time
import re
#import sys
#import pandas as pd
#from pytidyverse import *
#from dplython import (DplyFrame, X, diamonds, select, sift, sample_n, sample_frac, head, arrange, mutate, group_by, summarize, DelayFunction)

#remember to change directory
os.chdir("C:\\Users\\snm0205\\Desktop\\UMI\\Run2_10ng_8samples_300cycles")
# define an empty dictionary for primers
dict_primer = {}

#input primer file
file_primer = "Primers_hg38_26.txt"
dict_for_primer(file_primer, dict_primer)
#print(dict_primer.keys())

#define an empty dictionary for Read1 fastq   
dict_fastq_R1 = {}
dict_fastq_R2 = {}

#input Read1 fastq file
file_fastq_R1 = "20251-10_S1_L001_R1_001.fastq"
file_fastq_R2 = "20251-10_S1_L001_R2_001.fastq"
dict_for_fastq(file_fastq_R1, dict_fastq_R1)
dict_for_fastq(file_fastq_R2, dict_fastq_R2)

#function that takes in a primer file and an empty dictionary and returns 
#dictionary with chr-pos as key and primer as value
def dict_for_primer(file_primer, dict_primer_empty):
    if not file_primer:
        raise SystemError("Error: Specify primer file name\n")
    with open(file_primer, 'r') as fh_primer:
        for line in fh_primer:
            (key, val) = line.split()
            dict_primer_empty[key] = val

#function that takes in a fastq file and an empty dictionary and returs
#dictionary with seqid as key and seq as values
def dict_for_fastq(file_fastq, dict_fastq_empty):
    if not file_fastq:
        raise SystemError("Error: Specify fastq file name\n")
    n = 4
    with open(file_fastq, 'r') as fh:
         lines = []
         #count = 0
         for line in fh:
             lines.append(line.rstrip())
             if len(lines) == n:
                 #count += 1
                 ks = ['name', 'sequence', 'optional', 'quality']
                 record = {k: v for k, v in zip(ks, lines)}
                 #sys.stderr.write("Record: %s\n" % (str(record)))
                 #print(record['name'],record['sequence'])
                 dict_fastq_empty[record['name'].split(' ')[0]] = record['sequence']
                 lines = []
                 #print(count)
         return dict_fastq_empty
                



start = time.time()
counterCS_P = 0
counterCS = 0
counter_noCS_match = 0
#notMatchcount = 0
#for j in dict_fastq_R1:
#    for k in dict_fastq_R2:
#        if (j.split(' ')[0] == k.split(' ')[0]):
#            count += 1
#            #print (count, j.split(' ')[0])
#            break
#        else:
#            notMatchcount += 1


#def getKeysByVal(dictofElements):
#    listofItems = dictofElements.items()
#    for item in listofItems:

# CS ATTGGAGTCCT
UmiList = []
LociList = []
for key in set(dict_fastq_R1) & set(dict_fastq_R2):
    readR1 = dict_fastq_R1[key]
    readR2 = dict_fastq_R2[key]
    if re.match(r'(^.{12})ATTGGAGTCCT', readR2):
        counterCS += 1
        for items in dict_primer.items():
            if re.search(items[1], readR1):
                LociPrimer = items[0]
                #R1 = readR1
                #R2 = readR2
                Primer = items[1]
                searchCS = re.match(r'(^.{12})(ATTGGAGTCCT)', readR2)
                UMI = searchCS.group(1)
                CommSeq = searchCS.group(2)
                #print (LociPrimer, UMI, CommSeq)
                counterCS_P += 1
    else:
        counter_noCS_match += 1
        #if readR1.find(items[1]) != -1:
            #count += 1
            #print (items[1])
           
        
        
end = time.time()
print(end-start)
#print(notMatchcount)
print("Counter for CS = %d and counter for Primer = %d and counter for no CS match = %d" % (counterCS, counterCS_P, counter_noCS_match))

        