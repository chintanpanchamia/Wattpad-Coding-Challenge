# __author__ = 'chintanpanchamia'
import re
import string
import os
from trie import Trie
import pickle


def get_phrases(file_name):
    """
    :param file_name:
    :return: phrase list for appropriate corpus
    """
    phrases = list()
    with open(file_name, 'r') as f:
        for line in f:
            phrases.append(line.strip().lower())

    return phrases  # return phrase list


def get_pattern(phrase_list):
    """
    :param phrase_list:
    :return: compiled pattern for regex generated by clubbing phrases from the list
    """
    regex = r'\b'
    for phrase in sorted(phrase_list, key=lambda s: -len(s)):
        regex += r'(' + re.escape(phrase) + r')'
        regex += r'|'
    regex = regex[:-1]
    regex += r'\b'

    return re.compile(regex)  # return regex pattern of the format \b(phrase_1)|(phrase_2)|...|(phrase_n)\b


def get_score(filename, low_risk_pattern, high_risk_pattern):
    """
    Version 1, O(n x m x l) n - size of input, m - number of phrases, l - average length of a phrase;
    Time complexity, horribly inefficient
    :param filename:
    :param low_risk_pattern:
    :param high_risk_pattern:
    :return: generate score for input taken from passed file and against compiled patterns for high and low risk words
    """
    content = ''
    with open(filename, 'r') as f:
        for line in f:
            content += line.lower().strip() + ' '
    low_risk_frequency = len(low_risk_pattern.findall(content))  # get number of low-risk phrases matched
    high_risk_frequency = len(high_risk_pattern.findall(content))  # get number of high-risk phrases matched

    return 2 * high_risk_frequency + low_risk_frequency


def get_proper_score(filename, trie):
    """
    Version 2, O(n + lm) n - number of words in input, m - number of phrases, l - number of words in phrase;
    Time complexity
    :param filename:
    :param trie:
    :return: Calculate score of input sentence against generated Trie
    """
    content = list()
    regex = re.compile('[%s]' % re.escape(string.punctuation))  # regex for filtering out all punctuation
    with open(filename, 'r') as f:
        for line in f:
            line = line.lower()
            line = regex.sub('', line)  # removes all punctuation
            content.extend(line.strip().split(' '))  # format input text into a list of words

    pointers = list()  # list of pointers to traverse all possible phrases while iterating over every word of input

    score = 0

    for word in content:
        if trie.has_start(word):
            pointers.append(trie.head)  # add head of Trie if the current word seems to start a potential phrase

        if len(pointers) > 0:
            for j in range(len(pointers)):
                if pointers[j] is None:
                    continue

                if word in pointers[j].children:
                    pointers[j] = pointers[j][word]  # if the phrase continues, add move to current word-node
                    score += pointers[j].score  # and add the score
                else:
                    pointers[j] = None  # else disable that pointer

    return score


def add_phrases_to_trie(trie, phrase_list, score):
    """
    :param trie:
    :param phrase_list:
    :param score:
    :return: Add phrases to generate Trie, along with score used for indicating risk level: i.e. Low/High
    """
    if phrase_list is None or len(phrase_list) is 0:
        raise ValueError('Phrase list cannot be empty')

    for phrase in phrase_list:
        trie.add(phrase, score)  # add phrase to Trie


def save_trie_structure(trie_object, filename):
    """
    :param trie_object:
    :param filename:
    :return: Saves Trie structure generated, at Runtime, to facilitate easy movement of the structure
    """
    with open(filename, 'wb') as save_file:
        pickle.dump(trie_object, save_file, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    low_risk_phrases = get_phrases('Data/low_risk_phrases.txt')  # get phrase lists from files
    high_risk_phrases = get_phrases('Data/high_risk_phrases.txt')
    trie = Trie()  # create a Trie instance
    add_phrases_to_trie(trie, low_risk_phrases, 1)  # load data onto Trie
    add_phrases_to_trie(trie, high_risk_phrases, 2)

    save_trie_structure(trie, 'trie.pkl')  # save the structure for mobility
    filename_regex = r'\b(input(\d+).txt)\b'  # regex to match inputXX.txt filename format
    filename_pattern = re.compile(filename_regex)

    with open('output.txt', 'w') as output:  # write output to this file
        path = './Data/'  # walk in said directory for input files
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                match = filename_pattern.match(filename)  # match to see which file should be processed
                if match is not None:
                    filename = os.path.join(root, filename)
                    output.writelines('{0}:{1}\n'.format(filename, get_proper_score(filename, trie)))


if __name__ == '__main__':
    main()

