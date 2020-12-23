import pytest 

def eq(a, b):
    return kind(a) == kind(b) and value(a) == value(b)


def kind(tk):
    try:
        return tk.kind
    except AttributeError:
        return tk[0]

def value(tk):
    try:
        return str(tk.value)
    except AttributeError:
        return str(tk[1])


@pytest.fixture(scope='module')
def lex():
    ns = {'__name__': 'lex'}
    exec(open('lex.py').read(), ns)
    try:
        func = ns['lex']
    except KeyError:
        raise ValueError('não definiu a função lex(source) no módulo lex.py')

    return lambda src: [(kind(tk), value(tk)) for tk in func(src)]


@pytest.fixture(scope='module')
def values(lex):
    return lambda src: list(map(value, lex(src)))


@pytest.fixture(scope='module')
def kinds(lex):
    return lambda src: list(map(kind, lex(src)))


@pytest.fixture(scope='module')
def simple_lex(lex):
    get_kind = kind

    def fn(code, kind=None):
        toks = lex(code)
        assert list(map(value, toks)) == code.split()
        if kind is not None:
            for tok in toks:
                assert get_kind(tok) == kind, f'token {kind} inválida: {tok}'
        return True
    return fn


@pytest.fixture(scope='module')
def single(lex):
    def single(src):
        toks = lex(src)
        assert len(toks) == 1, f'lista de tokens com múltiplos elementos: {toks}'
        return toks[0]

    return single


class TestLexemas:
    def test_encontra_lexemas_em_caso_simples(self, values, simple_lex):
        assert values('(max x y)') == '( max x y )'.split()
        assert simple_lex('( max x y )')

    def test_classifica_tipos_em_caso_simples(self, kinds):
        assert kinds('(max x y)') == ['LPAR', 'NAME', 'NAME', 'NAME', 'RPAR']

    def test_encontra_lexemas_de_identificadores(self, simple_lex):
        assert simple_lex('x foo-bar odd? str->int %foo set-value!', kind='NAME')

    def test_encontra_lexemas_numéricos(self, simple_lex):
        assert simple_lex('1 2.0 -1 3.14 42.0 +100', kind='NUMBER')

    def test_encontra_lexemas_de_caracteres(self, simple_lex):
        assert simple_lex(r'#\a #\Backspace', kind='CHAR')

    def test_encontra_lexemas_valores_especiais(self, simple_lex):
        assert simple_lex('#t #f', kind='BOOL')

    def test_encontra_lexemas_de_strings(self, single):
        assert single('"hello-world"') == ("STRING", '"hello-world"')
        assert single('"hello world"') == ("STRING", '"hello world"')
        
    def test_aceita_escape_de_strings(self, single):
        assert single(r'"hello \"world\""') == ("STRING", r'"hello \"world\""')

    def test_aceita_símbolo_de_quote(self, values):
        assert values("'(+ 1 2)") == ["'", "(", "+", "1", "2", ")"]

    def test_aceita_comentários(self, single):
        assert single("x ;; comentário") == ('NAME', 'x')

    def test_ignora_quebras_de_linha(self, lex):
        assert lex("(sin\nx)") == [('LPAR', '('), ('NAME', 'sin'), ('NAME', 'x'), ('RPAR', ')')] 

    def test_identificadores_especiais(self, simple_lex):
        assert simple_lex('+ - ...', kind='NAME')


