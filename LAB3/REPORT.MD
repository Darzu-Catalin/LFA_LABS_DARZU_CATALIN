# Lexer & Scanner
### Course: Formal Languages & Finite Automata
### Author: Darzu Catalin

----

## Theory

### Lexical Analysis and Lexers

A **lexer** (also called a scanner or tokenizer) is a fundamental component of programming language processors, such as compilers and interpreters. Its role is to break down an input string into smaller, meaningful units called tokens. These tokens represent the building blocks of a language's syntax, such as commands, directions, actions, items, or keywords.

In this project, we design a lexer for a **domain-specific language (DSL)** created for a turn-based battle game. The language is inspired by battle mechanics where a player issues commands such as moving, attacking, blocking, using items, or casting spells. The lexer identifies and categorizes these commands and their arguments into tokens based on rules defined using regular expressions.
### Domain-Specific Languages (DSLs)

A **domain-specific language** is tailored for a particular domain. Unlike general-purpose languages, DSLs are expressive and simple for specific tasks. In this lab, the DSL enables scripting battle commands, such as:
```
MOVE 10 forward
ATTACK slash with sword
USE potion on self
CAST fireball on enemy
```

These structured commands are used to control characters in a game-like simulation. Our lexer understands the syntax and breaks the commands into a structured sequence of tokens for further analysis or execution.

## Objectives

The primary objectives of this lab are to:

1. **Understand Lexical Analysis in the Context of a DSL:**
   - Learn how lexical analysis works to convert raw command text into structured tokens.
   - Recognize the importance of lexers in DSL design and execution.

2. **Design and Implement a Lexer for the Chess DSL:**
   - Define token types and their regex patterns.
   - Develop a lexer that processes battle commands.
   - Handle lexical errors and invalid tokens.

## Implementation description


### Token Specification

The lexer recognizes the following token types:


- `COMMAND: MOVE, ATTACK, BLOCK, USE, CAST`

- `DIRECTION: forward, back, left, right`

- `ACTION: slash, punch, kick, shoot`

- `WEAPON: sword, bow, dagger`

- `ITEM: potion, elixir, scroll`

- `SPELL: fireball, heal, shield, icebolt`

- `TARGET: self, enemy, allies`

- `NUMBER: integer values for steps or repetitions`

- `KEYWORD: on, with`

- `COMMENT: lines or content starting with #`

- `EOF: end of input`


### Lexer Logic

Each line of input is read and tokenized according to a prioritized list of regular expressions. The lexer processes tokens using the following steps:
### The lex method

This method has the role of tokenizing the input string into a list of tokens


1. **Regex Pattern Compilation:**
    - All token regex patterns are combined into one compiled pattern.
2. **Lexing Function:**
    - Iterate over the input string.
    - Match the next valid token using the compiled pattern.
    - If the token matches COMMENT, it is ignored.
    - If the token is not recognized (no pattern matched), a lexical error is logged.
    - Valid tokens are appended to a list.
    - Return the token list at the end.
3. **Error Handling:**
   - Any unknown word or symbol that doesn't match a token pattern results in an error, reported with line and column.

### Token Patterns Example
```
(r'\b(MOVE|ATTACK|BLOCK|USE|CAST)\b', TokenType.COMMAND)

(r'\b(forward|back|left|right)\b', TokenType.DIRECTION)

(r'\b(slash|punch|kick|shoot)\b', TokenType.ACTION)

(r'\b(sword|bow|dagger)\b', TokenType.WEAPON)

(r'\b(potion|elixir|scroll)\b', TokenType.ITEM)

(r'\b(fireball|heal|shield|icebolt)\b', TokenType.SPELL)

(r'\b(self|enemy|allies)\b', TokenType.TARGET)

(r'\b(with|on)\b', TokenType.KEYWORD)

(r'\b\d+\b', TokenType.NUMBER)
```

### Lexer Function
```python
import re
from tokens import TokenType

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}')"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.errors = []
        self.patterns = [
            (r'#.*', TokenType.COMMENT),
            (r'\b(MOVE|ATTACK|BLOCK|USE|CAST)\b', TokenType.COMMAND),
            (r'\b(forward|back|left|right)\b', TokenType.DIRECTION),
            (r'\b(slash|punch|kick|shoot)\b', TokenType.ACTION),
            (r'\b(sword|bow|dagger)\b', TokenType.WEAPON),
            (r'\b(potion|elixir|scroll)\b', TokenType.ITEM),
            (r'\b(fireball|heal|shield|icebolt)\b', TokenType.SPELL),
            (r'\b(self|enemy|allies|ally)\b', TokenType.TARGET),
            (r'\b(with|on)\b', TokenType.KEYWORD),
            (r'\b\d+\b', TokenType.NUMBER),
        ]

    def tokenize(self):
        lines = self.text.split('\n')
        for line_number, line in enumerate(lines, start=1):
            original_line = line
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            while line:
                matched = False
                for pattern, token_type in self.patterns:
                    regex = re.compile(pattern)
                    match = regex.match(line)
                    if match:
                        value = match.group(0)
                        if token_type != TokenType.COMMENT:
                            self.tokens.append(Token(token_type, value))
                        line = line[len(value):].lstrip()
                        matched = True
                        break
                if not matched:
                    broken_token = re.match(r'\S+', line)
                    if broken_token:
                        error_token = broken_token.group(0)
                        self.errors.append(
                            f"Line {line_number}: Unexpected token '{error_token}' in line: '{original_line.strip()}'"
                        )
                        line = line[len(error_token):].lstrip()
                    else:
                        break 
        self.tokens.append(Token(TokenType.EOF, None))
        return self.tokens

    def has_errors(self):
        return len(self.errors) > 0

    def print_errors(self):
        for err in self.errors:
            print("[ERROR]", err)

```


