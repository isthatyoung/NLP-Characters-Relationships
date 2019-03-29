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
def main():
    dir = "../NLP-project/text_data/"
    raw_text_data = read_file(dir)
    processed_text_data = preprocessing(raw_text_data)
    print(processed_text_data['Harry Potter and the Prisoner of Azkaban'])

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
    for key in data.keys():
        text_of_book = data[key]
        pattern = r'^[¡]*'
        new_sentence = []
        for sentence in text_of_book:
            sentence = sentence.strip('\n')
            sentence = re.sub(pattern, '', sentence)
            new_sentence.append(sentence)

        sentence_word_list = []
        ##Tokenization
        for sentence in new_sentence:
            sentence_word_list.append(word_tokenize(sentence))

        ##Stemming
        new_stemming_sentence_word_list = []
        ps = PorterStemmer()

        for sentence_word in sentence_word_list:
            stemming_words = []
            for word in sentence_word:
                stemming_words.append(ps.stem(word))
            new_stemming_sentence_word_list.append(stemming_words)

        ##Lemmatization
        new_lemmatized_sentence_word_list = []
        lemmatizer = WordNetLemmatizer()

        for sentence_word in new_stemming_sentence_word_list:
            lemmatized_words = []
            for word in sentence_word:
                lemmatized_words.append(lemmatizer.lemmatize(word))
            new_lemmatized_sentence_word_list.append(lemmatized_words)
        processed_data[key] = new_lemmatized_sentence_word_list

    return processed_data








if __name__ == '__main__':
    main()