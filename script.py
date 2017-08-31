# __author__ = 'chintanpanchamia'
import re
import os


def get_phrases(file_name):
    """
    :param file_name:
    :return: phrase list for appropriate corpus
    """
    phrases = []
    with open(file_name, 'r') as f:
        for line in f:
            phrases.append(line.strip().lower())

    return phrases


# compile pattern for regex generated from all phrases in the list
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

    return re.compile(regex)


# generate score for input taken from passed file and against compiled patterns for high and low risk words
def get_score(filename, low_risk_pattern, high_risk_pattern):
    content = ''
    with open(filename, 'r') as f:
        for line in f:
            content += line.lower().strip() + ' '
    low_risk_frequency = len(low_risk_pattern.findall(content))
    high_risk_frequency = len(high_risk_pattern.findall(content))

    return 2 * high_risk_frequency + low_risk_frequency


# main function
def main():
    low_risk_phrases = get_phrases('low_risk_phrases.txt')
    high_risk_phrases = get_phrases('high_risk_phrases.txt')

    low_risk_phrases_pattern = get_pattern(low_risk_phrases)
    high_risk_phrases_pattern = get_pattern(high_risk_phrases)

    filename_regex = r'\b(input(\d+).txt)\b'
    filename_pattern = re.compile(filename_regex)

    path = '.'  # look in present working directory for input files
    for root, directory, filenames in os.walk(path):
        for filename in filenames:
            match = filename_pattern.match(filename)
            if match is not None:
                print '{0}:{1}'.format(filename.split('.')[0], get_score(filename, low_risk_phrases_pattern,
                                                                         high_risk_phrases_pattern))


if __name__ == '__main__':
    main()