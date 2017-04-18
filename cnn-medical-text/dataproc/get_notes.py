"""
    This script reads in the csv exported from MySQL containing notes for all patients.
    First, it reads in the file containing the SUBJECT_IDs of all patients that had at least one top 10 (or top 100) ICD9 code.
    Then, for each row in the notes database with a qualifying subject ID:
    It tokenizes the words, removes all non-alphanumeric tokens, removes all completely numeric tokens, and removes stop words
    It then writes the result, with just the subject ID and notes, to a new output file.
"""

import csv
import os
import sys

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from constants import DATA_DIR

stop_words = stopwords.words('english')
#retain only alphanumeric
tokenizer = RegexpTokenizer(r'\w+')

def main(Y):
    subjects = set([])
    print("getting the list of relevant subjects")
    with open('%s/patients_%s.csv' % (DATA_DIR, Y), 'r') as csvfile:
        patientreader = csv.reader(csvfile)
        next(patientreader)
        for line in patientreader:
            subjects.add(int(line[0]))

    print("processing notes file")
    with open('%s/NOTEEVENTS.csv' % (DATA_DIR), 'r') as csvfile:
        with open('%s/notes_%s.csv' % (DATA_DIR, Y), 'w') as outfile:
            print("writing to %s/notes_%s.csv" % (DATA_DIR, Y))
            outfile.write(','.join(['SUBJECT_ID', 'HADM_ID', 'CHARTTIME', 'TEXT']) + '\n')
            notereader = csv.reader(csvfile)
            next(notereader)
            i = 0
            for line in notereader:
                if i % 10000 == 0:
                    print(i)
                subj = int(line[1])
#                hadm = int(line[2])
                if subj in subjects:
                    #probably okay to normalize to lowercase. medical terms written in lowercase.
                    note = unicode(line[10])
                    tokens = [t.lower() for t in tokenizer.tokenize(note) if not t.isnumeric() and t.lower() not in stop_words]
                    text = '"' + ' '.join(tokens) + '"'
                    if i % 10000 == 0:
                        print(text[:80])
                    outfile.write(','.join([line[1], line[2], line[4], text]) + '\n')
                i += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python " + str(os.path.basename(__file__) + " [|Y|]"))
        sys.exit(0)
    main(sys.argv[1])