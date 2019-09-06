#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import json
import os


class Tools:

    """
    Classe responsável por disponibilizar ferramentas mais utlizadas
    Author: Ismael Pires
    """

    def __init__(self):
        pass

    @classmethod
    def format_data(cls, _path, _output='list'):

        if _path is None:
            return None

        try:

            extension = os.path.splitext(_path)[1][1:].strip().lower()

            if extension == 'json':

                with open(_path) as json_file:
                    return json.load(json_file)

            elif extension == 'csv':
                with open(_path) as csv_file:

                    # Lendo os dados do arquivo csv
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    result = {}

                    # Definindo o dicionário de dados
                    for row in csv_reader:

                        # Definindo cada item do meu dicionário, o primeiro item da lista é a chave do dicionário
                        result[row[0]] = row[1:]

                return result

            else:
                return None

        except (AttributeError, ValueError, TypeError, KeyboardInterrupt, Exception) as e:
            print('Ocorreu um erro ao converter os dados. [{}] (fd-01)'.format(e))
            return None


