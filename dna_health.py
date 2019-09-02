#!/usr/bin/env python3

# MIT License

# Copyright (c) 2019 Pipin Fitriadi

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import defaultdict
from unittest import main, TestCase

"""
Hackerrank: Determining DNA Health
URL: https://www.hackerrank.com/challenges/determining-dna-health/problem

Try to be solved by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 21th 2019,
updated at May 28th 2019.
"""


class Node:
    def __init__(
        self,
        key='',
        in_keys=False,
        suffix=None,
        key_suffix=None,
        health=0
    ):
        self.key = key
        self.in_keys = in_keys
        self.suffix: Node = suffix
        self.key_suffix: Node = key_suffix
        self.childs = set()
        self.health = health


class AhoCorasick:
    def __init__(self, keys: list):
        self.tree = self.build_tree(keys)

    def build_tree(self, keys: list) -> Node:
        keys = sorted(keys)
        root = {}
        root[''] = Node()
        keys_name = [key for key, _ in keys]

        for key, health in keys:
            for k in range(
                len(key)
            ):
                current_key = key[:k+1]

                if current_key not in root:
                    root[current_key] = Node(
                        current_key,
                        current_key in keys_name
                    )

                if key == current_key:
                    root[current_key].health = health

                parent_key = current_key[:-1]

                if parent_key not in root:
                    root[parent_key] = Node(
                        parent_key,
                        parent_key in keys_name
                    )

                if key == parent_key:
                    root[current_key].health = health

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

                        if key_suffix in keys_name:
                            root[key].key_suffix = root[key_suffix]
                            break

                    break

        return root['']

    def find_in(self, text: str) -> dict:
        output = 0
        node = self.tree

        for i, t in enumerate(text):
            while node:
                for child in node.childs:
                    key = child.key

                    if key[-1:] == t:
                        if child.in_keys:
                            output += child.health

                        key_suffix = child.key_suffix

                        if key_suffix:
                            while key_suffix:
                                key = key_suffix.key
                                output += key_suffix.health
                                key_suffix = key_suffix.key_suffix

                        node = child
                        is_found = True
                        break
                else:
                    node = node.suffix
                    is_found = False

                if is_found:
                    break
            else:
                node = self.tree

        return output


def min_max_dna_health(file_path: str) -> tuple:
    with open(file_path, 'r') as content:
        lines = content.readlines()

    genes = list(
        map(
            tuple,
            zip(
                lines[1].rstrip().split(),
                list(
                    map(
                        int,
                        lines[2].rstrip().split()
                    )
                )
            )
        )
    )
    min_health = -1
    max_health = -1

    for s_itr in range(
        int(
            lines[3]
        )
    ):
        first_last_d = lines[s_itr + 4].split()
        s_gene = defaultdict(int)

        for gene, health in genes[
            int(
                first_last_d[0]
            ):int(
                first_last_d[1]
            ) + 1
        ]:
            s_gene[gene] += health

        total_health = AhoCorasick(
            s_gene.items()
        ).find_in(
            first_last_d[2]
        )

        if min_health == -1 or total_health < min_health:
            min_health = total_health

        if max_health == -1 or total_health > max_health:
            max_health = total_health

    return min_health, max_health


class Test(TestCase):
    def test_1(self):
        self.assertEqual(
            min_max_dna_health('../input00.txt'),
            (0, 19)
        )

    def test_2(self):
        self.assertEqual(
            min_max_dna_health('../input01.txt'),
            (3218660, 11137051)
        )

    # def test_3(self):
    #     self.assertEqual(
    #         min_max_dna_health('../input13.txt'),
    #         (40124729287, 61265329670)
    #     )

    # def test_4(self):
    #     self.assertEqual(
    #         min_max_dna_health('../input30.txt'),
    #         (12317773616, 12317773616)
    #     )


from time import time


def timer_genes_1(file_path: str):
    with open(file_path, 'r') as content:
        lines = content.readlines()

    t0 = time()
    genes = list(
        map(
            tuple,
            zip(
                lines[1].rstrip().split(),
                list(
                    map(
                        int,
                        lines[2].rstrip().split()
                    )
                )
            )
        )
    )
    t1 = time()
    return t1 - t0


def timer_genes_2(file_path: str):
    with open(file_path, 'r') as content:
        lines = content.readlines()

    t0 = time()
    genes = lines[1].rstrip().split()
    health = list(
        map(
            int,
            lines[2].rstrip().split()
        )
    )
    genes = list(
        map(
            tuple,
            zip(
                genes,
                health
            )
        )
    )
    t1 = time()
    return t1 - t0


def timer_genes_3(file_path: str):
    with open(file_path, 'r') as content:
        lines = content.readlines()

    t0 = time()
    genes = lines[1].rstrip().split()
    healths = list(map(int, lines[2].rstrip().split()))
    gMap = defaultdict(lambda: [[], [0]])
    subs = set()

    for id, gene in enumerate(genes):
        gMap[gene][0].append(id)

        for j in range(1, min(len(gene), 500)+1):
            subs.add(gene[:j])

    for v in gMap.values():
        for i, ix in enumerate(v[0]):
            v[1].append(v[1][i]+healths[ix])
    t1 = time()
    return t1 - t0

def run_test():
    for i in ['00', '01', '13', '30']:
        path = f'../input{i}.txt'
        tg1 = timer_genes_1(path)
        tg2 = timer_genes_2(path)
        tg3 = timer_genes_3(path)

        if tg1 <= tg2:
            if tg1 <= tg3:
                print('tg1')
            else:
                print('tg3')
        else:
            if tg2 <= tg3:
                print('tg2')
            else:
                print('tg3')

        print()

if __name__ == '__main__':
    # main()

    import os

    os.chdir(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    run_test()
