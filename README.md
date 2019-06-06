# kohonen-algorithm
Algoritmo de Kohonen

# requisitos

* Python 3.+

# estrutura do projeto

- **examples**: Diretório com os arquivos comos dados de entrada
- **results**: Diretório com os arquivos com os resultados do treinamento
- **tests**: Diretório com os arquivos definidos para teste


# ajuda

`./main.py  --help`

# execução

#### treinamento

`./main.py -tr -i "examples/binary.json" -o "results/binary.json" -mi 10 -mc 2 -lr 0.60 -nb 0`

#### teste

`./main.py -ts -i "tests/binary.json" -w "results/binary.json" -mc 2`

## have fun :)