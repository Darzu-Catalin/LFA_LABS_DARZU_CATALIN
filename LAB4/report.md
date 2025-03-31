# Regular expressions
### Course: Formal Languages & Finite Automata
### Author: Darzu Catalin
### Variant: 1

----

## Theory

### What are regular expressions?

Regular expressions (regex or regexp) are specialized text patterns that describe search criteria. They act as a powerful query language for text, allowing you to specify complex patterns to match, extract, or manipulate strings. Developed in the 1950s by mathematician Stephen Cole Kleene as a notation for regular languages, they've become an indispensable tool in computing, text processing, and data analysis.
At their core, regex patterns define rules for matching character sequences, enabling precise text operations that would be cumbersome or impossible with simple string methods. Their compact syntax packs remarkable expressive power, making them both challenging to master and incredibly valuable once understood.

### What Are Regular Expressions Used For?

Regular expressions are essential tools for text processing across many domains. Developers use them for validating user input like email addresses or phone numbers. Data analysts employ regex for searching through large datasets to find specific patterns or extracting particular information from unstructured text.

They excel at tasks such as:
- **Validation** of formatted strings like postal codes or credit card numbers
- **Search and replace** operations in text editors and word processors
- **Data extraction** from logs, documents, or web pages

### Basic Building Blocks

**Literal Characters**: Match themselves (e.g., the character A in a pattern always matches 'A').

**Character Classes**: [aeiou] matches any single character inside the brackets, in this case a vowel.

**Quantifiers**:

* ```+``` (“zero or more”)

* ```+```(“one or more”)

* ```?``` (“zero or one”)

* ```{n}``` (“exactly n occurrences”)

* ```{m,n}``` (“between m and n occurrences”)

* **Metacharacters**: Characters like . (dot) match any single character (except possibly newlines, depending on the engine). Others such as ^, $, \b anchor a pattern to the start/end of a line or word boundary.

Formally, these constructs map cleanly onto concepts from automata theory, meaning every regular expression can be recognized by a finite state machine. This computational backing makes them efficient and robust for text processing tasks.
## Objectives

The primary objectives of this lab are to:

1. Write and cover what regular expressions are, what they are used for;
2. Write a code that will generate valid combinations of symbols conform given regular expressions by giving a set of regexes as input and get valid word as an output
3. Write a function that will show sequence of processing regular expression
## Implementation description

The key component is a regex combination generator that does three things:

1. **Tokenization**: Splits a custom regex string into recognizable tokens.

2. **Parsing Groups and Quantifiers**: Interprets each token—especially groups like ```(x|y)``` followed by possible operators like ```*, +, ?,``` or digits—for repetition counts.

3. Random Generation: Produces valid strings by choosing randomly among alternatives and repeating them the required number of times.

### tokenize method

The ```tokenize``` method has the purpose of breaking down regex patterns into understandable patterns for the code:

```
    def tokenize(self, regex_str):
        self.steps.append(f"1. Tokenizing: '{regex_str}'")

        patterns = [
            (r'\([^()]+\)(?:\*|\+|\?|\d+)?', 'group'),
            (r'[A-Za-z0-9]\*', 'zero_or_more'),
            (r'[A-Za-z0-9]\+', 'one_or_more'),
            (r'[A-Za-z0-9]\?', 'optional'),
            (r'[A-Za-z0-9]\d+', 'repeat'),
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
                if regex_str[i].isspace():
                    i += 1
                else:
                    tokens.append((regex_str[i], 'literal'))
                    i += 1

        token_summary = ", ".join([f"'{t[0]}'" for t in tokens])
        self.steps.append(f"2. Tokens identified: {token_summary}")
        return tokens
```

The way it works is that it starts by logging the tokenization step, and then defines the pattern matches for different regex elements, those elements being:
* Groups with quantifiers ```(abc)*```
* Zero-or-more ```a*```
* One-or-more ```b*```
* Optionals ```c?```
* Literal repetitions 
* Simple literals

