from dataclasses import dataclass

EPSILON = None

@dataclass
class Automata:
    initial_state: int
    final_state: int
    transitions: dict[tuple[int, str], int]
    n_states: int

#[expr#]

def single_char_automata(char):
    return Automata(
        initial_state=0,
        final_state=1,
        transitions={(0, char): 1},
        n_states=2
    )

def concat(automata_one, automata_two):
    automata_two = increment_states_by(automata_two,automata_one.n_states)
    automata_two = change_initial_transitions(automata_two,automata_one.final_state)
    return Automata(
        initial_state=automata_one.initial_state,
        final_state=automata_two.final_state,
        transitions=automata_one.transitions | automata_two.transitions,
        n_states=automata_one.n_states + automata_two.n_states - 1
    )

# used in concat
def change_initial_transitions(automata,new_initial_state):
    return Automata(
        initial_state=new_initial_state,
        final_state=automata.final_state,
        transitions={(src,tra):dst
            for (src,tra),dst in automata.transitions.items()
            if src != automata.initial_state}|
            {(new_initial_state,tra):dst
            for (src,tra),dst in automata.transitions.items()
            if src == automata.initial_state},
        n_states=automata.n_states
    )
    # (0,a),1 -> (3,a) -> 4
    # (0,a),1 -> (2,a),3
    # -> ((0,a),1),((1,a),3)

# used in concat
def increment_states_by(automata,quantity):
    return Automata(
        initial_state=automata.initial_state+quantity,
        final_state=automata.final_state+quantity,
        transitions={(src+quantity,tra): dst+quantity for (src,tra),dst in automata.transitions.items()},
        n_states = automata.n_states
    )

def fecho(automata): # *
    automata = increment_states_by(automata,2)
    return Automata(
        initial_state=0,
        final_state=1,
        transitions= automata.transitions |
        {(automata.final_state,EPSILON):automata.initial_state} |
        {(0,EPSILON):automata.initial_state} |
        {(automata.final_state,EPSILON):1} |
        {(0,EPSILON):1},
        n_states = automata.n_states + 2
    )

def union(automata_one, automata_two): # é o |
    automata_one = increment_states_by(automata_one,2)
    automata_two = increment_states_by(automata_two,automata_one.n_states + 2)
    return Automata(
        initial_state=0,
        final_state=1,
        transitions= automata_one.transitions | automata_two.transitions |
        {(0,EPSILON):automata_one.initial_state} |
        {(0,EPSILON):automata_two.initial_state} |
        {(automata_one.final_state,EPSILON): 1} |
        {(automata_two.final_state,EPSILON): 1},
        n_states=automata_one.n_states + automata_two.n_states + 2
    )

def parse(expr: str):
    automata = single_char_automata(EPSILON)

    i = 0
    while i < len(expr):
        letter = expr[i]
        if letter == '(':
            sub_automata, j = parse(expr[i+1:])
            i += j
            automata = concat(automata,sub_automata)
            # metodo de determinização
        elif letter == '*':
            automata = fecho(automata)
            # metodo de determinização
        elif letter == ')':
            return automata, i+1
        elif letter == '|':
            sub_automata, j = parse(expr[i+1])
            i += j
            automata = union(automata,sub_automata)
            # metodo de determinização
        else:
            new_automata = single_char_automata(letter)
            automata = concat(automata,new_automata)
        i += 1
    return automata, i

# o verify não está funcionando ok
def verify(automata,entrada):
    # b(a|b)* -> a
    estado_atual = automata.initial_state
    aceitacao = automata.final_state
    for char in entrada:
        estado_atual = automata.transitions[(estado_atual,char)]
        if not estado_atual:
            return False
    return estado_atual in aceitacao


if __name__ == '__main__':
    # print(parse('aaab*(a|b)*'))
    print(parse('(a|b)'))
    # print(verify(parse('(a|b)')[0],'ab'))
    # *b((a|b)|aa)a*')
    # a = concat(single_char_automata('a'),single_char_automata('b'))
    # print(concat(single_char_automata('a'),a))
