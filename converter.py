from tkinter.constants import RIGHT
from token import LEFTSHIFT

from encode import at_least_k, exactly_k

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def convert_number_link_to_SAT(a: list, k: int):
    n = len(a)
    variables = variable_generator(n, k)
    clauses = []
    # Một ô bất kỳ phải có ít nhất một hướng đi
    for i in range(n):
        for j in range(n):
            clauses += at_least_k([variables[i][j][m] for m in range(4)], 1)

    # Mọi ô trên màn chơi đều phải được gắn với một nhãn giá trị duy nhất
    for i in range(n):
        for j in range(n):
            t = exactly_k([variables[i][j][m] for m in range(4, len(variables[i][j]))], 1)
            if a[i][j] != 0:
                t.append([variables[i][j][3 + a[i][j]]])
            clauses += t

    # Mã hóa cho những ô có số
    # Các ô ở góc: Tồn tại duy nhất 1 trong 2 hướng đi
    if a[0][0] != 0:
        clauses += exactly_k([variables[0][0][RIGHT], variables[0][0][DOWN]], 1)
    if a[0][n - 1] != 0:
        clauses += exactly_k([variables[0][n - 1][LEFT], variables[0][n - 1][DOWN]], 1)
    if a[n - 1][n - 1] != 0:
        clauses += exactly_k([variables[n - 1][n - 1][LEFT], variables[n - 1][n - 1][UP]], 1)
    if a[n - 1][0] != 0:
        clauses += exactly_k([variables[n - 1][0][RIGHT], variables[n - 1][0][UP]], 1)

    # Câc ô ở biên: Tồn tại duy nhất 1 trong 3 hướng đi
    for i in range(1, n - 1):
        if a[0][i] != 0:
            clauses += exactly_k([variables[0][i][RIGHT], variables[0][i][DOWN], variables[0][i][LEFT]], 1)
        if a[n - 1][i] != 0:
            clauses += exactly_k([variables[n - 1][i][RIGHT], variables[n - 1][i][UP], variables[n - 1][i][LEFT]], 1)
        if a[i][0] != 0:
            clauses += exactly_k([variables[i][0][RIGHT], variables[i][0][DOWN], variables[i][0][UP]], 1)
        if a[i][n - 1] != 0:
            clauses += exactly_k([variables[i][n - 1][LEFT], variables[i][n - 1][DOWN], variables[i][n - 1][UP]], 1)

    # Các ô còn lại:
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if a[i][j] != 0:
                clauses += exactly_k(
                    [variables[i][j][UP], variables[i][j][RIGHT], variables[i][j][DOWN], variables[i][j][LEFT]], 1)

    # Mã hóa cho những ô không có số
    # Các ô ở góc: Tồn tại 2 trong 2 hướng đi
    if a[0][0] == 0:
        clauses += exactly_k([variables[0][0][RIGHT], variables[0][0][DOWN]], 2)
    if a[0][n - 1] == 0:
        clauses += exactly_k([variables[0][n - 1][LEFT], variables[0][n - 1][DOWN]], 2)
    if a[n - 1][n - 1] == 0:
        clauses += exactly_k([variables[n - 1][n - 1][LEFT], variables[n - 1][n - 1][UP]], 2)
    if a[n - 1][0] == 0:
        clauses += exactly_k([variables[n - 1][0][RIGHT], variables[n - 1][0][UP]], 2)

    # Các ô ở biên: Tồn tại 2 trong 3 hướng đi
    for i in range(1, n - 1):
        if a[0][i] == 0:
            clauses += exactly_k([variables[0][i][RIGHT], variables[0][i][DOWN], variables[0][i][LEFT]], 2)
        if a[n - 1][i] == 0:
            clauses += exactly_k([variables[n - 1][i][RIGHT], variables[n - 1][i][UP], variables[n - 1][i][LEFT]], 2)
        if a[i][0] == 0:
            clauses += exactly_k([variables[i][0][RIGHT], variables[i][0][DOWN], variables[i][0][UP]], 2)
        if a[i][n - 1] == 0:
            clauses += exactly_k([variables[i][n - 1][LEFT], variables[i][n - 1][DOWN], variables[i][n - 1][UP]], 2)

    # Các ô còn lại: Tồn tại 2 trong 4 hương đi
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if a[i][j] == 0:
                clauses += exactly_k(
                    [variables[i][j][UP], variables[i][j][RIGHT], variables[i][j][DOWN], variables[i][j][LEFT]], 2)

    # Các ô được kết nối có nhãn giá trị giống nhau
    # Góc
    for m in range(k):
        clauses += [
            [-variables[0][0][4 + m], -variables[0][0][RIGHT], variables[0][1][4 + m]],
            [-variables[0][0][4 + m], -variables[0][0][DOWN], variables[1][0][4 + m]],

            [-variables[0][n - 1][4 + m], -variables[0][n - 1][DOWN], variables[1][n - 1][4 + m]],
            [-variables[0][n - 1][4 + m], -variables[0][n - 1][LEFT], variables[0][n - 2][4 + m]],

            [-variables[n - 1][n - 1][4 + m], -variables[n - 1][n - 1][UP], variables[n - 2][n - 1][4 + m]],
            [-variables[n - 1][n - 1][4 + m], -variables[n - 1][n - 1][LEFT], variables[n - 1][n - 2][4 + m]],

            [-variables[n - 1][0][4 + m], -variables[n - 1][0][RIGHT], variables[n - 1][1][4 + m]],
            [-variables[n - 1][0][4 + m], -variables[n - 1][0][UP], variables[n - 2][0][4 + m]]
        ]
    # Biên
    for i in range(1, n - 1):
        for m in range(k):
            clauses += [
                [-variables[0][i][4 + m], -variables[0][i][RIGHT], variables[0][i + 1][m + 4]],
                [-variables[0][i][4 + m], -variables[0][i][DOWN], variables[1][i][m + 4]],
                [-variables[0][i][4 + m], -variables[0][i][LEFT], variables[0][i - 1][m + 4]],

                [-variables[n - 1][i][4 + m], -variables[n - 1][i][RIGHT], variables[n - 1][i + 1][m + 4]],
                [-variables[n - 1][i][4 + m], -variables[n - 1][i][UP], variables[n - 2][i][m + 4]],
                [-variables[n - 1][i][4 + m], -variables[n - 1][i][LEFT], variables[n - 1][i - 1][m + 4]],

                [-variables[i][0][4 + m], -variables[i][0][DOWN], variables[i + 1][0][m + 4]],
                [-variables[i][0][4 + m], -variables[i][0][UP], variables[i - 1][0][m + 4]],
                [-variables[i][0][4 + m], -variables[i][0][RIGHT], variables[i][1][m + 4]],

                [-variables[i][n - 1][4 + m], -variables[i][n - 1][DOWN], variables[i + 1][n - 1][m + 4]],
                [-variables[i][n - 1][4 + m], -variables[i][n - 1][UP], variables[i - 1][n - 1][m + 4]],
                [-variables[i][n - 1][4 + m], -variables[i][n - 1][LEFT], variables[i][n - 2][m + 4]],
            ]
    # Các ô còn lại
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            for m in range(0, k):
                clauses += [
                    [-variables[i][j][4 + m], -variables[i][j][UP], variables[i - 1][j][4 + m]],
                    [-variables[i][j][4 + m], -variables[i][j][DOWN], variables[i + 1][j][4 + m]],
                    [-variables[i][j][4 + m], -variables[i][j][LEFT], variables[i][j - 1][4 + m]],
                    [-variables[i][j][4 + m], -variables[i][j][RIGHT], variables[i][j + 1][4 + m]],
                ]

    return clauses


def variable_generator(n: int, k: int):
    index = 0
    variables = []
    for i in range(n):
        t1 = []
        for j in range(n):
            t2 = []
            for m in range(4):
                t2.append(index + i * n + j + m + 1)
            index += 4
            for m in range(k):
                t2.append(index + i * n + j + m + 1)
            index += (k - 1)
            t1.append(t2)
        variables.append(t1)
    return variables

