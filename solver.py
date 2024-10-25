from pysat.solvers import Glucose3

from converter import convert_number_link_to_SAT


def print_solution(solution: list, n: int, k: int):
    index = 0
    ans = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            index += 4
            for m in range(k):
                t = index + i * n + j + m
                if solution[t] > 0:
                    ans[i][j] = (m + 1)
            index += (k - 1)
    for i in range(n):
        for j in range(n):
            print(f'{ans[i][j]}', end=' ')
        print()


n = int(input('Size of the matrix = '))
k = int(input('Maximum value of the matrix = '))

print('Matrix:')

a = []
for i in range(n):
    t = input().split(' ')
    for j in range(len(t)):
        t[j] = int(t[j])
    a.append(t)
clauses = convert_number_link_to_SAT(a, k)

solver = Glucose3()
for clause in clauses:
    solver.add_clause(clause)

if solver.solve():
    model = solver.get_model()
    print('Solution:')
    print_solution(model, n, k)
