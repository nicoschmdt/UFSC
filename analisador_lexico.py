from dataclasses import dataclass,field
# from typing import NamedTuple

@dataclass
class TreeNode:
    value: str
    left_node: 'TreeNode'
    right_node: 'TreeNode'
    first_pos: set = field(default_factory=set)
    last_pos: set = field(default_factory=set)

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

# ['a','a','.','b','*','.','#','.']
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
        tree.first_pos = {number}
        tree.last_pos = {number}
        return number + 1
    else:
        if tree.left_node != None:
            number = enumerate_tree_leaf(tree.left_node,number)
        if tree.right_node != None:
            number = enumerate_tree_leaf(tree.right_node,number)
    return number

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