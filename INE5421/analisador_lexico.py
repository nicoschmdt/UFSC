from dataclasses import dataclass,field
import toml
import sys
# from typing import NamedTuple

@dataclass
class TreeNode:
    value: str
    left_node: 'TreeNode'
    right_node: 'TreeNode'
    nullable: bool = False
    first_pos: frozenset = field(default_factory=frozenset)
    last_pos: set = field(default_factory=set)
    follow_pos: set = field(default_factory=set)

@dataclass
class Automata:
    initial_state: frozenset[str]
    acceptance: frozenset[str]
    transitions: dict[tuple[frozenset[str], str], frozenset]

# metodo que explicita a concatenacao em uma expressao regular,
# para facilitar a conversao em AFD
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
    binary_operators = ['|', '.']
    precedence = {
        '|': 0,
        '.': 1,
    }
    output = []
    operator_stack = []
    for i, letter in enumerate(expr):
        if letter in binary_operators:
            if operator_stack:
                while (
                    operator_stack and
                    operator_stack[-1] != '(' and
                    precedence[operator_stack[-1]] >= precedence[letter]
                ):
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
    if symbol in ['.', '|']:
        right, right_end = tree(head)
        left, left_end = tree(right_end)
        return TreeNode(
            right_node=right,
            left_node=left,
            value=symbol,
        ), left_end
    elif symbol in ['*', '?', '+']:
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
        tree.first_pos = frozenset({number})
        tree.last_pos = frozenset({number})
        return number + 1
    else:
        if tree.left_node != None:
            number = enumerate_tree_leaf(tree.left_node,number)
        if tree.right_node != None:
            number = enumerate_tree_leaf(tree.right_node,number)
        first_pos_last_pos_and_nullable(tree)
    return number

# metodo que calcula os conjuntos firstpos, lastpos e nullable
# de cada no da arvore gerada a partir da ER
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

    elif tree.value == '+':
        tree.nullable = False
        tree.first_pos = tree.right_node.first_pos
        tree.last_pos = tree.right_node.last_pos

# metodo que calcula o conjunto followpos de cada no-folha da arvore
# gerada a partir da ER
def follow_pos(tree, terminals):
    if tree.right_node is None and tree.left_node is None:
        # print(f'follow_pos[{tree.value}] = {terminals}')
        tree.follow_pos = terminals

    elif tree.nullable:
        # print(f'{tree.value} is nullable, terminals: {tree.first_pos} | {terminals}')
        follow_pos(tree.right_node, tree.first_pos | terminals)

    elif tree.value == '.':
        follow_pos(tree.right_node, terminals)
        if tree.right_node.nullable:
            follow_pos(tree.left_node, tree.right_node.first_pos | terminals)
        else:
            follow_pos(tree.left_node, tree.right_node.first_pos)

    elif tree.value == '|':
        follow_pos(tree.left_node, terminals)
        follow_pos(tree.right_node, terminals)

def get_follow_pos_table(tree):
    table = {}
    input_symbols = set()
    stack = [tree]
    while stack:
        node = stack.pop()
        if node.left_node is not None and node.right_node is not None:
            stack.append(node.left_node)
            stack.append(node.right_node)
        elif node.right_node is not None:
            stack.append(node.right_node)
        else:
            if node.value != '#':
                input_symbols |= {node.value}
                node_number = next(iter(node.first_pos))
                table[node_number] = (node.follow_pos, node.value)
            else:
                node_number = next(iter(node.first_pos))
                table[node_number] = (frozenset(), node.value)

    return table, input_symbols

