import os

from common import build_inverted_index, parse_document, read_dir, extract_tokens, search

print(f'Введите запрос:')
query = input()

relative_folder_path = 'downloaded_pages'
folder_path = os.path.abspath(relative_folder_path)

docs = map(lambda doc: parse_document(doc), read_dir(folder_path))
terms = list(map(lambda doc: map(lambda token: token.lower(), extract_tokens(doc)), docs))

inverted_index = build_inverted_index(terms)

result = search(query, inverted_index)

print('Результат булевого поиска:', result)
