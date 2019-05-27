#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2019 Pipin Fitriadi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
    Class AhoCorasick Version 2.5.2

    the Aho–Corasick algorithm is a string-searching algorithm invented by
    Alfred V. Aho and Margaret J. Corasick.

    Implemented by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 19th, 2019
    and updated at May 28th, 2019.

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
        found = defaultdict(list)
        t = 0
        node = self.tree

        while t < len(text):
            if node is None:
                node = self.tree

            key = node.key
            len_key = len(key)

            if key == '':
                for child in node.childs:
                    key = child.key

                    if key == text[t:t + len(key)]:
                        node = child
                        break
                else:
                    node = node.suffix
                    t += 1
            elif key == text[t:t + len_key]:
                output = t + len_key - 1
                in_keys = node.in_keys

                if in_keys:
                    found[key].append(output)

                key_suffix_found = 0
                key_suffix = node.key_suffix

                if key_suffix:
                    while key_suffix:
                        found[key_suffix.key].append(output)
                        key_suffix_found += 1
                        key_suffix = key_suffix.key_suffix

                for child in node.childs:
                    key = child.key

                    if key == text[t:t + len(key)]:
                        node = child
                        break
                else:
                    node = node.suffix
                    t += 1

                    if key_suffix_found:
                        if in_keys:
                            for i in range(key_suffix_found):
                                node = node.suffix

                            t += key_suffix_found
                        else:
                            for child in node.childs:
                                key = child.key

                                if key == text[t:t + len(key)]:
                                    node = child
                                    break
                            else:
                                node = node.suffix
                                t += 1

            else:
                node = node.suffix
                t += 1

        # print(found)
        return found

    def are_keys_found_equal_to(
        self,
        text: str,
        other_keys_found: dict
    ) -> bool:
        k1 = self.find_in(text)
        k2 = other_keys_found
        k1_keys = k1.keys()

        if len(k1) != len(k2):
            return False
        elif k1_keys != k2.keys():
            return False

        for key in k1_keys:
            get_k1_key = k1[key]
            get_k2_key = k2[key]
            len_k1_key = len(get_k1_key)

            if len_k1_key != len(k2[key]):
                return False

            for k in range(len_k1_key):
                if get_k1_key[k] != get_k2_key[k]:
                    return False

        return True


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

    def test_AhoCorasick_keys_found_1(self):
        self.assertEqual(
            AhoCorasick(
                ['a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa']
            ).are_keys_found_equal_to(
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

    def test_AhoCorasick_keys_found_2(self):
        self.assertEqual(
            AhoCorasick(
                ['a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa']
            ).are_keys_found_equal_to(
                'abcacaab',
                {
                    'a': [0, 3, 5, 6],
                    'ab': [0, 6],
                    'bc': [1],
                    'bca': [1],
                    'c': [2, 4],
                    'caa': [4]
                }
            ),
            True
        )

    def test_AhoCorasick_keys_found_3(self):
        self.assertEqual(
            AhoCorasick(
                ['b', 'c', 'aa', 'd', 'b']
            ).are_keys_found_equal_to(
                'caaab',
                {
                    'aa': [1, 2],
                    'b': [4],
                    'c': [0]
                }
            ),
            True
        )

    def test_AhoCorasick_keys_found_4(self):
        self.assertEqual(
            AhoCorasick(
                ['a', 'b', 'c', 'aa', 'd']
            ).are_keys_found_equal_to(
                'xyz',
                {}
            ),
            True
        )

    def test_AhoCorasick_keys_found_5(self):
        self.assertEqual(
            AhoCorasick(
                ['c', 'aa', 'd']
            ).are_keys_found_equal_to(
                'bcdybc',
                {
                    'd': [2],
                    'c': [1, 5]
                }
            ),
            True
        )

    def test_AhoCorasick_keys_found_6(self):
        self.assertEqual(
            AhoCorasick(
                ['a', 'ab', 'bab', 'bc', 'bca', 'c', 'ca', 'caa']
            ).are_keys_found_equal_to(
                'abcacaab',
                {
                    'a': [0, 3, 5, 6],
                    'ab': [0, 6],
                    'bc': [1],
                    'bca': [1],
                    'c': [2, 4],
                    'ca': [2, 4],
                    'caa': [4]
                }
            ),
            True
        )


if __name__ == '__main__':
    main()
