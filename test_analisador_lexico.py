from analisador_lexico import (
    Automata,
    construct_AFD,
    e_fecho_remover,
    enumerate_tree_leaf,
    execute,
    follow_pos,
    insert_concat,
    make_automata,
    rpn,
    tokenize,
    tree,
)

def test_insert_concat_two_letters():
    assert insert_concat('ab#') == 'a.b.#'

def test_insert_concat_or_closeset():
    assert insert_concat('(a|b)*#') == '(a|b)*.#'

def test_insert_concat_or_closeset():
    assert insert_concat('(c|(a|b)*)b#') == '(c|(a|b)*).b.#'

def test_insert_concat_aa_astar():
    assert insert_concat("(aaa*)#") == "(a.a.a*).#"

def test_rpn_aa_astar():
    assert rpn("(a.a.a*).#") == ['a', 'a', '.', 'a', '*', '.', '#', '.']

def test_rpn_concat_two_letters():
    assert rpn('(a.b).#') == ['a','b','.','#','.']

def test_rpn_concat_four_letters_with_closeset():
    assert rpn('(a.a.b*.c).#') == ['a','a','.','b','*','.','c','.','#','.']

def test_rpn_concat_five_letters_with_closeset_and_union():
    assert rpn('(a.a.b*.c|d).#') == ['a','a','.','b','*','.','c','.','d','|','#','.']

def test_rpn_concat_with_parentesis():
    assert rpn('((a.b)*|b).#') == ['a','b','.','*','b','|','#','.']

def test_rpn_or_with_closeset():
    assert rpn('((a|b)*).#') == ['a','b','|','*','#','.']

def test_rpn_or():
    concated = insert_concat('(program|end|var)#')
    test = rpn(concated)
    assert test == [
        'p','r','.','o','.','g','.','r','.','a','.','m','.',
        'e','n','.','d','.',
        '|',
        'v','a','.','r','.',
        '|',
        '#','.']

def test_accepts_first_id():
    test = [
        'p','r','.','o','.','g','.','r','.','a','.','m','.',
        'e','n','.','d','.',
        '|',
        'v','a','.','r','.',
        '|',
        '#','.']
    rpn_tree, _ = tree(test)
    last_leaf = enumerate_tree_leaf(rpn_tree,1) - 1
    follow_pos(rpn_tree,set())
    # print(rpn_tree)
    afd = construct_AFD(rpn_tree, last_leaf)
    assert execute(afd, 'var') in afd.acceptance

def test_rejects_non_id():
    test = [
        'p','r','.','o','.','g','.','r','.','a','.','m','.',
        'e','n','.','d','.',
        '|',
        'v','a','.','r','.',
        '|',
        '#','.']
    rpn_tree, _ = tree(test)
    last_leaf = enumerate_tree_leaf(rpn_tree,1) - 1
    follow_pos(rpn_tree, set())

    afd = construct_AFD(rpn_tree, last_leaf)
    assert execute(afd, 'meowmeow') not in afd.acceptance

def test_tree():
    print(tree('(a|b)*.a.b.b.#'))


def test_remove_epsilon_non_recursive():
    #      |  a  |  b  |  &
    # -----+-----+-----+-----
    #  {1} | {2} | {-} | {3}
    #  {2} | {-} | {-} | {-}
    # *{3} | {4} | {2} | {-}
    #  {4} | {1} | {2} | {-}

    initial_automata = Automata(
        initial_state=frozenset({1}),
        acceptance=frozenset({
            frozenset({3})
        }),
        transitions={
            (frozenset({1}), 'a'): frozenset({2}),
            (frozenset({1}), '&'): frozenset({3}),

            (frozenset({3}), 'a'): frozenset({4}),
            (frozenset({3}), 'b'): frozenset({2}),

            (frozenset({4}), 'a'): frozenset({1}),
            (frozenset({4}), 'b'): frozenset({2}),
        },
    )

    #         | a      | b
    # --------+--------+------
    # *{1}    | {2, 4} | {2}
    #  {2}    | {-}    | {-}
    # *{3}    | {4}    | {2}
    #  {4}    | {1}    | {2}
    #  {2, 4} | {1}    | {2}

    expected = Automata(
        initial_state=frozenset({1}),
        acceptance=frozenset({
            frozenset({1}),
            frozenset({3}),
        }),
        transitions={
            (frozenset({1}), 'a'): frozenset({2, 4}),
            (frozenset({1}), 'b'): frozenset({2}),

            (frozenset({3}), 'a'): frozenset({4}),
            (frozenset({3}), 'b'): frozenset({2}),

            (frozenset({4}), 'a'): frozenset({1}),
            (frozenset({4}), 'b'): frozenset({2}),

            (frozenset({2, 4}), 'a'): frozenset({1}),
            (frozenset({2, 4}), 'b'): frozenset({2}),
        },
    )

    assert e_fecho_remover(initial_automata, {}) == expected

