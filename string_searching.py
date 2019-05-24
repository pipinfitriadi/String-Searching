#!/usr/bin/env python3

# from unittest import main, TestCase
from collections import defaultdict


class Node:
    def __init__(
        self,
        path='',
        in_keys=False,
        suffix=None,
        key_suffix=None,
        childs=set()
    ):
        self.path = path
        self.in_keys = in_keys
        self.suffix: Node = suffix
        self.key_suffix: Node = key_suffix
        self.childs = childs


class AhoCorasick:
    """
    the Aho–Corasick algorithm is a string-searching algorithm invented by
    Alfred V. Aho and Margaret J. Corasick.

    Implemented by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 19th, 2019
    and updated at May 23th, 2019.

    Source: https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
    """

    def __init__(self, keys: list):
        self.tree = self.build_tree(keys)

    def build_tree(self, keys: list) -> Node:
        root = defaultdict(Node)
        root['']

        for key in keys:
            node = root[key]
            node.path = key
            node.in_keys = True
            node.childs.add(
            	   root[
            	       key[:-1]
            	   ]
            )
        
        root_keys = root.keys()
        
        for path in root_keys:
            if path == '':
                continue
            
            node = root[path]
            
            for p in path:
                path = path[1:]
                
                if path in root_keys:
                    node.suffix = root[path]
                    
                    for key in path:
                        if path in keys:
                            node.key_suffix = root[path]
                            break
                        
                        path = path[1:]
                    
                    break

        return root['']

    def find_in(self, text: str):
        pass

    # def is_tree_words_equal_to(self, another_tree_words: dict):
    #     t1 = self.tree_words
    #     t2 = another_tree_words

    #     if len(t1) != len(t2):
    #         return False
    #     elif t1.keys() != t2.keys():
    #         return False

    #     for node in t1.keys():
    #         t1_node = t1[node]
    #         t1_node_keys = t1_node.keys()
    #         t2_node = t2[node]

    #         if len(t1_node) != len(t2_node):
    #             return False
    #         elif (
    #             t1_node_keys
    #             != t2_node.keys()
    #             != {
    #                 'childs',
    #                 'in_words',
    #                 'suffix_link',
    #                 'word_suffix_link'
    #             }
    #         ):
    #             return False

    #         for key in t1_node_keys:
    #             t1_node_key = t1_node[key]
    #             t2_node_key = t2_node[key]

    #             if (
    #                 key != 'childs'
    #                 and t1_node_key != t2_node_key
    #             ):
    #                 return False
    #             elif key == 'childs':
    #                 if len(t1_node_key) != len(t2_node_key):
    #                     return False
    #                 elif set(t1_node_key) != set(t2_node_key):
    #                     return False

    #     return True

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


# class Test(TestCase):
#     def test_AhoCorasick_tree_words_1(self):
#         self.assertEqual(
#             AhoCorasick(
#                 ['']
#             ).is_tree_words_equal_to(
#                 {
#                     '': {
#                         'childs': [],
#                         'in_words': False,
#                         'word_suffix_link': None,
#                         'suffix_link': None
#                     }
#                 }
#             ),
#             True
#         )

    # def test_AhoCorasick_tree_words_2(self):
    #     self.assertEqual(
    #         AhoCorasick(
    #             'a ab'
    #         ).is_tree_words_equal_to(
    #             {
    #                 '': {
    #                     'childs': ['a'],
    #                     'in_words': False,
    #                     'word_suffix_link': None,
    #                     'suffix_link': None
    #                 },
    #                 'a': {
    #                     'childs': ['ab'],
    #                     'in_words': True,
    #                     'word_suffix_link': None,
    #                     'suffix_link': ''
    #                 },
    #                 'ab': {
    #                     'childs': [],
    #                     'in_words': True,
    #                     'word_suffix_link': None,
    #                     'suffix_link': ''
    #                 }
    #             }
    #         ),
    #         True
    #     )

    # def test_AhoCorasick_tree_words_3(self):
    #     self.assertEqual(
    #         AhoCorasick(
    #             [
    #                 'a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa'
    #             ]
    #         ).is_tree_words_equal_to(
    #             {
    #                 '': {
    #                     'childs': ['a', 'b', 'c'],
    #                     'in_words': False,
    #                     'suffix_link': None,
    #                     'word_suffix_link': None
    #                 },
    #                 'a': {
    #                     'childs': ['ab'],
    #                     'in_words': True,
    #                     'suffix_link': '',
    #                     'word_suffix_link': None
    #                 },
    #                 'b': {
    #                     'childs': ['ba', 'bc'],
    #                     'in_words': False,
    #                     'suffix_link': '',
    #                     'word_suffix_link': None
    #                 },
    #                 'c': {
    #                     'childs': ['ca'],
    #                     'in_words': True,
    #                     'suffix_link': '',
    #                     'word_suffix_link': None
    #                 },
    #                 'ab': {
    #                     'childs': [],
    #                     'in_words': True,
    #                     'suffix_link': 'b',
    #                     'word_suffix_link': None
    #                 },
    #                 'ba': {
    #                     'childs': ['bab'],
    #                     'in_words': False,
    #                     'suffix_link': 'a',
    #                     'word_suffix_link': 'a'
    #                 },
    #                 'bc': {
    #                     'childs': ['bca'],
    #                     'in_words': True,
    #                     'suffix_link': 'c',
    #                     'word_suffix_link': 'c'
    #                 },
    #                 'ca': {
    #                     'childs': ['caa'],
    #                     'in_words': False,
    #                     'suffix_link': 'a',
    #                     'word_suffix_link': 'a'
    #                 },
    #                 'bab': {
    #                     'childs': [],
    #                     'in_words': True,
    #                     'suffix_link': 'ab',
    #                     'word_suffix_link': 'ab'
    #                 },
    #                 'bca': {
    #                     'childs': [],
    #                     'in_words': True,
    #                     'suffix_link': 'ca',
    #                     'word_suffix_link': 'a'
    #                 },
    #                 'caa': {
    #                     'childs': [],
    #                     'in_words': True,
    #                     'suffix_link': 'a',
    #                     'word_suffix_link': 'a'
    #                 }
    #             }
    #         ),
    #         True
    #     )

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
        ).tree
    )
