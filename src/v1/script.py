class Pilha(object):
    def __init__(self):
        self.dados = []
 
    def empilha(self, elemento):
        self.dados.append(elemento)
 
    def desempilha(self):
        if not self.vazia():
            return self.dados.pop(-1)
        else:
            return -1
 
    def vazia(self):
        return len(self.dados) == 0

def potencia(numero, elevado):
    resultado = numero**elevado
    return resultado

def divisao(numero,dividido):
    resultado = numero/dividido
    return resultado

def multiplicacao(numero, multiplicado):
    resultado = numero*multiplicado
    return resultado

def soma(numero, somado):
    resultado = numero + somado
    return resultado

def subtracao(numero, menos):
    resultado = numero - menos
    return resultado

''' vai criar os tokens ''' 
def tokens (lista):
    prenum = ''
    nlista=[]
    for teste in lista:
        if(teste == ' '):
            None
        else:
            if(teste == '(' or teste == ')'):
                if(prenum != ''):
                    temp = ['Num', prenum]
                    numero = prenum
                    c=0
                    for b in numero:
                        if(b == '.'):
                            if(numero[0] == '.'):
                                  print("erro")
                            if(numero[len(numero)-1] == '.'):
                                  print("erro")
                        c = c+1
                    nlista.append(temp)
                    print(nlista)
                
                    prenum = ''
                temp = ['Exp', teste]
                nlista.append(temp)
                print(nlista)
                

            else:
                if(teste == '+' or teste == '-' or teste == '*' or teste == '/' or teste == '^'):
                    if(prenum != ''):
                        temp = ['Num', prenum]
                        numero = prenum
                        c=0
                        for b in numero:
                            if(b == '.'):
                                if(numero[0] == '.'):
                                    print("erro")
                                if(numero[len(numero)-1] == '.'):
                                    print("erro")
                        nlista.append(temp)
                        print(nlista)
                    
                        prenum = ''
                    temp = ['Op', teste]
                    nlista.append(temp)
                    print(nlista)
                
                else:
                    if(teste == '.'):
                        prenum = prenum + teste
                    else:
                        teste1 = int(teste)
                        if(teste1 >=0):
                            prenum = prenum + teste
    if(prenum != ''):
        temp = ['Num', prenum]
        numero = prenum
        c=0
        for b in numero:
            if(b == '.'):
                if(numero[0] == '.'):
                    print("erro")
                if(numero[len(numero)-1] == '.'):
                    print("erro")
            c = c+1
        nlista.append(temp)
    return nlista

def valida(lista):
    p = Pilha()
    i=0
    fu = 0
    for teste in lista:
        if(teste[0] == 'Exp'):
            if(teste[1] == '('):
                p.empilha('(')
            if(teste[1] == ')'):
                fu = p.desempilha()
        if(teste[0] == 'Op'):
            if(teste[1] == '+' or teste[1] == '/' or teste[1] == '*' or teste[1] == '^'):
                if((i-1) < 0):
                    if not(lista[0][0] == 'Num' or lista[0][0] == 'Exp'):
                            print("erro")
                else:
                    if not(lista[i-1][0] == 'Num' or lista[i-1][1] == ')'):
                        print("erro")
                if((i+1) >= len(lista)):
                    if not(lista[len(lista)-1][0] == 'Num' or lista[len(lista)-1][0] == 'Exp'):
                        print("erro")
                else:
                    if not(lista[i+1][0] == 'Num' or lista[i+1][1] == '(' or lista[i+1][1] == '-'):
                        print("erro") 
            if(teste[1] == '-'):
                if((i-1) < 0):
                    if not(lista[0][0] == 'Num' or lista[0][0] == 'Exp' or lista[0][1]=='-'):
                            print("erro")
                else:
                    if not(lista[i-1][0] == 'Num' or lista[i-1][0] == 'Exp' or lista[i-1][1] == '-'):
                        print("erro")
                if((i+1) >= len(lista)):
                    if not(lista[len(lista)-1][0] == 'Num' or lista[len(lista)-1][0] == 'Exp'):
                        print("erro")
                else:
                    if not(lista[i+1][0] == 'Num' or lista[i+1][1] == '(' or lista[i+1][1] == '-'):
                        print("erro") 
        i = i + 1
    if(not p.vazia() or fu == -1):
        print("erro")


def calc(lista):
    i = 0
    for valor in lista:
        token = valor[0]
        if(token == 'Exp'):
            if(token[1] == '('):
                None
        i = i + 1

def calc1(lista):
    i=0
    for valor in lista:
        token = valor
        if(token[0] == 'Op'):
            if(token[1] == '+'):
                if(lista[i-1][0] == 'Num'):
                    num1 = float(lista[i-1][1])
                else:
                    print("erro")
                if(lista[i+1][0] == 'Num'):
                    num2 = float(lista[i+1][1])
                else:
                    print("erro")
                resul = soma(num1, num2)
                lista.pop(i+1)
                lista.pop(i)
                lista.pop(i-1)
                lista.insert((i-1),['Num', resul])
                calc1(lista)
            if(token[1] == '-'):
                if(lista[i-1][0] == 'Num'):
                    num1 = float(lista[i-1][1])
                else:
                    print("erro")
                if(lista[i+1][0] == 'Num'):
                    num2 = float(lista[i+1][1])
                else:
                    print("erro")
                resul = subtracao(num1, num2)
                lista.pop(i+1)
                lista.pop(i)
                lista.pop(i-1)
                lista.insert((i-1),['Num', resul])
                calc1(lista)
        else:
            calc2(lista)
        i = i + 1


def calc2(lista):
    i=0
    for valor in lista:
        token = valor
        if(token[0] == 'Op'):
            if(token[1] == '*'):
                if(lista[i-1][0] == 'Num'):
                    num1 = float(lista[i-1][1])
                else:
                    print("erro")
                if(lista[i+1][0] == 'Num'):
                    num2 = float(lista[i+1][1])
                else:
                    print("erro")
                resul = multiplicacao(num1, num2)
                lista.pop(i+1)
                lista.pop(i)
                lista.pop(i-1)
                lista.insert((i-1),['Num', resul])
                calc2(lista)
            if(token[1] == '/'):
                if(lista[i-1][0] == 'Num'):
                    num1 = float(lista[i-1][1])
                else:
                    print("erro")
                if(lista[i+1][0] == 'Num'):
                    num2 = float(lista[i+1][1])
                else:
                    print("erro")
                resul = divisao(num1, num2)
                lista.pop(i+1)
                lista.pop(i)
                lista.pop(i-1)
                lista.insert((i-1),['Num', resul])
                calc2(lista)
        else:
            calc3(lista)
        i = i + 1
    return lista

def calc3(lista):
    i=0
    for valor in lista:
        token = valor
        if(token[0] == 'Op'):
            if(token[1] == '^'):
                if(lista[i-1][0] == 'Num'):
                    num1 = float(lista[i-1][1])
                else:
                    print("erro")
                if(lista[i+1][0] == 'Num'):
                    num2 = float(lista[i+1][1])
                else:
                    print("erro")
                resul = potencia(num1, num2)
                lista.pop(i+1)
                lista.pop(i)
                lista.pop(i-1)
                lista.insert((i-1),['Num', resul])
                calc3(lista)
        i = i + 1
    lista2 = lista
    print(lista2)
    return lista2
expressao  = input("Digite a expressao")

lista1 = tokens(expressao)
valida(lista1)
calc1(lista1)
print(lista1)
'''print(lista)'''