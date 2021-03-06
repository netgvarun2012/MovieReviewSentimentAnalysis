# -*- coding: utf-8 -*-
"""IMDB Review Webpage.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15KBORrStpxu5iKrjU5XnAwAjksNU3ONo
"""
 
#pip install GitPython
#git.Repo.clone_from(
  #  'https://github.com/gitpython-developers/GitPython',
 #   './git-python
#git clone --depth 1 -b v2.3.0 https://github.com/tensorflow/models.git

# install requirements to use tensorflow/models repository
#pip install -Uqr models/official/requirements.txt
# you may have to restart the runtime afterwards

#pip install flask-ngrok

import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import logging
from tensorflow.keras.models import load_model

import sys
sys.path.append('models')
import official.nlp.data.classifier_data_lib
import official.nlp.bert.tokenization
import official.nlp.optimization

from google.colab import drive
drive.mount('/content/gdrive')

"""
Each line of the dataset is composed of the review text and its label
- Data preprocessing consists of transforming text to BERT input features:
input_word_ids, input_mask, segment_ids
- In the process, tokenizing the text is done with the provided BERT model tokenizer
"""

 # Label categories
 # 1 - Insincere Question
 # 0 - Sincere Question
label_list = [0,1]


 # maximum length of (token) input sequences
max_seq_length = 128
train_batch_size = 32



# Get BERT layer and tokenizer:
# More details here: https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4
bert_layer = hub.KerasLayer('https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2', trainable=True) # Meaning, We want to 'fine-tune' by training the last layer for our custom usecase.

# Each bert layer has a number of attributes:
vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy() # We wil use this variable at later time (number of unique words in our dictionary/vocabulary).
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy() # We can indicate if the Model is case-sensitive or not using this parameter.
tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case) # Tokenizer is an object that is responsible for generation of embeddings for 'raw input text'.

# This provides a function to convert raw text into those 3 arrays that are described above.
# Uses tokenizer which we created above.
# Uses classifier_data_lib class from Tensorflow.

def to_feature(text, label, label_list=label_list, max_seq_length=max_seq_length, tokenizer=tokenizer):
  example = classifier_data_lib.InputExample(guid=None,               # We don't need 'guid' i.e. unique id for input.
                                             text_a = text.numpy(),   # We pass raw text.
                                             text_b = None,           # Not required since We are using Masked Language Model (MLM). 
                                             label = label.numpy())   # We also pass labels.

  feature = classifier_data_lib.convert_single_example(0, example, label_list, max_seq_length, tokenizer) # Will give a feature tuple with 3 outputs as described earlier.
  return (feature.input_ids, feature.input_mask, feature.segment_ids, feature.label_id)

def to_feature_map(text, label):
  input_ids, input_mask, segment_ids, label_id = tf.py_function(to_feature, inp=[text,label], Tout=[tf.int32, tf.int32, tf.int32, tf.int32])
  input_ids.set_shape([max_seq_length])
  input_mask.set_shape([max_seq_length])
  segment_ids.set_shape([max_seq_length])
  label_id.set_shape([])
  x = {'input_words_ids' : input_ids,
       'input_mask': input_mask,
       'input_type_id': segment_ids
       }  
  return (x, label_id)

model = load_model("/content/gdrive/MyDrive/IMDBPredictions/IMDB_Predict.h5",custom_objects={'KerasLayer': hub.KerasLayer})

model.summary()

from flask import Flask, request, jsonify, url_for, render_template
import uuid
from flask_ngrok import run_with_ngrok
from flask import Flask
app = Flask(__name__,template_folder='/content/gdrive/MyDrive/IMDBPredictions/templates',
            static_folder='/content/gdrive/MyDrive/IMDBPredictions/static')
run_with_ngrok(app)   #starts ngrok when the app is run

Expected = {
    "Review":{"min":1,"max":2000}
}

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/')
def indexes():
  
  return render_template('MovieReview.html')


@app.route('/submitted', methods=['POST'])
def submitted():
  sys.stdout.flush()
  content = request.form['text']
  errors = []
  app.logger.debug('I am inside submitted')

  sample_example = [content]
  test_data = tf.data.Dataset.from_tensor_slices((sample_example, [1]*len(sample_example)))
  test_data = test_data.map(to_feature_map).batch(1)
  preds = model.predict(test_data)
  threshold = 0.5
  prediction = ['POSITIVE' if pred >= threshold else 'NEGATIVE' for pred in preds]

  return render_template('MovieReview.html',prediction= 'Movie review is '+ prediction[0] )

app.run(debug=True)

