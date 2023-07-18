import json
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from sklearn.preprocessing import LabelEncoder

def get_data():
	with open('intents.json') as file:
		jsondata = json.load(file)
    
	training_sentences = []
	training_labels = []
	labels = []

	for intent in jsondata['intents']:
		for pattern in intent['patterns']:
			training_sentences.append(pattern.lower())
			training_labels.append(intent['tag'].lower())

		if intent['tag'] not in labels:
			labels.append(intent['tag'].lower())

	return jsondata, labels, training_sentences, training_labels

def process_data(vocab_size, max_len, labels, training_labels, training_sentences):
	num_classes = len(labels)

	lbl_encoder = LabelEncoder()
	lbl_encoder.fit(training_labels)
	training_labels = lbl_encoder.transform(training_labels)

	tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
	tokenizer.fit_on_texts(training_sentences)
	sequences = tokenizer.texts_to_sequences(training_sentences)
	padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

	return padded_sequences, num_classes, training_labels, tokenizer, lbl_encoder
