import copy
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

# FATORAÇÃO E FIRST?

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
        if (nonterminal, productions) not in producoes_indeterminantes.items():
            new_grammar[nonterminal] = productions

    repeated_terminals = {}
    for nonterminal, productions in producoes_indeterminantes.items():
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

def remove_indirect_indetermination():
    pass


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

    # S -> ABC | A
    # A -> aA | &
    # B -> bB | ACd
    # C -> cC | &

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


def fatoracao(grammar: dict):
    if len(direct_indeterminant_productions(grammar)) > 0:
        grammar = remove_direct_indetermination(grammar)
    get_first(grammar)
        # for x in ndd:
        #     print(f'{x}->{ndd[x]}')
    # print(f'ndd {ndd}')
    return grammar



if __name__ == '__main__':
    print('Usage: don\'t')