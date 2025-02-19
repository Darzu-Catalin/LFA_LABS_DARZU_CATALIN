import random

class Grammar:
    def __init__(self):
        # Define non-terminals, terminals, and production rules for Variant 13.
        self.non_terminals = {'S', 'B', 'D'}
        self.terminals = {'a', 'b', 'c'}
        self.productions = {
            'S': ['aB'],
            'B': ['aD', 'bB', 'cS'],
            'D': ['aD', 'bS', 'c']
        }
        self.start_symbol = 'S'
        self.max_depth = 15

    def _derive(self, symbol, depth=0):
        """
        Recursively derive a string starting from the given symbol.
        Uses a depth limit to prevent infinite recursion.
        """
        if depth > self.max_depth:
            return ''
        if symbol in self.terminals:
            return symbol
        # Randomly choose one production for the current non-terminal.
        production = random.choice(self.productions[symbol])
        return ''.join(self._derive(s, depth + 1) for s in production)

    def generate_valid_strings(self, count=5):
        """
        Generates 'count' valid strings, ensuring they are non-empty
        and do not exceed the maximum length.
        """
        results = set()
        while len(results) < count:
            candidate = self._derive(self.start_symbol)
            if candidate and len(candidate) <= self.max_depth:
                results.add(candidate)
        return list(results)

    def to_finite_automaton(self):
        """
        Converts the grammar into a Finite Automaton.
        Each non-terminal becomes a state (named as 'q_<non-terminal>'),
        with an extra start state 'q_start' and an accept state 'q_accept'.
        """
        # Define states
        states = {f'q_{nt}' for nt in self.non_terminals} | {'q_start', 'q_accept'}
        transitions = {state: {} for state in states}

        # Build transitions from non-terminal states.
        for nt in self.non_terminals:
            state = f'q_{nt}'
            for prod in self.productions.get(nt, []):
                symbol = prod[0]
                if len(prod) > 1 and prod[1] in self.non_terminals:
                    next_state = f'q_{prod[1]}'
                else:
                    next_state = 'q_accept'
                transitions[state][symbol] = next_state

        # Add transitions from the dedicated start state.
        for prod in self.productions[self.start_symbol]:
            symbol = prod[0]
            if len(prod) > 1 and prod[1] in self.non_terminals:
                next_state = f'q_{prod[1]}'
            else:
                next_state = 'q_accept'
            transitions['q_start'][symbol] = next_state

        return FiniteAutomaton(states, self.terminals, transitions, 'q_start', {'q_accept'})

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        """
        Determines if the input string is accepted by the automaton.
        The string is valid if the automaton ends in one of the accept states.
        """
        current_state = self.start_state
        for char in input_string:
            if char not in self.alphabet:
                return False
            if char not in self.transitions.get(current_state, {}):
                return False
            current_state = self.transitions[current_state][char]
        return current_state in self.accept_states

def main():
    grammar = Grammar()

    # Generate and display valid strings.
    generated = grammar.generate_valid_strings(5)
    print("Generated Strings:")
    for s in generated:
        print(f"  {s}")

    # Convert grammar to finite automaton and test some strings.
    fa = grammar.to_finite_automaton()
    test_samples = [
        "aac", "abac", "abbac", "acaac", "abcaac",
        "acabbbcabcacaac", "acaaaabaabacaba"
    ]
    print("\nFinite Automaton Test Results:")
    for test in test_samples:
        status = "valid" if fa.accepts(test) else "invalid"
        print(f"  '{test}': {status}")

if __name__ == "__main__":
    main()
