#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random

from classes.Tools import Tools


class Kohonen:

    """

    """
    input = {}
    weigths = []
    decrease = True
    neighborhood = 1
    max_clusters = 2
    max_interaction = 2
    learning_rate = 0.98

    def __init__(self):
        pass

    @classmethod
    def training(cls, _params):
        """
        Método de processamento do algoritmo de Kohonen
        :param _params:        Dicionário de dados
        :return:
        """

        print(_params)

        # Convertendo os dados de entrada para uma lista de dados
        cls.input = Tools.format_data(_params['input'])

        print(cls.input)

        # Definindo a matriz de pesos
        if cls.set_weigths():
            print("Definição da matrix de pesos realizada com sucesso!")

        print("\nMatriz de pesos:")
        print("--------------------------------------------------------")
        for item in cls.weigths:
            print(item)
        print("--------------------------------------------------------\n")

        count = 1
        clusters = {}
        value_decrease = round((cls.learning_rate / cls.max_interaction), 5)

        # Verificando se já foi realizado o número máximo de interações
        while count <= cls.max_interaction:

            print("######################## Interacao [{}] ##########################".format(count))
            # print "Max Clusters: [{}] | Max Interacoes [{}] | Taxa de aprendizado [{}] | Raio: [{}]".format(
            # max_clusters, _max_interactions, _learning_rate, _neighborhood)

            clusters.clear()

            for item in cls.input:

                # Dicionário da entrada
                d = item
                # Valor(lista) da entrada
                x = list(x.values())[0]

                # Zerando a lista de distancias
                distance = []

                # Calculando a distância de cada neoronio de saída (número de cluster)
                for y in range(_max_clusters):
                    result = 0
                    # print "\n--------------------------------------------------------"
                    for z in range(len(x)):
                        # print "Valor de x[{}] = [{}]".format(z, x[z])
                        # print "Valor de w[{}][{}] = [{}]".format(z, y, cls.weigths[z][y])
                        result += round((cls.weigths[z][y] - x[z]) ** 2, 2)

                    distance.append(round(result, 2))

                # print "\nValor das distancias: {}".format(distance)
                winner_neuron = distance.index(min(distance))
                # print "Neurônio vencedor: [{}] \n".format(winner_neuron)

                if clusters.get(winner_neuron) is not None:
                    if _output == "FULL":
                        clusters[winner_neuron].append(d)
                    elif _output == "KEYS":
                        clusters[winner_neuron].append(list(d.keys())[0])
                    else:
                        clusters[winner_neuron].append(list(d.values())[0])
                else:
                    if _output == "FULL":
                        clusters[winner_neuron] = [d]
                    elif _output == "KEYS":
                        clusters[winner_neuron] = [list(d.keys())[0]]
                    else:
                        clusters[winner_neuron] = [list(d.values())[0]]

                # print "Matriz de pesos:"
                # print "--------------------------------------------------------"
                # for item in cls.weigths:
                #     print item
                # print "--------------------------------------------------------\n"

                # Atualizando os pesos
                cls.update_weigths(x, winner_neuron, _neighborhood, _learning_rate, _max_clusters)

            count = count + 1

            # Aplicando o decrésimo da taxa de aprendizado
            if _decrease:
                _learning_rate = round(_learning_rate - value_decrease, 5)
            print("Valor da taxa de aprendizado [{}]\n".format(_learning_rate))

        f = open('./weigths_{}_{}_{}_{}_{}.txt'.format(
            _max_clusters, _max_interactions, _neighborhood, _learning_rate, _decrease), 'w')

        for item in cls.weigths:
            f.write(json.dumps(item) + "\n")

        print("Meus Grupos: {}\n".format(list(clusters.keys())))

        for item in clusters.items():
            print(json.dumps(item))
            f.write(json.dumps(item) + "\n")

        f.close()

        return clusters

    @classmethod
    def test(cls, _params):

        clusters = {}

        with open(_file_weigth+".txt", "r") as f:
            data = f.readlines()
            for line in data:
                cls.weigths.append(line.replace("\n", "").replace("[", "").replace("]", "").split(','))

        # print "Matriz de pesos:"
        # print "--------------------------------------------------------"
        # for item in cls.weigths:
        #     print item
        # print "--------------------------------------------------------\n"

        for x in _input:

            # Dicionário da entrada
            d = x
            # Valor(lista) da entrada
            x = list(x.values())[0]

            # Zerando a lista de distancias
            distance = []

            # Calculando a distância de cada neoronio de saída (número de cluster)
            for y in range(_max_clusters):
                result = 0
                # print "\n--------------------------------------------------------"
                for z in range(len(x)):
                    # print "Valor de x[{}] = [{}]".format(z, x[z])
                    # print "Valor de w[{}][{}] = [{}]".format(z, y, float(cls.weigths[z][y]))
                    result += round((float(cls.weigths[z][y]) - float(x[z])) ** 2, 2)

                distance.append(round(result, 2))

            # print "\nValor das distancias: {}".format(distance)
            winner_neuron = distance.index(min(distance))
            # print "Neurônio vencedor: [{}] \n".format(winner_neuron)

            if clusters.get(winner_neuron) is not None:
                if _output == "FULL":
                    clusters[winner_neuron].append(d)
                elif _output == "KEYS":
                    clusters[winner_neuron].append(list(d.keys())[0])
                else:
                    clusters[winner_neuron].append(list(d.values())[0])
            else:
                if _output == "FULL":
                    clusters[winner_neuron] = [d]
                elif _output == "KEYS":
                    clusters[winner_neuron] = [list(d.keys())[0]]
                else:
                    clusters[winner_neuron] = [list(d.values())[0]]
        return clusters

    @classmethod
    def set_weigths(cls):
        """
        Define a matriz de pesos de acordo com os valores das colunas
        Exemplo: Sorteia um valor entre o valor minimo e maximo de uma coluna
        """
        if cls.weigths is None or len(cls.weigths) <= 0:

            print("Tamanho das entradas [{}]".format(len(cls.input.values())))
            cls.weigths = []
            items = []
            item_size = 0

            try:

                # Definindo lista com os valores de cada item
                for item in cls.input.values():

                    # Definindo o tamanho do maior item informado
                    item_size = len(item)

                    # Lendo os valores de cada item
                    for value in item:
                        items.append(value)

                # Definindo o valor minimo e maximo da coluna
                min_input = (min(items) + 0.1) if int(min(items)) >= 0 else (min(items) - 0.1)
                max_input = (max(items) - 0.1) if int(max(items)) > 0 else (max(items) + 0.1)

                print("Valor minimo: [{}] | Valor maximo: [{}]".format(min_input, max_input))

                # Número de linhas é igual ao tamanho do maior item
                # Número de colunas é igual ao número de clusters
                # TODO: Tentar deixar mais parecido com o real linhas e colunas

                # Laço pelo número máximo de grupos
                for col in range(cls.max_clusters):

                    # Laço pelo número máximo de items
                    for row in range(item_size):

                        # Verificando se já existe a coluna na matriz
                        if cls.check_key_exists(col) is False:
                            cls.weigths.append([])

                        # Defininfo mais um item para a coluna
                        cls.weigths[col].append(round(random.uniform(min_input, max_input), 2))

            except (ValueError, TypeError, Exception) as e:
                print('Ocorreu um erro ao identificar os dados de cada item. [{}] (sw-01) '.format(e))
                return False

        return True

    @classmethod
    def update_weigths(cls, _x, _wn, _nh, _lr, _mc):

        # Atualizando a matriz de pesos
        for y in range(len(_x)):

            # Verificando se foi informado o raio (vizinhanca)
            if _nh is not None and _nh > 0:

                # Verificando toda a vizinhanca
                for n in range(1, _nh + 1):

                    # Verificando se o indice saiu da faixa permitida [0...] e se existe a posição na matriz de pesos
                    if (_wn - n) > -1 and cls.check_key_exists(y, _wn - n):
                        # print "Vou atualizar o antecessor [{}]".format(cls.weigths[y][_wn - n])
                        cls.weigths[y][_wn - n] = round(
                            cls.weigths[y][_wn - n] + _lr * (_x[y] - cls.weigths[y][_wn - n]), 2)

                    # Verificando se o indice saiu da faixa permitida [max_clusters] e
                    # se existe a posição na matriz de pesos
                    if (_wn - n) < _mc and cls.check_key_exists(y, _wn + n):
                        # print "Vou atualizar o predecessor [{}]".format(cls.weigths[y][_wn + n])
                        cls.weigths[y][_wn + n] = round(
                            cls.weigths[y][_wn + n] + _lr * (_x[y] - cls.weigths[y][_wn + n]), 2)

            # Atualizando os pesos do neuronio vencedor
            cls.weigths[y][_wn] = round(cls.weigths[y][_wn] + _lr * (_x[y] - cls.weigths[y][_wn]), 2)

        return True

    @classmethod
    def check_key_exists(cls, _col, _row=None):
        try:
            cls.weigths[_col] if _row is None else cls.weigths[_col][_row]
        except IndexError:
            return False
        return True