def construct_AFD(tree, number):
    follow_pos_table, input_symbols = get_follow_pos_table(tree)
    # from pprint import pprint
    # pprint(follow_pos_table)
    d_states = {tree.first_pos}
    d_transitions = {}
    marked = [tree.first_pos]
    while d_states:
        T = d_states.pop()
        marked.append(T)
        for symbol in input_symbols:
            U = set()
            for state in T:
                follow_pos, value = follow_pos_table[state]
                if symbol == value:
                    U |= follow_pos
                U = frozenset(U)
                if U and U not in marked:
                    d_states |= {U}
                d_transitions[(T, symbol)] = U

    acceptance = set()
    for state in marked:
        # print(f'{number} in {state} ? {number in state}')
        if number in state:
            acceptance |= {state}
    # print(acceptance)

    acceptance = frozenset(acceptance)
    return Automata(
        initial_state=tree.first_pos,
        acceptance=acceptance,
        transitions=d_transitions,
    )

def ER_to_AFD(expr):
    expr = insert_concat(f'({expr})#')
    rpn_list = rpn(expr)
    tree_list, _ = tree(rpn_list)
    last_leaf = enumerate_tree_leaf(tree_list, 1) - 1
    follow_pos(tree_list, set())
    return construct_AFD(tree_list, last_leaf)

def tree_to_tuple(tree):
    if tree is None:
        return None
    return (tree.value,tree_to_tuple(tree.left_node),tree_to_tuple(tree.right_node))

# metodo auxiliar que obtem todo o alfabeto da linguagem
def alphabet(automata):
    return {char for _, char in automata.transitions}


def rename_states(autom: Automata, shift: int):
    states = all_states(autom)
    state_conversion_dic = {}

    index = 0
    for state in states:
        if state:
            state_conversion_dic[state] = frozenset([index + shift])
            index += 1
        else:
            state_conversion_dic[state] = frozenset()

    new_initial_state = state_conversion_dic[autom.initial_state]

    new_acceptance_states = set()
    for estado_aceitacao in autom.acceptance:
        new_acceptance_states.add(state_conversion_dic[estado_aceitacao])

    new_transitions = {}
    for transicao in autom.transitions:
        estado_origem, caractere = transicao
        original_trans = frozenset(autom.transitions[transicao])
        new_transitions[(state_conversion_dic[estado_origem],caractere)] = state_conversion_dic[original_trans]

    renamed_automata = Automata(
        initial_state=new_initial_state,
        acceptance=frozenset(new_acceptance_states),
        transitions=new_transitions,
    )
    return renamed_automata


def join_n_with_epsilon(autom_dic: dict):
    # armazena os tamanhos dos automatos para renomear os estados por indice
    total_states = 0
    for token in autom_dic.keys():
        total_states += len(all_states(autom_dic[token]))-1

    # define os novos estados iniciais e finais como a indice e indice+
    join_initial_state = frozenset([total_states + 1])
    join_acceptance_states = []

    dicAFD_Token = {}
    renamed_autom_list = []
    total_states_until_x = 0
    for key in autom_dic.keys():
        renamed = rename_states(autom_dic[key], total_states_until_x)
        renamed_autom_list.append(renamed)

        for possibility in renamed.acceptance:
            dicAFD_Token[possibility] = key
        total_states_until_x += len(all_states(autom_dic[key]))-1

    join_transitions = {}
    for x in renamed_autom_list:
        join_transitions.update(x.transitions)

    acceptance_state =[]
    for x in renamed_autom_list:
        for former_acceptance_state in x.acceptance:
            acceptance_state.append(former_acceptance_state)
    join_acceptance_states = frozenset(acceptance_state)

    join_transitions[(join_initial_state, "&")] = frozenset({autom.initial_state for autom in renamed_autom_list})

    return (
        Automata(
            initial_state=join_initial_state,
            acceptance=join_acceptance_states,
            transitions=join_transitions,
        ),
        dicAFD_Token
    )

# metodo que recebe o automato e retorna todos os estados
def all_states(automata: Automata):
    states = {automata.acceptance} | {automata.initial_state}
    for (source, _), destiny in automata.transitions.items():
        states |= {source, destiny}
    return frozenset(states)


