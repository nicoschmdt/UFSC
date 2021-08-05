import string

palavra = '().+*|'

def insertConcat(expr):
    for i in range(len(expr)-1):
        if expr[i] not in palavra and expr[i+1] not in palavra:
            expr = expr[:i+1] + '.' + expr[i+1:]
            return insertConcat(expr)
        elif expr[i] not in '(|.' and expr[i+1] not in ')+*|.':
            expr = expr[:i+1] + '.' + expr[i+1:]
            return insertConcat(expr)
    return expr

print(insertConcat('(a|b)*a(a|b)'))