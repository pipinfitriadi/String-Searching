#!/usr/bin/env python3

"""
Hackerrank: Determining DNA Health
URL: https://www.hackerrank.com/challenges/determining-dna-health/problem

Try to be solved by Pipin Fitriadi (pipinfitriadi@gmail.com) at May 21th, 2019
and updated at May 21th, 2019.
"""

if __name__ == '__main__':
    n = int(input())

    genes = input().rstrip().split()

    health = list(map(int, input().rstrip().split()))

    s = int(input())

    for s_itr in range(s):
        firstLastd = input().split()

        first = int(firstLastd[0])

        last = int(firstLastd[1])

        d = firstLastd[2]
