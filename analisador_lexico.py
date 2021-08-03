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

class TreeNode(NamedTuple):
    left: TreeNode
    right: TreeNode
    value: str

def rpn(expr):
    operands = ['|','.']
    result = []
    wait = False
    waiting = ''
    for letter in expr:
        if letter not in operands and letter != '*':
            result.append(letter)
            if wait:
                wait = False
                result.append(waiting)
        elif letter == '*':
            if result[-1] == '.':
                result.insert(len(result)-1,letter)
            else:
                result.append(letter)
        else:
            wait = True
            waiting = letter
    return result


# ['a','a','.','b','*','.','#','.']
def tree(rpn_list):
    *head,symbol = rpn_list
    if symbol in ['.','|']:
        return TreeNode(
            left=tree(head[:-1]),
            right=head[-1],
            value=symbol,
        )
    # elif symbol == '*':
    #     return TreeNode(
    #         left=,
    #         right=,
    #         value=symbol,
        # )


if __name__ == '__main__':
    print(rpn('a.a.b*.c|d'))
    # aa.b*.