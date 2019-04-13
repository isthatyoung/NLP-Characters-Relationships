##TODO: 1. Preprocessing raw data
##      2. Format 7 novels in dictionary type
##      3. Sentence segmentation
##      4. Tokenization
##      5. Find name entities
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
from collections import Counter
from tabulate import tabulate
nlp = spacy.load('en_core_web_sm')
import pandas as pd
from pandas.core.frame import DataFrame

def main():
    dir = "../text_data/"
    raw_text_data = read_file(dir)
    data_before_token, processed_text_data = preprocessing(raw_text_data)
    print(processed_text_data['Harry Potter and the Sorcerer Stone'])
    csv_file = Path(dir+'name_count.csv')
    if not csv_file.exists():
        name_counts = list_name_entities(data_before_token)
        name_counts.to_csv(dir+'name_count.csv')
    else:
        name_counts = pd.read_csv(dir+'name_count.csv', header=None)


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
    processed_data = {}
    data_before_token = {}

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    for key in data.keys():
        text_of_book = data[key]
        pattern = r'^[¡]*'
        new_sentence = []

        for sentence in text_of_book:
            sentence = sentence.strip('\n')
            sentence = sentence.strip('\r')
            sentence = re.sub(pattern, '', sentence)
            new_sentence.append(sentence)

        data_before_token[key] = new_sentence

        sentence_word_list = []

        ##Tokenization
        for sentence in new_sentence:
            sentence = re.split('(\.|\?|\!)', sentence)
            sentence_word_list.append(sentence)

        processed_data[key] = sentence_word_list


    return data_before_token, processed_data


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




if __name__ == '__main__':
    main()