from dataclasses import dataclass

@dataclass
class Automata:
    initial_state: int
    final_states: set[int]
    transitions: dict[tuple[int, str], int]

#[expr#]
def make_automata(expr: str):
    automata_tree = tree(expr+'#')
    # for char in expr:
        # pass


def tree(expr):
    if expr[-1] == '(':
        pass
    elif expr[-1] == ')':
        pass
    elif expr[-1] == '*':
        return(expr[-3],expr[-2])
    else:
        return(tree(), expr[-1])

def nullable():
    pass
def firstpos():
    pass
def lastpos():
    pass

def verify(automato,entrada):
    # b(a|b)* -> a
    estado_atual = automato.initial_state
    aceitacao = automato.final_states
    for char in entrada:
        estado_atual = automata.transitions[(estado_atual,char)]
        if not estado_atual:
            return False
    return estado_atual in aceitacao
