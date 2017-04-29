
from re import compile
import inspect
from sympy import *
import itertools
from DemoFunctions import *

flatten = lambda l: [item for sublist in l for item in sublist]
indent = lambda s:  len(s)-len(s.lstrip())

def_RE = compile('def(.*)\((.*)\)\:')
assign_RE = compile('(.*)=(.*)')
while_RE = compile('.*while(.*)\:')
if_RE = compile('.*if(.*)\:')
elif_RE = compile('.*elif(.*)\:')
else_RE = compile('.*else\:')

return_RE = compile('.*return(.*)')


class GenInvariant:
    def __init__(self, F):

        self.F = F  # Python function to wrap
        self.source = inspect.getsource(self.F).split("\n")  # Source code of the wrapped function

        self.Vars = {}  # Dict of variables for templates, format: {str(v) : sympy(v)}
        self.Coeffs = {}  # Dict of coefficients for templates, format: {str(c) : sympy(c)}
        self.Terms = []  # List of sympy terms that will compose the template

        self.initVars()

    def initVars(self):

        var_list = []

        # Read through the source code of the wrapped function and
        for line in self.source:
            assign_match = assign_RE.match(line)

            if assign_match:
                var_list.append(assign_match.group(1).strip())

        for v in set(var_list):
            self.Vars[v] = var(v)

    def buildTerms(self, degree):

        n_vars = len(self.Vars)
        exps = []
        for i in range(degree + 1):
            exps.append([i] * n_vars)
        exps = flatten(exps)
        exps = list(set(list(itertools.permutations(exps, n_vars))))

        for e in exps:
            subterm = 1
            for i in range(n_vars):
                subterm *= self.Vars[list(self.Vars.keys())[i]] ** e[i]
            self.Terms.append(subterm)

    def printTerms(self):
        term_str = "Terms:\t"
        terms = sorted(self.Terms, key=lambda x: len(str(x)),reverse=True)
        for t in terms[:-1]:
            term_str += "{},".format(latex(t))
        term_str += "{}\n".format(latex(terms[-1]))
        print (term_str)

    #
    # def printReport(self):
    #     f = open('InvariantReport.tex','w')
    #     term_str = "Terms:\t$"
    #     terms = sorted(self.Terms, key=lambda x: len(str(x)),reverse=True)
    #     for t in terms[:-1]:
    #         term_str += "{},".format(latex(t))
    #     term_str += "{}$\\\\".format(latex(terms[-1]))
    #     f.write(term_str)
    #     f.close()


    def bindCoeffs(self, terms):
        for t in terms:
            const = Symbol("c" + str(i))
            C["c" + str(i)] = const
            E += const * T[i]


if __name__ == '__main__':
    G = GenInvariant(HW21)
    print(G.Vars)
    G.buildTerms(2)
    G.printReport()
