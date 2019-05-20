#!/usr/bin/env python3

from unittest import main, TestCase


class AhoCorasick:
    """
    the Aho–Corasick algorithm is a string-searching algorithm invented by
    Alfred V. Aho and Margaret J. Corasick.

    Implemented by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 19th, 2019
    and updated at May 20th, 2019.

    Source: https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
    """

    def __init__(self, words: list, tree_words={}):
        if tree_words:
            recursive = True
        else:
            recursive = False
            tree_words[''] = {
                'childs': [],
                'in_words': False,
                'word_suffix_link': None
            }

        words = set(words)

        if '' in words:
            words.remove('')

        for word in words:
            if word not in tree_words:
                tree_words[word] = {
                    'childs': [],
                    'in_words': False
                }

            if len(word) == 1:
                parent = ''
            else:
                parent = word[:-1]

                if parent not in tree_words:
                    tree_words = AhoCorasick(
                        [parent],
                        tree_words
                    ).tree_words

            tree_words[parent]['childs'] = list(
                set(
                    tree_words[parent]['childs']
                    + [word]
                )
            )

            if recursive is False:
                tree_words[word]['in_words'] = word in words

        if recursive is False:
            for word in tree_words:
                len_word = len(word)

                if len_word == 1:
                    suffix_link = ''
                elif len_word > 1:
                    for w in range(len_word):
                        first_w = w + 1

                        if first_w == len_word:
                            suffix_link = ''
                            break

                        suffix_link = word[first_w:]

                        if suffix_link in tree_words:
                            break
                else:
                    suffix_link = None

                tree_words[word]['suffix_link'] = suffix_link

                if suffix_link in words:
                    word_suffix_link = suffix_link
                else:
                    if suffix_link is None or len(suffix_link) <= 1:
                        word_suffix_link = None
                    else:
                        len_suffix = len(suffix_link)

                        for s in range(len_suffix):
                            first_s = s + 1

                            if first_s == len_suffix:
                                word_suffix_link = None
                                break

                            word_suffix_link = suffix_link[first_s:]

                            if word_suffix_link in words:
                                break

                tree_words[word]['word_suffix_link'] = word_suffix_link

        self.tree_words = tree_words

    def find_in(self, string):
        words = {}
        tree = self.tree_words

        if len(tree) == 1:
            return words

        node = ''
        position = 0

        while len(string):
            for child in tree[node]['childs']:
                if string.find(child) == 0:
                    node = child
                    break
            else:
                node = tree[node]['suffix_link']

            if node:
                if string.find(node) == 0:
                    word_suffix_link = tree[node]['word_suffix_link']

                    if tree[node]['in_words'] is True:
                        get_node = words.get(node)

                        if get_node:
                            if position not in get_node:
                                words[node].append(position)
                        else:
                            words[node] = [position]

                        if not tree[node]['childs']:
                            node = tree[node]['suffix_link']
                            position += 1
                            string = string[1:]

                    if word_suffix_link:
                        get_word_suffix = words.get(word_suffix_link)
                        w_position = position + 1

                        if get_word_suffix:
                            if w_position not in get_word_suffix:
                                words[word_suffix_link].append(w_position)
                        else:
                            words[word_suffix_link] = [w_position]

                        position += 1
                        string = string[1:]
            else:
                position += 1
                string = string[1:]

        return words

    def is_tree_words_equal_to(self, another_tree_words: dict):
        t1 = self.tree_words
        t2 = another_tree_words

        if len(t1) != len(t2):
            return False
        elif t1.keys() != t2.keys():
            return False

        for node in t1.keys():
            t1_node = t1[node]
            t1_node_keys = t1_node.keys()
            t2_node = t2[node]

            if len(t1_node) != len(t2_node):
                return False
            elif (
                t1_node_keys
                != t2_node.keys()
                != {
                    'childs',
                    'in_words',
                    'suffix_link',
                    'word_suffix_link'
                }
            ):
                return False

            for key in t1_node_keys:
                t1_node_key = t1_node[key]
                t2_node_key = t2_node[key]

                if (
                    key != 'childs'
                    and t1_node_key != t2_node_key
                ):
                    return False
                elif key == 'childs':
                    if len(t1_node_key) != len(t2_node_key):
                        return False
                    elif set(t1_node_key) != set(t2_node_key):
                        return False

        return True

    def are_words_found_equal_to(self, string, words: dict):
        w1 = self.find_in(string)
        w2 = words
        w1_keys = w1.keys()

        if len(w1) != len(w2):
            return False
        elif w1_keys != w2.keys():
            return False

        for key in w1_keys:
            get_w1_key = w1[key]
            get_w2_key = w2[key]
            len_w1_key = len(get_w1_key)

            if len_w1_key != len(w2[key]):
                return False

            for k in range(len_w1_key):
                if get_w1_key[k] != get_w2_key[k]:
                    return False

        return True


