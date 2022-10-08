import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import re
from tensorflow import keras
from keras.layers import Dense, GRU, Input, Dropout, Embedding
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from db_data import host, user, password, db_name
import psycopg2

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
try:
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT text FROM news_biznes")
        dat = cursor.fetchall()


    texts_true = []
    texts_false = []
    for i in range(0,20):
        texts_true.append(dat[i])

    texts_true1 = [item for sublist in texts_true for item in sublist]
    for i in range(21,36):
        texts_false.append(dat[i])

    texts_false1 = [item for sublist in texts_false for item in sublist]

    count_true = len(texts_true)
    count_false = len(texts_false)
    total_lines = count_true + count_false
    texts = texts_false1 + texts_true1
    print(count_true, count_false, sep=" ")


    maxWordsCount = 1000
    tokenizer = Tokenizer(num_words=maxWordsCount, filters='!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»', lower=True, split=' ', char_level=False)
    tokenizer.fit_on_texts(texts)

    dist = list(tokenizer.word_counts.items())


    max_text_len = 10
    data = tokenizer.texts_to_sequences(texts)
    data_pad = keras.preprocessing.sequence.pad_sequences(data, maxlen=max_text_len)


    X = data_pad
    Y = np.array([[1, 0]]*count_true + [[0, 1]]*count_false)
    print(Y)

    indeces = np.random.choice(X.shape[0], size=X.shape[0], replace=False)
    X = X[indeces]
    Y = Y[indeces]


    model = Sequential()
    model.add(Embedding(maxWordsCount, 128, input_length = max_text_len))
    model.add(GRU(128, return_sequences=True))
    model.add(GRU(64))
    model.add(Dense(2, activation='softmax'))
    model.summary()

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=Adam(0.0001))

    history = model.fit(X, Y, batch_size=32, epochs=50)

    reverse_word_map = dict(map(reversed, tokenizer.word_index.items()))

    def sequence_to_text(list_of_indices):
        words = [reverse_word_map.get(letter) for letter in list_of_indices]
        return(words)

    for i in range(36, 70):
        t = "".join(dat[i]).lower()
        data = tokenizer.texts_to_sequences([t])
        data_pad = keras.preprocessing.sequence.pad_sequences(data, maxlen=max_text_len)

        res = model.predict(data_pad)
        print(res, np.argmax(res), sep='\n')
        if np.argmax(res) == 0:
            print(t)

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        # cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")