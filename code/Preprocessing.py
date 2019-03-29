import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import chardet
import re
import os
def main():
    dir = "../text_data/"
    raw_text_data = read_file(dir)
    processed_text_data = preprocessing(raw_text_data)
  

def read_file(dir):
    files = []
    book = {}
    pattern = '\.txt'
    for f in os.listdir(dir):
        if re.search(pattern,f):
            files.append(f)
    pattern = '(.+)\..+$'
    for file_name in files:
        decode_text = []
        with open(dir+file_name, 'rb') as f_read:
            text = f_read.readlines()
            for line in text:
                type = chardet.detect(line)
                line = line.decode(type["encoding"])
                decode_text.append(line)
            file_name = re.findall(pattern,file_name)[0]
            book[file_name] = decode_text
        f_read.close()
    return book

def preprocessing(data):
    processed_data = {}
    for key in data.keys():
        text_of_book = data[key]
        # sentences = sent_tokenize(text_of_book)
        pattern = r'^[¡]*'
        new_sentence = []
        for sentence in text_of_book:
            sentence = sentence.strip('\n')
            sentence = re.sub(pattern, '', sentence)
            new_sentence.append(sentence)
        sentence_word_list = []
        for sentence in new_sentence:
            sentence_word_list.append(word_tokenize(sentence))
        processed_data[key] = sentence_word_list
    return processed_data





if __name__ == '__main__':
    main()