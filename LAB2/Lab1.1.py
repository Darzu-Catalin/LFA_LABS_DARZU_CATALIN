import random

class Grammar:
    def __init__(self):
        # Variant 13 definition:
        self.VN = {'S', 'B', 'D'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ['aB'],
            'B': ['aD', 'bB', 'cS'],
            'D': ['aD', 'bS', 'c']
        }
        self.start = 'S'

    def generate_string(self, max_depth=10):
        def derive(symbol, depth, derivation):
            if depth > max_depth:
                return '', derivation
            if symbol in self.VT:
                return symbol, derivation
            production = random.choice(self.P[symbol])
            derived_string = ''
            new_derivation = derivation + f"{symbol}→{production} "
            for s in production:
                result, new_derivation = derive(s, depth + 1, new_derivation)
                derived_string += result
            return derived_string, new_derivation

        return derive(self.start, 0, "")

    def generate_strings(self, count, max_depth=10):
        results = []
        for _ in range(count):
            derived_string, derivation = self.generate_string(max_depth)
            results.append((derived_string, derivation.strip()))
        return results

    def to_finite_automaton(self):
        # Map nonterminals S, B, D to states: qS, qB, qD.
        # Introduce a final state qF for terminal productions.
        states = {'qS', 'qB', 'qD', 'qF'}
        transitions = {
            # S → aB
            'qS': {
                'a': {'qB'}
            },
            # B → aD, B → bB, B → cS
            'qB': {
                'a': {'qD'},
                'b': {'qB'},
                'c': {'qS'}
            },
            # D → aD, D → bS, D → c (c leads to final state)
            'qD': {
                'a': {'qD'},
                'b': {'qS'},
                'c': {'qF'}
            }
        }
        return FiniteAutomaton(states, self.VT, transitions, 'qS', {'qF'})

    def classify_grammar(self):
        is_type_3 = True
        is_type_2 = True
        is_type_1 = True

        for non_terminal, productions in self.P.items():
            for production in productions:
                # Check for Type 3 (Regular Grammar):
                # Valid forms: A → a or A → aB or A → Ba (depending on right/left linear)
                if len(production) == 1 and production[0] in self.VT:
                    continue
                elif len(production) == 2 and production[0] in self.VT and production[1] in self.VN:
                    continue
                elif len(production) == 2 and production[0] in self.VN and production[1] in self.VT:
                    continue
                else:
                    is_type_3 = False

                # Check for Type 2 (Context-Free Grammar)
                if len(non_terminal) != 1 or non_terminal not in self.VN:
                    is_type_2 = False

                # Check for Type 1 (Context-Sensitive Grammar)
                if len(production) < len(non_terminal):
                    is_type_1 = False

        if is_type_3:
            return "Type 3 (Regular)"
        elif is_type_2:
            return "Type 2 (Context-Free)"
        elif is_type_1:
            return "Type 1 (Context-Sensitive)"
        else:
            return "Type 0 (Unrestricted)"


class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        current_states = {self.start_state}
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states.update(self.transitions[state][symbol])
            if not next_states:
                return False
            current_states = next_states
        return bool(current_states & self.accept_states)


if __name__ == "__main__":
    grammar = Grammar()
    generated_strings = grammar.generate_strings(5, max_depth=10)
    print("Generated strings with derivations:")
    for string, derivation in generated_strings:
        print(f"String: {string}, Derivation: {derivation}")

    fa = grammar.to_finite_automaton()
    test_strings = [
        "a",     # Too short for a complete derivation; likely rejected.
        "aa",    # e.g. S -> aB -> a(aD) but D never yields terminal-only.
        "ac",    # S -> aB -> a(cS) -> ... might loop.
        "aab",   # S -> aB -> a(aD) -> a(aD) -> ... possibilities.
        "aac",   # S -> aB -> a(aD) -> a(aD) ... eventually D -> c
    ]

    print("\nTesting strings in automaton:")
    for s in test_strings:
        print(f"String {s} is {'accepted' if fa.accepts(s) else 'rejected'} by FA")

    print("\nClassifying the grammar based on Chomsky hierarchy:")
    print(grammar.classify_grammar())
