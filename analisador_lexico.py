from dataclasses import dataclass,field
# from typing import NamedTuple

@dataclass
class TreeNode:
    value: str
    left_node: 'TreeNode'
    right_node: 'TreeNode'
    nullable: bool
    first_pos: set = field(default_factory=set)
    last_pos: set = field(default_factory=set)
    follow_pos: set = field(default_factory=set)

@dataclass
class Automata:
    inital_state: set
    acceptance: set
    transitions: dict[tuple[set, str], set]

def insert_concat(expr):
    palavra = '().+*|'
    for i in range(len(expr)-1):
        if expr[i] not in palavra and expr[i+1] not in palavra:
            expr = expr[:i+1] + '.' + expr[i+1:]
            return insert_concat(expr)
        elif expr[i] not in '(|.' and expr[i+1] not in ')+*|.':
            expr = expr[:i+1] + '.' + expr[i+1:]
            return insert_concat(expr)
    return expr

def rpn(expr):
    binary_operators = ['|','.']
    output = []
    operator_stack = []
    for letter in expr:
        if letter in binary_operators:
            if operator_stack:
                if operator_stack[-1] in binary_operators and letter in binary_operators:
                    output.append(operator_stack.pop())
            operator_stack.append(letter)
        elif letter == '(':
            operator_stack.append(letter)
        elif letter == ')':
            while operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()
        else:
            output.append(letter)
    while operator_stack:
        output.append(operator_stack.pop())

    return output

def tree(rpn_list):
    *head, symbol = rpn_list
    if symbol in ['.','|']:
        right, right_end = tree(head)
        left, left_end = tree(right_end)
        return TreeNode(
            right_node=right,
            left_node=left,
            value=symbol,
        ), left_end
    elif symbol in ['*','?','+']:
        right, right_end = tree(head)
        return TreeNode(
            right_node=right,
            left_node=None,
            value=symbol,
        ), right_end
    else:
        return TreeNode(
            right_node=None,
            left_node=None,
            value=symbol,
        ), head

def enumerate_tree_leaf(tree,number):
    if tree.left_node == None and tree.right_node == None:
        tree.nullable = False
        tree.first_pos = {number}
        tree.last_pos = {number}
        return number + 1
    else:
        if tree.left_node != None:
            number = enumerate_tree_leaf(tree.left_node,number)
        if tree.right_node != None:
            number = enumerate_tree_leaf(tree.right_node,number)
        first_pos_last_pos_and_nullable(tree)
    return number

def first_pos_last_pos_and_nullable(tree):
    if tree.value == '|':
        tree.first_pos = tree.left_node.first_pos | tree.right_node.first_pos
        tree.last_pos = tree.left_node.last_pos | tree.right_node.last_pos
        tree.nullable = tree.left_node.nullable or tree.right_node.nullable

    elif tree.value == '.':
        tree.nullable = tree.left_node.nullable and tree.right_node.nullable
        if tree.left_node.nullable:
            tree.first_pos = tree.left_node.first_pos | tree.right_node.first_pos
        else:
            tree.first_pos = tree.left_node.first_pos
        if tree.right_node.nullable:
            tree.last_pos = tree.left_node.last_pos | tree.right_node.last_pos
        else:
            tree.last_pos = tree.right_node.last_pos

    elif tree.value == '*':
        tree.nullable = True
        tree.first_pos = tree.right_node.first_pos
        tree.last_pos = tree.right_node.last_pos

def follow_pos(tree, lista):
    if tree.right_node == None and tree.left_node == None:
        if tree.value == '#':
            tree.follow_pos = set()
        else:
            tree.follow_pos = lista

    elif tree.value in '*+':
        follow_pos(tree.left_node, tree.first_pos.union(lista))

    elif tree.value == '.':
        follow_pos(tree.right_node, lista)
        follow_pos(tree.left_node, tree.right_node.first_pos)

    elif tree.value == '|':
        follow_pos(tree.left_node, lista)
        follow_pos(tree.right_node, lista)

def get_follow_pos_table(tree):
    table = {}
    input_symbols = set()
    stack = [tree]
    while stack:
        node = stack.pop()
        if node.left_node != None and node.right_node != None:
            stack.append(node.left_node)
            stack.append(node.right_node)
        elif node.right_node != None:
            stack.append(right_node)
        else:
            input_symbols |= {node.value}
            if node.value != '#':
                table[node.first_pos.pop()] = (node.follow_pos,node.value)
    return table, input_symbols

def construct_AFD(tree,expr,number):
    follow_pos_table, input_symbols = get_follow_pos_table(tree)
    d_states = tree.first_pos
    d_transitions = {}
    symbols = set(follow_pos_table)

    # not_marked = set(follow_pos_table.keys())
    not_marked = tree.first_pos

    while not_marked:
        T = not_marked.pop()
        for symbol in input_symbols:
            U = set()
            for state in T:
                if state == follow_pos_table[state][1]:
                    U |= follow_pos_table
                if U and U not in d_states:
                    not_marked.append(U)
                d_transitions[(T,state)] = U

    acceptance_list = set()
    for state in d_states:
        if number in state:
            acceptance_list |= {state}

    return Automata(
        inital_state=tree.follow_pos,
        acceptance=acceptance_list,
        transitions=d_transitions,
    )

def ER_to_AFD(expr):
    expr = insert_concat(expr+'#')
    rpn = rpn(expr)
    tree = tree(rpn)
    last_leaf = enumerate_tree_leaf(tree) - 1
    follow_pos(tree,set())
    automata = construct_AFD(tree,expr,last_leaf)

def tree_to_tuple(tree):
    if tree is None:
        return None
    return (tree.value,tree_to_tuple(tree.left_node),tree_to_tuple(tree.right_node))

if __name__ == '__main__':
    test = rpn('a.(a|b)*.#')
    # print(tree(test))
    tree, _ = tree(test)
    print(enumerate_tree_leaf(tree,1))
    # print(tree_to_tuple(tree))
    # a.a.(a|b)*.#