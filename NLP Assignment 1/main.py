import nltk
import re
import random

from nltk.corpus import brown

nltk.download('brown')

def remove_special_chars(string:str)->str:
    cleaned_text = re.sub('[^A-Za-z0-9\s\']+', ' ', string)
    cleaned_text = re.sub(r'\'{2,}', ' ', cleaned_text)
    return cleaned_text

def limit_spaces(string:str)->str:
    cleaned_text = re.sub(r'\s{2,}', ' ' , string)
    return cleaned_text

def preprocess(string:str)->str:
    cleaned_text = remove_special_chars(string)
    cleaned_text = limit_spaces(cleaned_text)
    return cleaned_text

def tokenize(corpus:str):
    corpus_tokens = list(set(corpus.split(' ')))
    return corpus_tokens

def max_probability(current_prob , current_val , best_prob , best_val):
    if current_prob > best_prob:
        best_prob = current_prob
        best_val = current_val
    return best_prob , best_val

def n_gram_generator(n_gram:int , sentence_max_len:int ,  corpus:str, tokens:list , corpus_1d_list:list):
    num_random_words = n_gram-1
    sent = []

    n_gram_model = {}

    random_choice = random.randint(0 , len(corpus_1d_list))
    for index in range(num_random_words):
        sent.append(corpus_1d_list[random_choice + index])

    while(len(sent) < sentence_max_len):
        best_prob = 0
        best_prob_value = ""

        key = sent[-num_random_words:]
        values = []

        denominator = ' '.join(key)
        for token in tokens:
            numerator = denominator + ' ' + token + ' '
            probability = corpus.count(numerator) / corpus.count(denominator)

            best_prob , best_prob_value =  max_probability(probability  , token , best_prob , best_prob_value)

            if probability:
                values.append(probability) 

        n_gram_model[denominator] = values
        sent.append(best_prob_value)
        
    return ' '.join(sent) , n_gram_model


def main():
    sentences = brown.sents()
    limiter = 1000
    # input 
    max_sentences_count = int(input("Number of Sentences: "))

    n_gram = int(input("Enter 2 for bigram or 3 for trigram: "))
    if n_gram < 2 or n_gram > 3:
        print("invalid input")
        return

    sentence_max_len = int(input("Max number of words: "))

    # corpus = input("Enter your Corpus Sentences")

    corpus_string = ""
    for sent in sentences[:limiter]:
        corpus_string = corpus_string + " ".join(sent) + " "
    corpus_string = corpus_string.removesuffix(' ')

    corpus_string = preprocess(corpus_string.lower())
    # print(corpus_string)

    tokens = tokenize(corpus_string)
    corpus_1d_list = corpus_string.split(' ')
    
    for index in range(max_sentences_count):
        output_sentence , n_gram_model= n_gram_generator(n_gram , sentence_max_len , corpus_string , tokens , corpus_1d_list)  
        print(f"Sentence {index}: {output_sentence}")
        # print(f"N-gram Model: {n_gram_model}")

if __name__ == "__main__":
    main()