# Chomsky Normal Form Converter

**Course**: Formal Languages and Finite Automata
**Author**: Darzu Catalin
**Variant**: 13
**Date**: 05/05/2025

---

## 1. Theory

Chomsky Normal Form (CNF) is a canonical form for context-free grammars (CFGs) that restricts productions to binary or terminal forms, simplifying parsing and proof techniques and serving as a foundation for algorithmic applications such as the CYK parser.

### 1.1 Formal Definition

A grammar \$G = (V, \Sigma, R, S)\$ is in CNF if every production in \$R\$ satisfies one of the following:

1. \$A \rightarrow BC\$ where \$A,B,C \in V\$, and neither \$B\$ nor \$C\$ is the start symbol;
2. \$A \rightarrow a\$ where \$A \in V\$ and \$a \in \Sigma\$;
3. \$S \rightarrow \epsilon\$ if (and only if) \$\epsilon \in L(G)\$ and \$S\$ does not appear on the right-hand side of any production.

These restrictions ensure that each production either expands to exactly two nonterminals or to a single terminal, with the only exception being the start symbol producing the empty string when necessary.

### 1.2 Equivalent Transformations and Normal Forms

CNF is one among several normal forms for CFGs. Others include:

* **Greibach Normal Form (GNF):** All productions are of the form \$A \rightarrow a\alpha\$, where \$a\$ is a terminal and \$\alpha\$ is (possibly empty) string of nonterminals. Useful for constructing top-down parsers.
* **Extended CNF:** Allows mixed productions \$A \rightarrow Bc\$ or \$A \rightarrow cB\$, which can sometimes reduce grammar size.
* **Binary-CNF vs. Strict-CNF:** In Binary-CNF, the start symbol may appear in the right-hand side; Strict-CNF forbids this entirely.

Conversion between these forms preserves language equivalence (up to \$\epsilon\$), enabling different parsing strategies.

### 1.3 Key Transformation Steps and Invariants

When converting an arbitrary CFG to CNF, the following invariants and subtleties guide each phase:

1. **Preserve Language Membership:** Each transformation must maintain the set of generated strings, except possibly removing \$\epsilon\$ if the original grammar admitted it but CNF does not allow \$\epsilon\$ except via the start symbol.
2. **Avoid Exponential Blow-up:** While naive elimination of nullable combinations can lead to \$O(2^k)\$ new rules, algorithmic optimizations (e.g., using counting or marking) can keep the blow-up polynomial.
3. **Maintain Start Symbol Integrity:** Introducing a fresh start symbol \$S\_0\$ when \$S\$ appears on right-hand sides ensures no rule \$A \rightarrow BC\$ ever has \$B\$ or \$C\$ as the original start.

### 1.4 Theoretical Implications

* **Parsing Complexity:** The CYK algorithm runs in \$O(n^3 |R|)\$ time with CNF grammars, giving a tight bound for membership testing.
* **Decidability:** CNF preserves decidability of emptiness, finiteness, and membership, aligning CFGs with well-understood computational models.
* **Algorithmic Tools:** Many proofs of closure properties and pumping lemmas for CFGs leverage CNF to simplify case analyses.

### 1.5 Practical Considerations

* **Grammar Size vs. Readability:** CNF grammars tend to be larger and less human-readable; for educational or debugging purposes, Readable Normal Form (RNF) or annotated grammars are sometimes preferred.
* **Automated Tool Support:** Modern parser generators (e.g., ANTLR) often bypass explicit CNF conversion, using more flexible internal representations, but understanding CNF remains essential for theoretical courses and certain verification tools.

---

## 2. Objectives

The main goal is to build an automated converter that transforms an arbitrary CFG into CNF by applying the following sequence of steps:

1. **Eliminate ε‑productions** – rules that produce the empty string;
2. **Eliminate unit‑productions** – rules of the form \$A \rightarrow B\$, where both \$A\$ and \$B\$ are nonterminals;
3. **Remove useless symbols** – nonterminals that are non‑productive or unreachable;
4. **Replace terminals in complex productions** with intermediate nonterminals;
5. **Binarize long productions** – split rules of length > 2 into chains of binary productions.

We implement these steps in a modular Python program, allowing testing on multiple grammar variants.

---

## 3. Implementation Details

The code is organized into functions, each handling one transformation step. Below are two representative examples:

### 3.1 Grammar Parsing

```python
def _parse(lines: List[str]) -> Dict[str, Set[Tuple[str, ...]]]:
    g: Dict[str, Set[Tuple[str, ...]]] = {}
    for l in lines:
        L, R = l.split("->")
        L = L.strip()
        for alt in R.split("|"):
            alt = alt.strip()
            g.setdefault(L, set()).add(
                tuple(alt) if alt and alt != EPS else tuple()
            )
    return g
```

This function converts production lines into a Python dictionary where:

* The **key** is the left‑hand side nonterminal;
* The **value** is a set of tuples representing each right‑hand side alternative.

---

### 3.2 ε‑Production Elimination

```python
def _rm_eps(g: Dict[str, Set[Tuple[str, ...]]], start="S"):
    nullable, changed = set(), True
    while changed:
        changed = False
        for A, prods in g.items():
            if (
                A not in nullable
                and any((not p) or all(s in nullable for s in p) for p in prods)
            ):
                nullable.add(A)
                changed = True

    ng = {A: set() for A in g}
    for A, prods in g.items():
        for p in prods:
            idx = [i for i, s in enumerate(p) if s in nullable]
            subsets = [[]]
            for i in idx:
                subsets += [old + [i] for old in subsets]
            for sub in subsets:
                alt = tuple(sym for i, sym in enumerate(p) if i not in sub)
                if alt or A == start:
                    ng[A].add(alt)
    return ng
```

This function identifies nullable nonterminals and generates all variants of productions without them, retaining ε only for the start symbol.

---

## 4. Variant 13: Original Grammar

```text
1. S → aB
2. S → DA
3. A → a
4. A → BD
5. A → bDAB
6. B → b
7. B → BA
8. D → ε
9. D → BA
10. C → BA
```

We will apply steps 1–5 to this grammar.

---

## 5. Results for Variant 13

The transformation pipeline prints intermediate grammars at each stage when run:

1. **Initial Grammar**
2. **After ε‑elimination**
3. **After unit‑production removal**
4. **After removing useless symbols**
5. **After terminal replacement and binarization**

The final result is a CNF grammar containing only productions of the form \$A \rightarrow BC\$, \$A \rightarrow a\$, and optionally \$S \rightarrow ε\$.

---

## 6. Conclusion

We built a complete, generic converter from CFG to CNF, with visibility into each transformation step, suitable for both theoretical exploration and practical application in parser construction.

**Author**: Darzu Catalin
**Variant**: 13
**Date**: 05/05/2025

---

## 7. References

1. Chomsky, N. (1959). *On certain formal properties of grammars*. *Information and Control*.
2. Aho, A. V., & Ullman, J. D. (1972). *The Theory of Parsing, Translation, and Compiling*.
3. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.).
4. Lecture notes – Technical University of Moldova, course “Formal Languages and Finite Automata".
