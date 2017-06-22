# Interpretador de Expressão Matemática Simples

### Instalação
É necessário ter Python 3 instalado, disponível [aqui](https://www.python.org/downloads/).

### Como executar
Navegue até a pasta src e digite ```python3 interpretador.py "1 + 2 + 3"``` no terminal.  
Substitua a expressão "1 + 2 + 3" pela desejada. Não esqueça de colocar as em volta da expressão.

### Operadores
* A - B
* A + B
* A * B
* A / B
* A ^ B
* -A

### Gramática
```
Exp ::= Num | ( Exp ) | - Exp | Exp BinOp Exp
Num ::= [0-9]+([.][0-9]+)?
BinOp ::= + | - | * | / | ^
```

### Expressões de teste
Há algumas expressões de teste no arquivo [testes.txt](testes.txt).