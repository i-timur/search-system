import collections
import os
from typing import List

import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords


def read_dir(folder_path: str) -> List[str]:
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    txt_files = [f for f in files if f.lower().endswith('.txt')]
    txt_files = sorted(txt_files, key=lambda name: int(name.split('.')[0]))
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
    nltk.download('punkt')
    nltk.download('stopwords')
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words and not any(c.isdigit() for c in word)]

    return filtered_words

def build_inverted_index(terms):
    inverted_index = {}
    for doc_id, term_list in enumerate(terms):
        terms_set = set(term_list)
        for term in terms_set:
            if term in inverted_index:
                inverted_index[term].append(doc_id + 1)
            else:
                inverted_index[term] = [doc_id + 1]

    return inverted_index


def shunting_yard(infix_tokens):
    precedence = {}
    precedence['NOT'] = 3
    precedence['AND'] = 2
    precedence['OR'] = 1
    precedence['('] = 0
    precedence[')'] = 0

    output = []
    operator_stack = []

    for token in infix_tokens:
        if (token == '('):
            operator_stack.append(token)

        elif (token == ')'):
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()

        elif (token in precedence):
            if (operator_stack):
                current_operator = operator_stack[-1]
                while (operator_stack and precedence[current_operator] > precedence[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]

            operator_stack.append(token)  # add token to stack

        else:
            output.append(token.lower())

    while (operator_stack):
        output.append(operator_stack.pop())

    return output


def apply_operator(operator, operands, index_size):
    if operator == 'AND':
        return list(set(operands[0]).intersection(set(operands[1])))
    elif operator == 'OR':
        return list(set(operands[0]).union(set(operands[1])))
    elif operator == 'NOT':
        return list(set(range(1, index_size + 1)).difference(set(operands[0])))
def search(query, inverted_index):
    spaced_query = query.replace('(', '( ')
    spaced_query = spaced_query.replace(')', ' )')
    postfix_query = collections.deque(shunting_yard(spaced_query.split()))

    results_stack = []

    while postfix_query:
        result = []
        token = postfix_query.popleft()

        if (token != 'AND' and token != 'OR' and token != 'NOT'):
            if token in inverted_index:
                result = inverted_index[token]
            else:
                result = []
        elif (token == 'AND'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            result = apply_operator('AND', [left_operand, right_operand], 100)
        elif (token == 'OR'):
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            result = apply_operator('OR', [left_operand, right_operand], 100)
        elif (token == 'NOT'):
            right_operand = results_stack.pop()
            result = apply_operator('NOT', [right_operand], 100)

        results_stack.append(result)

    if len(results_stack) != 1:
        raise ValueError('Invalid query')

    return results_stack.pop()

