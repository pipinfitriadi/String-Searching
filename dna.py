if __name__ == '__main__':
    with open('input30.txt', 'r') as f:
        test_case = f.readlines()

    genes = test_case[1].rstrip().split()
    health = list(
        map(
            int,
            test_case[2].rstrip().split()
        )
    )
    min_health = -1
    max_health = -1

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
        total_health = 0
        gene = genes[first:last+1]

        for g in set(gene):
            gene_health = 0

            for k, v in enumerate(gene):
                if v == g:
                    gene_health += health[k+first]

            found = 0
            dummy_d = d[found:]

            while found != -1 and found < len(dummy_d):
                found = dummy_d.find(g)

                if found != -1:
                    total_health += gene_health
                    found += 1
                    dummy_d = dummy_d[found:]

        if min_health == -1 or total_health < min_health:
            min_health = total_health

        if max_health == -1 or total_health > max_health:
            max_health = total_health

    print(min_health, max_health)
