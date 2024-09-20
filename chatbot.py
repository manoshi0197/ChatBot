# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 20:20:48 2021

@author: Manas Chamola
"""

import nltk
import numpy as np
import random
import string

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# file=open('chatbot.txt','r',errors = 'ignore')
# raw_data=file.read()
# raw_data=raw_data.lower()
with open('chatbot.txt','r',errors = 'ignore') as file:
    raw_data = file.read().lower()
nltk.download('punkt')
nltk.download('wordnet')
sent_tk = nltk.sent_tokenize(raw_data)
word_tk = nltk.word_tokenize(raw_data)

# lemma = nltk.stem.WordNetLemmatizer()

# def LemmaTokens1(tokens):
#     return [lemma.lemmatize(token) for token in tokens]
# remove_punct = dict((ord(punct), None) for punct in string.punctuation)
# def LemmaNormalize(txt):
#     return LemmaTokens1(nltk.word_tokenize(txt.lower().translate(remove_punct)))

def lemma_tokens(tokens):
    lem = WordNetLemmatizer()
    return [lem.lemmatize(token) for token in tokens]
def lemma_normalize(txt):
    remove_punct = dict((ord(punct), None) for punct in string.punctuation)
    tokens = word_tokenize(txt.lower().translate(remove_punct))
    return lemma_tokens(tokens)

GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREET_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

vectorizer = TfidfVectorizer().fit_transform(GREET_INPUTS)
# def greeting(sentence):
 
#     for word in sentence.split():
#         if word.lower() in GREET_INPUTS:
#             return random.choice(GREET_RESPONSES)

def greeting(sentence):
    """
    This function takes a sentence as input and checks if any of the words in the sentence are a greeting.
    If a greeting is found, a random greeting response is returned.
    """
    input_vector = vectorizer.transform([sentence.lower()])
    similarities = np.asarray(input_vector.dot(vectorizer.T).todense())[0]
    closest_greeting_idx = np.argmax(similarities)
    if similarities[closest_greeting_idx] > 0.5:
        return GREET_RESPONSES[closest_greeting_idx]
    else:
        return None
    
    # first_word = sentence.split()[0].lower()
    # if first_word in GREET_INPUTS:
    #     return random.choice(GREET_RESPONSES)
        
def response(user_response):
    rob_resp=''
    sent_tk.append(user_response)
    TfidfVector = TfidfVectorizer(tokenizer=lemma_normalize, stop_words='english')
    tfidfVec = TfidfVector.fit_transform(sent_tk)
    vals_list = cosine_similarity(tfidfVec[-1], tfidfVec)
    index=vals_list.argsort()[0][-2]
    flat_result = vals_list.flatten()
    flat_result.sort()
    req_tfidf_result = flat_result[-2]
    if(req_tfidf_result==0):
        rob_resp=rob_resp+"I am Sorry, but i didn't understand what you are saying."
        return rob_resp
    else:
        rob_resp = rob_resp+sent_tk[index]
        return rob_resp

"""   
flag=True
print("COV19ROB: Hi! My name is COV19ROB. I will answer your queries about Covid-19. If you want to exit, type Quit!")
while(flag==True):
    usr_response = input()
    usr_response=usr_response.lower()
    if(usr_response!='quit'):
        if(usr_response=='thanks' or usr_response=='thank you' ):
            flag=False
            print("COV19ROB: You are welcome..")
        else:
            if(greeting(usr_response)!=None):
                print("COV19ROB: "+greeting(usr_response))
            else:
                print("COV19ROB: ",end="")
                print(response(usr_response))
                sent_tk.remove(usr_response)
    else:
        flag=False
        print("COV19ROB: Bye! take care..")
"""