### Test cases list

This list has a set of different cases used to check the lexer' s functionality

```
test_cases = [
    ("Valid MOVE & direction", "MOVE 10 forward"),
    ("Valid MOVE backward", "MOVE 3 back"),
    ("Valid ATTACK with weapon", "ATTACK slash with sword"),
    ("Valid ATTACK without weapon", "ATTACK punch"),
    ("Valid BLOCK", "BLOCK"),
    ("Valid BLOCK with direction", "BLOCK left"),
    ("Valid USE on self", "USE potion on self"),
    ("Valid USE on group", "USE elixir on allies"),
    ("Valid CAST offensive", "CAST fireball on enemy"),
    ("Valid CAST supportive", "CAST heal on allies"),
    ("Valid CAST without target", "CAST shield"),

    ("MOVE with direction first (wrong order)", "MOVE forward 10"),
    ("MOVE with word instead of number", "MOVE fast right"),
    ("ATTACK without action", "ATTACK with sword"),
    ("USE without 'on'", "USE potion self"),
    ("CAST with unknown spell", "CAST explosion on enemy"),
    ("Unknown command", "FLY 4 forward"),
    ("Junk input", "JUMP 4 with feet"),
    ("Only keyword", "with sword"),
    ("Valid command + extra trash", "BLOCK left quickly swiftly silently"),
]
```

### Running the test cases

This for loop is used to test the lexer and input the results.

```
def run_tests():
    for idx, (label, script) in enumerate(test_cases, start=1):
        print(f"\n{'='*50}")
        print(f"TEST {idx}: {label}")
        print(f"{'-'*50}")
        print(f"Input: {script}\n")

        lexer = Lexer(script)
        tokens = lexer.tokenize()

        print("Tokens:")
        for token in tokens:
            print(token)

        if lexer.has_errors():
            print("\nErrors:")
            lexer.print_errors()
        else:
            print("\nNo errors found")
```

The way it works, is that it iterates through the **test_cases** list, calls the **tokenize** method to tokenize the input, and prints the tokens themselves.

