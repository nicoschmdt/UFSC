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
    inital_state: set
    acceptance: set
    transitions: dict[tuple[set, str], set]

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

# metodo que calcula o conjunto followpos de cada no-folha da arvore
# gerada a partir da ER
def follow_pos(tree, lista):
    if tree.right_node is None and tree.left_node is None:
        if tree.value == '#':
            tree.follow_pos = set()
        else:
            tree.follow_pos = lista

    elif tree.value in '*+':
        follow_pos(tree.right_node, tree.first_pos.union(lista))

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
        if node.left_node is not None and node.right_node is not None:
            stack.append(node.left_node)
            stack.append(node.right_node)
        elif node.right_node is not None:
            stack.append(node.right_node)
        else:
            if node.value != '#':
                input_symbols |= {node.value}
                node_number = next(iter(node.first_pos))
                table[node_number] = (node.follow_pos,node.value)
            else:
                node_number = next(iter(node.first_pos))
                table[node_number] = (None,None)

    return table, input_symbols

def construct_AFD(tree,expr,number):
    follow_pos_table, input_symbols = get_follow_pos_table(tree)
    d_states = [tree.first_pos]
    d_transitions = {}
    symbols = set(follow_pos_table)
    marked = [tree.first_pos]
    while d_states:
        T = d_states.pop()
        marked.append(T)
        for symbol in input_symbols:
            U = set()
            for state in T:
                if symbol == follow_pos_table[state][1]:
                    if symbol == '#':
                        U = {}
                    else:
                        U |= follow_pos_table[state][0]
                if U and U not in marked:
                    d_states.append(frozenset(U))
                d_transitions[(T,symbol)] = U

    acceptance_list = set()
    for state in marked:
        if number in state:
            acceptance_list |= {state}

    return Automata(
        inital_state=tree.first_pos,
        acceptance=acceptance_list,
        transitions=d_transitions,
    )

def ER_to_AFD(expr):
    expr = insert_concat(expr+'#')
    rpn_list = rpn(expr)
    tree_list, _ = tree(rpn_list)
    last_leaf = enumerate_tree_leaf(tree_list,1) - 1
    follow_pos(tree_list,set())
    return construct_AFD(tree_list,expr,last_leaf)

def tree_to_tuple(tree):
    if tree is None:
        return None
    return (tree.value,tree_to_tuple(tree.left_node),tree_to_tuple(tree.right_node))

# metodo auxiliar que calcula o fecho de um estado do AFND
# que sera utilizado na determinizacao do mesmo
def computarFecho(estados, automata):
    pilha = []
    fechamento = set()
    for estado in estados:
        pilha.append(estado)
        fechamento.add(estado)
    while pilha != []:
        elemento = pilha.pop()
        for transicao in automata.transitions.items():
            if elemento in transicao[0][0] and transicao[0][1] == '':
                if elemento not in fechamento:
                    fechamento.add(elemento)
                    pilha.append(elemento)
    return frozenset(fechamento)

# metodo auxiliar que obtem todo o alfabeto da linguagem
def obterAlfabeto(automata):
    alfabeto = set()
    for transition in automata.transitions.items():
        alfabeto.add(transition[0][1])
    return alfabeto


# metodo que recebe o automato unido por transicoes epsilon
# e retorna o AFD equivalente
def determinizarAutomato(automata, alfabeto):

    AFN = Automata({},{},{})
    estados_marcados = []
    estados_nao_marcados = []
    estados_nao_marcados.append(computarFecho(automata.inital_state, automata))

    while estados_nao_marcados != []:
        novoEstado = estados_nao_marcados.pop()
        estados_marcados.append(novoEstado)
        for simbolo in alfabeto:
            movimentacao = automata.transitions.get((novoEstado, simbolo))
            U = computarFecho(movimentacao, automata)
            if U not in estados_nao_marcados and U not in estados_marcados:
                estados_nao_marcados.append(U)
            AFN.transitions[(novoEstado, simbolo)] = U
    return AFN

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
    return result

def read_specs_file(path):
    with open(path) as f:
        return toml.load(f)

# melhorar como pegar os lexemas
def get_lexemas(path):
    content = ''
    with open(path) as f:
        content = f.read()
    return content.split()

def make_automata(specs):
    automata = None
    for regex in expand_regexes(specs['tokens']).values():
        if automata is None:
            automata = ER_to_AFD(regex)
        else:
            another_aut = ER_to_AFD(regex)
            # automata = union(automata,another_aut)
            pass
    # determinizar automato
    return automata

def tokenize(automata, lexema):
    pass
    # tenta rodar o automato no lexema para gerar um token
    # se funcionar retorna lexema + tipo dele

def analyze(specs, lexemas):
    automata = make_automata(specs)
    symbol_table = []
    for word in lexemas:
        lexema, lexema_type = tokenize(automata, word)
        symbol_table.append((lexema,lexema_type))
    return symbol_table

def main(args):
    _, file, specs = args
    lexemas = get_lexemas(file)
    symbol_table = analyze(specs, lexemas)
    # dar um jeito de escrever em um arquivo


# saber qual estado de aceitação parou para saber qual token foi reconhecido -> duvida

if __name__ == '__main__':
    main(sys.argv)
    # _, path = sys.argv
    # print(get_lexemas(path))
    # specs = read_specs_file(specs_path)