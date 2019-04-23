#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random


class Kohonen:

    """

    """
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
        exit(0)

        # Definindo a matriz de pesos
        if cls.set_weigths(_params['input'], _params['max_clusters']):
            print("Definição da matrix de pesos realizada com sucesso!")

        print("\nMatriz de pesos:")
        print("--------------------------------------------------------")
        for item in cls.weigths:
            print(item)
        print("--------------------------------------------------------\n")

        count = 1
        clusters = {}
        _value_decrease = round((_learning_rate / _max_interactions), 5)

        # Verificando se já foi realizado o número máximo de interações
        while count <= _max_interactions:

            print("######################## Interacao [{}] ##########################".format(count))
            # print "Max Clusters: [{}] | Max Interacoes [{}] | Taxa de aprendizado [{}] | Raio: [{}]".format(
            # max_clusters, _max_interactions, _learning_rate, _neighborhood)

            clusters.clear()

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
                _learning_rate = round(_learning_rate - _value_decrease, 5)
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
    def set_weigths(cls, _input, _max_clusters):
        """
        Define a matriz de pesos de acordo com os valores das colunas
        Exemplo: Sorteia um valor entre o valor minimo e maximo de uma coluna
        """
        if cls.weigths is None or len(cls.weigths) <= 0:
            # print "Tamanho das entradas [{}]".format(len(_input[0].values()[0]))
            cls.weigths = []

            # Laço pelo número de colunas
            for x in range(_max_clusters):
                items = []

                # Definindo lista com os valores de cada coluna
                for y in _input:
                    for z in list(y.values())[0]:
                        items.append(z)

                # Definindo o valor minimo e maximo da coluna
                min_input = (min(items) + 0.1) if min(items) >= 0 else (min(items) - 0.1)
                max_input = (max(items) - 0.1) if max(items) > 0 else (max(items) + 0.1)

                # print "Valor minimo: [{}] | Valor maximo: [{}]".format(min_input, max_input)

                # Definindo a matriz de pesos por coluna
                for z in range(len(list(_input[0].values())[0])):
                    if cls.check_key_exists(z) is False:
                        cls.weigths.append([])

                    cls.weigths[z].append(round(random.uniform(min_input, max_input), 2))

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
    def check_key_exists(cls, _x, _y=None):
        try:
            cls.weigths[_x] if _y is None else cls.weigths[_x][_y]
        except IndexError:
            return False
        return True
