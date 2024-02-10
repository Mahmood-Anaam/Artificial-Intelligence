
import nltk
from nltk.corpus import brown, stopwords
from nltk.util import ngrams



# ................................
stop_words = None
corpus = None
sentence = None

# Function to init program
def init():
    global stop_words,corpus
    nltk.download('brown')
    stop_words = set(stopwords.words('english'))
    corpus_words = brown.words()
    corpus = [w.lower() for w in corpus_words if w.isalpha() and w.lower() not in stop_words]
    print("\n\n")
    
# ................................


# Function to ask the user for initial word/token W1
def initialWord():
    word = ""
    while True:
        word = input("Enter an initial word/token: ").lower()
        if word not in corpus:
            choice = input("The word is not in the corpus. Do you want to try again? (Y/N): ")
            choice = choice.lower()
            if choice == 'n':
                quit()
        else:
            break
    return word
            
# ................................
# Function to reutern 3 words to follow word
def get_next_words(word):
    ngram_freq = nltk.FreqDist(ngrams(corpus, 2))
    possible_next_words = [ngram[1] for ngram in ngram_freq if ngram[0] == word]
    sorted_next_words = sorted(possible_next_words, key=lambda next_word: ngram_freq[(word, next_word)], reverse=True)[:3]
    probabilities = {}
    for i, next_word in enumerate(sorted_next_words):
        prob = ngram_freq[(word,next_word)] / len(possible_next_words)
        probabilities[next_word] = prob
         
    return probabilities

# ................................

def main():
    
    # init program
    init()
    global sentence
    
    # Ask the user for initial word/token W1
    word = initialWord()
    sentence = [word]

    
    while True:
        next_words = get_next_words(word.lower())
        next_words_keys = list(next_words.keys())

        print("\nWhich word should follow:")
        for i, w in enumerate(next_words_keys):
            print("{}) {} P({} {}) = {:.6f}".format(i+1,w,word,w,next_words[w]))
        print(f"{len(next_words)+1}) QUIT")
        
        choice = input("Enter your choice: ")  
        if choice == str(len(next_words) + 1):
            break
        
        elif choice.isdigit() and 1 <= int(choice) <= len(next_words):
            word = next_words_keys[int(choice) - 1]
            sentence.append(word)
        
        else:
            word = next_words_keys[0]
            sentence.append(word)
    
    print("\nFinal Sentence:", ' '.join(sentence))
            
    print("\n\n ................ End Part (C) ................\n\n")




# ................................

if __name__ == '__main__':
    main()

 
