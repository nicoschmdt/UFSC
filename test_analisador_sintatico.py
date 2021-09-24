from analisador_sintatico import (
    direct_indeterminant_productions,
    fatoracao,
    get_first,
    get_follow,
    remove_direct_indetermination,
    remove_direct_indetermination,
    remove_indirect_indetermination,
    remove_left_recursion,
    create_table,
    parse,
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

def test_remove_indirect_indetermination_jerusa_example():
    # S -> AC | BC
    # A -> aD | cC
    # B -> aB | dD
    # C -> eC | eA
    # D -> fD | CB

    # S -> aDC | cCC | aBC | dDC
    # A -> aD | cC
    # B -> aB | dD
    # C -> eC | eA
    # D -> fD | CB


    # S -> aS'| cCC | dDC
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
        "S": [["a", r"\S'"], ["c", r"\C", r"\C"], ["d", r"\D", r"\C"]],
        "S'":[[r"\D", r"\C"], [r"\B", r"\C"]],
        "A": [["a", r"\D"], ["c", r"\C"]],
        "B": [["a", r"\B"], ["d", r"\D"]],
        "C": [["e", r"\C'"]],
        "C'":[[r"\C"], [r"\A"]],
        "D": [["f", r"\D"], [r"\C", r"\B"]],
    }

    # TODO: Transformar produções em sets
    # assert remove_indirect_indetermination(grammar) == expected


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


def test_producoes_indeterminantes_a_few_more():
    # S -> aDC | cCC | aBC | dDC
    # A -> aD | cC
    # B -> aB | dD
    # C -> eC | eA
    # D -> fD | CB
    grammar = {
        'S':[
            ['a', r'\D', r'\C'],
            ['c', r'\C', r'\C'],
            ['a', r'\B', r'\C'],
            ['d', r'\D', r'\C'],
        ],
        'A':[
            ['a', r'\D'],
            ['c', r'\C'],
        ],
        'B':[
            ['a', r'\B'],
            ['d', r'\D'],
        ],
        'C':[
            ['e', r'\C'],
            ['e', r'\A'],
        ],
        'D':[
            ['f', r'\D'],
            [r'\C', r'\B'],
        ],
    }

    expected = {
        'S':[
            ['a', r'\D', r'\C'],
            ['a', r'\B', r'\C'],
        ],
        'C':[
            ['e', r'\C'],
            ['e', r'\A'],
        ],
    }

    assert direct_indeterminant_productions(grammar) == expected


def test_remove_direct_indetermination_simple():
    grammar = {
        'S':[
            ['a',r'\A'],
            ['a',r'\B',r'\C'],
            ['a',r'\D',r'\C'],
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
            [r"\B",r"\C"],
            [r"\D",r"\C"],
        ],
        'A':[
            ['c'],
        ],
        'B':[
            ['d'],
        ],
    }

    assert remove_direct_indetermination(grammar) == expected

def test_remove_direct_indetermination_slightly_complex():
    # S -> aDC | cCC | aBC | dDC
    # A -> aD | cC
    # B -> aB | dD
    # C -> eC | eA
    # D -> fD | CB
    grammar = {
        'S':[
            ['a', r'\D', r'\C'],
            ['c', r'\C', r'\C'],
            ['a', r'\B', r'\C'],
            ['d', r'\D', r'\C'],
        ],
        'A':[
            ['a', r'\D'],
            ['c', r'\C'],
        ],
        'B':[
            ['a', r'\B'],
            ['d', r'\D'],
        ],
        'C':[
            ['e', r'\C'],
            ['e', r'\A'],
        ],
        'D':[
            ['f', r'\D'],
            [r'\C', r'\B'],
        ],
    }

    expected = {
        "S": [
            ["a", r"\S'"],
            ["c", r"\C", r"\C"],
            ["d", r"\D", r"\C"]
        ],
        "S'": [
            [r"\D", r"\C"],
            [r"\B", r"\C"]
        ],
        "A": [
            ["a", r"\D"],
            ["c", r"\C"]
        ],
        "B": [
            ["a", r"\B"],
            ["d", r"\D"]
        ],
        "C": [
            ["e", r"\C'"]
        ],
        "C'":[
            [r"\C"],
            [r"\A"]
        ],
        "D": [
            ["f", r"\D"],
            [r"\C", r"\B"]
        ],
    }

    # TODO: Transformar produções em sets
    # assert remove_direct_indetermination(grammar) == expected


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

def test_simple_get_first():
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
        'S': {'a', 'b'},
        'A': {'c'},
        'B': {'d'},
        'C': {'e'},
        'D': {'f'},
    }

    assert get_first(grammar) == expected

def test_nonterminal_get_first():
    grammar = {
        'S':[
            [r'\A', r'\B', r'\C'],
        ],
        'A':[
            ['a',r'\A'],
            ['epsilon']
        ],
        'B':[
            ['b',r'\B'],
            [r'\A',r'\C','d']
        ],
        'C':[
            ['c', r'\C'],
            ['epsilon'],
        ],
    }
    expected = {
        'S':{'a', 'b', 'c', 'd'},
        'A':{'a', 'epsilon'},
        'B':{'b', 'a', 'c', 'd'},
        'C':{'c','epsilon'},
    }


    assert get_first(grammar) == expected


def test_follow():
    grammar = {
        'S':[
            [r'\A', r'\B', r'\C'],
        ],
        'A':[
            ['a',r'\A'],
            ['epsilon']
        ],
        'B':[
            ['b',r'\B'],
            [r'\A',r'\C','d']
        ],
        'C':[
            ['c', r'\C'],
            ['epsilon'],
        ],
    }
    expected = {
        'S':{'$'},
        'A':{'a', 'b', 'c', 'd'},
        'B':{'c', '$'},
        'C':{'d', '$'},
    }


    assert get_follow(grammar) == expected

# criar teste para criação da tabela

def test_table_parse_jerusa_example():
    table = {
        ('E','id'):[r'\T', r"\E'"],
        ('E','¬'):[r'\T', r"\E'"],
        ("E'",'v'):[r'v', r'\T', r"\E'"],
        ("E'",'$'):['epsilon'],
        ('T','id'):[r'\F',r"\T'"],
        ('T','¬'):[r'\F',r"\T'"],
        ("T'",'v'):['epsilon'],
        ("T'",'^'):[r'^', r'\F', r"\T'"],
        ("T'",'$'):['epsilon'],
        ('F','id'):['id'],
        ('F','¬'):['id',r'\F'],
    }
    _input = "id v id ^ id"

    assert parse(_input,r'\E', table)