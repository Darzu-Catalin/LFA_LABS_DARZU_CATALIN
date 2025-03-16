from lexer import Lexer

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

if __name__ == "__main__":
    print("=== Running Structured Line-by-Line Tests ===")
    run_tests()
