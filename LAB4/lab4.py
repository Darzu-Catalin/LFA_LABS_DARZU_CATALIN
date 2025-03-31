import random
import re


class CombinationGenerator:
    def __init__(self, max_repetitions=5):
        self.max_repetitions = max_repetitions
        self.steps = []

    def _normalize_regex(self, regex_str):
        """
        Normalize the input 'regex' string so we can tokenize it more easily:
          - Replace '^n' with 'n' (e.g. (3|4)^5 -> (3|4)5).
          - Replace any Unicode superscripts, e.g. '²' -> '2', '³' -> '3'.
        """
        # Handle Unicode superscripts:
        regex_str = regex_str.replace('²', '2')
        regex_str = regex_str.replace('³', '3')

        # Convert things like (3|4)^5 -> (3|4)5
        regex_str = re.sub(r'\)\^(\d+)', r')\1', regex_str)  # )^5 -> )5

        # Convert single letters/digits with ^n, e.g. X^3 -> X3
        regex_str = re.sub(r'([A-Za-z0-9])\^(\d+)', r'\1\2', regex_str)

        return regex_str

    def tokenize(self, regex_str):
        """
        Convert the normalized 'regex' string into tokens.
        Each token is either:
          - a group like '(a|b)*', '(3|4)5', etc.
          - a letter with a repetition marker: x*, x+, x?, x3
          - a multi-digit literal: e.g. '36'
          - a single character literal
        """
        self.steps.append(f"1. Tokenizing: '{regex_str}'")

        patterns = [
            # (a|b)(?:*|+|?|number)?
            (r'\([^()]+\)(?:\*|\+|\?|\d+)?', 'group'),
            # single letter + star/plus/optional or explicit digit repetition
            (r'[A-Za-z]\*', 'zero_or_more'),
            (r'[A-Za-z]\+', 'one_or_more'),
            (r'[A-Za-z]\?', 'optional'),
            (r'[A-Za-z]\d+', 'repeat'),
            # multi-digit literal (e.g. 36)
            (r'\d+', 'literal'),
            # fallback: single char (letter/digit) as literal
            (r'[A-Za-z0-9]', 'literal')
        ]

        tokens = []
        i = 0
        while i < len(regex_str):
            matched = False
            for pattern, token_type in patterns:
                match = re.match(pattern, regex_str[i:])
                if match:
                    token_text = match.group(0)
                    tokens.append((token_text, token_type))
                    i += len(token_text)
                    matched = True
                    break
            if not matched:
                # If it's whitespace, skip it; otherwise treat as literal
                if regex_str[i].isspace():
                    i += 1
                else:
                    tokens.append((regex_str[i], 'literal'))
                    i += 1

        token_summary = ", ".join(f"'{t[0]}'" for t in tokens)
        self.steps.append(f"2. Tokens identified: {token_summary}")
        return tokens

    def parse_group(self, group_token):
        """
        Parse a group of the form '(a|b)', possibly with a repetition marker.
        e.g. (a|b)*, (3|4)5, (UV|w|(x))*, etc.
        """
        match = re.match(r'\(([^()]+)\)([*+?]|\d+)?', group_token)
        if not match:
            return [group_token], [1]  # fallback

        content, operator = match.groups()
        # content -> something like 'a|b', or '3|4', or 'UV|w|(x)'
        # operator -> '*', '+', '?', or '5', etc.

        # Split the content on '|' to get alternatives
        alternatives = [alt.strip() for alt in content.split('|')]

        possible_counts = [1]  # default: exactly one
        rep_description = "exactly 1"
        if operator == '*':
            possible_counts = range(self.max_repetitions + 1)  # 0..5
            rep_description = "zero-or-more"
        elif operator == '+':
            possible_counts = range(1, self.max_repetitions + 1)  # 1..5
            rep_description = "one-or-more"
        elif operator == '?':
            possible_counts = range(2)  # 0..1
            rep_description = "optional"
        elif operator and operator.isdigit():
            # e.g. (3|4)5 means "repeat exactly 5 times"
            n = int(operator)
            possible_counts = [n]
            rep_description = f"exactly {n}"

        self.steps.append(f"- Group '{group_token}': alternatives={alternatives}, repetition={rep_description}")
        return alternatives, possible_counts

    def generate_combinations(self, regex_str, count=10, seed=None):
        """
        Generate 'count' random strings matching 'regex_str'.
        """
        if seed is not None:
            random.seed(seed)
        self.steps = [f"Processing: '{regex_str}'"]

        # 1) normalize (handle ^5, etc.)
        normalized = self._normalize_regex(regex_str)
        # 2) tokenize
        tokens = self.tokenize(normalized)

        results = []
        for c_i in range(count):
            combo = []
            self.steps.append(f"\nCombination #{c_i + 1}:")

            for token, ttype in tokens:
                if ttype == 'literal':
                    combo.append(token)
                    self.steps.append(f"  - literal '{token}' → appended")

                elif ttype == 'zero_or_more':
                    char = token[0]
                    r = random.randint(0, self.max_repetitions)
                    combo.append(char * r)
                    self.steps.append(f"  - '{char}*' → repeated {r} times")

                elif ttype == 'one_or_more':
                    char = token[0]
                    r = random.randint(1, self.max_repetitions)
                    combo.append(char * r)
                    self.steps.append(f"  - '{char}+' → repeated {r} times")

                elif ttype == 'optional':
                    char = token[0]
                    r = random.randint(0, 1)
                    if r == 1:
                        combo.append(char)
                        self.steps.append(f"  - '{char}?' → included")
                    else:
                        self.steps.append(f"  - '{char}?' → omitted")

                elif ttype == 'repeat':
                    # e.g. X3 = X repeated 3 times
                    m = re.match(r'([A-Za-z0-9])(\d+)', token)
                    if m:
                        char, num = m.groups()
                        num = int(num)
                        combo.append(char * num)
                        self.steps.append(f"  - '{char}{num}' → repeated {num} times")
                    else:
                        combo.append(token)
                        self.steps.append(f"  - unrecognized repeat '{token}'")

                elif ttype == 'group':
                    # parse group & choose randomly
                    alts, counts = self.parse_group(token)
                    chosen_count = random.choice(counts)
                    if chosen_count == 0:
                        # zero times => skip
                        combo_value = ""
                    else:
                        chosen_alt = random.choice(alts)
                        combo_value = chosen_alt * chosen_count
                    combo.append(combo_value)
                    self.steps.append(f"  - group '{token}' → '{combo_value}'")

            result = ''.join(combo)
            results.append(result)
            self.steps.append(f"  => final: '{result}'")

        return results

    def get_steps(self):
        return self.steps


# ----------------------- DEMO of "Variant 1" --------------------------------

if __name__ == "__main__":
    # This is the “Variant 1” from your image, placed on one line
    # with spaces between each piece:
    variant_1 = (
        "(a|b)(c|d)E+G? "  # line 1
        "P(Q|R|S)T(UV|W|(X))*Z+ "  # line 2
        "1(0|1)* 2(3|4)^5 36"  # line 3
    )

    gen = CombinationGenerator(max_repetitions=5)
    combinations = gen.generate_combinations(variant_1, count=10, seed=123)

    print("SAMPLE COMBINATIONS:")
    for s in combinations:
        print("  ", s)

    print("\nDETAIL STEPS:")
    for st in gen.get_steps():
        print(st)
