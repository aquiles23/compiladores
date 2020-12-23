from pprint import pprint

ε = ()
grammar = [
    ("start", ("value",)),
    ("value", ("A",)),
    ("value", ("list",)),
    ("list", ("[", "args", "]")),
    ("args", ()),  # ε
    ("args", ("value", "tail")),
    ("tail", (",", "value", "tail")),
    ("tail", ()),  # ε
]

non_terminal = {left for (left, right) in grammar}

def is_terminal(symb):
    return symb not in non_terminal

# Inicia os conjuntos FIRST vazios
first_sets = {rule: set() for rule in grammar}
first_sets.update({symb: set() for symb in non_terminal})

# Inicia os conjuntos follow, colocando o símbolo terminal na regra 
# de start
follow_sets = {symb: set() for symb in non_terminal}
follow_sets['start'] = { '$' }


def FIRST(rule, first_sets) -> set:
    # Se a regra for do tipo name -> ε (representada aqui por uma tupla vazia)
    # acrescentamos o ε no conjunto FIRST(name)
    if not rule:
        return {ε}

    # Se o primeiro símbolo da regra for um terminal, fazemos
    # FIRST(regra) = { primeiro_symbolo }
    elif is_terminal(rule[0]):
        return {rule[0]}

    # Temos uma produção não-vazia que *não* começa com um símbolo terminal 
    # Di
    else:
        out = set()
        y, *xs = rule
        first_y = first_sets[y]

        # Atualiza o FIRST(regra) com FIRST(Y)
        out.update(first_y)

        # Verifica se ε está contido no FIRST(Y). Se estiver, fazemos
        # duas operações: 1) retiramos o ε da saída e incluímos os 
        # elementos FIRST(xs)  
        if ε in first_y:
            out.discard(ε)
            out.update(FIRST(xs, first_sets))
        return out


n_rules = 0
while True:
    for name, rule in grammar:
        conj = FIRST(rule, first_sets)
        first_sets[name].update(conj)
        first_sets[(name, rule)].update(conj)


        # Cada regra na gramática pode ser decomposta num formato do tipo
        # nome -> a B c  (onde a e c podem ser vazios).
        # Estamos interessados nas regras onde B é um não-terminal para
        # atualizarmos o conjunto FOLLOW de B.
        for i in range(len(rule)):
            B, *c = rule[i:]
            if is_terminal(B):
                continue
            
            # Se c for vazia ( nome -> a B ), então atualizamos 
            # FOLLOW(B) com todos elementos de FOLLOW(nome) 
            if not c:
                follow_sets[B].update(follow_sets[name])

            # Se c não for vazio, ( nome -> a B c ), adicionamos o
            # FIRST(c) (exceto ε) aof FOLLOW(B). Caso FIST(c) possua
            # ε, então também adicionamos FOLLOW(nome)
            else:
                first_c = FIRST(c, first_sets)
                follow_sets[B].update(first_c - {ε})

                if ε in first_c:
                    follow_sets[B].update(follow_sets[name])
                    
    
    # Verifica que se houve mudança nos conjuntos FIRST durante a última
    # iteração
    n_rules_ = sum(len(conj) for conj in first_sets.values())
    n_rules_ += sum(len(conj) for conj in follow_sets.values())
    if n_rules_ == n_rules:
        break
    else:
        n_rules = n_rules_

print('FIRST')
pprint(first_sets)

print('FOLLOW')
pprint(follow_sets)

