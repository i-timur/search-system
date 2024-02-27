import os

from lemmatize import read_dir, extract_tokens


def build_inverted_index(terms):
    inverted_index = {}
    for doc_id, term_list in enumerate(terms):
        for term in term_list:
            if term in inverted_index:
                inverted_index[term].append(doc_id)
            else:
                inverted_index[term] = [doc_id]
    return inverted_index

relative_folder_path = 'downloaded_pages'
folder_path = os.path.abspath(relative_folder_path)

docs = map(read_dir(folder_path))
