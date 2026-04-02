def sum_of_n_nos(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

print(sum_of_n_nos(5))