import os
from typing import List

from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def read_dir(folder_path: str) -> List[str]:
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    txt_files = [f for f in files if f.lower().endswith('.txt')]
    result = []
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            result.append(file.read())

    return result

def parse_document(text: str) -> str:
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text(separator=' ')

def extract_tokens(text: str) -> List[str]:
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words and not any(c.isdigit() for c in word)]

    return filtered_words


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
