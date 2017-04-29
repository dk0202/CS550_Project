from sympy import *
import itertools

flatten = lambda l: [item for sublist in l for item in sublist]


def init_variables(var_list):
    Vars = {}
    for v in var_list:
        Vars[v] = var(v)

    return Vars


def possible_terms(var_list, degree):
    n_vars = len(var_list)
    exps = []
    for i in range(degree + 1):
        exps.append([i] * n_vars)
    exps = flatten(exps)
    exps = list(set(list(itertools.permutations(exps, n_vars))))

    V = init_variables(var_list)
    T = []

    for e in exps:
        subterm = 1
        for i in range(n_vars):
            subterm *= V[var_list[i]] ** e[i]
        T.append(subterm)

    return V, T


def collect_args(V1_Cond):
    V1_Cond = expand(V1_Cond)
    A = V1_Cond.args
    consts = [x for x in A if x in C.values()]

    COEFFS = []
    TERMS = []

    A_sub = [a.args for a in A]
    for a in A_sub:
        coeff = 1
        term = 1
        for n in [i for i in a if (type(i) == Integer or abs(i) == 1 or i in C.values())]:
            coeff *= n
        for n in [i for i in a if not (type(i) == Integer or abs(i) == 1 or i in C.values())]:
            term *= n
        COEFFS.append(coeff)
        TERMS.append(term)
    D = {t: 0 for t in set(TERMS)}
    for i, j in zip(COEFFS, TERMS):
        if not (i == 1 and j == 1):
            D[j] += i
    for c in consts:
        D[1] += c
    return D


def solve_constraints(V_cond):
    pass


def gen_Template(V, T):
    E = 0
    C = {}
    for i in range(len(T)):
        const = Symbol("c" + str(i))
        C["c" + str(i)] = const
        E += const * T[i]
    return E, C


def gen_V0(Template, assignments):
    pass


def gen_V1(V0, V, assignments):
    V1 = V0
    for a in assignments:
        V1 = V1.subs(V[a], assignments[a])
    return V1


def substitutions(orig_eq, subs):
    modified_eq = orig_eq
    for s in subs:
        modified_eq = modified_eq.subs(s, subs[s])
    return modified_eq


def print_constraints(Cons):
    print("{} = 0".format([i for i in Cons if Cons[i] == 0]))
    for c in [i for i in Cons if Cons[i] != 0]:
        print("{} = {}".format(c, Cons[c]))




if __name__ == '__main__':
    V, T = possible_terms(['a', 's', 't'], 1)
    VT, C = gen_Template(V, T)
    print("VT:\n")
    print(VT)
    V1 = VT
    V1 = V1.subs(a, a + 1)
    V1 = V1.subs(s, s + t + 2)
    V1 = V1.subs(t, t + 2)
    V1 = expand(V1)
    print("V1:\n")
    print(V1)
    solve(tuple(collect_args(V1 - VT).values()), C.values())