The method has multiple layers of processing. As previously mentioned, it begins by logging the input string. After that, it defines a priority-ordered list of pattern matches, with groups being highest priority and applies patterns sequentially until all tokens are identified.

### parse_group method

This method handles the regex structures through patterns analysis, and returns both the alternatives and repetition counts, providing everything necessary for the subsequent  random generation

```
    def parse_group(self, group_token):
        match = re.match(r'\(([^()]+)\)(?:([*+?])|(\d+))?', group_token)
        if not match:
            return [group_token], [1]

        content, operator, repeat_count = match.groups()
        alternatives = [alt.strip() for alt in content.split('|')]

        if operator == '*':
            possible_counts = range(self.max_repetitions + 1)
            rep_type = "zero or more (0-5)"
        elif operator == '+':
            possible_counts = range(1, self.max_repetitions + 1)
            rep_type = "one or more (1-5)"
        elif operator == '?':
            possible_counts = range(2)
            rep_type = "optional (0-1)"
        elif repeat_count:
            count = int(repeat_count)
            possible_counts = [count]
            rep_type = f"exactly {count}"
        else:
            possible_counts = [1]
            rep_type = "exactly 1"

        self.steps.append(f"- Group '{group_token}': alternatives={alternatives}, repetition={rep_type}")
        return alternatives, possible_counts
```
The key aspects of this method are:
* Structural parsing through the usage of a regex in order to decompose groups into content and quantifiers
* It splits group content by ```|``` to identify all valid options
* Distinguishes between ```*```, ```+```, ```?``` and exact counts
* And handles bare groups without quantifiers



### The generate_combinations method

This is the core generation method which combines all the components. It has a multi-stage process, which starts by iterating through the tokens to build outputs, and then makes probabilistic choices for alternatives and repetitions. Each token type has its own custom handling:
* Literals are included as they are
* Quantifiers  generate appropriate character repetitions
* Groups trigger recursive  alternative selection
* Special cases such as exponents are getting normalized before being processed
```
 def generate_combinations(self, regex_str, count=10, seed=None):
        if seed is not None:
            random.seed(seed)

        self.steps = []
        self.steps.append(f"Processing regex: '{regex_str}'")

        normalized_regex = regex_str
        for i in range(2, 10):
            if i == 2:
                normalized_regex = normalized_regex.replace('²', '2')
            elif i == 3:
                normalized_regex = normalized_regex.replace('³', '3')
            else:
                normalized_regex = normalized_regex.replace(f'^{i}', str(i))

        tokens = self.tokenize(normalized_regex)
        combinations = []

        for i in range(count):
            combination = []
            self.steps.append(f"\ncombination #{i + 1}:")

            for token, token_type in tokens:
                if token_type == 'literal':
                    combination.append(token)
                    self.steps.append(f"- Literal '{token}': added")

                elif token_type == 'zero_or_more':
                    char = token[0]
                    rep_count = random.randint(0, self.max_repetitions)
                    combination.append(char * rep_count)
                    self.steps.append(f"- '{char}*': using {rep_count} occurrences (repetition = zero or more)")

                elif token_type == 'one_or_more':
                    char = token[0]
                    rep_count = random.randint(1, self.max_repetitions)
                    combination.append(char * rep_count)
                    self.steps.append(f"- '{char}+': using {rep_count} occurrences")

                elif token_type == 'optional':
                    char = token[0]
                    rep_count = random.randint(0, 1)
                    if rep_count == 1:
                        combination.append(char)
                        self.steps.append(f"- '{char}?': included")
                    else:
                        self.steps.append(f"- '{char}?': omitted")

                elif token_type == 'repeat':
                    match = re.match(r'([A-Za-z0-9])(\d+)', token)
                    if match:
                        char, count = match.groups()
                        count = int(count)
                        combination.append(char * count)
                        self.steps.append(f"- '{char}{count}': repeated {count} times")
                    else:
                        self.steps.append(f"- Failed to parse repeat token: '{token}'")
                        combination.append(token)

                elif token_type == 'group':
                    alternatives, possible_counts = self.parse_group(token)

                    repeat_count = random.choice(possible_counts)

                    if repeat_count > 0:
                        chosen_alternative = random.choice(alternatives)
                        group_value = chosen_alternative * repeat_count
                        self.steps.append(
                            f"- Group '{token}': selected '{chosen_alternative}' repeated {repeat_count} times")
                    else:
                        group_value = ""
                        self.steps.append(f"- Group '{token}': selected 0 repetitions")

                    combination.append(group_value)

            result = ''.join(combination)
            combinations.append(result)
            self.steps.append(f"- Result: '{result}'")

        return combinations
```

