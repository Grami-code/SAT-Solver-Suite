import time

def simplify(formula, literal):
    new_formula = []
    for clause in formula:
        if literal in clause:
            continue
        new_clause = [l for l in clause if l != -literal]
        new_formula.append(new_clause)
    return new_formula

def dpll(formula, assignment={}):
    if not formula:
        return True
    if any(clause == [] for clause in formula):
        return False
    unit_clauses = [c[0] for c in formula if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0]
        return dpll(simplify(formula, literal), assignment | {abs(literal): literal > 0})
    literal = formula[0][0]
    return (
        dpll(simplify(formula, literal), assignment | {abs(literal): literal > 0}) or
        dpll(simplify(formula, -literal), assignment | {abs(literal): literal < 0})
    )

def find_pure_literals(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            counter[literal] = counter.get(literal, 0) + 1
    pure_literals = set()
    for literal in counter:
        if -literal not in counter:
            pure_literals.add(literal)
    return pure_literals

def dp(formula):
    formula = [clause[:] for clause in formula]
    while True:
        if not formula:
            return "SAT"
        if any(clause == [] for clause in formula):
            return "UNSAT"
        pure_literals = find_pure_literals(formula)
        if pure_literals:
            for lit in pure_literals:
                formula = simplify(formula, lit)
        else:
            literal = formula[0][0]
            resolvents = []
            for c1 in formula:
                if literal in c1:
                    for c2 in formula:
                        if -literal in c2:
                            resolvent = list(set([l for l in c1 if l != literal] + [l for l in c2 if l != -literal]))
                            resolvents.append(resolvent)
            formula = [clause for clause in formula if literal not in clause and -literal not in clause]
            formula += resolvents

def resolution(formula):
    clauses = set(frozenset(c) for c in formula)
    new = set()
    while True:
        pairs = [(c1, c2) for c1 in clauses for c2 in clauses if c1 != c2]
        for (ci, cj) in pairs:
            for l in ci:
                if -l in cj:
                    resolvent = (ci - {l}) | (cj - {-l})
                    if not resolvent:
                        return "UNSAT"
                    new.add(frozenset(resolvent))
        if new.issubset(clauses):
            return "SAT"
        clauses.update(new)

# GUI

print("Choose SAT method:")
print("1. Resolution")
print("2. Davis–Putnam (DP)")
print("3. DPLL")
optiune = int(input("Chosen method (1-3): "))

# Exemplu de formulă CNF: (x1 ∨ ¬x2) ∧ (¬x1 ∨ x3) ∧ (¬x3)
formula = [[1, -2], [-1, 3], [-3]]
print("CNF tested formula:", formula)

start = time.time()
if optiune == 1:
    rezultat = resolution(formula)
elif optiune == 2:
    rezultat = dp(formula)
elif optiune == 3:
    rezultat = "SAT" if dpll(formula) else "UNSAT"
else:
    rezultat = "Invalid option"
end = time.time()

print(f"Result: {rezultat}")
print(f"Execution time: {round(end - start, 6)} seconds")