## Results
```
==================================================
TEST 1: Valid MOVE & direction
--------------------------------------------------
Input: MOVE 10 forward

Tokens:
Token(COMMAND, 'MOVE')
Token(NUMBER, '10')
Token(DIRECTION, 'forward')
Token(EOF, 'None')

No errors found

==================================================
TEST 2: Valid MOVE backward
--------------------------------------------------
Input: MOVE 3 back

Tokens:
Token(COMMAND, 'MOVE')
Token(NUMBER, '3')
Token(DIRECTION, 'back')
Token(EOF, 'None')

No errors found

==================================================
TEST 3: Valid ATTACK with weapon
--------------------------------------------------
Input: ATTACK slash with sword

Tokens:
Token(COMMAND, 'ATTACK')
Token(ACTION, 'slash')
Token(KEYWORD, 'with')
Token(WEAPON, 'sword')
Token(EOF, 'None')

No errors found

==================================================
TEST 4: Valid ATTACK without weapon
--------------------------------------------------
Input: ATTACK punch

Tokens:
Token(COMMAND, 'ATTACK')
Token(ACTION, 'punch')
Token(EOF, 'None')

No errors found

==================================================
TEST 5: Valid BLOCK
--------------------------------------------------
Input: BLOCK

Tokens:
Token(COMMAND, 'BLOCK')
Token(EOF, 'None')

No errors found

==================================================
TEST 6: Valid BLOCK with direction
--------------------------------------------------
Input: BLOCK left

Tokens:
Token(COMMAND, 'BLOCK')
Token(DIRECTION, 'left')
Token(EOF, 'None')

No errors found

==================================================
TEST 7: Valid USE on self
--------------------------------------------------
Input: USE potion on self

Tokens:
Token(COMMAND, 'USE')
Token(ITEM, 'potion')
Token(KEYWORD, 'on')
Token(TARGET, 'self')
Token(EOF, 'None')

No errors found

==================================================
TEST 8: Valid USE on group
--------------------------------------------------
Input: USE elixir on allies

Tokens:
Token(COMMAND, 'USE')
Token(ITEM, 'elixir')
Token(KEYWORD, 'on')
Token(TARGET, 'allies')
Token(EOF, 'None')

No errors found

==================================================
TEST 9: Valid CAST offensive
--------------------------------------------------
Input: CAST fireball on enemy

Tokens:
Token(COMMAND, 'CAST')
Token(SPELL, 'fireball')
Token(KEYWORD, 'on')
Token(TARGET, 'enemy')
Token(EOF, 'None')

No errors found

==================================================
TEST 10: Valid CAST supportive
--------------------------------------------------
Input: CAST heal on allies

Tokens:
Token(COMMAND, 'CAST')
Token(SPELL, 'heal')
Token(KEYWORD, 'on')
Token(TARGET, 'allies')
Token(EOF, 'None')

No errors found

==================================================
TEST 11: Valid CAST without target
--------------------------------------------------
Input: CAST shield

Tokens:
Token(COMMAND, 'CAST')
Token(SPELL, 'shield')
Token(EOF, 'None')

No errors found

==================================================
TEST 12: MOVE with direction first (wrong order)
--------------------------------------------------
Input: MOVE forward 10

Tokens:
Token(COMMAND, 'MOVE')
Token(DIRECTION, 'forward')
Token(NUMBER, '10')
Token(EOF, 'None')

No errors found

==================================================
TEST 13: MOVE with word instead of number
--------------------------------------------------
Input: MOVE fast right

Tokens:
Token(COMMAND, 'MOVE')
Token(DIRECTION, 'right')
Token(EOF, 'None')

Errors:
[ERROR] Line 1: Unexpected token 'fast' in line: 'MOVE fast right'

==================================================
TEST 14: ATTACK without action
--------------------------------------------------
Input: ATTACK with sword

Tokens:
Token(COMMAND, 'ATTACK')
Token(KEYWORD, 'with')
Token(WEAPON, 'sword')
Token(EOF, 'None')

No errors found

==================================================
TEST 15: USE without 'on'
--------------------------------------------------
Input: USE potion self

Tokens:
Token(COMMAND, 'USE')
Token(ITEM, 'potion')
Token(TARGET, 'self')
Token(EOF, 'None')

No errors found

==================================================
TEST 16: CAST with unknown spell
--------------------------------------------------
Input: CAST explosion on enemy

Tokens:
Token(COMMAND, 'CAST')
Token(KEYWORD, 'on')
Token(TARGET, 'enemy')
Token(EOF, 'None')

Errors:
[ERROR] Line 1: Unexpected token 'explosion' in line: 'CAST explosion on enemy'

==================================================
TEST 17: Unknown command
--------------------------------------------------
Input: FLY 4 forward

Tokens:
Token(NUMBER, '4')
Token(DIRECTION, 'forward')
Token(EOF, 'None')

Errors:
[ERROR] Line 1: Unexpected token 'FLY' in line: 'FLY 4 forward'

==================================================
TEST 18: Junk input
--------------------------------------------------
Input: JUMP 4 with feet

Tokens:
Token(NUMBER, '4')
Token(KEYWORD, 'with')
Token(EOF, 'None')

Errors:
[ERROR] Line 1: Unexpected token 'JUMP' in line: 'JUMP 4 with feet'
[ERROR] Line 1: Unexpected token 'feet' in line: 'JUMP 4 with feet'

==================================================
TEST 19: Only keyword
--------------------------------------------------
Input: with sword

Tokens:
Token(KEYWORD, 'with')
Token(WEAPON, 'sword')
Token(EOF, 'None')

No errors found

==================================================
TEST 20: Valid command + extra trash
--------------------------------------------------
Input: BLOCK left quickly swiftly silently

Tokens:
Token(COMMAND, 'BLOCK')
Token(DIRECTION, 'left')
Token(EOF, 'None')

Errors:
[ERROR] Line 1: Unexpected token 'quickly' in line: 'BLOCK left quickly swiftly silently'
[ERROR] Line 1: Unexpected token 'swiftly' in line: 'BLOCK left quickly swiftly silently'
[ERROR] Line 1: Unexpected token 'silently' in line: 'BLOCK left quickly swiftly silently'
```

## Conclusion

This lab demonstrates the design and implementation of a lexer for a battle game DSL. The lexer uses regular expressions to identify tokens, process commands, and report errors. With structured test cases and robust error handling, the lexer provides a strong foundation for building more complex language features, such as a parser or interpreter.

The project emphasizes the value of domain-specific languages in simplifying user interaction within a defined context. By designing a custom command language for battle mechanics, the lexer ensures that players' inputs can be easily processed and understood by the system. This mirrors real-world applications of DSLs in areas like game scripting, chat bots, and AI behaviors.


## References

[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)

[3] [Formal Languages and Finite Automata, Guide for practical lessons](https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf)