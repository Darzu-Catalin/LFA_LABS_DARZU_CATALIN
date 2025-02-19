# The title of the work

### Course: Formal Languages & Finite Automata
### Author: Dârzu Cătălin

----

## Theory
A formal language is a set of strings made from symbols in a finite alphabet, defined by rules called a grammar. Grammars are categorized into four types (Chomsky hierarchy), with regular grammars (Type-3) being the simplest.

A finite automaton (FA) is a simple machine that processes strings and decides whether they belong to a language. It has states, transitions, a start state, and accept states.

Finite automata and regular grammars are equivalent: any regular grammar can be converted into a finite automaton, and vice versa. This makes FAs essential for tasks like pattern matching, lexical analysis, and designing compilers.

In addition, understanding these models is crucial for developing efficient algorithms in computer science, as they provide the foundation for parsing, recognizing patterns, and designing compilers. The simplicity of regular grammars allows for efficient implementation and quick analysis of strings. Finite automata offer a clear, state-based method to simulate and verify the behavior of these grammars, making them highly useful in practical applications such as text processing, search engines, and network protocol design.
## Objectives:

* Discover what a language is and what it needs to have in order to be considered a formal one;
* Provide the initial setup for the evolving project that I will work on during this semester.
* Get the grammar definition and develop a code that implements a grammar class capable of generating valid strings and converting to a finite automaton with string validation functionality.

## Implementation description

### Grammar Class
* Initialization of the grammar with non-terminals (VN), terminals (VT), production rules (P), and a start symbol (S). The rules define how symbols can be replaced to generate strings.

```
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
```
* generate_strings implementation generates valid strings by recursively applying production rules. It ensures uniqueness and limits string length to 15 characters.
```
    def generate_valid_strings(self, count=5):
        results = set()
        while len(results) < count:
            candidate = self._derive(self.start_symbol)
            if candidate and len(candidate) <= self.max_depth:
                results.add(candidate)
        return list(results)
```

* to_finite_automaton implementation converts the grammar into a finite automaton. It creates states for non-terminals, defines transitions based on production rules, and sets the start and accept states.
```
    def to_finite_automaton(self):
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
```

### FiniteAutomaton Class

* Initializes the automaton with states, an alphabet, transition rules, a start state, and accept states. These define how the automaton processes input strings.
```
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
```
* check_string implementation simulates the automaton by processing each symbol in the input string. It returns True if the string ends in an accept state, otherwise False.
```
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
```
### Main function
* Creates a Grammar object, generates 5 valid strings, converts the grammar to a finite automaton, and tests a list of strings for validity.
```
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
```


* Output / Result:

<img src="img.png">


## Conclusions 
In this lab, I learned how to implement a formal grammar and a finite automaton to both generate and verify strings in a defined language. The project demonstrates how a grammar can be transformed into a finite automaton and how sample strings can be tested to determine if they conform to the language's rules. This practical exercise has clarified the theory for me and illustrated the real-world applicability of these concepts.
## References
1. Lecture notes from else