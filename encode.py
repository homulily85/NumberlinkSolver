from itertools import combinations

def at_most_k(a:list,k:int):
    tuples = combinations(a,k+1)
    clauses = []
    for tuple in tuples:
        clause = []
        for element in tuple:
            clause.append(-element)
        clauses.append(clause)
    return clauses


def at_least_k(a:list,k:int):
    for i in range(len(a)):
        a[i]=-a[i]
    return at_most_k(a,len(a)-k)

def exactly_k(a: list,k:int):
    return  at_most_k(a,k)+at_least_k(a,k)
