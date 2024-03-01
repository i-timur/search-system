import os

from common import read_dir, extract_tokens, parse_document, build_inverted_index

relative_folder_path = 'downloaded_pages'
folder_path = os.path.abspath(relative_folder_path)

docs = map(lambda doc: parse_document(doc), read_dir(folder_path))
terms = list(map(lambda doc: map(lambda token: token.lower(), extract_tokens(doc)), docs))

inverted_index = build_inverted_index(terms)

with open('inverted_index.txt', 'w', encoding='utf-8') as file:
    for term, doc_ids in inverted_index.items():
        file.write(f'{term} {" ".join(map(str, doc_ids))}\n')