def test_remove_epsilon_non_recursive_2_epsilon_transitions():
    #      |  a  |  b  |  &
    # -----+-----+-----+-----
    #  {1} | {2} | {-} | {3}
    #  {2} | {-} | {-} | {-}
    # *{3} | {4} | {2} | {4}
    #  {4} | {1} | {2} | {-}

    initial_automata = Automata(
        initial_state=frozenset({1}),
        acceptance=frozenset({
            frozenset({3}),
        }),
        transitions={
            (frozenset({1}), 'a'): frozenset({2}),
            (frozenset({1}), '&'): frozenset({3}),

            (frozenset({3}), 'a'): frozenset({4}),
            (frozenset({3}), 'b'): frozenset({2}),
            (frozenset({3}), '&'): frozenset({4}),

            (frozenset({4}), 'a'): frozenset({1}),
            (frozenset({4}), 'b'): frozenset({2}),
        },
    )

    #            | a         | b
    # -----------+-----------+------
    # *{1}       | {1, 2, 4} | {2}
    #  {2}       | {-}       | {-}
    # *{3}       | {1, 4}    | {2}
    #  {4}       | {1}       | {2}
    # *{1, 2, 4} | {1, 2, 4} | {2}
    # *{1, 4}    | {1, 2, 4} | {2}


    expected = Automata(
        initial_state=frozenset({1}),
        acceptance=frozenset({
            frozenset({1}),
            frozenset({3}),
            frozenset({1, 2, 4}),
            frozenset({1, 4})}
        ),
        transitions={
            (frozenset({1}), 'a'): frozenset({1, 2, 4}),
            (frozenset({1}), 'b'): frozenset({2}),

            (frozenset({3}), 'a'): frozenset({1, 4}),
            (frozenset({3}), 'b'): frozenset({2}),

            (frozenset({4}), 'a'): frozenset({1}),
            (frozenset({4}), 'b'): frozenset({2}),

            (frozenset({1, 2, 4}), 'a'): frozenset({1, 2, 4}),
            (frozenset({1, 2, 4}), 'b'): frozenset({2}),

            (frozenset({1, 4}), 'a'): frozenset({1, 2, 4}),
            (frozenset({1, 4}), 'b'): frozenset({2}),
        },
    )

    assert e_fecho_remover(initial_automata, {}) == expected


