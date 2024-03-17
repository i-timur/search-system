import os

from sklearn.feature_extraction.text import TfidfVectorizer

from common import parse_document, read_dir, extract_tokens

relative_folder_path = 'downloaded_pages'
folder_path = os.path.abspath(relative_folder_path)

docs = map(lambda doc: parse_document(doc), read_dir(folder_path))

vectorizer = TfidfVectorizer(tokenizer=lambda x: extract_tokens(x))

x = vectorizer.fit_transform(docs)

for idx, tfidf in enumerate(x.toarray()):
    result_terms = ''

    for word, tfidf_word, idf in zip(vectorizer.get_feature_names_out(), tfidf, vectorizer.idf_):
        result_terms += f'{word} {idf} {tfidf_word}\n'

    with open('tf-idf_terms/' + str(idx + 1) + '.txt', 'wt', encoding='utf-8') as file:
        file.write(result_terms)

docs = map(lambda doc: parse_document(doc), read_dir(folder_path))

def process_text(text):
    lemmas = extract_tokens(text, lemmatize=True)
    return ' '.join(lemmas)

vectorizer_lemmas = TfidfVectorizer(preprocessor=process_text, tokenizer=lambda x: extract_tokens(x, lemmatize=True))

x_lemmas = vectorizer_lemmas.fit_transform(docs)

for idx, tfidf in enumerate(x_lemmas.toarray()):
    result_lemmas = ''

    for lemma, tfidf_lemma, idf in zip(vectorizer_lemmas.get_feature_names_out(), tfidf, vectorizer_lemmas.idf_):
        result_lemmas += f'{lemma} {idf} {tfidf_lemma}\n'

    with open('tf-idf_lemmas/' + str(idx + 1) + '.txt', 'wt', encoding='utf-8') as file:
        file.write(result_lemmas)
