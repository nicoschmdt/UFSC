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

# insere lista na chave se vazio, append se ja existe nao adiciona valores repetidos a lista
def dictExclusiveInsertAppend(dicionarioDict, chave, valor):
    inserted = False
    if chave not in dicionarioDict:
        dicionarioDict[chave] = [valor]
        inserted = True
    else:
        if valor not in dicionarioDict[chave]:
            dicionarioDict[chave].append(valor)
            inserted = True
    return dicionarioDict, inserted;


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
        print(f'repetitions: {repetitions}')
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

def getFirst(grammar: dict):
    first = {}
    adicionei = True
    while adicionei:
        print(f'            rodando while')
        adicionei = False
        for cabeca in grammar:
            for producao in grammar[cabeca]:
                # epsilon
                if producao == ['epsilon']:
                    first, inserido = dictExclusiveInsertAppend(first, cabeca, producao)
                    adicionei = (adicionei | inserido)
                    print(f'adicionando epsilon a first de {cabeca}')
                    # print('continue')
                    continue

                # terminal
                if type(producao) == str:
                    first, inserido = dictExclusiveInsertAppend(first, cabeca, producao)
                    adicionei = (adicionei | inserido)
                    print(f'adicionando terminal sozinho {producao} a first de {cabeca}')
                    # print('continue')
                    continue

                # terminal
                if type(producao[0]) == str:
                    first, inserido = dictExclusiveInsertAppend(first, cabeca, producao[0])
                    adicionei = (adicionei | inserido)
                    print(f'adicionando terminal {producao[0]} em first de {cabeca}')
                    # print('continue')
                    continue
                print(f'passei reto com {producao}')

                # n terminal
                if type(producao[0]) == list:
                    if producao[0][0] in first:
                        print(f'a producao que eu to olhando é {producao[0][0]}, cabeca {cabeca}')
                        print(first)
                        espandir = False
                        tryExtend = copy.deepcopy(first)
                        if cabeca not in tryExtend:
                            tryExtend[cabeca] = first[producao[0][0][0]]
                        else:
                            tryExtend[cabeca].extend(first[producao[0][0][0]])
                        print(tryExtend)
                        print(first)
                        first, inserido = dictExclusiveInsertAppend(first, cabeca, first[producao[0][0]])
                        adicionei = (adicionei | inserido)
                        print(f'expandindo por nao terminal {producao[0]} em first de {cabeca} com {first[producao[0][0]]}')
                        # print('continue')
                        continue
                print(f'passei reto com {producao}')

    for cabeca in grammar:
        for producao in grammar[cabeca]:
            # nterminal
            for x in producao[0]:
                pass
    for x in first:
        print(f'first[{x}] = {first[x]}')
    return first




def fatoracao(grammar: dict):
    if len(direct_indeterminant_productions(grammar)) > 0:
        grammar = remove_direct_indetermination(grammar)
    getFirst(grammar)
        # for x in ndd:
        #     print(f'{x}->{ndd[x]}')
    # print(f'ndd {ndd}')
    return grammar



if __name__ == '__main__':
    print('Usage: don\'t')