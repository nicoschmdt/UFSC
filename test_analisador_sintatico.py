from analisador_sintatico import (
    remove_left_recursion,
    fatoracao,
    remove_direct_indetermination,
    direct_indeterminant_productions,
    )



def test_remove_left_recursion():
    # S -> Sa | Ab
    # A -> Sb | b

    # S -> AbS'
    # S'-> aS' | epsilon
    # A -> bA'
    # A'-> bS'bA' | epsilon

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

def test_fatoracao():

    # S -> AC | BC
    # A -> aD | cC
    # B -> aB | dD
    # C -> eC | eA
    # D -> fD | CB

    # S -> AS'| cCC | dDC
    # S'-> DC | BC
    # A -> aD | cC
    # B -> aB | dD
    # C -> eC'
    # C'-> C | A
    # D -> fD | CB

    grammar = {
        "S": [[r"\A", r"\C"], [r"\B", r"\C"]],
        "A": [["a", r"\D"], ["c", r"\C"]],
        "B": [["a", r"\B"], ["d", r"\D"]],
        "C": [["e", r"\C"], ["e", r"\A"]],
        "D": [["f", r"\D"], [r"\C", r"\B"]],

    }
    expected = {
        "S": [[r"\A", r"\S'"], ["c", r"\C", r"\C"], ["d", r"\D", r"\C"]],
        "S'":[[r"\D", r"\C"], [r"\B", r"\C"]],
        "A": [["a", r"\D"], ["c", r"\C"]],
        "B": [["a", r"\B"], ["d", r"\D"]],
        "C": [["e", r"\C'"]],
        "C'":[[r"\C"], [r"\A"]],
        "D": [["f", r"\D"], [r"\C", r"\B"]],
    }

    # assert fatoracao(grammar) == expected


def test_do_seis():
    grammar = {
        "S":[
            [r'\A', 'b'],
            [r'\A', r'\B','c']
            ],
        "B":[
            ['b', r'\B'],
            [r'\A','d'],
            ['epsilon'],
            ],
        "A":[
            [r'\A','a'],
            ['epsilon']
            ],
    }

def test_producoes_indeterminantes():
    grammar = {
        'S':[
            ['a', r'\A'],
            ['a', r'\B'],
            ['a'],
        ],
        'A':[
            ['c'],
        ],
        'B':[
            ['d'],
        ],
    }
    expected = {
        'S': [
            ['a',r'\A'],
            ['a',r'\B'],
            ['a'],
        ],
    }

    assert direct_indeterminant_productions(grammar) == expected


def test_producoes_indeterminantes_multiple_from_same_nonterminal():
    grammar = {
        'S':[
            ['a', r'\A'],
            ['a', r'\B'],
            ['a'],
            ['b', r'\A'],
            ['b', r'\B'],
        ],
        'A':[
            ['c'],
        ],
        'B':[
            ['d'],
        ],
    }
    expected = {
        'S': [
            ['a',r'\A'],
            ['a',r'\B'],
            ['a'],
            ['b', r'\A'],
            ['b', r'\B'],
        ],
    }

    assert direct_indeterminant_productions(grammar) == expected


def test_remove_direct_indetermination_simple():
    grammar = {
        'S':[
            ['a',r'\A'],
            ['a',r'\B']
        ],
        'A':[
            ['c'],
        ],
        'B':[
            ['d'],
        ],
    }
    expected = {
        'S':[
            ['a',r"\S'"],
        ],
        "S'":[
            [r"\A"],
            [r"\B"]
        ],
        'A':[
            ['c'],
        ],
        'B':[
            ['d'],
        ],
    }

    assert remove_direct_indetermination(grammar) == expected


def test_remove_direct_indetermination_multiple_on_same_nonterminal():
    grammar = {
        'S':[
            ['a', r'\A'],
            ['a', r'\B'],
            ['b', r'\C'],
            ['b', r'\D'],
        ],
        'A':[
            ['c'],
        ],
        'B':[
            ['d'],
        ],
        'C':[
            ['e'],
        ],
        'D':[
            ['f'],
        ],
    }
    expected = {
        'S':[
            ['a', r"\S'"],
            ['b', r"\S''"],
        ],
        "S'":[
            [r"\A"],
            [r"\B"],
        ],
        "S''":[
            [r"\C"],
            [r"\D"],
        ],
        'A':[
            ['c'],
        ],
        'B':[
            ['d'],
        ],
        'C':[
            ['e'],
        ],
        'D':[
            ['f'],
        ],
    }

    assert remove_direct_indetermination(grammar) == expected
