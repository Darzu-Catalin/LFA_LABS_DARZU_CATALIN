# Parser & Abstract Syntax Tree Lab Report

**Course**: Formal Languages & Finite Automata
**Topic**: Parser & Building an Abstract Syntax Tree for Command Language
**Author**: Darzu Catalin

---

## 1. Theory

**Parsing** is the process of analyzing a sequence of tokens to determine its grammatical structure. The typical result is a **parse tree** or an **abstract syntax tree** (AST), which represents constructs hierarchically and strips away unnecessary punctuation.

An **AST** preserves the semantic relationships between nodes (commands, arguments) and omits syntactic details like keywords or delimiters, facilitating further analysis or execution.

## 2. Objectives

1. Define a `TokenType` enum for categories: `COMMAND`, `DIRECTION`, `ACTION`, `WEAPON`, `ITEM`, `SPELL`, `TARGET`, `IDENTIFIER`, `NUMBER`, `KEYWORD`, `COMMENT`, `EOF`.
2. Implement a **lexer** using regular expressions to scan input lines and emit typed tokens.
3. Design a simple AST structure (here, we use Python dictionaries for commands).
4. Build a **recursive‑descent parser** for our command DSL:

   ```bnf
   Script    → (Command)*
   Command   → COMMAND ( (KEYWORD Arg) | Arg )*
   Arg       → DIRECTION | ACTION | WEAPON | ITEM | SPELL | TARGET | NUMBER | IDENTIFIER
   ```
5. Develop a driver that lexes and parses sample scripts, then displays tokens and the parsed AST.

## 3. Implementation Details

### 3.1 `tokens.py`

Defines all the token categories:

```python
class TokenType(Enum):
    COMMAND, DIRECTION, ACTION, WEAPON, ITEM, SPELL, TARGET,
    IDENTIFIER, NUMBER, KEYWORD, COMMENT, EOF = auto(), auto(), auto(), auto(), auto(), auto(), auto(), auto(), auto(), auto(), auto(), auto()
```

### 3.2 `lexer.py`

Uses a list of regex patterns to match tokens in order. Comments (`#…`) are skipped; unrecognized substrings are reported as errors.

### 3.3 `parser.py`

Implements:

* `parse()`: loops until `EOF`, collecting commands.
* `command()`: expects a `COMMAND` token, then zero or more arguments. Each argument can be prefixed by a `KEYWORD` (e.g. `with sword`) or bare (e.g. `slash`).
* `eat()`, `advance()` helpers to consume tokens and enforce expectations.

### 3.4 `main.py`

Driver that:

1. **Lexes** each script, printing tokens and any lexer errors.
2. **Parses** into a list of command dicts, printing errors if parsing fails.
3. **Displays** parsed commands in a clear, numbered list.

---

## 4. Sample Scripts & Results

**Script 1: Movement & Combat**

```text
MOVE forward
ATTACK with sword on enemy
BLOCK left
```

```
Tokens:
  Token(COMMAND, 'MOVE')
  Token(DIRECTION, 'forward')
  Token(COMMAND, 'ATTACK')
  Token(KEYWORD, 'with')
  Token(WEAPON, 'sword')
  Token(KEYWORD, 'on')
  Token(TARGET, 'enemy')
  Token(COMMAND, 'BLOCK')
  Token(DIRECTION, 'left')
  Token(EOF, 'None')

Parsed Commands:
  1. MOVE → forward
  2. ATTACK → sword, enemy
  3. BLOCK → left
```

**Script 2: Usage & Spells**

```text
USE potion on self
CAST fireball on all
SLASH enemy
```

```
Tokens:
  Token(COMMAND, 'USE')
  Token(ITEM, 'potion')
  Token(KEYWORD, 'on')
  Token(TARGET, 'self')
  Token(COMMAND, 'CAST')
  Token(SPELL, 'fireball')
  Token(KEYWORD, 'on')
  Token(TARGET, 'all')
  Token(COMMAND, 'SLASH')
  Token(TARGET, 'enemy')
  Token(EOF, 'None')

Parsed Commands:
  1. USE → potion, self
  2. CAST → fireball, all
  3. SLASH → enemy
```

---

## 5. Conclusions

We demonstrated a full pipeline from lexing to parsing for a domain‑specific command language. The modular design allows easy extension with new commands, argument types, or syntactic patterns.

Such ASTs (here, simple dict trees) can feed into interpreters, simulators, or code generators for game logic.

---

## 6. References

* Aho, A. V., Sethi, R., & Ullman, J. D. (1986). *Compilers: Principles, Techniques, and Tools.*
* Python `re` module documentation: [https://docs.python.org/3/library/re](https://docs.python.org/3/library/re)
* Lecture notes – Technical University of Moldova, course "Formal Languages and Finite Automata".
