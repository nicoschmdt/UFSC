from analisador_sintatico import remove_left_recursion

# S -> Sa | Ab
# A -> Sb | b

# S -> AbS'
# S'-> aS' | epsilon
# A -> bA'
# A'-> bS'bA' | epsilon

def test_remove_left_recursion():
    grammar = {
        "S": [[r"\S", "a"], [r"\A", "b"]],
        "A": [[r"\S","b"], ["b"]]
    }
    expected = {
        "S": [[r'\A', 'b', r"\S'"]],
        "S'": [['a', r"\S'"], ['epsilon']],
        "A": [['b', r"\A'"]],
        "A'": [['b', r"\S'", 'b', r"\A'"], ['epsilon']]
    }
    assert remove_left_recursion(grammar) == expected