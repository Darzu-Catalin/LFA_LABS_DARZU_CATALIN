from typing import Dict, Set, Tuple, List

EPS = "ε"  # Marker for epsilon

# ────────────────────────── Parsing ──────────────────────────
def _parse(lines: List[str]) -> Dict[str, Set[Tuple[str, ...]]]:
    g: Dict[str, Set[Tuple[str, ...]]] = {}
    for l in lines:
        L, R = l.split("->")
        L = L.strip()
        for alt in R.split("|"):
            alt = alt.strip()
            # an empty tuple represents ε
            g.setdefault(L, set()).add(
                tuple(alt) if alt and alt != EPS else tuple()
            )
    return g

# ───────────────── ε‑elimination ─────────────────
def _rm_eps(g: Dict[str, Set[Tuple[str, ...]]], start="S"):
    # 1) find nullable nonterminals
    nullable, changed = set(), True
    while changed:
        changed = False
        for A, prods in g.items():
            if A not in nullable and any(
                (not p) or all(s in nullable for s in p)
                for p in prods
            ):
                nullable.add(A)
                changed = True

    # 2) rebuild grammar without epsilons
    ng = {A: set() for A in g}
    for A, prods in g.items():
        for p in prods:
            # generate all subsets of positions of p where the symbol is nullable
            idx = [i for i, s in enumerate(p) if s in nullable]
            subsets = [[]]
            for i in idx:
                subsets += [old + [i] for old in subsets]

            for sub in subsets:
                alt = tuple(sym for i, sym in enumerate(p) if i not in sub)
                # keep the empty RHS only for the start symbol
                if alt or A == start:
                    ng[A].add(alt)
    return ng

# ───────────── Unit‑production removal ─────────────
def _rm_unit(g: Dict[str, Set[Tuple[str, ...]]]):
    ng = {A: set() for A in g}
    for A in g:
        stack, seen = [A], set()
        while stack:
            X = stack.pop()
            for p in g[X]:
                # if p is a single nonterminal → unit production
                if len(p) == 1 and p[0].isupper():
                    B = p[0]
                    if B not in seen:
                        seen.add(B)
                        stack.append(B)
                else:
                    ng[A].add(p)
    return ng

# ─────── Useless‑symbol removal ───────
def _rm_useless(g: Dict[str, Set[Tuple[str, ...]]], start="S"):
    # (a) remove non‑productive symbols
    prod, changed = set(), True
    while changed:
        changed = False
        for A, prods in g.items():
            if A not in prod and any(
                all((not s.isupper()) or s in prod for s in p)
                for p in prods
            ):
                prod.add(A)
                changed = True

    g = {
        A: {p for p in prods if all((not s.isupper()) or s in prod for s in p)}
        for A, prods in g.items() if A in prod
    }

    # (b) remove unreachable symbols
    acc, changed = {start}, True
    while changed:
        changed = False
        for A in list(acc):
            for p in g.get(A, []):
                for s in p:
                    if s.isupper() and s in g and s not in acc:
                        acc.add(s)
                        changed = True

    return {A: g[A] for A in acc}

# ───────── Terminals → Variables ─────────
def _term_to_var(g: Dict[str, Set[Tuple[str, ...]]]):
    mp: Dict[str, str] = {}
    extra: Dict[str, Set[Tuple[str, ...]]] = {}
    cnt = 1

    for A, prods in list(g.items()):
        newset = set()
        for p in prods:
            if len(p) >= 2:
                rep = []
                for s in p:
                    if s.isupper():
                        rep.append(s)
                    else:
                        if s not in mp:
                            v = f"T{cnt}"
                            cnt += 1
                            mp[s] = v
                            extra[v] = {(s,)}
                        rep.append(mp[s])
                newset.add(tuple(rep))
            else:
                newset.add(p)
        g[A] = newset

    # add the definitions for the new terminal‑variables
    g.update(extra)
    return g

# ───────────── Binarize long RHS ─────────────
def break_long(
    g: Dict[str, Set[Tuple[str, ...]]], prefix="X"
) -> Dict[str, Set[Tuple[str, ...]]]:
    newg: Dict[str, Set[Tuple[str, ...]]] = {A: set() for A in g}
    fresh_id = 1

    def fresh() -> str:
        nonlocal fresh_id
        v = f"{prefix}{fresh_id}"
        fresh_id += 1
        newg.setdefault(v, set())
        return v

    for A, prods in g.items():
        for rhs in prods:
            # keep length 0,1,2 as is
            if len(rhs) <= 2:
                newg[A].add(rhs)
            else:
                # split A → X1 X2 … Xk into binary chain
                first, *rest = rhs
                aux = fresh()
                newg[A].add((first, aux))

                prev = aux
                while len(rest) > 2:
                    sym, *rest = rest
                    nxt = fresh()
                    newg[prev].add((sym, nxt))
                    prev = nxt

                newg[prev].add(tuple(rest))
    return newg

# ─────────────────── Public CNF converter ────────────────────
def to_cnf(lines: List[str], start="S") -> Dict[str, Set[Tuple[str, ...]]]:
    g = _parse(lines)
    print("► Initial grammar:")
    print(pretty(g), "\n")

    g = _rm_eps(g, start)
    print("► After ε‑elimination:")
    print(pretty(g), "\n")

    g = _rm_unit(g)
    print("► After unit‑production removal:")
    print(pretty(g), "\n")

    g = _rm_useless(g, start)
    print("► After removing useless symbols:")
    print(pretty(g), "\n")

    g = _term_to_var(g)
    print("► After replacing terminals in long RHS:")
    print(pretty(g), "\n")

    g = break_long(g)
    print("► Final Chomsky Normal Form:")
    print(pretty(g), "\n")

    return g

def pretty(g: Dict[str, Set[Tuple[str, ...]]]) -> str:
    lines = []
    for A in sorted(g):
        rhss = []
        for p in sorted(g[A]):
            if not p:
                rhss.append(EPS)
            else:
                rhss.append("".join(p))
        lines.append(f"{A} → {' | '.join(rhss)}")
    return "\n".join(lines)

# ──────────────────────── Main: Variant 13 ────────────────────────
if __name__ == "__main__":
    variant13: List[str] = [
        "S->aB",
        "S->DA",
        "A->a",
        "A->BD",
        "A->bDAB",
        "B->b",
        "B->BA",
        "D->ε",
        "D->BA",
        "C->BA",
    ]

    cnf13 = to_cnf(variant13, start="S")
