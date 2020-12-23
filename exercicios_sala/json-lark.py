# 
# Instruções: 
# 
# 1) Complete a gramática abaixo para suportar o formato JSON 
# de acordo com as especificações no json.org. 
# 
# 2) JSON é um formato bastante criticado por não possuir regra de
# comentários. Acrescente uma regra para comentários na linguagem.
# Adote o estilo de comentários C/Java, onde os comentários começam
# com // e vão até o final da linha.
#
# 3) Outra crítica ao formato JSON está no fato de não permitir uma vírgula
# opcional no final das listas e objetos. Crie suporte a estas vírgulas.
# como no exemplo abaixo.
#
#   { 
#       "nome": "Linus",
#       "os": "Linux",  // Vírgula proibida no JSON original!
#   }
#
# 4) Finalmente, uma extensão comum ao formato JSON é aceitar chaves com
# nomes de variáveis, eliminando a necessidade das aspas. Isto é um comando
# válido em Java, mas não é aceito pelo JSON. Dê suporte a chaves com
# nomes de variáveis especificados como letras e underscore seguidas de 
# qualquer número de dígitos, letras e underscores.
#
#   { 
#       nome: "Linus",
#       os: "Linux",
#   }

from lark import Lark, InlineTransformer


class JSONTransformer(InlineTransformer):
    def string(self, tk):
        return eval(tk)

    def number(self, tk):
        return float(tk)

    def true(self):
        return True
    
    def false(self):
        return False
    
    def null(self):
        return None

    def array(self, *args):
        return list(args)

    def object(self, *args,**kwargs):
        return dict(kwargs)


grammar = Lark(r"""
?start : value

?value : STRING  -> string 
       | NUMBER  -> number
       | object 
       | array
       | "true"  -> true
       | "false" -> false
       | "null"  -> null

object : "{" (key("," key)*)? "}"         // TODO

key : STRING ":" value 

array  : "[" ( value ("," value)* )?"]"  

STRING : /"([^"\\\n\r\b\f]+|\\["\\\/bfnrt]|\\u[0-9a-fA-F]{4})*"/

NUMBER : /-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/

%ignore /\s+/
""")

exemplo = r"""
{ 
	"nome": "Linus",
	"os": "Linux"
}
"""

transformer = JSONTransformer()
tree = grammar.parse(exemplo)
print(tree.pretty())

json = transformer.transform(tree)
print(json)