import platform
from os import system
import sys
import nltk
from nltk.corpus import brown,reuters,stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import numpy as np
# ................................
stop_words = None

# Function to looad Data
def looadData():
    global stop_words
    nltk.download('brown')
    nltk.download('reuters')
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = set(stopwords.words('english'))

# ................................

# Function to remove stopwords and tokenize the text
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    return [token for token in tokens if token.isalpha() and token not in stop_words]

# ................................

# Function to get the word frequency distribution
def get_word_frequency(corpus):
    word_freq = FreqDist()
    for file_id in corpus.fileids():
        words = preprocess_text(' '.join(corpus.words(file_id)))
        word_freq.update(words)
    return word_freq    
# ................................

# Function to get the word frequency distribution
def displayTopTenWords(name,words_freq):
    print("\n\n\n")
    print(f"Top Ten Words in the {name} Corpus:")
    print("Rank\tWord\t\tFrequency")
    for rank, (word, freq) in enumerate(words_freq.most_common(10), 1):
        print(f"{rank}\t{word}\t\t{freq}")
 
# ................................

# Function to calculate log(rank) and log(frequency) for the first n words
def calculate_log_rank_frequency(words_freq, n=1000):
    sorted_words = words_freq.most_common(n)
    ranks = np.arange(1, n+1)
    frequencies = [count for _, count in sorted_words]
    log_ranks = np.log(ranks)
    log_freqs = np.log(frequencies)
    return log_ranks, log_freqs

# ................................

# Function to calculate unigram occurrence probability
def calculate_unigram_probability(words_freq, word):
    total_words = sum(words_freq.values())
    word_count = words_freq[word.lower()]
    probability = word_count / total_words
    return word_count, total_words, probability

# ................................

# Function to Generate log(rank) vs log(frequency) plots for
# the first 1000 words in Brown Corpus

def generateLogPloting(name, words_freq):
    log_ranks, log_freqs = calculate_log_rank_frequency(words_freq, 1000)
    plt.figure(figsize=(8, 6))
    plt.plot(log_ranks, log_freqs)
    plt.xlabel('log(Rank)')
    plt.ylabel('log(Frequency)')
    plt.title(f'{name} Corpus: log(Rank) vs log(Frequency)')
    plt.show()


# ................................

def main():
    
    looadData()
    # Get word frequency distribution for Brown Corpus
    brown_word_freq = get_word_frequency(brown)

    # Get word frequency distribution for Reuters Corpus
    reuters_word_freq = get_word_frequency(reuters)

    # Display top ten words for both corpora
    displayTopTenWords(name="Brown",words_freq=brown_word_freq)
    displayTopTenWords(name="Reuters",words_freq=reuters_word_freq)
    
    # Generate log(rank) vs log(frequency) plots for the first 1000 words for both corpora
    generateLogPloting(name="Brown",words_freq=brown_word_freq)
    generateLogPloting(name="Reuters",words_freq=reuters_word_freq)
    
    # Calculate unigram occurrence probability for the words 'technical' and 'not technical' in Brown Corpus
    brown_technical = calculate_unigram_probability(words_freq=brown_word_freq, word="technical")
    brown_nottechnical = calculate_unigram_probability(words_freq=brown_word_freq, word="not technical")
    
    # Calculate unigram occurrence probability for the words 'technical' and 'not technical' in Reuters Corpus
    reuters_technical = calculate_unigram_probability(words_freq=reuters_word_freq, word="technical")
    reuters_nottechnical = calculate_unigram_probability(words_freq=reuters_word_freq, word="not technical")
    
    # Display the counts and probabilities for Brown Corpus
    print("\n\n")
    print("\nBrown Corpus:\n")
    print("Word\t\tCount\t\tProbability")
    print("technical\t{}\t\t{:.6f}".format(brown_technical[0], brown_technical[2]))
    print("not technical\t{}\t\t{:.6f}".format(brown_nottechnical[0], brown_nottechnical[2]))
    
    # Display the counts and probabilities for Reuters Corpus
    print("\n\n")
    print("\nReuters Corpus:\n")
    print("Word\t\tCount\t\tProbability")
    print("technical\t{}\t\t{:.6f}".format(reuters_technical[0], reuters_technical[2]))
    print("not technical\t{}\t\t{:.6f}".format(reuters_nottechnical[0], reuters_nottechnical[2]))
    
    print("\n\n ................ End Part (A) ................\n\n")




# ................................

if __name__ == '__main__':
    main()

 