def e_fecho_remover(automata: Automata, state_tokens):
    def join_transitions(transition_table, sources, letter):
        # print(f'novo join pra {letter}')
        destinies = set()
        for source in sources:
            source = source if isinstance(source, frozenset) else frozenset({source})
            destinies |= transition_table.get((source, letter), frozenset())
            # print(f'source: {source}, destinies: {destinies}')

        new_destiny = frozenset(destinies)

        return new_destiny

    def e_fecho(source):
        fecho = set()
        for src in source:
            x = src if isinstance(src, frozenset) else frozenset({src})
            try:
                destiny = automata.transitions[x, '&']
                fecho |= x | e_fecho(destiny)
            except KeyError:
                destiny = frozenset({})
                fecho |= x
        fecho = frozenset(fecho)
        return fecho

    states = all_states(automata)
    new_states = set()
    _alphabet = alphabet(automata) - {'&'}
    new_transitions = {}
    acceptance = set() | automata.acceptance
    for (source, char), destiny in automata.transitions.items():
        if char == '&':
            destiny = destiny | e_fecho(destiny)
            if any(frozenset({state}) in acceptance for state in destiny):
                acceptance |= frozenset({source})
            for letter in _alphabet:
                new_destiny = join_transitions(automata.transitions, {*source, *destiny}, letter)

                if not new_destiny:
                    continue

                new_transitions[source, letter] = new_destiny

                if new_destiny not in states:
                    new_states |= {new_destiny}
        else:
            new_transitions[source, char] = destiny

    while new_states:
        new_state = new_states.pop()
        states |= {new_state}
        for letter in _alphabet:
            for state in new_state:
                if frozenset({state}) in acceptance:
                    acceptance |= frozenset({new_state})
                    # considera o novo estado como aceitação para o token
                    state_token = frozenset({state})
                    if state_token in state_tokens and new_state not in state_tokens:
                        state_tokens[new_state] = state_tokens[state_token]
            destiny = join_transitions(new_transitions, new_state, letter)

            if not destiny:
                continue

            new_transitions[new_state, letter] = destiny
            if destiny not in states:
                new_states |= {destiny}

    return Automata(
        initial_state=automata.initial_state,
        acceptance=frozenset(acceptance),
        transitions=new_transitions,
    )

# metodo que recebe o automato unido por transicoes epsilon
# e retorna o AFD equivalente
def determinize(automata: Automata, alfabeto, state_tokens):
    automata = e_fecho_remover(automata, state_tokens)
    show_automata(automata, state_tokens)

    new_transitions = {}

    states_pendentes = {automata.initial_state}
    states_feitos = set()

    old_all_states = all_states(automata)

    while states_pendentes:
        state = states_pendentes.pop()
        states_feitos |= {state}
        for caractere in alfabeto:
            # tira transições vazias
            if automata.transitions.get((state, caractere), set()):
                target = automata.transitions[(state, caractere)]
                new_transitions[state, caractere] = target
                if target not in states_feitos:
                    states_pendentes |= {target}

    new_automata = Automata(
        initial_state=automata.initial_state,
        acceptance=automata.acceptance,
        transitions=new_transitions,
    )

    new_all_states = all_states(new_automata)
    dead_states = old_all_states - new_all_states

    return Automata(
        initial_state=automata.initial_state,
        acceptance=automata.acceptance - dead_states,
        transitions=new_transitions,
    )


def expand_regexes(specs):
    return {token: expand_regex(regex) for token, regex in specs['tokens'].items()}

class InvalidRegexError(Exception):
    pass

