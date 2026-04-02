def sum_of_n_nos(n):
    if n == 1:   # base case
        return 1
    return n + sum_of_n_nos(n - 1)

print(sum_of_n_nos(5))