Besides that, it has step logging and provides step by step display of every decision taken by the code so that the logic of the generation behaviour becomes clearer, by mentioning each taken decision ```Literal 'K' added``` , occurrences ```'J+': using 4 occurences``` and repetitions ```repetition= zero or more```
### The main function



```
def main():
    generator = RegexCombinationGenerator(max_repetitions=5)

    example_regexes = [
        "O(P|Q|R)+ 2(3|4)",
        "A*B(C|D|E)F(G|H|I)²",
        "J+K(L|M|N)*O?(P|Q)³"
    ]

    for regex in example_regexes:
        print(f"\nGenerating combinations for: {regex}")
        combinations = generator.generate_combinations(regex, count=5)
        print("Sample combinations:")
        for combo in combinations:
            print(f"  - {combo}")

        print("\nProcessing steps:")
        for step in generator.get_processing_steps():
            print(f"  {step}")
```
The purpose of the ```main``` function is simply to demonstrage the usage of the code. The way it works is that it:
* Creates a generator instance
* Processes  the sample regex patterns
* Displays both the results and the step-by-step proccesing logic.




## Results

1. An input pattern such as:

```(a|b)(c|d)E+G? P(Q|R|S)T(UV|w|(x))*Z+ 1(0|1)* 2(3|4)^5 36```
2. The generator interprets each piece (groups, quantifiers, etc.) and, for each generated combination, logs the decisions made.

3. Typical outcomes could look like:

```acEE PSS T(x)(x)(x) ZZZ 10 2 44444 36```

```bdEEE PQR TUVUV Z 1 2 33333 36```

(and so on…)

The system chooses randomly which alternative to pick from ```(a|b)``` or ```(c|d)```, how many ```Es``` to emit for ```E+```, whether ```G?``` is included, and how many times ```(UV|W|(X))``` repeats, etc.
## Conclusion

In this lab, we covered the key ideas behind regular expressions and their theoretical underpinnings in formal language theory. We then examined a method to generate valid strings from a customized regex pattern (with basic group and quantifier support). The multi‐step approach (tokenization, parsing, combination generation) illustrates how these textual patterns can be methodically decoded and transformed into real output strings.

By bridging the gap between theoretical formalisms (like finite automata) and practical software implementations (like Python scripts), this process showcases how formal languages can be used in real‐world contexts. The result is a versatile, educational tool that aids in grasping how regex engines (and by extension, automata) methodically interpret pattern specifications.ll, this project illustrates the computational power of regular expressions and their role in automating text processing tasks. The developed solution not only reinforces the theoretical understanding of finite automata and formal languages but also has practical applications in fields like data validation, lexical analysis, and pattern recognition.


## References

[1] Stephen Cole Kleene (1951). Representation of Events in Nerve Nets and Finite Automata.

[2] Formal Languages and Finite Automata, Guide for Practical Lessons. [Available at FCIM educational site or library resources]

[3] Regular Expressions on Wikipedia: https://en.wikipedia.org/wiki/Regular_expression

[4] Official Python re Documentation: https://docs.python.org/3/library/re.html