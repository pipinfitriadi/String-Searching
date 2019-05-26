#!/usr/bin/env python3

from collections import defaultdict
from unittest import main, TestCase


class Node:
    def __init__(
        self,
        key='',
        in_keys=False,
        suffix=None,
        key_suffix=None
    ):
        self.key = key
        self.in_keys = in_keys
        self.suffix: Node = suffix
        self.key_suffix: Node = key_suffix

        # Value of parameter childs should be declare
        # explicitly in instance class. Because if every
        # instance class use default value, than it would
        # be have same object identity. This rule works
        # for data type set, dict, list, and tuple.
        self.childs = set()

    # Recommended way to implement __eq__ and __hash__
    # Source:
    # https://stackoverflow.com/questions/45164691/recommended-way-to-implement-eq-and-hash
    def __members(self):
        return (
            self.key,
            self.in_keys,
            self.suffix,
            self.key_suffix,

            # Type error Unhashable type:set
            # Source:
            # https://stackoverflow.com/questions/23577724/type-error-unhashable-typeset
            frozenset(
                # I used set() instead self.childs for frozenset,
                # because self.childs lenght would be incorect
                # if it is converted into frozenset.
                set()
            )
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        elif self.key != other.key:
            return False
        elif self.in_keys != other.in_keys:
            return False
        elif (
            (
                self.suffix is None
                and other.suffix is not None
            ) or (
                self.suffix is not None
                and other.suffix is None
            )
        ):
            return False
        elif (
            self.suffix is not None
            and other.suffix is not None
            and self.suffix.key != other.suffix.key
        ):
            return False
        elif (
            (
                self.key_suffix is None
                and other.key_suffix is not None
            ) or (
                self.key_suffix is not None
                and other.key_suffix is None
            )
        ):
            return False
        elif (
            self.key_suffix is not None
            and other.key_suffix is not None
            and self.key_suffix.key != other.key_suffix.key
        ):
            return False
        elif len(self.childs) != len(other.childs):
            return False
        elif (
            len(self.childs) > 0
            and (
                {node.key for node in self.childs}
                != {node.key for node in other.childs}
            )
        ):
            return False

        for n in self.childs:
            for o in other.childs:
                if n.key != o.key:
                    continue
                elif not (n == o):
                    return False

        return True

    def __hash__(self):
        return hash(
            self.__members()
        )


class AhoCorasick:
    """
    Class AhoCorasick Version 2.4.3

    the Aho–Corasick algorithm is a string-searching algorithm invented by
    Alfred V. Aho and Margaret J. Corasick.

    Implemented by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 19th, 2019
    and updated at May 26th, 2019.

    Source: https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
    """

    def __init__(self, keys: list):
        self.tree = self.build_tree(keys)

    def build_tree(self, keys: list) -> Node:
        keys = sorted(keys)
        root = {}
        root[''] = Node()

        for key in keys:
            for k in range(
                len(key)
            ):
                current_key = key[:k+1]

                if current_key not in root:
                    root[current_key] = Node(
                        current_key,
                        current_key in keys
                    )

                parent_key = current_key[:-1]

                if parent_key not in root:
                    root[parent_key] = Node(
                        parent_key,
                        parent_key in keys
                    )

                root[parent_key].childs.add(
                    root[current_key]
                )

        for key in root:
            for k in range(
                len(key)
            ):
                suffix = key[k+1:]

                if suffix in root:
                    root[key].suffix = root[suffix]

                    for s in range(
                        len(suffix)
                    ):
                        key_suffix = suffix[s:]

                        if key_suffix in keys:
                            root[key].key_suffix = root[key_suffix]
                            break

                    break

        return root['']

    def find_in(self, text: str) -> dict:
        result = defaultdict(list)
        t = 0

        while t < len(text):
            node = self.tree

            while node is not None:
                remaining_text = text[t:]
                key = node.key

                if key != '':
                    len_key = len(key)

                    if key == remaining_text[:len_key]:
                        if node.in_keys:
                            result[key].append(
                                t + len_key - 1
                            )

                        key_suffix = node.key_suffix

                        if key_suffix:
                            while key_suffix:
                                t += 1
                                key = key_suffix.key
                                result[key].append(
                                    t + len(key) - 1
                                )
                                key_suffix = key_suffix.key_suffix

                for child in node.childs:
                    key = child.key

                    if key == remaining_text[:len(key)]:
                        node = child
                        break
                else:
                    node = node.suffix
                    t += 1

        return result

    # def are_words_found_equal_to(self, string, another_words: dict):
    #     w1 = self.find_in(string)
    #     w2 = another_words
    #     w1_keys = w1.keys()

    #     if len(w1) != len(w2):
    #         return False
    #     elif w1_keys != w2.keys():
    #         return False

    #     for key in w1_keys:
    #         get_w1_key = w1[key]
    #         get_w2_key = w2[key]
    #         len_w1_key = len(get_w1_key)

    #         if len_w1_key != len(w2[key]):
    #             return False

    #         for k in range(len_w1_key):
    #             if get_w1_key[k] != get_w2_key[k]:
    #                 return False

    #     return True


class Test(TestCase):
    def test_AhoCorasick_tree_1(self):
        self.assertEqual(
            AhoCorasick(
                ['']
            ).tree == Node(),
            True
        )

    def test_AhoCorasick_tree_2(self):
        tree = Node()
        a = Node('a', True, tree)
        ab = Node('ab', True, tree)

        tree.childs.add(a)
        a.childs.add(ab)

        self.assertEqual(
            AhoCorasick(
                ['a', 'ab']
            ).tree == tree,
            True
        )

    def test_AhoCorasick_tree_3(self):
        tree = Node()
        a = Node('a', True, tree)
        b = Node('b', False, tree)
        c = Node('c', True, tree)
        ab = Node('ab', True, b)
        ba = Node('ba', False, a, a)
        bc = Node('bc', True, c, c)
        ca = Node('ca', False, a, a)
        bab = Node('bab', True, ab, ab)
        bca = Node('bca', True, ca, a)
        caa = Node('caa', True, a, a)

        tree.childs = {a, b, c}
        a.childs.add(ab)
        b.childs = {ba, bc}
        c.childs.add(ca)
        ba.childs.add(bab)
        bc.childs.add(bca)
        ca.childs.add(caa)

        self.assertEqual(
            AhoCorasick(
                ['a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa']
            ).tree == tree,
            True
        )

    def test_AhoCorasick_tree_4(self):
        tree = Node()
        a = Node('a', False, tree)
        b = Node('b', True, tree)
        c = Node('c', True, tree)
        d = Node('d', True, tree)
        aa = Node('aa', True, a)

        tree.childs = {a, b, c, d}
        a.childs.add(aa)

        self.assertEqual(
            AhoCorasick(
                ['b', 'c', 'aa', 'd', 'b']
            ).tree == tree,
            True
        )

    def test_AhoCorasick_tree_5(self):
        tree = Node()
        a = Node('a', True, tree)
        b = Node('b', True, tree)
        c = Node('c', True, tree)
        d = Node('d', True, tree)
        aa = Node('aa', True, a, a)

        tree.childs = {a, b, c, d}
        a.childs.add(aa)

        self.assertEqual(
            AhoCorasick(
                ['a', 'b', 'c', 'aa', 'd']
            ).tree == tree,
            True
        )

    def test_AhoCorasick_tree_6(self):
        tree = Node()
        a = Node('a', False, tree)
        c = Node('c', True, tree)
        d = Node('d', True, tree)
        aa = Node('aa', True, a)

        tree.childs = {a, c, d}
        a.childs.add(aa)

        self.assertEqual(
            AhoCorasick(
                ['c', 'aa', 'd']
            ).tree == tree,
            True
        )

    # def test_AhoCorasick_words_found_1(self):
    #     self.assertEqual(
    #         AhoCorasick(
    #             [
    #                 'a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa'
    #             ]
    #         ).are_words_found_equal_to(
    #             'abccab',
    #             {
    #                 'a': [0, 4],
    #                 'ab': [0, 4],
    #                 'bc': [1],
    #                 'c': [2, 3]
    #             }
    #         ),
    #         True
    #     )

    # def test_AhoCorasick_words_found_2(self):
    #     self.assertEqual(
    #         AhoCorasick(
    #             [
    #                 'b', 'c', 'aa', 'd', 'b'
    #             ]
    #         ).are_words_found_equal_to(
    #             'caaab',
    #             {
    #                 'aa': [1, 2],
    #                 'b': [4],
    #                 'c': [0]
    #             }
    #         ),
    #         True
    #     )


if __name__ == '__main__':
    # main()

    print(
        AhoCorasick(
            ['a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa']
        ).find_in('abccab')
    )
