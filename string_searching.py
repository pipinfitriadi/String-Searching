#!/usr/bin/env python3

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


class AhoCorasick:
    """
    Class AhoCorasick Version 2.3.1

    the Aho–Corasick algorithm is a string-searching algorithm invented by
    Alfred V. Aho and Margaret J. Corasick.

    Implemented by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 19th, 2019
    and updated at May 25th, 2019.

    Source: https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
    """

    def __init__(self, keys: list):
        self.tree = self.build_tree(keys)

    def build_tree(self, keys: list) -> Node:
        keys = sorted(keys)
        root = {}
        root[''] = Node()

        for key in keys:
            for k, _ in enumerate(key):
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
            for k, _ in enumerate(key):
                suffix = key[k+1:]

                if suffix in root:
                    root[key].suffix = root[suffix]

                    for s, _ in enumerate(suffix):
                        key_suffix = suffix[s:]

                        if key_suffix in keys:
                            root[key].key_suffix = root[key_suffix]
                            break

                    break

        return root['']

    def find_in(self, text: str):
        pass

    def compare_node(node_1: Node, node_2: Node) -> bool:
        if node_1.key != node_2.key:
            return False
        elif node_1.in_keys != node_2.in_keys:
            return False
        elif (
            (
                node_1.suffix is None
                and node_2.suffix is not None
            ) or (
                node_1.suffix is not None
                and node_2.suffix is None
            )
        ):
            return False
        elif (
            node_1.suffix is not None
            and node_2.suffix is not None
            and node_1.suffix.key != node_2.suffix.key
        ):
            return False
        elif (
            (
                node_1.key_suffix is None
                and node_2.key_suffix is not None
            ) or (
                node_1.key_suffix is not None
                and node_2.key_suffix is None
            )
        ):
            return False
        elif (
            node_1.key_suffix is not None
            and node_2.key_suffix is not None
            and node_1.key_suffix.key != node_2.key_suffix.key
        ):
            return False
        elif len(node_1.childs) != len(node_2.childs):
            return False
        elif (
            len(node_1.childs) > 0
            and (
                {node.key for node in node_1.childs}
                != {node.key for node in node_2.childs}
            )
        ):
            return False

        for n_1 in node_1.childs:
            for n_2 in node_2.childs:
                if n_1.key != n_2.key:
                    continue
                elif not AhoCorasick.compare_node(n_1, n_2):
                    return False

        return True

    def is_tree_equal_to(self, another_tree: Node):
        return AhoCorasick.compare_node(self.tree, another_tree)

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
            ).is_tree_equal_to(
                Node()
            ),
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
            ).is_tree_equal_to(tree),
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
            ).is_tree_equal_to(tree),
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
            ).is_tree_equal_to(tree),
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
            ).is_tree_equal_to(tree),
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
            ).is_tree_equal_to(tree),
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
    main()

    # print(
    #     AhoCorasick(
    #         ['a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa']
    #     ).tree
    # )
