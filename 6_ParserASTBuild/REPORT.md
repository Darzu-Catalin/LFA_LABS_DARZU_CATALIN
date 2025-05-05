# Parser & Abstract Syntax Tree Lab Report

**Course**: Formal Languages & Finite Automata
**Topic**: Parser & Building an Abstract Syntax Tree for Command Language
**Author**: Darzu Catalin
**Date**: 05/05/2025

---

## 1. Theory

Parsing transforms a linear sequence of tokens into a hierarchical structure, enabling compilers, interpreters, and analysis tools to understand program intent. This section delves into the theoretical underpinnings of lexical analysis, parsing techniques, syntax representations, and their formal guarantees.

### 1.1 Lexical Analysis: From Regular Languages to Tokens

* **Regular Languages & Finite Automata**: Lexical analysis relies on the equivalence of regular expressions and deterministic finite automata (DFAs). Given a set of token definitions (regex patterns), we construct NFAs via Thompson’s construction, convert them to a combined DFA using subset construction, and minimize the DFA to optimize performance.
* **Maximal Munch Principle**: The scanner applies the DFA to consume the longest valid lexeme at each step, ensuring correct token boundaries (e.g., distinguishing `==` from two `=` tokens).
* **Token Attributes**: Beyond type tags, tokens often carry semantic values (e.g., integer literals, identifier names) and source position metadata for error reporting.

### 1.2 Context-Free Grammars and Syntax Trees

* **CFG Formalism**: A context-free grammar \$G = (V, \Sigma, R, S)\$ defines language syntax via productions \$A \rightarrow \alpha\$ with \$A \in V\$ and \$\alpha \in (V \cup \Sigma)^\*\$. CFGs capture nested structures and recursion inherent in programming languages.
* **Parse Tree vs. Abstract Syntax Tree (AST)**:

  * **Parse Tree**: Concrete syntax tree mirroring every grammar rule application, including terminals and nonterminals. Useful for grammar validation.
  * **AST**: A simplified tree where intermediate syntactic nodes (e.g., punctuation, optional constructs) are omitted. AST focuses on semantic constructs: commands, operations, operands.

### 1.3 Parsing Strategies: LL and LR Families

1. **LL Parsing (Top-Down)**

   * **LL(1) Grammars**: Single-token lookahead, no left recursion, and grammars must be left-factored. A predictive parser uses FIRST and FOLLOW sets to build a parse table guaranteeing \$O(n)\$ parsing time.
   * **Recursive-Descent**: Implements each nonterminal via a function. Backtracking may be introduced for ambiguous grammars but can degrade to exponential time without care.

2. **LR Parsing (Bottom-Up)**

   * **SLR(1), LALR(1), LR(1)**: Increasing lookahead and context for reduction decisions, balancing grammar support with parse table size.
   * **Shift-Reduce Algorithm**: Maintains a stack of symbols and parser states. At each step, consults ACTION and GOTO tables to shift tokens or reduce a production.
   * **Error Handling**: LR parsers detect syntax errors upon encountering an unexpected token when no valid ACTION exists, enabling error reporting at precise locations.

### 1.4 Error Detection and Recovery

* **Panic Mode**: Discard input tokens until a synchronizing set (e.g., statement terminators) appears.
* **Phrase-Level Recovery**: Use heuristics to insert or delete tokens to resume parsing; may annotate the AST with error nodes.
* **Error Productions**: Extend the grammar with productions specifically designed to catch and describe common syntax mistakes.

### 1.5 AST Design Patterns and Construction

* **Node Hierarchies**: Define a class hierarchy with base `ASTNode` and specialized subclasses (e.g., `CommandNode`, `ArgNode`). Each node stores children and relevant attributes.
* **Factory and Builder Patterns**: Centralize node instantiation, enforce invariants, and simplify extension.
* **Visitor Pattern**: Implement operations (pretty-printing, semantic analysis, code generation) separately from tree structure via double dispatch.
* **Immutability and Sharing**: ASTs can be immutable to facilitate safe sharing across compiler phases and caching analyses.

### 1.6 Domain-Specific Language (Command DSL)

Our DSL supports scripting for game commands. The EBNF grammar:

```ebnf
Script    = { Command } ;
Command   = COMMAND , { (KEYWORD , Arg) | Arg } ;
Arg       = DIRECTION | ACTION | WEAPON | ITEM | SPELL | TARGET | NUMBER | IDENTIFIER ;
```

