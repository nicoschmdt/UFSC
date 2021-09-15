from analisador_lexico import rpn, insert_concat, tree, verify, enumerate_tree_leaf, follow_pos, construct_AFD

def test_insert_concat_two_letters():
    assert insert_concat('ab#') == 'a.b.#'

def test_insert_concat_or_closeset():
    assert insert_concat('(a|b)*#') == '(a|b)*.#'

def test_insert_concat_or_closeset():
    assert insert_concat('(c|(a|b)*)b#') == '(c|(a|b)*).b.#'

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
    assert verify(afd, 'var')

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
    follow_pos(rpn_tree,set())
    # print(rpn_tree)
    afd = construct_AFD(rpn_tree, last_leaf)
    assert not verify(afd, 'meowmeow')

def test_tree():
    print(tree('(a|b)*.a.b.b.#'))