import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import json
import pickle
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import numpy as np

#initialize -----
lemmatizer = WordNetLemmatizer()
list_of_words=[]
documents = []
classes = []
ignore_list = ['?', '[', ':', ';', '!']
data_file = open('intents.json').read()
intents = json.loads(data_file)

#get list of classes  -----
def compileClassList(pattern):
    word = nltk.word_tokenize(pattern)
    list_of_words.extend(word)
    documents.append((word, intent['tag']))
    if intent['tag'] not in classes:
        classes.append(intent['tag'])

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize words, add documents and get classes and add it to list -----
        compileClassList(pattern)


list_of_words = [lemmatizer.lemmatize(word.lower()) for word in list_of_words if word not in ignore_list]
list_of_words = sorted(list(set(list_of_words)))
classes = sorted(list(set(classes)))
pickle.dump(list_of_words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))


# initialize training data  -----
training = []
value = [0] * len(classes)

def initializeTrainingdata():     
    for document in documents:
        # initializing bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern = document[0]
        # lemmatize each word - create base word, in attempt to represent related words
        pattern = [lemmatizer.lemmatize(word.lower()) for word in pattern]
        # create our bag of words array with 1, if word match found in current pattern
        for word in list_of_words:
            bag.append(1) if word in pattern else bag.append(0)

        # output is a '0' for each tag and '1' for current tag (for each pattern)
        output_row = list(value)
        output_row[classes.index(document[1])] = 1

        training.append([bag, output_row])
        
initializeTrainingdata()


# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training Done, data has been created")

def createCovBotModel():
    # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
    # equal to number of intents to predict output intent with softmax
    training_covbot_model = Sequential()
    training_covbot_model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    training_covbot_model.add(Dropout(0.5))
    training_covbot_model.add(Dense(64, activation='relu'))
    training_covbot_model.add(Dropout(0.5))
    training_covbot_model.add(Dense(len(train_y[0]), activation='softmax'))
    # Compile training_covbot_model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this training_covbot_model
    sgd_nag = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    training_covbot_model.compile(loss='categorical_crossentropy', optimizer=sgd_nag, metrics=['accuracy'])
    #fitting and saving the training_covbot_model
    hist = training_covbot_model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
    training_covbot_model.save('covbot_model.h5', hist)   


createCovBotModel()
print("created succesfully....")

