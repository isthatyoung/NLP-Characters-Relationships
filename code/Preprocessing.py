##TODO: 1. Preprocessing raw data
##      2. Format 7 novels in dictionary type
##      3. Sentence segmentation
##      4. Tokenization
##      5. Find name entities
##      6. Analyze words and unique words in every books
##      6. Analyze top 30 characters by occurrence count

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import chardet
import re
import os
import json
from pathlib import Path
import spacy
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from tabulate import tabulate
nlp = spacy.load('en_core_web_sm')
import pandas as pd
from pandas.core.frame import DataFrame

def main():
    dir = "../text_data/"
    raw_text_data = read_file(dir)
    processed_text_data = preprocessing(raw_text_data)
    book_analysis(processed_text_data)
    #print(processed_text_data['Harry Potter and the Sorcerer Stone'])
    csv_file = Path(dir+'name_count.csv')
    if not csv_file.exists():
        name_counts = list_name_entities(processed_text_data)
        name_counts.to_csv(dir+'name_count.csv')
    else:
        name_counts = pd.read_csv(dir+'name_count.csv', header=None)
    analyze_subject_object(processed_text_data)



def read_file(dir):
    json_file = Path('{}Raw-Harry-Potter-Series.json'.format(dir))
    book = {}
    if not json_file.exists():
        files = []
        pattern = '\.txt'
        for readfile in os.listdir(dir):
            if re.search(pattern, readfile):
                files.append(readfile)
        pattern = '(.+)\..+$'
        for file_name in files:
            decode_text = []
            with open(dir + file_name, 'rb') as f_read:
                text = f_read.readlines()
                for line in text:
                    type = chardet.detect(line)
                    line = line.decode(type["encoding"])
                    decode_text.append(line)

                file_name = re.findall(pattern, file_name)[0]
                book[file_name] = decode_text
            f_read.close()

        ##TODO:Save book to json file
        with open(dir + 'Raw-Harry-Potter-Series.json', 'a') as outfile:
            json.dump(book, outfile, ensure_ascii=False)
            outfile.write('\n')
    else:
        readfile = open('{}Raw-Harry-Potter-Series.json'.format(dir),"r")
        book = eval(readfile.read())

    return book


def preprocessing(data):

    data_into_sentences = {}

    for key in data.keys():
        text_of_book = data[key]

        pattern = r'^[¡]*'

        all_paragraph = []
        for para in text_of_book:
            para = para.strip('\n')
            para = re.sub(pattern, '', para)
            all_paragraph.append(para)

        all_sentence = []
        for i in all_paragraph:
            for j in sent_tokenize(i):
                all_sentence.append(j)

        data_into_sentences[key] = all_sentence

    return data_into_sentences

def book_analysis(data):
    ps = PorterStemmer()
    total_word_count = []
    total_unique_word_count = []
    book_title = ['Harry Potter and the Sorcerer Stone', 'Harry Potter and The Chamber Of Secrets', 'Harry Potter and the Prisoner of Azkaban',
                  'Harry Potter and the Goblet of Fire', 'Harry Potter and the Order of the Phoenix', 'Harry Potter and The Half-Blood Prince',
                  'Harry Potter and the Deathly Hallows']

    for i in range(len(book_title)):
        text = data[book_title[i]]
        str_text = ''
        for sentence in text:
            str_text += sentence.lower()
        word_count = len(str_text.split())
        unique_word_count = len(set(ps.stem(word) for word in str_text.split()))

        total_word_count.append(word_count)
        total_unique_word_count.append(unique_word_count)

    print("Total words:{}".format(total_word_count))
    print("Total unique words {}".format(total_unique_word_count))

    plt.figure(1)
    ind = np.arange(len(book_title))
    width = 0.35
    plt.bar(ind - width/2, total_word_count, width, color='SkyBlue', label='total words')
    plt.bar(ind + width/2, total_unique_word_count, width, color='IndianRed', label = 'unique words')
    plt.ylabel('Total number of words')
    plt.xlabel('Harry Potter series')
    plt.xticks(ind, [1,2,3,4,5,6,7])
    plt.legend(loc="best")
    plt.title('Total words count of Harry Potter series')
    plt.show()



def list_name_entities(data):
    unique_name = set()
    name_entities = []
    for key in data.keys():
        text = data[key]
        for sentence in text:
            doc = nlp(sentence)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    unique_name.add(ent.text)
                    name_entities.append(ent.text)

    name_counts = pd.value_counts(name_entities)
    print(name_counts)
    return name_counts

def analyze_subject_object(data):
    content_json = []
    verse = 0
    book_title = ['Harry Potter and the Sorcerer Stone', 'Harry Potter and The Chamber Of Secrets', 'Harry Potter and the Prisoner of Azkaban',
                  'Harry Potter and the Goblet of Fire', 'Harry Potter and the Order of the Phoenix', 'Harry Potter and The Half-Blood Prince',
                  'Harry Potter and the Deathly Hallows']
    #print(data[book_title[6]])
    final_data = []
    for i in range(len(book_title)):
        text = data[book_title[i]]
        for sentence in text:
            verse = verse + 1
            chunk = {"book_id": i+1}
            chunk["text"] = sentence
            chunk["verse"] = verse
            content_json.append(chunk)

    for i in range(len(content_json)):
        final_data.append(content_json[i]["text"])












if __name__ == '__main__':
    main()