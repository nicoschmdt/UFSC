from dataclasses import dataclass
from typing import NamedTuple

# metodos para fazer
# construir arvore sintatica a partir da entrada
# para isso precisa por as fun de concat os '.' (trazer função para ca)
# por fim a construção da arvore (nicole)
# fazer as funções:
# -anulavel (marcos)
# -primeira_pos
# -ultima_pos
# -pos_seguinte
# a | b -> a b |
# a.b*.a.a -> ab*.a.a.

# class TreeNode(NamedTuple):
#     left: TreeNode
#     right: TreeNode
#     value: str


def rpn(expr):
    # stack = []
    # result = []
    operators = ['|','.','*','?','+']
    binary_operators = ['|','.']
    unary_operators = ['*','?','+'] # mais precedencia
    # wait = False
    # waiting = ''
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
# def tree(rpn_list):
#     *head,symbol = rpn_list
#     if symbol in ['.','|']:
#         return TreeNode(
#             left=tree(head[:-1]),
#             right=head[-1],
#             value=symbol,
#         )
    # elif symbol == '*':
    #     return TreeNode(
    #         left=,
    #         right=,
    #         value=symbol,
        # )


if __name__ == '__main__':
    print(rpn('a.(a|b)*.a.a.#'))
    # aa.b*.