Examples:

* `MOVE forward`
* `ATTACK with sword on enemy`
* `CAST fireball on all`

Each command node encapsulates a primary action and a list of argument nodes, optionally labeled by keywords.

### 1.7 Formal Properties and Guarantees

* **Termination and Determinism**: LL(1) and LR(1) parsing algorithms guarantee linear-time \$O(n)\$ parsing for valid or erroneous inputs, where \$n\$ is the number of tokens.
* **Correctness**: Under formal CFG assumptions, a parser either produces a parse/AST for any string in the language or reports a syntax error for strings not in the language.
* **Extensibility**: Modular design allows adding new commands and argument types by extending token patterns and grammar rules without rewriting core parsing logic.

---

## 2. Objectives

1. Define the `TokenType` enum capturing 12 categories for lexemes.
2. Implement a DFA-based lexer in `lexer.py`, optimizing for speed and maximal munch.
3. Design AST node classes in `ast.py`, supporting visitor-based traversal.
4. Implement a predictive recursive-descent parser in `parser.py`, mapping grammar rules to functions and constructing AST instances.
5. Build a `main.py` driver that tokenizes input scripts, parses them into ASTs, and serializes results in human-readable form.

---

## 3. Implementation Details

*(Detailed in `tokens.py`, `lexer.py`, `parser.py`, `ast.py`, and `main.py` with code listings and inline comments.)*

---

## 4. Sample Scripts & Results

*(Movement & Combat, Usage & Spells, plus error recovery examples with faulty input and annotated ASTs.)*

---

## 5. Conclusions

This lab demonstrates how theory—regular languages, CFGs, parsing algorithms—maps to practical implementations. The resulting pipeline transforms raw command scripts into structured ASTs, ready for semantic processing or execution.

---

---

## 6. Future Directions and Extensions

After building a basic parser and AST, further steps can expand the compiler-like toolchain:

### 6.1 Semantic Analysis

* **Symbol Table Construction**: Map identifiers and commands to definitions and scopes. Although our DSL is command-oriented, one can introduce variables and nested scopes.
* **Type Checking**: Enforce argument type constraints (e.g., `ATTACK` requires a `WEAPON` or `TARGET`, not a `SPELL`), reporting semantic errors.
* **Contextual Rules**: Validate command sequences (e.g., `MOVE forward` must precede `ATTACK`) using additional DSL-level semantics.

### 6.2 Grammar Transformations

* **Left Recursion Elimination**: For grammars with left-recursive rules, apply transformations: replace `A → A α | β` with `A → β R` and `R → α R | ε` to support recursive-descent.
* **Left Factoring**: Refactor productions sharing prefixes to eliminate parsing conflicts: transform `A → α β1 | α β2` into `A → α R`, `R → β1 | β2`.
* **Grammar Normalization**: Convert DSL grammar into Greibach or Chomsky normal form for compatibility with other parsing algorithms like CYK.

### 6.3 Advanced Parsing Techniques

* **Packrat Parsing**: Use memoization to implement linear-time PEG parsers supporting unlimited lookahead and backtracking without exponential blow-up.
* **Parser Generators**: Integrate tools like ANTLR or PLY to automatically generate lexers and parsers from grammar specifications, enabling richer language features.

### 6.4 Code Generation and Execution

* **Intermediate Representation (IR)**: Translate AST into an IR (e.g., three-address code) suitable for optimization and code emission.
* **Interpreter**: Walk the AST or IR to perform actions directly (e.g., simulate game commands) or compile to a target language (e.g., Python or bytecode).
* **Optimization Passes**: Apply transformations like command scheduling, dead code elimination (unused commands), or constant folding on numeric arguments.

### 6.5 Tooling and Visualization

* **AST Visualization**: Generate graphical representations of parse trees and ASTs using libraries like Graphviz, aiding debugging and teaching.
* **Integrated Development Environment (IDE) Support**: Provide syntax highlighting, autocomplete based on token definitions, and real-time error reporting using the lexer/parser.

---

## 7. References

* Aho, A. V., Sethi, R., & Ullman, J. D. (1986). *Compilers: Principles, Techniques, and Tools* (Dragon Book).
* Hopcroft, J. E., & Ullman, J. D. (1979). *Introduction to Automata Theory, Languages, and Computation*.
* Python `re` module documentation: [https://docs.python.org/3/library/re](https://docs.python.org/3/library/re)