def val_to_str(valor):
    expressao = None
    print("[val_to_str]",valor)
    if type(valor) != tuple:
        expressao = (f"{valor}")
    else:
        tipo = valor[0]
        variaveis = valor[1]
        if tipo=="EXPRESSAO":
            expressao = (f"{variaveis[0]} {variaveis[1]} {variaveis[2]}")
        elif tipo == "FUNCAO":
            expressao = (f"{variaveis[0]}({variaveis[1]})")
        elif tipo == "INDICE":
            expressao = (f"{variaveis[0]}[{variaveis[1]}]")
    return expressao


def connect_end(self):
    if(self.temp_if):
            print("[new_edge]",self.temp_if)
            aux = []
            for indices, nivel_indice in self.temp_if.items():
                if (self.nivel + 1) == nivel_indice:
                    self.graph.add_edge(indices, self.counter)
                    aux.append(indices)
            for i in aux:
                self.temp_if.pop(i)
    return self
                


def new_edge(self):
    #  ligar bool expressions as instruções fora dos parenteses
    if (self.temp != None):
        self.graph.add_edge(self.temp, self.counter)
        self.temp = None 
        connect_end(self)
   # ligar as instruções do mesmo nivel num if
    else:
        # normais instruções seguidas
        if(self.counter >1):
                self.graph.add_edge((self.counter)-1, self.counter)
        connect_end(self)
    return self

def createCondition(tipo, triplo, graph, counter):
    print("[createCondition]", triplo)
    print("[createCondition]", tipo)
    variables, symbol, number = triplo
    instruction_text =  f"{tipo}({variables} {symbol} {number})"
    graph.add_node(counter, shape="diamond", label= instruction_text)
    
