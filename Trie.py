# __author__ = 'chintanpanchamia'


class Node:
    """
    Class defining Node that makes the Trie structure
    """
    def __init__(self, label=None, score=0):
        self.label = label
        self.score = score
        self.children = dict()

    def add_child(self, key, score=0):  # add a child node to current node's dictionary
        if not isinstance(key, Node):
            self.children[key] = Node(key, score)
        else:
            self.children[key.label] = key

    def __getitem__(self, key):  # special function to directly return child node for convenience
        return self.children[key]

    def __str__(self):
        return ','.join((self.label, str(self.score)))


class Trie:
    """
    Class defining Trie data-structure for storing phrases
    """
    def __init__(self):
        self.head = Node()  # root node with None label

    def __getitem__(self, key):
        return self.head.children[key]  # special function to return first level child

    def has_start(self, key):  # check if a phrase in the trie starts with said label/key
        if key in self.head.children:
            return True
        else:
            return False

    def add(self, phrase, score):  # function to add a phrase to the tree
        if phrase is None or phrase is '':
            raise ValueError('Phrase to be added cannot be empty!')

        current_node = self.head
        phrase_words = phrase.lower().strip().split(' ')
        done = True

        for i in range(0, len(phrase_words)):
            if phrase_words[i] in current_node.children:  # walk the head of the trie till the words fail to match
                current_node = current_node.children[phrase_words[i]]
            else:
                done = False
                break

        if not done:
            while i < len(phrase_words):
                current_node.add_child(phrase_words[i])  # add the remaining words below the last match
                current_node = current_node.children[phrase_words[i]]
                i += 1

        current_node.score = score  # phrase ending will contain the score to be added upon complete phrase match
