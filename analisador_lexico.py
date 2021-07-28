from dataclasses import dataclass

EPSILON = None

@dataclass
class Automata:
    initial_state: int
    final_state: int
    transitions: dict[tuple[int, str], int]
    n_states: int

#[expr#]
def make_automata(expr: str):

    n_states = 2
    state_number = 2

    expressions = parse(expr)


def epsilon_automata():
    return Automata(
        initial_state=0,
        final_state=1,
        transitions={(0, EPSILON): 1},
        n_states=2
    )

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

def fecho(automata):
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

def union(automata_one, automata_two):
    automata_one = increment_states_by(automata_one,2)
    automata_two = increment_states_by(automata_two,automata_one.n_states + 2)
    return Automata(
        initial_state=0,
        final_state=1,
        transitions= automata_one.transitions | automata_two.transitions |
        {(0,EPSILON):automata_one.initial_state} |
        {(0,EPSILON):automata_two.initial_state} |
        {(automata_one.final_state,EPSILON):1} |
        {(automata_two.final_state,EPSILON):1},
        n_states= automata_one.n_states + automata_two.n_states + 2
    )

def parse(expr :str):
    # ['a','a','a','b*','(a|b)']
    # (aab* | (aba)*) -> ['aab*' '|' '(aba)*'] -> ['a','b','a']
    expressions = []
    concat = ''
    # parenteses_to_close = 0
    for letter, next_letter in zip(expr[:-1], expr[1:]):

        if letter == '(' or concat:
            concat += letter

            if letter == '(':
                parenteses_to_close += 1
            elif letter == ')':
                parenteses_to_close -= 1

            if next_letter == ')':
                expressions.append(concat+next_letter)
                concat = ''

        elif letter not in ['|', '*'] and next_letter not in ['*']:
            expressions.append(letter)
        elif letter not in ['|', '*'] and next_letter == '*':
            expressions.append(letter+next_letter)
    print(expressions)





# aaab*(a|b)
# a a a b* (a|b)

# def tree(expr):


# def nullable():
#     pass
# def first_pos():
#     pass
# def last_pos():
#     pass
# def follow_pos():
#     pass

def verify(automato,entrada):
    # b(a|b)* -> a
    estado_atual = automato.initial_state
    aceitacao = automato.final_state
    for char in entrada:
        estado_atual = automata.transitions[(estado_atual,char)]
        if not estado_atual:
            return False
    return estado_atual in aceitacao


if __name__ == '__main__':
    # parse('aaab*(a|b)')
    a = concat(single_char_automata('a'),single_char_automata('b'))
    print(concat(single_char_automata('a'),a))
