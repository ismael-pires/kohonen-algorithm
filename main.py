#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import sys

from classes.Kohonen import Kohonen

version = '1.0.0'


def get_argument(_needle, _haystack, _default=None):
    """
    Método responsável por obter o valor de um argumento
    :param _needle:         Nome do argumento
    :param _haystack:       Lista de argumentos
    :param _default:        Valor padrão
    :return: mixed
    """
    try:

        for value in _needle:
            if value in _haystack:
                pos = _haystack.index(value)
                if pos > 0:
                    return _haystack[pos + 1]

        return _default if _default is not None else False
    except (ValueError, TypeError):
        return False


if __name__ == "__main__":

    info_help = 'Parâmetros disponíveis: \r\n' \
                '\t -tr, --training             Sinaliza operação de treinamento \n' \
                '\t -ts, --test                 Sinaliza operação de teste \n' \
                '\t -h, --help                  Exibe o menu de ajuda \n' \
                '\t -v, --version               Exibe a versão do sistema \r\n\n' \
                'Treinamento: (--training)\r\n' \
                '\t -i, --input                 Endereço onde está o arquivo com os dados a serem processados\n' \
                '\t -o, --output                Endereço onde será criado o arquivo com os resultados\n' \
                '\t -mi, --max_interaction      Número máximo de interações (Padrão: 2)\n' \
                '\t -mc, --max_clusters         Número máximo de grupos que serão definidos (Padrão: 2) \n' \
                '\t -lr, --learning_rate        Taixa de aprendizado (Padrão:0.98) \n' \
                '\t -de, --decrease             Decrementação (Padrão:True)\n' \
                '\t -nb, --neighborhood         Vizinhos mais próximos (Padrão:1) \r\n\n' \
                'Teste: (--test)\r\n' \
                '\t -i, --input                 Endereço onde está o arquivo com os dados a serem processados\n' \
                '\t -w, --weight                Endereço onde foi criado o arquivo com os pesos\n' \
                '\t -mc, --max_clusters         Número máximo de grupos que serão definidos (Padrão: 2) \n' \

    # Obtendo os parametros
    arguments = sys.argv

    # Verificando se foi informado algum parametro
    if arguments is not None and len(arguments) > 1:

        if '-h' in arguments or '--help' in arguments:
            print(info_help)
            exit(0)

        if '-v' in arguments or '--version' in arguments:
            print('version')
            exit(0)

        if '-tr' in arguments or '--training' in arguments:

            params = {
                'input': get_argument(['-i', '--input'], arguments, 'examples/binary.json'),
                'output': get_argument(['-o', '--output'], arguments, 'results/binary.json'),
                'max_interaction': int(get_argument(['-mi', '--max_interaction'], arguments, 2)),
                'max_clusters': int(get_argument(['-mc', '--max_clusters'], arguments, 2)),
                'learning_rate': float(get_argument(['-lr', '--learning_rate'], arguments, 0.98)),
                'decrease': bool(get_argument(['-de', '--decrease'], arguments, True)),
                'neighborhood': int(get_argument(['-nb', '--neighborhood'], arguments, 1))
            }

            print('Iniciando o treinamento [{}] ...'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            Kohonen.training(params)
            print('Treinamento finalizado [{}] ...'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            exit(0)

        if '-ts' in arguments or '--test' in arguments:

            params = {
                'input': get_argument(['-i', '--input'], arguments, 'tests/binary.json'),
                'weight': get_argument(['-w', '--weight'], arguments, 'results/binary.json'),
                'max_clusters': int(get_argument(['-mc', '--max_clusters'], arguments, 2))
            }

            print('Iniciando os testes [{}] ...'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            Kohonen.test(params)
            print('Testes finalizados [{}] ...'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            exit(0)
    else:
        print(info_help)
        exit(0)
