#!/usr/bin/env python3

"""
Hackerrank: Determining DNA Health
URL: https://www.hackerrank.com/challenges/determining-dna-health/problem

Try to be solved by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 21th, 2019
and updated at May 21th, 2019.
"""


class AhoCorasick:
    def __init__(self, first, words, health):
        self.tree_words = self.__tree_words(first, words, health, {})

    def __tree_words(self, first, words, heatlh, tree_words={}):
        genes = words

        if tree_words:
            recursive = True
        else:
            recursive = False
            tree_words[''] = {
                'childs': [],
                'in_words': False,
                'word_suffix_link': None,
                'health': []
            }

        is_words_type_acceptable = True

        if isinstance(words, str):
            words = words.split(' ')
        elif (
            not isinstance(words, list)
            and not isinstance(words, tuple)
        ):
            is_words_type_acceptable = False

        if is_words_type_acceptable:
            words = set(words)

            if '' in words:
                words.remove('')

            for word in words:
                if word not in tree_words:
                    tree_words[word] = {
                        'childs': [],
                        'in_words': False,
                        'health': []
                    }

                if len(word) == 1:
                    parent = ''
                else:
                    parent = word[:-1]

                    if parent not in tree_words:
                        tree_words = self.__tree_words(
                            first,
                            [parent],
                            heatlh,
                            tree_words
                        )

                tree_words[parent]['childs'] = list(
                    set(
                        tree_words[parent]['childs']
                        + [word]
                    )
                )

                if recursive is False:
                    tree_words[word]['in_words'] = word in words

                    if word in words:
                        for w in [i for i, w in enumerate(genes) if w == word]:
                            tree_words[word]['health'].append(
                                heatlh[first+w]
                            )

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

        return tree_words

    def find_in(self, string):
        words = {}
        health = 0
        tree = self.tree_words

        if len(tree) == 1:
            return health, words

        node = ''
        position = 0

        while len(string):
            if node is not None:
                for child in tree[node]['childs']:
                    if string.find(child) == 0:
                        node = child
                        break
                else:
                    node = tree[node]['suffix_link']

                    if node == '':
                        position += 1
                        string = string[1:]
            else:
                node = ''

            if node:
                if string.find(node) == 0:
                    word_suffix_link = tree[node]['word_suffix_link']

                    if tree[node]['in_words'] is True:
                        get_node = words.get(node)

                        if get_node:
                            if position not in get_node:
                                health += sum(
                                    tree[node]['health']
                                )
                                words[node].append(position)
                        else:
                            health += sum(
                                tree[node]['health']
                            )
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
                                health += sum(
                                    tree[node]['health']
                                )
                                words[word_suffix_link].append(w_position)
                        else:
                            health += sum(
                                tree[node]['health']
                            )
                            words[word_suffix_link] = [w_position]

                        position += 1
                        string = string[1:]
            elif node is None:
                position += 1
                string = string[1:]

        return health, words


if __name__ == '__main__':
    n = int(input())

    genes = input().rstrip().split()

    health = list(map(int, input().rstrip().split()))

    s = int(input())

    min_health = 0
    max_health = 0

    for s_itr in range(s):
        firstLastd = input().split()

        first = int(firstLastd[0])

        last = int(firstLastd[1])

        d = firstLastd[2]

        h, gene = AhoCorasick(
            first,
            genes[first:last+1],
            health
        ).find_in(d)

        if h < min_health:
            min_health = h

        if h > max_health:
            max_health = h

    print(min_health, max_health)
