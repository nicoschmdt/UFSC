
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


    from pprint import pprint
    pprint(new_grammar)
    return new_grammar