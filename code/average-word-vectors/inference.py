from concurrent.futures import ThreadPoolExecutor
import json
import re

from gensim import models
import numpy as np


#  TODO: Can we load this outside of handler to persist between lambda invocations when possible
print("Loading GloVe model")
MODEL = models.KeyedVectors.load_word2vec_format("s3://gensim/models/glove-wiki-gigaword-300.txt")
print("GloVe model loaded")


def clean_word(word):
    """Clean a word by removing unnecessary characters."""
    return re.sub(r'[^a-zA-Z0-9]', '', word)


def get_word_vector(word):
    """Retrieve the vector for a given word from the model."""
    try:
        return MODEL.get_vector(word)
    except KeyError:
        return None


def process_word(word):
    """Process a single word: clean, split, and get vectors for sub-words."""
    sub_words = re.split(r'[_\-\s]', word)
    cleaned_sub_words = [clean_word(sub_word) for sub_word in sub_words if sub_word]
    vectors = []

    for sub_word in cleaned_sub_words:
        vec = get_word_vector(sub_word)
        if vec is not None:
            vectors.append(vec)

    if len(vectors) == 0:
        return None
    if len(vectors) == 1:
        return vectors[0]
    if len(vectors) > 1:
        return np.mean(vectors, axis=0)


def get_average_word_vector(word_list):
    """
    Get the average vector for a list of words.

    :param word_list: list of words
    :return: average vector of the words in the list
    """

    with ThreadPoolExecutor() as executor:
        # Parallelize the processing of words
        all_vectors = list(executor.map(process_word, word_list))

    # Flatten the list of lists and filter out any empty lists
    vectors = [vec for vec in all_vectors if isinstance(vec, np.ndarray) and vec.size > 0]

    if vectors:
        average_vector = np.mean(vectors, axis=0)
        return average_vector.tolist()
    else:
        return  None
