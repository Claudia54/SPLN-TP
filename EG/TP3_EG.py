from lark import Lark, Transformer, Visitor, Discard, Token,Tree
from lark.visitors import Interpreter
from collections import Counter
from pydot import Dot, Node, Edge
from aux import *
from lark.tree import pydot__tree_to_png
import pprint
import pygraphviz as pgv

grammar2 = '''
// Regras Sintaticas
start: codigo +
codigo : def_func | linhas
        
linhas : linha+

linha   :while_loop
        | if_statement
        | for_loop
        | create
        | atribuicao
        | do_while_statement
        | print_statement
        | input_statement   


print_statement: "print" "("  STRING ("," VAR)? ")" -> print_string
                | "print" "("  VAR ")" -> print_var

input_statement: "input" "("  STRING "," VAR ")" -> input_string
                | "input" "("  VAR ")"   -> input_var       

atribuicao : (TYPE)? VAR "=" expressao
           | (TYPE)? VAR "=" est_dados
           | func_atr "=" expressao
           | func_atr "=" est_dados
     

create: TYPE VAR

expressao : expressao "+" expressao -> adicao   
         | expressao "-" expressao -> subtracao
         | expressao "*" expressao -> multiplicacao
         | expressao "/" expressao -> divisao
         | expressao -> exp_exp
         | val -> exp_val
         | func
         | func_atr

est_dados: dict 
         | array
         | tuple
         | list 

func : VAR "(" val ")"
func_atr : VAR "[" def_val "]"

bool_expressao : expressao "<" expressao  -> menor
            | expressao "<=" expressao    -> menor_igual
            | expressao ">" expressao     -> maior
            | expressao ">=" expressao    -> maior_igual
            | expressao "==" expressao    -> igual
            | expressao "!=" expressao    -> diferente
            | (expressao|bool_expressao) ("&&" (expressao|bool_expressao))+   -> bool_and    
            | (expressao|bool_expressao) ("||" (expressao|bool_expressao))+   -> bool_or  

def_func : TYPE VAR def_list  "{" linhas ("return" val)? "}"

while_loop : "while" "(" bool_expressao ")" "{" linhas "}"

do_while_statement :  "do"  "{" linhas "}" "while" "(" bool_expressao ")"


if_statement : "if" "(" bool_expressao ")" "{" linhas "}" elif_statement* else_statement?
elif_statement : "elif" "(" bool_expressao ")" "{" linhas "}"
else_statement : "else" "{" linhas "}"


intervalo : VAR 
          | array

for_loop : "for" VAR "in" intervalo "{" linhas "}"

list : "(" (val ("," val)*)? ")"

def_list: "(" (def_val ("," def_val)*)? ")"

array : "[" (val ("," val)*) ? "]"

dict : "{" pair+ "}"

pair : key ":" val

key: STRING | NUMERO

tuple : "(" val "," val ")"

val : STRING
    | NUMERO
    | VAR
    | BOOLEAN

def_val : STRING
    | NUMERO
    | VAR


// Regras Lexicográficas
NUMERO:/\d+(\.[0-9]+)?/
SIMB: /\+|\-/
CONS: /(cons)/   
SNOC: /(snoc)/
PONTO: "."
IN: "in"
FOR: "for"
IF: "if"
ELSE: "else"
WHILE: "while"
ELIF: "elif"
TYPE:/(numero|string|dict|list|array\b)/
BOOLEAN: /True|False/
VAR: /[a-zA-Z][a-zA-Z0-9_]*/
STRING: /"([^"]+)"/
RETURN : "return"




// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase = "+ [100,200][3,12]"



texto1 ="""
print("w")
do{
print("A")
print("b")
}while(i < 10)
print("x")
""" 


texto2 ="""
string variavel
dict a
print("asa")
a = {"hoje":3}
numero myfunction(number, y, z){
                numero x
                numero b
                if(number<5){
                        x=x+1
                }else{
                        x=x-1
                }
                return x
        }
numero e
numero i = a[\"hoje\"]
numero i = 3
numero w = 6
print("Computador:",w)
input(t)
a[\"hoje\"] = 5
while(i < 10){
        x = myfunction(x)
        if(i == 5){
                i = i +2
        }else{
                i = i +1
        }   
}
w=w+3
if(w<5){
    if(w==3){
     w=5
    }
}

""" 

texto3 ="""
print("w")
if(x>5){
print("novo")
print("b")
print("b")
}elif(x>4){
print("nnn")
print("r")
}
print("rr")
print("final???")
"""

texto4 ="""
print("w")
while(x>5){
print("novo")
print("algo")
print("novo")
}
print("fim")
print("novo1")
print("novo2")
"""

texto5 ="""
print("w")
{
print("novo")
print("algo")
print("novo")
}while(x>5)
print("fim")
"""


texto6 = """
numero myfunction(number, y, z){
    numero x
    print("x") 
    return x
}
"""

#texto ="""Number myfunction (number){
#                Number x
#                if(number<5){
#                        x=x+1
#                }else{
#                        x=x-1
#                }
#                return x
#        }
#""" 

class TransformerLinguagem(Interpreter):

    def __init__(self):
        self.variaveis = {0:{}}
        self.funcoes = []
        self.not_defined = []
        self.repetido = []
        self.mencionado = []
        self.no_value = []
        self.counter_tipo = {}
        self.nivel = 0
        self.ciclo = 0
        self.condicional =0
        self.strut_controlo = []
        self.struct_if=[]
        self.aninhadoIF=0
        self.aninhado = 0
        self.print=0
        self.input=0
        self.substituir =0
        self.variaveisTotais=[]
        self.counter = 0 
        self.temp = None
        self.temp_if = {}
        self.graph = pgv.AGraph(directed=True)

    def start(self, elementos):
        r = self.visit_children(elementos)
        dicionario = self.variaveis[self.nivel]
        print("[DICIONARIO DE VARIAVEIS]")
        pprint.pprint(self.variaveis)
        for keys in dicionario.keys():
            val = dicionario[keys]
            if val["valor"] == None:
                print("SEM VALOR",keys)
                self.no_value.append(keys)
            tipo = val["tipo"]
            if tipo not in self.counter_tipo.keys():
                self.counter_tipo[tipo] = 1
            else:
                aux = self.counter_tipo[tipo] + 1
                self.counter_tipo[tipo] = aux
            
        #print(f"variaveis: {self.variaveis}")
        #print(f"funcoes: {self.funcoes}")
        #print(f"not_defined: {self.not_defined}")
        #print(f"repetido: {self.repetido}")
        #print(f"mencionado: {self.mencionado}")
        #print(f"no_value: {self.no_value}")
        return r
    def codigo(self, items):
        linhas = self.visit_children(items)
        return linhas

    def linhas(self, items):
        linhas = self.visit_children(items)
        print(linhas)
        return linhas
    

    def create(self, items):
        val = self.visit_children(items)
        tipo = None
        variavel = None
        if val[0].type == 'TYPE':
            tipo = str(val[0])
        if val[1].type == 'VAR':
            variavel = str(val[1])
            if variavel not in self.variaveisTotais:
                self.variaveisTotais.append(variavel)
        flag = True
        nivel_atual = self.nivel
        while(nivel_atual>=0 and flag):
            dicionario = self.variaveis[nivel_atual]
            if variavel in dicionario.keys():
                flag = False
            nivel_atual -= 1
        if not flag and variavel not in self.repetido:
            self.repetido.append(variavel)
        else:
            dicionario = self.variaveis[self.nivel]
            dicionario[variavel] = {"valor":None,"tipo":tipo}
            self.variaveis[self.nivel]=dicionario
        pass
    
    def print_string (self, items):
        self.counter+=1
        val = self.visit_children(items)
        print(f"[print_string] counter: {self.counter} | temp: {self.temp} | val {val[0].value}")
        instruction_text = f"print('{val[0].value}')"
        #cria nodo e liga ao anterior
        self.graph.add_node(self.counter, shape="oval", label=instruction_text)
        self = new_edge(self)
        if len(val) > 1:
            variavel = str(val[1])
            flag = True
            nivel_atual = self.nivel
            while(nivel_atual>=0 and flag):
                dicionario = self.variaveis[nivel_atual]
                if variavel in dicionario.keys():
                    flag = False
                nivel_atual -= 1
            if flag and variavel not in self.not_defined:
                self.not_defined.append(variavel)
            if variavel not in self.mencionado:
                self.mencionado.append(variavel)
        self.print+=1
        return instruction_text
    
    def print_var (self, items):
        self.counter+=1
        val = self.visit_children(items)
        print(" FOI AQUI QUE ENTREI ")
        variavel = str(val[0])
        instruction_text = f"print('{variavel}')"
        self.graph.add_node(self.counter, shape="oval", label=instruction_text)
        self = new_edge(self)
        flag = True
        nivel_atual = self.nivel
        while(nivel_atual>=0 and flag):
            dicionario = self.variaveis[nivel_atual]
            if variavel in dicionario.keys():
                flag = False
            nivel_atual -= 1
        if flag and variavel not in self.not_defined:
            self.not_defined.append(variavel)
        if variavel not in self.mencionado:
                self.mencionado.append(variavel)
        if variavel not in self.variaveisTotais:
            self.variaveisTotais.append(variavel)
        self.print+=1
        return instruction_text

    def input_string (self, items):
        self.counter+=1
        val = self.visit_children(items)
        print("ENTREI AQUI")
        instruction_text = f"input('{val[0].value}')"
        self.graph.add_node(self.counter, shape="oval", label=instruction_text)
        self = new_edge(self)
        if len(val) > 1:
            variavel = str(val[1])
            flag = True
            nivel_atual = self.nivel
            while(nivel_atual>=0 and flag):
                dicionario = self.variaveis[nivel_atual]
                if variavel in dicionario.keys():
                    flag = False
                nivel_atual -= 1
            if flag and variavel not in self.not_defined:
                self.not_defined.append(variavel)
            if variavel not in self.mencionado:
                    self.mencionado.append(variavel)
        self.input+=1
        return instruction_text
    
        
    def input_var (self, items):
        self.counter+=1
        val = self.visit_children(items)
        variavel = str(val[0])
        flag = True
        instruction_text = f"input('{val[0].value}')"
        self.graph.add_node(self.counter, shape="oval", label=instruction_text)
        self = new_edge(self)
        nivel_atual = self.nivel
        while(nivel_atual>=0 and flag):
            dicionario = self.variaveis[nivel_atual]
            if variavel in dicionario.keys():
                flag = False
            nivel_atual -= 1
        if flag and variavel not in self.not_defined:
            self.not_defined.append(variavel)
        if variavel not in self.mencionado:
                self.mencionado.append(variavel)
        if variavel not in self.variaveisTotais:
            self.variaveisTotais.append(variavel)
        self.input+=1
       

    #########################TODO#####################
    #verificar se for a atribuição num dicionario para alterar
    #o valor no indice. Talvez seja melhor separar em várias funções
    def atribuicao(self, items):
        self.counter += 1
        val = self.visit_children(items)
        val0 = val[0]
        tipo = None
        indice = None
        nome = None
        valor = None
        if type(val0) == tuple:
            nome,indice = val0[1]
            valor = val[1]
        elif val0.type =="TYPE":
            tipo = str(val0)
            nome = str(val[1])
            valor = val[2]
        elif val0.type =="VAR":
            nome = str(val0)
            valor = val[1]
        instruction_text = f"{nome} = {val_to_str(valor)}"
        self.graph.add_node(self.counter, shape="oval", label=instruction_text)
        self = new_edge(self)
        if not tipo:
            flag = True
            nivel_atual = self.nivel
            while(nivel_atual>=0 and flag):
                dicionario = self.variaveis[nivel_atual]
                if nome in dicionario.keys():
                    flag = False
                    aux = dicionario[nome]
                    aux["valor"] = valor 
                    dicionario[nome] = aux
                    self.variaveis[nivel_atual] = dicionario
                nivel_atual -= 1
            if flag and nome not in self.not_defined:
                self.not_defined.append(nome)
        else:
            flag = True
            nivel_atual = self.nivel
            while(nivel_atual>=0 and flag):
                dicionario = self.variaveis[nivel_atual]
                if nome in dicionario.keys():
                    flag = False
                    aux = dicionario[nome] 
                    aux["valor"] = valor
                    dicionario[nome] = aux
                    self.variaveis[nivel_atual] = dicionario
                nivel_atual -= 1
            if not flag and nome not in self.repetido:
                dicionario = self.variaveis[self.nivel]
                aux = dicionario[nome] 
                aux["valor"] = valor
                dicionario[nome] = aux
                self.variaveis[self.nivel] = dicionario
                
                self.repetido.append(nome)
            else:
                dicionario = self.variaveis[self.nivel]
                dicionario[nome] = {"valor":valor,"tipo":tipo}
                self.variaveis[self.nivel] = dicionario
        if nome not in self.mencionado:
            self.mencionado.append(nome)  
        if nome not in self.variaveisTotais:
            self.variaveisTotais.append(nome)
        #if type(valor) != Tree:
        print("VALOR",valor)
        if type(valor) == list:
            valor = valor[0]
            if (type(valor) == str) and ("\"" not in valor) and (valor not in self.mencionado):
                self.mencionado.append(nome)
        pass

    def expressao(self,items):
        val = self.visit_children(items)
        return val[0]

    def adicao(self, items):
        val = self.visit_children(items)
        val1 = val[0]
        val2 = val[1]
        return "EXPRESSAO",(val1, "+" ,val2)
    
    def subtracao(self, items):
        val = self.visit_children(items)
        val1 = val[0]
        val2 = val[1]
        return "EXPRESSAO",(val1, "-" ,val2)
    
    def multiplicacao(self, items):
        val = self.visit_children(items)
        val1 = val[0]
        val2 = val[1]
        return "EXPRESSAO",(val1, "*" ,val2)
    
    def divisão(self, items):
        val = self.visit_children(items)
        val1 = val[0]
        val2 = val[1]
        return "EXPRESSAO",(val1, "/" ,val2)
    
    def exp_val(self, items):
        val = self.visit_children(items)
        return val[0]

    def func(self, items):
        val = self.visit_children(items)
        name = str(val[0])
        lista = val[1]                       
        return "FUNCAO",(name,lista)
    ##################TODO#####################################
    #ir buscar o valor no indice e devolver esse valor
    #ainda é preciso resolver a est_dados
    
    def func_atr(self, items):
        val = self.visit_children(items)
        name = str(val[0])
        indice = val[1]                       
        flag_name = True
        flag_indice = True
        nivel_atual = self.nivel
        if type(indice) == str and "\"" not in name:
            while(nivel_atual>=0 and (flag_name or flag_indice)):
                dicionario = self.variaveis[nivel_atual]
                if name in dicionario.keys():
                    flag_name = False
                if indice in dicionario.keys():
                    flag_indice = False
                nivel_atual -= 1
            if flag_name:
                self.not_defined.append(name)
            if flag_indice:
                self.not_defined.append(indice)
        return "INDICE",(name,indice)

    def est_dados(self, items):
        val = self.visit_children(items)
        return val[0]

    def bool_expressao(self, items):
        return items
    #createCondition(variables, symbol, number, graph, counter):
    def bool_and(self, items):
        tudo = self.visit_children(items)
        return (tudo[0], "&&" ,tudo[1])
    
    def bool_or(self, items):
        tudo = self.visit_children(items)
        return (tudo[0], "||" ,tudo[1])
    
    def menor(self, items):
        tudo = self.visit_children(items)
        return (tudo[0], "<" ,tudo[1])
    
    def menor_igual(self, items):
        tudo = self.visit_children(items)
        return (tudo[0], "<=" ,tudo[1])
    
    def maior(self, items):
        tudo = self.visit_children(items)
        return (tudo[0], ">" ,tudo[1])
    
    def maior_igual(self, items):
        tudo = self.visit_children(items)
        return (tudo[0], ">=" ,tudo[1])
    
    def igual(self, items):
        tudo = self.visit_children(items)
        return (tudo[0], "==" ,tudo[1])
    
    def diferente(self, items):
        tudo = self.visit_children(items)
        return (tudo[0], "!=" ,tudo[1])
    

    def def_func(self, items):
        self.nivel += 1

        self.variaveis[self.nivel] = {}
        lista = self.visit(items.children[2])
        dicionario = self.variaveis[self.nivel]
        for elems in lista:
            dicionario[elems] = {"valor": 1, "tipo": None}
        instruction_text =  f"return {self.visit(items.children[4])}"
        self.variaveis[self.nivel] = dicionario
        tudo = self.visit_children(items)
        self.counter +=1
        self.graph.add_node(self.counter, shape="oval", label= instruction_text)
        self = new_edge(self)
        nome = str(tudo[1])
        for keys in dicionario.keys():
            val = dicionario[keys]
            if val["valor"] == None:
                print("DEF_FUNC: NO VALUE", keys)
                self.no_value.append(keys)
            tipo = val["tipo"]
            if tipo not in self.counter_tipo.keys():
                self.counter_tipo[tipo] = 1
            else:
                aux = self.counter_tipo[tipo] + 1
                self.counter_tipo[tipo] = aux
        self.variaveis.pop(self.nivel)
        self.nivel -= 1
        return items

    def while_loop(self, items):
        ##incrementar variaveis
        self.ciclo+=1
        self.nivel += 1
        self.counter +=1 
        if self.strut_controlo:
            self.aninhado += 1
        self.strut_controlo.append(1)
        self.variaveis[self.nivel] = {}
        ##criar nodo no grafico
        original = self.counter
        triplo = self.visit(items.children[0])
        createCondition("while", triplo, self.graph, self.counter)
        self = new_edge(self)
        #visitar os filhos
        self.visit_children(items)
        self.temp = original
        self.graph.add_edge(self.counter, original)
        self = connect_end(self, original) #garantir que todos os caminhos retornam para o while
        dicionario = self.variaveis[self.nivel]
        #tratamento dos resultados da visita
        for keys in dicionario.keys():
            val = dicionario[keys]
            if val["valor"] == None:
                self.no_value.append(keys)
            tipo = val["tipo"]
            if tipo not in self.counter_tipo.keys():
                self.counter_tipo[tipo] = 1
            else:
                aux = self.counter_tipo[tipo] + 1
                self.counter_tipo[tipo] = aux
        #decrementar variaveis
        self.variaveis.pop(self.nivel)
        self.strut_controlo.pop()
        self.nivel -= 1
        
        return items
    
    def do_while_statement(self,items):
        self.ciclo+=1
        self.nivel += 1
        if self.strut_controlo:
            self.aninhado += 1
        self.strut_controlo.append(1)
        self.variaveis[self.nivel] = {}
        original = self.counter + 1
        print("[do_while]",self.visit(items.children[0]))
        triplo = self.visit(items.children[1])
        self.counter += 1
        createCondition( "while", triplo, self.graph, self.counter)
        self = new_edge(self)
        self.graph.add_edge(self.counter, original)
        dicionario = self.variaveis[self.nivel]
        for keys in dicionario.keys():
            val = dicionario[keys]
            if val["valor"] == None:
                self.no_value.append(keys)
            tipo = val["tipo"]
            if tipo not in self.counter_tipo.keys():
                self.counter_tipo[tipo] = 1
            else:
                aux = self.counter_tipo[tipo] + 1
                self.counter_tipo[tipo] = aux
        self.variaveis.pop(self.nivel)
        self.strut_controlo.pop()
        self.nivel -= 1


        return items


    def if_statement(self, items): 
        self.condicional+=1
        self.nivel += 1
        if self.strut_controlo:
            self.aninhado += 1
            if (self.struct_if):
                self.aninhadoIF+=1
        self.strut_controlo.append(1)
        self.struct_if.append(1)
        self.variaveis[self.nivel] = {}
        self.counter +=1

        #tratar do grafico
        original = self.counter
        triplo = self.visit(items.children[0])
        createCondition( "if", triplo, self.graph, self.counter)
        self = new_edge(self)
        #visitar as linhas
        print(self.visit(items.children[1]))#ler as linhas dentro do if
        self.temp = original
        self.temp_if[self.counter] = self.nivel
        #tratar das variaveis dps de visitar os filhos
        dicionario = self.variaveis[self.nivel]
        for keys in dicionario.keys():
            val = dicionario[keys]
            if val["valor"] == None:
                self.no_value.append(keys)
            tipo = val["tipo"]
            if tipo not in self.counter_tipo.keys():
                self.counter_tipo[tipo] = 1
            else:
                aux = self.counter_tipo[tipo] + 1
                self.counter_tipo[tipo] = aux
        #dar pop
        self.variaveis.pop(self.nivel)
        self.strut_controlo.pop()
        self.struct_if.pop()
        self.nivel -= 1
        #elif e else
        if len(items.children) > 2:
            self.visit(items.children[2])#caso exista visitar o elif
            if len(items.children) == 4:
                self.visit(items.children[3])#caso exista visiar o else
        return items

    def elif_statement(self, items):
        self.condicional+=1
        self.nivel += 1
        if self.strut_controlo:
            self.aninhado += 1
        self.strut_controlo.append(1)
        self.variaveis[self.nivel] = {}
        self.counter +=1 

        triplo = self.visit(items.children[0])
        original = self.counter
        createCondition( "elif", triplo, self.graph, self.counter)
        self = new_edge(self)
        self.visit_children(items)
        self.temp_if[self.counter] = self.nivel
        self.temp = original
        dicionario = self.variaveis[self.nivel]
        for keys in dicionario.keys():
            val = dicionario[keys]
            if val["valor"] == None:
                self.no_value.append(keys)
            tipo = val["tipo"]
            if tipo not in self.counter_tipo.keys():
                self.counter_tipo[tipo] = 1
            else:
                aux = self.counter_tipo[tipo] + 1
                self.counter_tipo[tipo] = aux
        self.strut_controlo.pop()
        self.variaveis.pop(self.nivel)
        self.nivel -= 1
        return 

    def else_statement(self, items):
        self.condicional+=1
        self.nivel += 1
        self.variaveis[self.nivel] = {}
        if self.strut_controlo:
            self.aninhado += 1
        self.strut_controlo.append(1)
        self.visit_children(items)
        self.temp_if[self.counter] = self.nivel
        dicionario = self.variaveis[self.nivel]
        for keys in dicionario.keys():
            val = dicionario[keys]
            if val["valor"] == None:
                self.no_value.append(keys)
            tipo = val["tipo"]
            if tipo not in self.counter_tipo.keys():
                self.counter_tipo[tipo] = 1
            else:
                aux = self.counter_tipo[tipo] + 1
                self.counter_tipo[tipo] = aux
        self.variaveis.pop(self.nivel)
        self.strut_controlo.pop()
        self.nivel -= 1
        pass

    def for_loop(self, items):
        self.ciclo+=1
        self.nivel += 1
        if self.strut_controlo:
            self.aninhado += 1
        self.strut_controlo.append(1)
        self.variaveis[self.nivel] = {}
        tudo = self.visit_children(items)
        dicionario = self.variaveis[self.nivel]
        for keys in dicionario.keys():
            val = dicionario[keys]
            if val["valor"] == None:
                self.no_value.append(keys)
            tipo = val["tipo"]
            if tipo not in self.counter_tipo.keys():
                self.counter_tipo[tipo] = 1
            else:
                aux = self.counter_tipo[tipo] + 1
                self.counter_tipo[tipo] = aux
        self.variaveis.pop(self.nivel)
        self.strut_controlo.pop()
        self.nivel -= 1
        pass

    def list(self, items):
        lista = self.visit_children(items)
        list_l = []
        for elem in lista:
            list_l.append(elem)
        return list_l
    
    def def_list(self, items):
        lista = self.visit_children(items)
        list_l = []
        for elem in lista:
            list_l.append(elem)
        return list_l

    def array(self, items):
        lista = self.visit_children(items)
        array = []
        for elem in lista:
            array.append(elem)
        return array

    def dict(self, items):
        lista = self.visit_children(items)
        dic = {}
        for chave, val in lista:
            chave = chave.strip('"')
            dic[chave] = val
        return dic

    def pair(self, items):
        val = self.visit_children(items)
        return val[0],val[1]

    def key(self, items):
        val = self.visit_children(items)
        if val[0].type == "NUMERO":
            return float(val[0])
        if val[0].type == "STRING":
            return str(val[0])

    def tuple(self, items):
        lista = self.visit_children(items)
        return lista

    def val(self, items):
        val = self.visit_children(items)
        flag = True
        nivel_atual = self.nivel
        if val[0].type == "VAR":
            while(nivel_atual>=0 and flag):
                dicionario = self.variaveis[nivel_atual]
                if val[0] in dicionario.keys():
                    flag = False
                nivel_atual -= 1
            if flag and val[0] not in self.not_defined:
                self.not_defined.append(val[0])
            return str(val[0])
        if val[0].type == "NUMERO":
            return float(val[0])
        if val[0].type == "STRING":
            return str(val[0])
        if val[0].type == "BOOLEAN":
            return float(val[0])
        return val[0]
    
    def def_val(self, items):
        val = self.visit_children(items)
        if val[0].type == "VAR":
            return str(val[0])
        if val[0].type == "NUMERO":
            return float(val[0])
        if val[0].type == "STRING":
            return str(val[0])
        return val[0]
    
    def visualizar(self):
        # Salva e exibe o gráfico
        self.graph.draw("control_flow_graph.png", prog="dot", format="png")
    

    def gerar_relatorio(self):
    
        total_variaveis = len(self.variaveisTotais), # total de variavei
        total_ciclos =self.ciclo# falta leitura e escrita e atribuições
        total_condicionais = self.condicional
        total_mencionado= self.mencionado
        total_naodefinido= [token.value for token in self.not_defined]

        variaveis_repetidas = [token.value for token in self.repetido]
        variaveis = [token.value for token in self.variaveisTotais]
        no_value = [token.value for token in self.no_value]

        template_html = f"""
      <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Análise</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        h1 {{
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        p {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <h1>Relatório de Análise</h1>
    <table>
        <tr>
            <th>Variáveis</th>
            <td>{variaveis}</td>
        </tr>
        <tr>
            <th>Total de variáveis por tipo</th>
            <td>{self.counter_tipo}</td>
        </tr>
        <tr>
            <th>Total de variáveis</th>
            <td>{total_variaveis}</td>
        </tr>
        <tr>
            <th>Total de variáveis declaradas e nunca mencionadas</th>
            <td>{no_value}</td>
        </tr>
        <tr>
            <th>Total variáveis não declaradas</th>
            <td>{total_naodefinido}</td>
        </tr>
        <tr>
            <th>Total variáveis redeclaradas</th>
            <td>{variaveis_repetidas}</td>
        </tr>
        <tr>
            <th>Total de instruções de leitura</th>
            <td>{self.input}</td>
        </tr>
        <tr>
            <th>Total de instruções de escrita</th>
            <td>{self.print}</td>
        </tr>
        <tr>
            <th>Total de ciclos</th>
            <td>{total_ciclos}</td>
        </tr>
        <tr>
            <th>Total de condicionais</th>
            <td>{total_condicionais}</td>
        </tr>
        <tr>
            <th>Total de estruturas de controlo aninhadas</th>
            <td>{self.aninhado}</td>
        </tr>
         <tr>
            <th>Total ifs aninhados que possam ser substituidos por um só if</th>
            <td>{self.aninhadoIF}</td>
        </tr>
    </table>
</body>
</html>

        """

        # Escrever o HTML gerado em um arquivo
        with open("relatorio.html", "w") as f:
            f.write(template_html)


    
    
p = Lark(grammar2) 
tree1 = p.parse(texto2)
analiser= TransformerLinguagem()
tree= analiser.visit(tree1)
analiser.visualizar()
#tree_png = p.tree_to_png(treeT, "tree.png")
#analiser.gerar_relatorio()
