#!/usr/bin/python
# -*- coding: utf-8 -*-

version = '1.0.0'

import time
import sys

from classes.Kohonen import Kohonen


def get_argument(_needle, _haystack):

    """
    Método responsável por obter o valor de um argumento
    :param _needle:         Nome do argumento
    :param _haystack:       Lista de argumentos
    :return: mixed
    """
    try:

        for value in _needle:
            if value in _haystack:
                pos = _haystack.index(value)
                if pos > 0:
                    return _haystack[pos + 1]

        return False
    except (ValueError, TypeError):
        return False


if __name__ == "__main__":

    info_help = 'Parâmetros disponíveis: \r\n' \
                   '\t -tr, --training             Sinaliza operação de treinamento \n' \
                   '\t -ts, --test                 Sinaliza operação de teste \n' \
                   '\t -h, --help                  Exibe o menu de ajuda \n' \
                   '\t -v, --version               Exibe a versão do sistema \r\n\n' \
                'Treinamento: (--training)\r\n' \
                   '\t -mi, --max_interaction      Número máximo de interações (Padrão: 2)\n' \
                   '\t -mc, --max_clusters         Número máximo de grupos que serão definidos (Padrão: 2) \n' \
                   '\t -lr, --learning_rate        Taixa de aprendizado (Padrão:0.98) \n' \
                   '\t -de, --decrease             Decrementação (Padrão:True)\n' \
                   '\t -nb, --neighborhood         Vizinhos mais próximos (Padrão:1) \n'

    # Obtendo os parametros
    arguments = sys.argv

    # Verificando se foi informado algum parametro
    if len(arguments) > 1:

        if '-h' in arguments or '--help' in arguments:
            print(info_help)
            exit(0)

        if '-v' in arguments or '--version' in arguments:
            print('version')
            exit(0)

        if '-tr' in arguments or '--training' in arguments:

            max_interaction = get_argument(['-mi', '--max_interaction'], arguments)
            max_clusters = get_argument(['-mc', '--max_clusters'], arguments)
            learning_rate = get_argument(['-lr', '--learning_rate'], arguments)
            decrease = get_argument(['-de', '--decrease'], arguments)
            neighborhood = get_argument(['-nb', '--neighborhood'], arguments)

            print('Iniciando o treinamento [{}] ...'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            Kohonen.training(inputs, _max_clusters=3, _max_interactions=10, _neighborhood=1,
                                            _learning_rate=0.98, _decrease=True, _output="KEYS")
            print('Treinamento finalizado [{}] ...'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
            exit(0)

        if '-ts' in arguments or '--test' in arguments:
            print('Test')
    else:
        print(help)
        exit(0)

        porcent = 1

        print(sys.argv)

    # if 4 < len(sys.argv) and sys.argv[4] in ('-p', '--porcent'):
    #         if 5 < len(sys.argv):
    #             porcent = float(sys.argv[5])
    #
    #     # TREINAMENTO ##################################################################################################
    #     print(time.strftime("%Y-%m-%d %H:%M:%S"))
    #     clusters = Kohonen.training(inputs, _max_clusters=3, _max_interactions=10, _neighborhood=1,
    #                                 _learning_rate=0.98, _decrease=True, _output="KEYS")
    #     print(time.strftime("%Y-%m-%d %H:%M:%S"))
    #
    #     sys.exit(0)
    #
    # elif len(sys.argv) > 1 and sys.argv[1] in ('-ts', '--test'):
    #
    #     inputs = weigth = None
    #
    #     # TESTE ########################################################################################################
    #
    #     if sys.argv[4] in ('-w', '--weigth'):
    #         weigth = str(sys.argv[5])
    #
    #     if inputs is not None:
    #
    #         print(time.strftime("%Y-%m-%d %H:%M:%S"))
    #         clusters = Kohonen.test(inputs, weigth, _max_clusters=3, _output="KEYS")
    #         print(time.strftime("%Y-%m-%d %H:%M:%S\n"))
    #
    #         print("Grupo da entrada: [{}]\n".format(list(clusters.keys())[0] + 1))
    #
    #     else:
    #         print("Não possível identificar a entrada de teste")
    #         exit(0)
