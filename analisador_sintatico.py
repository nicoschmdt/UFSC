import copy
import sys
from analisador_lexico import read_specs_file, get_lexemas
from typing import ClassVar

def remove_left_recursion(grammar):
    new_grammar = {}
    epsilon = ['epsilon']
    A = list(grammar.keys())
    stored = []
    for i, a_i in enumerate(A):
        name = fr"\{a_i}'"
        # eliminar recursão indireta
        for j, a_j in enumerate(A[:i]):
            new_productions = [] # fazem parte da nova G'
            production_to_add = [] # não terminais pra adicionar a nova G' no final
            for production in grammar[a_i]:
                s, *rest = production
                if a_j == s[1:]:
                    for substitute_production in new_grammar[a_j]:
                        resulted_production = substitute_production + rest
                        new_productions.append(resulted_production)
                else:
                    new_productions.append(production)
            if new_productions:
                print(f'new_productions: {new_productions}')
                grammar[a_i] = new_productions

        # eliminar recursões direta
        direct_recursion = []
        needed_for_dr = []
        for syntax in grammar[a_i]:
            to_compare, *dr = syntax
            using = to_compare[1:]
            if to_compare[0] == '\\' and a_i == using:
                direct_recursion.append(syntax)
            else:
                needed_for_dr.append(syntax)

        # syntax_nfdr -> needed for direct recursion (pensarei num nome melhor dps)
        if direct_recursion:
            for syntax_nfdr in needed_for_dr:
                if a_i not in new_grammar:
                    new_grammar[a_i] = []
                new_grammar[a_i].append(syntax_nfdr + [name])
            for syntax_dr in direct_recursion:
                new_syntax = syntax_dr[1:]
                if name not in new_grammar:
                    new_grammar[name[1:]] = []
                new_grammar[name[1:]].append(new_syntax + [name])
            new_grammar[name[1:]].append(epsilon)

    return new_grammar

# insere lista na chave se vazio, append se ja existe
def dictInsertAppend(dicionarioDict, chave, valor):
    if chave not in dicionarioDict:
        dicionarioDict[chave] = [valor]
    else:
        dicionarioDict[chave].append(valor)
    return dicionarioDict

def direct_indeterminant_productions(grammar: dict):
    sub_indeterminant_grammar = {}
    for nonterminal, productions in grammar.items():
        repetitions = {}
        for production in productions:
            head, *_ = production
            try:
                repetitions[head] += [production]
            except KeyError:
                repetitions[head] = [production]
        for head, productions in repetitions.items():
            if len(productions) > 1:
                try:
                    sub_indeterminant_grammar[nonterminal] += productions
                except KeyError:
                    sub_indeterminant_grammar[nonterminal] = productions
    return sub_indeterminant_grammar


def remove_direct_indetermination(grammar: dict):
    new_grammar = {}
    producoes_indeterminantes = direct_indeterminant_productions(grammar)

    for nonterminal, productions in grammar.items():
        new_grammar[nonterminal] = []
        for production in productions:
            if production not in producoes_indeterminantes.get(nonterminal, []):
                new_grammar[nonterminal] += [production]

    for nonterminal, productions in producoes_indeterminantes.items():
        repeated_terminals = {}
        for terminal, *tail in productions:
            # S', S'', S'''...
            suffix = "'" * (len(repeated_terminals) + 1)
            name = repeated_terminals.get(terminal, f"{nonterminal}{suffix}")
            repeated_terminals[terminal] = name

            # S' -> A | B | &
            try:
                new_grammar[name] += [tail]
            except KeyError:
                new_grammar[name] = [tail]

            # S -> aS' | bS''
            new_production = [terminal, fr'\{name}']
            try:
                if new_production not in new_grammar[nonterminal]:
                    new_grammar[nonterminal] += [new_production]
            except KeyError:
                new_grammar[nonterminal] = [new_production]

    return new_grammar

# insere set na chave se vazio, append se ja existe nao adiciona valores repetidos a set
def insert_or_union(_dict, key, value):
    if key not in _dict:
        _dict[key] = value
    else:
        _dict[key] |= value
    return _dict


def is_terminal(symbol):
    return not symbol.startswith('\\')


def is_non_terminal(symbol):
    return symbol.startswith('\\')


