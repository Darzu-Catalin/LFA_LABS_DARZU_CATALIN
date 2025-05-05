# src/parser.py

from tokens import TokenType
from lexer import Lexer, Token

class Parser:
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.tokens = self.lexer.tokenize()
        if self.lexer.has_errors():
            self.lexer.print_errors()
            raise SyntaxError("Lexer errors encountered")
        self.pos = 0
        self.current = self.tokens[0]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = Token(TokenType.EOF, None)

    def eat(self, ttype: TokenType):
        if self.current.type == ttype:
            self.advance()
        else:
            raise SyntaxError(f"Expected {ttype.name}, got {self.current.type.name}")

    def parse(self):
        commands = []
        while self.current.type != TokenType.EOF:
            commands.append(self.command())
        return commands

    def command(self):
        # 1) COMMAND
        cmd = self.current
        self.eat(TokenType.COMMAND)

        args = []
        # 2) parse any number of arguments, either prefixed or bare
        while True:
            if self.current.type == TokenType.KEYWORD:
                # prefixed: KEYWORD + arg
                self.eat(TokenType.KEYWORD)
                if self.current.type in {
                    TokenType.DIRECTION, TokenType.ACTION, TokenType.WEAPON,
                    TokenType.ITEM, TokenType.SPELL, TokenType.TARGET,
                    TokenType.NUMBER, TokenType.IDENTIFIER,
                }:
                    args.append(self.current.value)
                    self.advance()
                else:
                    raise SyntaxError(f"Unexpected argument after keyword: {self.current}")
            elif self.current.type in {
                TokenType.DIRECTION, TokenType.ACTION, TokenType.WEAPON,
                TokenType.ITEM, TokenType.SPELL, TokenType.TARGET,
                TokenType.NUMBER, TokenType.IDENTIFIER,
            }:
                # bare argument (only if none yet, or you could allow multiple)
                args.append(self.current.value)
                self.advance()
            else:
                break

        return {"command": cmd.value, "args": args}