class Test(TestCase):
    def test_AhoCorasick_tree_words_1(self):
        self.assertEqual(
            AhoCorasick(
                [''],
                {}
            ).is_tree_words_equal_to(
                {
                    '': {
                        'childs': [],
                        'in_words': False,
                        'word_suffix_link': None,
                        'suffix_link': None
                    }
                }
            ),
            True
        )

    def test_AhoCorasick_tree_words_2(self):
        self.assertEqual(
            AhoCorasick(
                [
                    'a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa'
                ],
                {}
            ).is_tree_words_equal_to(
                {
                    '': {
                        'childs': ['a', 'b', 'c'],
                        'in_words': False,
                        'suffix_link': None,
                        'word_suffix_link': None
                    },
                    'a': {
                        'childs': ['ab'],
                        'in_words': True,
                        'suffix_link': '',
                        'word_suffix_link': None
                    },
                    'b': {
                        'childs': ['ba', 'bc'],
                        'in_words': False,
                        'suffix_link': '',
                        'word_suffix_link': None
                    },
                    'c': {
                        'childs': ['ca'],
                        'in_words': True,
                        'suffix_link': '',
                        'word_suffix_link': None
                    },
                    'ab': {
                        'childs': [],
                        'in_words': True,
                        'suffix_link': 'b',
                        'word_suffix_link': None
                    },
                    'ba': {
                        'childs': ['bab'],
                        'in_words': False,
                        'suffix_link': 'a',
                        'word_suffix_link': 'a'
                    },
                    'bc': {
                        'childs': ['bca'],
                        'in_words': True,
                        'suffix_link': 'c',
                        'word_suffix_link': 'c'
                    },
                    'ca': {
                        'childs': ['caa'],
                        'in_words': False,
                        'suffix_link': 'a',
                        'word_suffix_link': 'a'
                    },
                    'bab': {
                        'childs': [],
                        'in_words': True,
                        'suffix_link': 'ab',
                        'word_suffix_link': 'ab'
                    },
                    'bca': {
                        'childs': [],
                        'in_words': True,
                        'suffix_link': 'ca',
                        'word_suffix_link': 'a'
                    },
                    'caa': {
                        'childs': [],
                        'in_words': True,
                        'suffix_link': 'a',
                        'word_suffix_link': 'a'
                    }
                }
            ),
            True
        )

    def test_AhoCorasick_words_found_1(self):
        self.assertEqual(
            AhoCorasick(
                [
                    'a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa'
                ],
                {}
            ).are_words_found_equal_to(
                'abccab',
                {
                    'a': [0, 4],
                    'ab': [0, 4],
                    'bc': [1],
                    'c': [2, 3]
                }
            ),
            True
        )

    def test_AhoCorasick_words_found_2(self):
        self.assertEqual(
            AhoCorasick(
                [
                    'b', 'c', 'aa', 'd', 'b'
                ],
                {}
            ).are_words_found_equal_to(
                'caaab',
                {
                    'aa': [1, 2],
                    'b': [4],
                    'c': [0]
                }
            ),
            True
        )


if __name__ == '__main__':
    # main()
    from json import dumps

    print(
        dumps(
            AhoCorasick(
                [
                    'a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa'
                ]
            ).tree_words,
            indent=4
        )
    )
