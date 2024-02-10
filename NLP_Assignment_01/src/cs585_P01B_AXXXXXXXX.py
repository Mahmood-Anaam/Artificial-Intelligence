
import nltk
from nltk.corpus import brown
from nltk.util import bigrams



# ................................


# Function to looad Data
def looadData():
    nltk.download('brown')


# ................................

# Calculate the probability of a sentence
def calculate_sentence_probability(bigram_model,sentence):
    words = nltk.word_tokenize(sentence)
    bigrams_list = list(bigrams(words))
    sentence_probability = 1.0

    for bigram in bigrams_list:
        probability = calculate_probability(bigram_model,bigram)
        sentence_probability *= probability

    # Assume probability of any bigram starting or ending a sentence is 0.25
    sentence_probability *= 0.25 * 0.25

    return sentence_probability

# ................................

# Calculate the probability of a bigram given its preceding word
def calculate_probability(bigram_model,bigram):
    preceding_word = bigram[0]
    bigram_count = bigram_model[bigram]
    preceding_word_count = bigram_model[preceding_word]
    probability = bigram_count / (preceding_word_count+1)
    return probability


# ................................

def main():
    
    looadData()
    print("\n\n")
    # Ask the user to enter a sentence
    sentence = input("Enter a sentence: ")
    # Apply lowercasing to the sentence
    sentence = sentence.lower()
    
    # Calculate P(S) assuming a 2-gram language model
    corpus_words = brown.words()
    bigram_model = nltk.FreqDist(bigrams(corpus_words))
  
    
    
    # Display the sentence, individual bigrams, and the final probability
    print("\n\n")
    print("Sentence:", sentence)
    print("Individual Bigrams and Probabilities:")

    words = nltk.word_tokenize(sentence)
    bigrams_list = list(bigrams(words))

    for bigram in bigrams_list:
        probability = calculate_probability(bigram_model,bigram)
        print(bigram, "-", probability)

    final_probability = calculate_sentence_probability(bigram_model,sentence)
    print("Final Probability (P(S)):", final_probability)
    
   
    
    print("\n\n ................ End Part (B) ................\n\n")




# ................................

if __name__ == '__main__':
    main()

 
