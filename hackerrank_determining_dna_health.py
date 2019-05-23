#!/usr/bin/env python3

"""
Hackerrank: Determining DNA Health
URL: https://www.hackerrank.com/challenges/determining-dna-health/problem

Try to be solved by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 21th 2019,
updated at May 23th 2019.
"""

from collections import defaultdict

if __name__ == '__main__':
    with open('../input0.txt', 'r') as f:
        test_case = f.readlines()

    genes = list(
        map(
            tuple,
            zip(
                test_case[1].rstrip().split(),
                list(
                    map(
                        int,
                        test_case[2].rstrip().split()
                    )
                )
            )
        )
    )
    # min_health = -1
    # max_health = -1

    for s_itr in range(
        int(
            test_case[3]
        )
    ):
        first_last_d = test_case[s_itr + 4].split()
        first = int(
            first_last_d[0]
        )
        last = int(
            first_last_d[1]
        )
        d = first_last_d[2]
    #     total_health = 0
        dna_gene = defaultdict(list)

        for gene, health in genes[first:last + 1]:
            dna_gene[gene].append(health)

        dna_gene = sorted(dna_gene.items())

    #     for g in set(dna_gene):
    #         gene_health = 0

    #         for k, v in enumerate(gene):
    #             if v == g:
    #                 gene_health += health[k+first]

    #         found = 0
    #         dummy_d = d[found:]

    #         while found != -1 and found < len(dummy_d):
    #             found = dummy_d.find(g)

    #             if found != -1:
    #                 total_health += gene_health
    #                 found += 1
    #                 dummy_d = dummy_d[found:]

    #     if min_health == -1 or total_health < min_health:
    #         min_health = total_health

    #     if max_health == -1 or total_health > max_health:
    #         max_health = total_health

    # print(min_health, max_health)
