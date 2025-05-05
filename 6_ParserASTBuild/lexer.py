# src/lexer.py

import re
from tokens import TokenType

class Token:
    def __init__(self, type_: TokenType, value):
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
            (r'#.*',                   TokenType.COMMENT),
            (r'\b(MOVE|ATTACK|BLOCK|USE|CAST)\b', TokenType.COMMAND),
            (r'\b(forward|back|left|right)\b',    TokenType.DIRECTION),
            (r'\b(slash|punch|kick|shoot)\b',     TokenType.ACTION),
            (r'\b(sword|bow|dagger)\b',           TokenType.WEAPON),
            (r'\b(potion|elixir|scroll)\b',       TokenType.ITEM),
            (r'\b(fireball|heal|shield|icebolt)\b', TokenType.SPELL),
            (r'\b(self|enemy|allies|ally)\b',     TokenType.TARGET),
            (r'\b(with|on)\b',                    TokenType.KEYWORD),
            (r'\b\d+\b',                          TokenType.NUMBER),
            (r'\b[A-Za-z_]\w*\b',                 TokenType.IDENTIFIER),
        ]

    def tokenize(self):
        lines = self.text.split('\n')
        for line_number, line in enumerate(lines, start=1):
            original = line
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            while line:
                matched = False
                for pattern, ttype in self.patterns:
                    regex = re.compile(pattern)
                    m = regex.match(line)
                    if m:
                        val = m.group(0)
                        if ttype != TokenType.COMMENT:
                            self.tokens.append(Token(ttype, val))
                        line = line[len(val):].lstrip()
                        matched = True
                        break

                if not matched:
                    bad = re.match(r'\S+', line).group(0)
                    self.errors.append(
                        f"Line {line_number}: Unexpected token '{bad}' in: {original.strip()}"
                    )
                    line = line[len(bad):].lstrip()

        self.tokens.append(Token(TokenType.EOF, None))
        return self.tokens

    def has_errors(self):
        return bool(self.errors)

    def print_errors(self):
        for err in self.errors:
            print("[ERROR]", err)
