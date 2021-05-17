import pandas as pd
import re
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt


my_path = "/Users/david/Dropbox/Computing/Linux/Python/fitzgap_data/website/"

my_columns = [
    "relationship_status",
    "brief_outline_hope",
    "gender_identity",
    "brief_outline_history",
]


data = pd.read_csv(my_path + "saved_data.csv", dtype=str, usecols=my_columns)


stop_words_file = my_path + "stopwords_list.txt"
stop_words = []
with open(stop_words_file, "r") as f:
    for line in f:
        stop_words.extend(line.split())
stop_words = stop_words

# stop_words = set(stopwords.words("english"))
# word_tokens = word_tokenize(example_sent)


def preprocess(raw_text):

    # regular expression keeping only letters
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split into words -> convert string into list ( 'hello world' -> ['hello', 'world'])
    words = letters_only_text.lower().split()

    cleaned_words = []
    lemmatizer = (
        PorterStemmer()
    )  # plug in here any other stemmer or lemmatiser you want to try out

    # remove stopwords
    for word in words:
        if word not in stop_words:
            cleaned_words.append(word)

    # stemm or lemmatise words
    stemmed_words = []
    for word in cleaned_words:
        word = lemmatizer.stem(
            word
        )  # dont forget to change stem to lemmatize if you are using a lemmatizer
        stemmed_words.append(word)

    # converting list back to string
    return " ".join(stemmed_words)


def plot_wordcloud(select_col, output_file):
    data["prep"] = select_col.apply(preprocess)
    # data["prep"] = data["brief_outline_hope"].apply(preprocess)

    # data["prep1"] = data["brief_outline_hope"].apply(preprocess)
    # data["prep2"] = data["brief_outline_history"].apply(preprocess)
    # data["prep3"] = data["gender_identity"].apply(preprocess)

    from collections import Counter

    Counter(" ".join(data["prep"]).split()).most_common(10)

    # nice library to produce wordclouds

    all_words = ""

    # looping through all incidents and joining them to one text, to extract most common words
    for arg in data["prep"]:

        tokens = arg.split()

        all_words += " ".join(tokens) + " "

    wordcloud = WordCloud(
        width=700, height=700, background_color="white", min_font_size=10
    ).generate(all_words)

    # plot the WordCloud image
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(my_path + "fgap_website_text_" + output_file + ".png")
    # plt.show()


data["brief_outline_hope"] = data["brief_outline_hope"].astype(
    str
)  # which will by default set the length to the max len it encounters
data["gender_identity"] = data["gender_identity"].astype(str)
data["brief_outline_history"] = data["brief_outline_history"].astype(str)

plot_wordcloud(data["brief_outline_hope"], "hope")
plot_wordcloud(data["brief_outline_history"], "history")
plot_wordcloud(data["gender_identity"], "gid")


from nltk.util import ngrams

#  n_gram = 2
#  n_gram_dic = dict(Counter(ngrams(all_words.split(), n_gram)))
#
#  for i in n_gram_dic:
#      if n_gram_dic[i] >= 2:
#          print(i, n_gram_dic[i])