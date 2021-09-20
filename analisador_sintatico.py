
# grammar: dict[str, list[list[str | list[str]]]]
def remove_left_recursion(grammar):
    no_lr_grammar = {}
    A = list(grammar.keys())
    stored = []
    for i, a_i in enumerate(A):
        for j, a_j in enumerate(A[:i]):
            remove = [] # fazem parte da nova G'
            production_to_add = [] # não terminais pra adicionar a nova G' no final
            name = a_i + '\''
            for production in grammar[a_i]:
                s, *_ = production
                if a_j == s:
                    remove.append(s)
                elif not isinstance(s,list):
                    production_to_add.append(s)
            for production in production_to_add:
                if a_i not in no_lr_grammar:
                    no_lr_grammar[a_i] = []
                no_lr_grammar[a_i].append(production + name)
            for removed in remove:
                if name not in no_lr_grammar:
                    no_lr_grammar[name] = []
                no_lr_grammar[name].append(removed + name)
            if name not in no_lr_grammar:
                no_lr_grammar[name] = []
                if no_lr_grammar[name]:
                    no_lr_grammar[name].append("epsilon")

        # eliminar recursões direta
        direct_recursion = []
        needed_for_dr = []
        for syntax in grammar[a_i]:
            to_compare, *dr = syntax
            using = to_compare[0]
            if isinstance(to_compare, list) and a_i == using:
                direct_recursion.append(syntax)
                # needed_for_dr.append(dr)
                # verificar se é possível usar dr -> pode estar vazio
            else:
                needed_for_dr.append(syntax)

            print(f'direct_recursion: {direct_recursion}')
            print(f'needed_for_dr: {needed_for_dr}')

        if direct_recursion:
            name = [a_i + '\'']
            print(f'name: {name}')
            for syntax_nfd in needed_for_dr:
                if a_i not in no_lr_grammar:
                    no_lr_grammar[a_i] = []
                syntax_nfd.append(name)
                no_lr_grammar[a_i].append(syntax_nfd)
                print(f'syntax_nfd: {no_lr_grammar[a_i]}')
            for syntax_dr in direct_recursion:
                if name not in no_lr_grammar:
                    no_lr_grammar[name] = []
                syntax_dr.append(name)
                no_lr_grammar[name].append(syntax_dr)
                print(f'syntax_dr: {no_lr_grammar[name]}')
            no_lr_grammar[name].append('epsilon')

    return no_lr_grammar



                    # if not isinstance(s,list):
                    #     no_lr_grammar[name].append()
        #eliminar recursões diretas de P' com A'


    # for syntax_id, syntaxes in grammar.items():
    #     direct_recursion = []
    #     needed_for_dr = []
    #     for syntax in syntaxes:
    #         s, *_ = syntax
            # S = Sa | b
            #
            # S = bS'
            # S'= aS' | epsilon
            # o primeiro é um NT e a recursão é direta
            # if isinstance(s, list) and syntax_id == s:
                # direct_recursion.append(syntax)
            # else:
                # needed_for_dr.append(syntax)

            # recursão indireta

        # if direct_recursion:
        #     name = syntax_id + '\''
        #     for
        # +syntax_nfd in needed_for_dr:
        #         no_lr_grammar[syntax_id].append(syntax_nfd + name)
        #     for syntax_dr in direct_recursion:
        #         no_lr_grammar[name].append(syntax_dr + name)
        #     no_lr_grammar[name].append('epsilon')





            # recursão indireta
            # elif


        # syntax_table[syntax_id] =


