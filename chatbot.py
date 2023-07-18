import numpy as np
from tensorflow import keras
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import wikipediaapi
import random
import data

#initial variables:
max_len = 100
vocab_size = 5000

#download stopwords and sentence splitter:
nltk.download('stopwords')
nltk.download('punkt')

wiki_wiki = wikipediaapi.Wikipedia('de')
stop_words = set(stopwords.words('german'))
stop_words.remove("wie")

#load the model:
model = keras.models.load_model('chat_model')

jsondata, labels, training_sentences, training_labels = data.get_data()
padded_sequences, num_classes, training_labels, tokenizer, lbl_encoder = data.process_data(vocab_size, max_len, labels, training_labels, training_sentences)

def search_wikipedia(topic):
    page_py = wiki_wiki.page(topic)
    summary =  page_py.summary
    return summary if len(summary) < 200 else '. '.join(nltk.sent_tokenize(summary)[:3])

def hasKeyword(sequence):
    return "<" in sequence and ">" in sequence

def executeSequence(input_sequence, question):
    if "<CURRENT_TIME>" in input_sequence:
        time = datetime.now()
        return input_sequence.replace("<CURRENT_TIME>", time.strftime("%H:%M"))
    elif "<CURRENT_DATE>" in input_sequence:
        date = datetime.now()
        return input_sequence.replace("<CURRENT_DATE>", date.strftime("%d.%m.%Y"))
    elif "<WEATHER>" in input_sequence:
        return input_sequence.replace("<WEATHER>", "Not implemented yet...")
    elif "<GOOGLE>" in input_sequence:
        query = question.lower().replace('google', '')
        if len(query) > 0:
            return f"Ich habe folgendes gefunden: {search_wikipedia(query)}"
        return None
    return input_sequence

def preprocess_question(question):
	#remove stopwords:
	question = ' '.join([word for word in word_tokenize(question) if word.lower() not in stop_words])
	#replace german characters:
	question = question.lower().replace("ö", "oe").replace("ü", "ue").replace("ä", "ae").replace("ß", "ss")
	return question

def chat(question):    
    
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([preprocess_question(question)]),
                                            truncating='post', maxlen=max_len))
    confidence = np.max(result)
    if confidence < 0.3:
        return random.choice(["Entschuldigung, da kann ich dir leider nicht helfen.", "Sorry keine Ahnung, was du meinst", "Da kann ich dir nicht helfen", "Das check ich nicht"])
	
    tag = lbl_encoder.inverse_transform([np.argmax(result)])
    print(f"Tag: {tag}")

    for i in jsondata['intents']:
        if i['tag'].lower() == tag:
            sequence = np.random.choice(i['responses'])
            if hasKeyword(sequence):
                return executeSequence(sequence, question)
            return sequence
    return "NULL"