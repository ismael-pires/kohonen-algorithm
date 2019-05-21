#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import random

from classes.Tools import Tools


class Kohonen:

    """

    """
    input = {}
    weigths = []
    output = None
    max_clusters = None
    neighborhood = None
    learning_rate = None
    max_interaction = None

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

        # Definindo os atributos da classe a partir dos parametros informados
        cls.decrease = _params['decrease']
        cls.neighborhood = _params['neighborhood']
        cls.max_clusters = _params['max_clusters']
        cls.max_interaction = _params['max_interaction']
        cls.learning_rate = _params['learning_rate']
        cls.output = _params['output']

        # Convertendo os dados de entrada para uma lista de dados
        cls.input = Tools.format_data(_params['input'])
        print(cls.input)

        # Definindo a matriz de pesos
        if cls.set_weigths():
            print("Definição da matrix de pesos realizada com sucesso!")

        print("\nMatriz de pesos:")
        print("--------------------------------------------------------")
        for weigth in cls.weigths:
            print(weigth)
        print("--------------------------------------------------------\n")

        # Definindo variáveis do algoritmo
        count = 1
        clusters = {}
        value_decrease = round((cls.learning_rate / cls.max_interaction), 5)

        # Verificando se já foi realizado o número máximo de interações
        while count <= cls.max_interaction:

            print("######################## Interacao [{}] ##########################".format(count))
            print("Max Clusters: [{}] | Max Interacoes [{}] | Taxa de aprendizado [{}] | Raio: [{}]".format(
                cls.max_clusters, cls.max_interaction, cls.learning_rate, cls.neighborhood))

            # Zerando os clusters gerados
            clusters.clear()

            for item in cls.input.items():

                # Definindo a chave e os valores de cada item
                key = item[0]
                values = item[1]

                # Zerando a lista de distancias
                distance = []

                # Calculando a distância de cada neoronio de saída (número de cluster)
                for col in range(cls.max_clusters):
                    result = 0
                    print("\n--------------------------------------------------------")
                    for row in range(len(values)):
                        print("Valor do item na posição [{}] = [{}]".format(row, values[row]))
                        print("Valor do peso de [{}][{}] = [{}]".format(row, col, cls.weigths[row][col]))
                        result += round((cls.weigths[row][col] - values[row]) ** 2, 2)

                    distance.append(round(result, 2))

                # Verificando qual foi o neorônio vencedor após a aplicação da distância
                print("\nValor das distancias: {}".format(distance))
                winner_neuron = distance.index(min(distance))
                print("Neurônio vencedor: [{}] \n".format(distance[winner_neuron]))

                print("\nMatriz de pesos:")
                print("--------------------------------------------------------")
                for weigth in cls.weigths:
                    print(weigth)
                print("--------------------------------------------------------\n")

                # Atualizando os pesos
                cls.update_weigths(values, winner_neuron)

                # Definindo os grupos com seus items correspondentes
                if clusters.get(winner_neuron) is not None:
                    clusters[winner_neuron].append({key: values})
                else:
                    clusters[winner_neuron] = [{key: values}]

            # Incrementando o contador de interações
            count = count + 1

            # Aplicando o decrésimo da taxa de aprendizado
            if cls.decrease:
                cls.learning_rate = round(cls.learning_rate - value_decrease, 5)

            print("Valor da taxa de aprendizado [{}]\n".format(cls.learning_rate))

        print("Meus Grupos: {}\n".format(list(clusters.keys())))

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

            print("Quantidade de itens dos dados de entrada [{}]".format(len(cls.input.values())))
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

                # Laço pelo número máximo de grupos
                for col in range(cls.max_clusters):

                    # Laço pelo número máximo de items
                    for row in range(item_size):

                        # Verificando se já existe a linha na matriz
                        if cls.check_key_exists(row) is False:
                            cls.weigths.append([])

                        # Defininfo mais um item para a coluna
                        cls.weigths[row].append(round(random.uniform(min_input, max_input), 2))

            except (ValueError, TypeError, Exception) as e:
                print('Ocorreu um erro ao identificar os dados de cada item. [{}] (sw-01) '.format(e))
                return False

        return True

    @classmethod
    def update_weigths(cls, _item, _wn):

        # Laço por cada posição do item informado
        for pos in range(len(_item)):

            # Verificando se foi informado o raio (vizinhanca)
            if cls.neighborhood is not None and cls.neighborhood > 0:

                # Verificando toda a vizinhanca
                for nh in range(1, cls.neighborhood + 1):

                    # Verificando se o indice saiu da faixa permitida [0...] e se existe a posição na matriz de pesos
                    if (_wn - nh) > -1 and cls.check_key_exists(pos, _wn - nh):

                        # print "Vou atualizar o antecessor [{}]".format(cls.weigths[y][_wn - n])
                        cls.weigths[pos][_wn - nh] = round(
                            cls.weigths[pos][_wn - nh] + cls.learning_rate * (_item[pos] - cls.weigths[pos][_wn - nh]), 2)

                    # Verificando se o indice saiu da faixa permitida [max_clusters]
                    # e se existe a posição na matriz de pesos
                    if (_wn - nh) < cls.max_clusters and cls.check_key_exists(pos, _wn + nh):

                        # print "Vou atualizar o predecessor [{}]".format(cls.weigths[y][_wn + n])
                        cls.weigths[pos][_wn + nh] = round(
                            cls.weigths[pos][_wn + nh] + cls.learning_rate * (_item[pos] - cls.weigths[pos][_wn + nh]), 2)

            # Atualizando os pesos do neuronio vencedor
            cls.weigths[pos][_wn] = round(cls.weigths[pos][_wn] + cls.learning_rate * (_item[pos] - cls.weigths[pos][_wn]), 2)

        print("\nMatriz de pesos atualizada:")
        print("--------------------------------------------------------")
        for weigth in cls.weigths:
            print(weigth)
        print("--------------------------------------------------------\n")

        return True

    @classmethod
    def check_key_exists(cls, _row, _col=None):
        try:
            cls.weigths[_row] if _col is None else cls.weigths[_row][_col]
        except IndexError:
            return False
        return True

    @classmethod
    def write_output(cls, _clusters):

        # Definindo o nome do diretório do arquivo de saída
        dirname = os.path.dirname(cls.output)

        # Verificando se o diretório existe, senão cria o mesmo
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except OSError as e:
                print("Ocorreu um erro ao criar o diretório do arquivo de saída. [{}] (wo-01)".format(e))

        # Escrevendo os dados dentro do arquivo de saída
        f = open(cls.output, 'w')
        for weigth in cls.weigths:
            print(json.dumps(weigth))
            f.write(json.dumps(weigth) + "\n")

        for cluster in _clusters.items():
            print(json.dumps(cluster))
            f.write(json.dumps(cluster) + "\n")

        f.close()

