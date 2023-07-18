import numpy as np 
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
import matplotlib.pyplot as plt
import data

#initial variables:
vocab_size = 5000
max_len = 100
epochs = 143
batch_size = 64
embedding_dim = 1024
hidden_size = 2048

def show_result(callback):

	x = range(0, len(callback.accuracy) ) # [i for i in range(1, len(callback.accuracy) + 1)]
	
	plt.plot(x, callback.accuracy, label="Accuracy")
	plt.legend(loc='best')

	# naming the x axis
	plt.xlabel('Epochs')
	# naming the y axis
	plt.ylabel('Losses')

	plt.show()

class Callback(keras.callbacks.Callback):
	def on_train_begin(self, logs={}):
		self.losses = []
		self.accuracy = []

	def on_epoch_end(self, epoch, logs={}):
		self.losses.append(logs.get('loss'))
		self.accuracy.append(logs.get('accuracy'))
	
def create_model():
	model = Sequential()
	model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
	model.add(GlobalAveragePooling1D())
	model.add(Dense(hidden_size, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))

	model.compile(loss='sparse_categorical_crossentropy', 
				optimizer='adam', metrics=['accuracy'])

	model.summary()
	return model

#get the data from intents.json
_, labels, training_sentences, training_labels = data.get_data()

#process and pad the data
padded_sequences, num_classes, training_labels, tokenizer, lbl_encoder = data.process_data(vocab_size, max_len, labels, training_labels, training_sentences)

#create the model and a callback to show the accuracy on a plot after training
model = create_model()
callback = Callback()

#train the model:
history = model.fit(padded_sequences, np.array(training_labels), batch_size=batch_size, epochs=epochs, callbacks=callback)

#show the plot of epoch to accuracy relation
show_result(callback)

#save the model:
model.save("chat_model")

print("Done")
exit()