def test_remove_epsilon_non_recursive_2_epsilon_transitions_multitarget():
    #      |  a  |  b  |  &
    # -----+-----+-----+-----
    #  {1} | {2} | {-} | {3, 4}
    #  {2} | {-} | {-} | {-}
    # *{3} | {4} | {2} | {-}
    #  {4} | {1} | {2} | {-}

    initial_automata = Automata(
        initial_state=frozenset({1}),
        acceptance=frozenset({
            frozenset({3}),
        }),
        transitions={
            (frozenset({1}), 'a'): frozenset({2}),
            (frozenset({1}), '&'): frozenset({frozenset({3}), frozenset({4})}),

            (frozenset({3}), 'a'): frozenset({4}),
            (frozenset({3}), 'b'): frozenset({2}),

            (frozenset({4}), 'a'): frozenset({1}),
            (frozenset({4}), 'b'): frozenset({2}),
        },
    )

    #            | a         | b
    # -----------+-----------+------
    # *{1}       | {1, 2, 4} | {2}
    #  {2}       | {-}       | {-}
    # *{3}       | {4}       | {2}
    #  {4}       | {1}       | {2}
    # *{1, 2, 4} | {1, 2, 4} | {2}


    expected = Automata(
        initial_state=frozenset({1}),
        acceptance=frozenset({
            frozenset({1}),
            frozenset({3}),
            frozenset({1, 2, 4}),
        }),
        transitions={
            (frozenset({1}), 'a'): frozenset({1, 2, 4}),
            (frozenset({1}), 'b'): frozenset({2}),

            (frozenset({3}), 'a'): frozenset({4}),
            (frozenset({3}), 'b'): frozenset({2}),

            (frozenset({4}), 'a'): frozenset({1}),
            (frozenset({4}), 'b'): frozenset({2}),

            (frozenset({1, 2, 4}), 'a'): frozenset({1, 2, 4}),
            (frozenset({1, 2, 4}), 'b'): frozenset({2}),
        },
    )

    assert e_fecho_remover(initial_automata, {}) == expected


def test_tokenize_single_token():
    specs = {
        "tokens": {
            "pr": "(program|end)",
        }
    }

    automata, state_tokens = make_automata(specs)
    from pprint import pformat
    print(f'state_tokens: {pformat(state_tokens)}')

    assert tokenize(automata, "program", state_tokens) == "pr"

def test_tokenize_single_token_wildcards():
    specs = {
        "tokens": {
            "as": "aa*",
        }
    }

    automata, state_tokens = make_automata(specs)
    from pprint import pformat
    print(f'state_tokens: {pformat(state_tokens)}')

    assert tokenize(automata, "aaa", state_tokens) == "as"




def test_tokenize_two_tokens_no_wildcards():
    specs = {
        "tokens": {
            "single_a": "a",
            "multi_a": "aaa",
        }
    }

    automata, state_tokens = make_automata(specs)

    assert tokenize(automata, "a", state_tokens) == "single_a"
    assert tokenize(automata, "aaa", state_tokens) == "multi_a"


def test_tokenize_two_tokens_wildcards():
    specs = {
        "tokens": {
            "single_a": "a",
            "multi_a": "aaa*",
        }
    }

    automata, state_tokens = make_automata(specs)

    assert tokenize(automata, "a", state_tokens) == "single_a"
    assert tokenize(automata, "aa", state_tokens) == "multi_a"
    assert tokenize(automata, "aaa", state_tokens) == "multi_a"


def test_tokenize_three_token_wildcards():
    specs = {
        "tokens": {
            "single_a": "a",
            "three_a": "aaa",
            "multi_a": "aandera",
        }
    }

    automata, state_tokens = make_automata(specs)

    assert tokenize(automata, "a", state_tokens) == "single_a"
    assert tokenize(automata, "aaa", state_tokens) == "three_a"
    assert tokenize(automata, "aandera", state_tokens) == "multi_a"


def test_tokenize_multiple_token():
    specs = {
        "tokens": {
            "pr": "(program|end)",
            "id": "simpleId",
            "se": "(:=|,|;|:)",
            "op": "(-|/)",
        }
    }

    automata, state_tokens = make_automata(specs)

    assert tokenize(automata, "program", state_tokens) == "pr"
    assert tokenize(automata, "simpleId", state_tokens) == "id"
    assert tokenize(automata, ":=", state_tokens) == "se"
    assert tokenize(automata, "-", state_tokens) == "op"


def test_tokenize_simple_program():
    specs = {
        "tokens": {
            "pr": "(program|end)",
            "id": "[a-z][a-z]*",
            "se": "(:=|,|;|:)",
            "op": "(-|/)",
        }
    }

    automata, state_tokens = make_automata(specs)

    assert tokenize(automata, "program", state_tokens) == "pr"
    assert tokenize(automata, "end", state_tokens) == "pr"
    assert tokenize(automata, "aaa", state_tokens) == "id"
    assert tokenize(automata, ":=", state_tokens) == "se"
    assert tokenize(automata, "-", state_tokens) == "op"