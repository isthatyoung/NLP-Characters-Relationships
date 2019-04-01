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
    # books = list(raw_text_data.keys())
    data_before_token, processed_text_data = preprocessing(raw_text_data)
    csv_file = Path(dir+'name_count.csv')
    if not csv_file.exists():
        name_counts = list_name_entities(data_before_token)
        name_counts.to_csv(dir+'name_count.csv')
    else:
        name_counts = pd.read_csv(dir+'name_count.csv', header=None)
    combine_entities(name_counts)





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

    #tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

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
            sentence_word_list.append(word_tokenize(sentence))

        processed_data[key] = sentence_word_list

        # for paragraph in text_of_book:
        #     paragraph = re.sub(pattern, '', paragraph)
        #     new_paragraph += paragraph
        #
        #
        # sentences = tokenizer.tokenize(new_paragraph)
        # print(sentences)
        #
        # for sentence in sentences:
        #     new_sentence.append(sentence.strip('\n'))
        # processed_data[key] = new_sentence

        # sentence_word_list = []
        # ##Tokenization
        # for sentence in new_sentence:
        #     sentence_word_list.append(word_tokenize(sentence))
        #
        # ##Stemming
        # new_stemming_sentence_word_list = []
        # ps = PorterStemmer()
        #
        # for sentence_word in sentence_word_list:
        #     stemming_words = []
        #     for word in sentence_word:
        #         stemming_words.append(ps.stem(word))
        #     new_stemming_sentence_word_list.append(stemming_words)
        #
        # ##Lemmatization
        # new_lemmatized_sentence_word_list = []
        # lemmatizer = WordNetLemmatizer()
        #
        # for sentence_word in new_stemming_sentence_word_list:
        #     lemmatized_words = []
        #     for word in sentence_word:
        #         lemmatized_words.append(lemmatizer.lemmatize(word))
        #     new_lemmatized_sentence_word_list.append(lemmatized_words)
        # processed_data[key] = new_lemmatized_sentence_word_list

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

def combine_entities(series):
    character_dictionary = {}
    names = series[0].values
    counts = series[1].values
    length = len(names)
    # for i in range(30):
    #     for j in range(31,length):
    #         if names[i] in names[j] or names[j] == names[i]+"'s" or names[j] == 'Dear ' + names[i]:
    #             counts[i] += counts[j]
    # new_name_counts = {"names":names, "counts":counts}
    # new_name_counts = DataFrame(new_name_counts)
    # print(new_name_counts)
    f = open('../character_dictionary_data/Character_Names.txt')
    text = f.readlines()
    for character in text:
        character = character.strip('\n')
        character = character.strip('\t')
        character_dictionary[character] = 0
    for i in range(length):
        for character in character_dictionary.keys():
            if names[i] in character:
                new_count = character_dictionary[character] + counts[i]
                character_dictionary[character] = new_count
    print(sorted(character_dictionary.items(), key=lambda item:item[1], reverse=True))














if __name__ == '__main__':
    main()