def get_first(grammar: dict):
    def add_firsts(production, first):
        if not production:
            return set()

        # se o first da producao ainda não foi calculado
        head, *tail = production
        if is_terminal(head):
            return {head}
        head = head[1:]

        firsts = set()
        for symbol in production:
            if is_terminal(symbol):
                symbol_first = {symbol}
            elif symbol[1:] in first:
                symbol_first = first[head]
            else:
                symbol_productions = grammar[symbol[1:]]
                symbol_first = set()
                for symbol_production in symbol_productions:
                    symbol_first |= add_firsts(symbol_production, first)
                    if 'epsilon' in symbol_first:
                        has_epsilon = True

                first[symbol[1:]] = symbol_first
            firsts |= symbol_first - {'epsilon'}
            if 'epsilon' not in symbol_first:
                break

        return firsts

    first = {}
    for head, productions in grammar.items():
        if head not in first:
            head_first = set()
            for production in productions:
                head_first |= add_firsts(production, first)
            first[head] = head_first

    return first


def get_follow(grammar: dict):
    def set_follow(production, follows, firsts, symbol):
        while production:
            head, *production = production
            if is_terminal(head):
                continue

            head = head[1:]

            head_follow = set()
            if not production:
                head_follow |= follows[symbol]

            for _next, has_more in zip(production, [*production[1:], None]):
                if is_terminal(_next):
                    head_follow |= {_next}
                else:
                    _next = _next[1:]
                    head_follow |= {first for first in firsts[_next] if first != 'epsilon'}
                    if 'epsilon' not in firsts[_next]:
                        break
                    if not has_more:
                        head_follow |= follows[symbol]
            insert_or_union(follows, head, head_follow)

    firsts = get_first(grammar)
    follows, new_follows = None, {}
    initial_symbol = next(iter(grammar))

    while follows != new_follows:
        follows = copy.deepcopy(new_follows)
        for head, productions in grammar.items():
            # adicionar $ no follow da cabeça inicial da gramatica
            for production in productions:
                if head == initial_symbol:
                    new_follows[head] = {'$'}
                symbol, *tail = production
                if is_terminal(symbol):
                    set_follow(tail, new_follows, firsts, head)
                elif is_non_terminal(symbol):
                    set_follow(production, new_follows, firsts, head)

    return follows


def remove_indirect_indetermination(grammar: dict):
    firsts = get_first(grammar)
    new_grammar = {}
    for symbol, productions in grammar.items():
        to_expand = set()
        nonterminals = set()
        # pega o simbolo inicial das produções que começam com um não terminal
        for production in productions:
            head, *tail = production
            if is_non_terminal(head):
                nonterminals |= {head}
        # dos simbolos que pegou verifica entre eles quais possuem um first em comum
        for non_terminal in nonterminals:
            for other_nonterminal in nonterminals - {non_terminal}:
                if firsts[non_terminal[1:]] & firsts[other_nonterminal[1:]]:
                    to_expand |= {non_terminal, other_nonterminal}
        # cria uma nova gramática expandindo os simbolos
        new_grammar[symbol] = []
        for production in productions:
            head, *tail = production
            if head in to_expand:
                # head_productions = grammar[head[1:]]
                for head_production in grammar[head[1:]]:
                    new_grammar[symbol] += [[*head_production,*tail]]
            else:
                new_grammar[symbol] += [production]

    return remove_direct_indetermination(new_grammar)


def fatoracao(grammar: dict):
    grammar = remove_left_recursion(grammar)
    return remove_indirect_indetermination(grammar)

def get_first_production(firsts: dict, follows: dict, production):
    production_first = []
    for symbol in production:
        if is_terminal(symbol):
            production_first += [symbol]
            return production_first

        else:
            production_first += list(firsts[symbol])
            if 'epsilon' not in firsts[symbol]:
                return production_first
    return production_first


def create_table(grammar: dict, firsts: dict, follows: dict):
    table = {}
    for nonterminal, productions in grammar.items():
        for production in productions:
            first = get_first_production(first, follows, production)
            if 'epsilon' in first:
                first.remove('epsilon')
                follow = follows[nonterminal]
                for terminal in follow:
                    table[(nonterminal,terminal)] = production
            for terminal in first:
                table[(nonterminal,terminal)] = production

    return table

def parse(lexemas, initial_symbol, table: dict):
    splitted = lexemas.split()
    stack = [initial_symbol]
    for lexema in splitted:
        while stack[-1] != lexema:
            nonterminal = stack.pop()
            if nonterminal == 'epsilon':
                continue
            try:
                production = table[(nonterminal[1:],lexema)]
            except KeyError:
                return False

            if production == 'epsilon':
                continue
            for symbol in reversed(production):
                stack.append(symbol)
        stack.pop()
    return True


def main(args):
    if len(args) == 1:
        print(f'Usage: {sys.argv[0]} input-file specs-file')
        return
    _, input_file, specs_file = args
    specs = read_specs_file(specs_file)
    lexemas = get_lexemas(input_file)
    # initial_symbol = next(iter(grammar))
    # table = create_table()
    # parsear o arquivo e verificar se percorrendo pela tabela o arquivo de entrada é aceito

if __name__ == '__main__':
    main(sys.argv)