def expand_regex(regex):
    result = ''
    option_range = []
    options = []
    bracket = False
    DIGITS_REGEX = '0123456789'
    WORDS_REGEX = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for symbol in regex:
        if symbol == ']':
            result += '|'.join(options) + ')'
            options = []
            bracket = False
        elif symbol == '[':
            result += '('
            bracket = True
        elif options or bracket:
            if not option_range or symbol == '-':
                option_range.append(symbol)
            elif option_range[-1] == '-':
                range_start_symbol = option_range[0]
                if range_start_symbol in DIGITS_REGEX and symbol in DIGITS_REGEX:
                    start = DIGITS_REGEX.find(range_start_symbol)
                    end = DIGITS_REGEX.find(symbol) + 1
                    options.extend(DIGITS_REGEX[start:end])
                elif range_start_symbol in WORDS_REGEX and symbol in WORDS_REGEX:
                    start = WORDS_REGEX.find(range_start_symbol)
                    end = WORDS_REGEX.find(symbol) + 1
                    options.extend(WORDS_REGEX[start:end])
                else:
                    raise InvalidRegexError(f'Unexpected regex range {range_start_symbol}-{symbol}')
                option_range = []
            else:
                options.extend(option_range)
                options.append(symbol)
                option_range = []
        else:
            result += symbol
    # print(f'''
    # -- expanded {regex}
    #    --    to {result}''')
    return result

def read_specs_file(path):
    with open(path) as f:
        return toml.load(f)

def get_lexemas(path):
    with open(path) as f:
        content = f.read()
        # print(f'    -- content: {content}')3
        return content.split()


def show_automata(automata, state_tokens):
    from pprint import pprint
    from dataclasses import asdict
    pprint(asdict(automata), width=80, indent=4)
    print(f'    -- state_tokens:')
    pprint(state_tokens, indent=4)


def make_automata(specs):
    automatas = {}
    tokens = expand_regexes(specs)
    for token, regex in tokens.items():
        # print(f'Criando autômato para {token}')
        automatas[token] = ER_to_AFD(regex)
        # print(f'    === Autômato para {token}')
        show_automata(automatas[token], {})

    joined_automata, state_tokens = join_n_with_epsilon(automatas)
    # print('    === Pré-deteminização:')
    # show_automata(joined_automata, state_tokens)
    alfabeto = alphabet(joined_automata) - {'&'}
    resulted_automata = determinize(joined_automata, alfabeto, state_tokens)
    state_tokens = {k: v for k, v in state_tokens.items() if k in resulted_automata.acceptance}

    print('    ===|=================')
    show_automata(resulted_automata, state_tokens)

    return resulted_automata, state_tokens


class UnknownToken(Exception):
    pass

# verify precisa conseguir reconhecer que tal estado de aceitação é referente a tal token
# mudar automata acceptance -> para relacionar

def execute(automata, lexema):
    state = frozenset(automata.initial_state)
    for char in lexema:
        try:
            state = frozenset(automata.transitions[(state, char)])
        except KeyError:
            return None
        if not state:
            return None
    return state

def tokenize(automata, lexema, state_tokens):
    def token_for(lexema):
        state = execute(automata, lexema)
        # print(f'=== {lexema} stopped at {state}')

        if state not in automata.acceptance:
            # print(f'  xx {state} not in {automata.acceptance}')
            return None

        return state_tokens[state]

    token = token_for(lexema)
    if not token:
        raise UnknownToken(lexema)

    # print(f'=== {lexema} works as a {token}!')
    return token



def analyze(specs, lexemas):
    automata, state_tokens = make_automata(specs)
    symbol_table = []
    for lexema in lexemas:
        token = tokenize(automata, lexema, state_tokens)
        symbol_table.append((lexema, token))
    return symbol_table

def main(args):
    if len(args) == 1:
        print(f'usage: {args[0]} input-file specs-file')
        return
    _, file, specs_path = args
    specs = read_specs_file(specs_path)
    lexemas = get_lexemas(file)
    # print(f'    -- lexemas: {lexemas}')
    symbol_table = analyze(specs, lexemas)
    with open('result.txt','w') as f:
        for item in symbol_table:
            f.write(f'{item}\n')


if __name__ == '__main__':
    main(sys.argv)