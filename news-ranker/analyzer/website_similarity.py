import json


import tensorflow as tf
import itertools
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print ("module %s loaded" % module_url)


def embed(input):
  return model(input)


def plot_similarity(labels, features, rotation):
  corr = np.inner(features, features)
  sns.set(font_scale=1.2)
  g = sns.heatmap(
      corr,
      xticklabels=labels,
      yticklabels=labels,
      vmin=0,
      vmax=1,
      cmap="YlOrRd")
  g.set_xticklabels(labels, rotation=rotation)
  g.set_title("Semantic Textual Similarity")
  plt.show()
  import pdb
  pdb.set_trace()


def run_and_plot(messages_):
  message_embeddings_ = embed(messages_)
  plot_similarity(messages_, message_embeddings_, 90)


def average_similarity(messages1, messages2):
    corr = np.corrcoef(messages1, messages2)
    return np.average(corr)


def find_similarity(message1, message2):
    message1_encoded = embed(message1)
    message2_encoded = embed(message2)
    return average_similarity(message1_encoded, message2_encoded)


def calc_all_similarities():
    with open('../data/extracted_headlines.json') as f:
        data = json.load(f)
    keys = list(data.keys())
    similarity_matrix = np.zeros((len(keys), len(keys)))
    for i in range(len(keys)):
        for j in range(len(keys)):
            similarity_matrix[i][j] = find_similarity(data[keys[i]], data[keys[j]])
    print(similarity_matrix)


calc_all_similarities()