# src/main.py

from lexer import Lexer, Token
from parser import Parser
from tokens import TokenType

def display_tokens(tokens):
    print("Tokens:")
    for tok in tokens:
        print(f"  {tok}")
    print()

def display_commands(cmds):
    print("Parsed Commands:")
    for i, cmd in enumerate(cmds, start=1):
        name = cmd["command"]
        args = cmd["args"]
        if args:
            arg_str = ", ".join(args)
        else:
            arg_str = "(no arguments)"
        print(f"  {i}. {name} → {arg_str}")
    print()

def run_script(script: str):
    print("\n=== Script ===")
    print(script.strip(), "\n")

    # 1) Lexing
    lexer = Lexer(script)
    tokens = lexer.tokenize()
    if lexer.has_errors():
        print("Lexing errors:")
        lexer.print_errors()
        return

    display_tokens(tokens)

    # 2) Parsing
    try:
        parser = Parser(script)
        commands = parser.parse()
    except SyntaxError as e:
        print("Parsing error:", e)
        return

    display_commands(commands)

if __name__ == "__main__":
    # Example scripts
    scripts = {
        "Movement & Combat": """
            MOVE forward
            ATTACK with sword on enemy
            BLOCK left
        """,
        "Usage & Casting": """
            USE potion on self
            CAST fireball on all
            SLASH enemy
        """
    }

    for title, script in scripts.items():
        print(f"\n--- {title} ---")
        run_script(script)

    # Interactive mode
    print("Enter your own commands (type 'exit' or blank line to quit):")
    while True:
        line = input(">>> ").strip()
        if not line or line.lower() == "exit":
            break
        run_script(line)
