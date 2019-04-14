import pandas as pd
import wordcloud
import matplotlib.pyplot as plt

def main():
    dir = '../text_data/name_count.csv'
    df = pd.read_csv(dir,header=None)
    names = df[0][:30].values
    counts = df[1][:30].values
    wordcount = {}
    w = wordcloud.WordCloud(max_font_size=100, max_words=30, background_color="white")
    text = ''
    for i in range(len(names)):
        wordcount[names[i]] = counts[i]
    w.generate_from_frequencies(wordcount)
    plt.figure()
    plt.imshow(w, interpolation='bilinear')
    plt.axis("off")
    plt.show()
main()