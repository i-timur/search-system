import os

import nltk
from nltk.stem import WordNetLemmatizer

from common import parse_document, read_dir, extract_tokens

nltk.download('wordnet')

relative_folder_path = 'downloaded_pages'
folder_path = os.path.abspath(relative_folder_path)

docs = map(lambda doc: parse_document(doc), read_dir(folder_path))

tokens = list(set(extract_tokens(' '.join(docs))))

with open('tokens.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(tokens))

lemmatizer = WordNetLemmatizer()

grouped_tokens = {}
for token in tokens:
    lemmatized_token = lemmatizer.lemmatize(token)
    if lemmatized_token not in grouped_tokens:
        grouped_tokens[lemmatized_token] = []
    grouped_tokens[lemmatized_token].append(token)

with open('lemmatized_tokens.txt', 'w', encoding='utf-8') as file:
    for lemma, tokens in grouped_tokens.items():
        file.write(f'{lemma} {" ".join(tokens)}\n')
