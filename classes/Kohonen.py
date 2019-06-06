#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import random

from classes.Tools import Tools


class Kohonen:

    """
    Classe responsável por executar os treinamentos e testes do algoritmo
    Author: Ismael Pires
    """

    input = {}
    weights = []
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
        Método responsável pelo processamento do algoritmo de Kohonen
        :param dict _params:        Dicionário com os parametros informados
        :return: boolean
        """

        # Definindo os atributos da classe a partir dos parametros informados
        cls.decrease = _params['decrease']
        cls.neighborhood = _params['neighborhood']
        cls.max_clusters = _params['max_clusters']
        cls.max_interaction = _params['max_interaction']
        cls.learning_rate = _params['learning_rate']
        cls.output = _params['output']

        # Convertendo os dados de entrada para uma lista de dados
        cls.input = Tools.format_data(_params['input'])

        # Definindo a matriz de pesos
        if not cls.set_weights():
            print("Ocorreu um erro ao definir a matriz de pesos. (tr-01)")
            return False

        print("Definição da matriz de pesos realizada com sucesso!")
        cls.show_weight_matrix()

        # Definindo variáveis do algoritmo
        count = 1
        clusters = {}
        value_decrease = round((cls.learning_rate / (cls.max_interaction + 1)), 5)

        # Verificando se já foi realizado o número máximo de interações
        while count <= cls.max_interaction:

            print("######################## Interacao [{}] ##########################".format(count))
            print("Max Clusters: [{}] | Max Interacoes [{}] | Taxa de aprendizado [{}] | Raio: [{}]".format(
                cls.max_clusters, cls.max_interaction, cls.learning_rate, cls.neighborhood))

            # Zerando os clusters gerados
            clusters.clear()

            try:
                for item in cls.input.items():

                    # Definindo a chave e os valores de cada item
                    key = item[0]
                    values = item[1]

                    # Zerando a lista de distancias
                    distance = []

                    # Calculando a distância de cada neoronio de saída (número de cluster)
                    for col in range(cls.max_clusters):
                        result = 0
                        # print("\n--------------------------------------------------------")
                        for row in range(len(values)):
                            # print("Valor do item na posição [{}] = [{}]".format(row, values[row]))
                            # print("Valor do peso de [{}][{}] = [{}]".format(row, col, cls.weigths[row][col]))
                            result += round((cls.weights[row][col] - float(values[row])) ** 2, 2)

                        distance.append(round(result, 2))

                    # Verificando qual foi o neurônio vencedor após a aplicação da distância euclidiana
                    # print("\nValor das distancias: {}".format(distance))
                    winner_neuron = distance.index(min(distance))
                    # print("Neurônio vencedor: [{}] \n".format(distance[winner_neuron]))

                    # Atualizando os pesos
                    cls.update_weights(values, winner_neuron)

                    # Definindo os grupos com seus items correspondentes
                    if clusters.get(winner_neuron) is not None:
                        clusters[winner_neuron].append({key: values})
                    else:
                        clusters[winner_neuron] = [{key: values}]

            except (ValueError, TypeError, Exception) as e:
                print('Ocorreu um erro ao processar a interação. [{}] (tr-02) '.format(e))

            # Incrementando o contador de interações
            count = count + 1

            # Aplicando o decrésimo da taxa de aprendizado
            if cls.decrease:
                cls.learning_rate = round(cls.learning_rate - value_decrease, 5)

            print("Valor da taxa de aprendizado [{}]\n".format(cls.learning_rate))

        print("Meus Grupos: {}\n".format(list(clusters.keys())))

        # Escrevendo arquivo de saída
        if not cls.write_output(clusters):
            print("Ocorreu um erro escrever o arquivo com os dados de saída. (tr-03)")
            return False

        print("Arquivo de saída criado com sucesso. [{}]".format(cls.output))
        return True

    @classmethod
    def test(cls, _params):

        clusters = {}
        cls.max_clusters = _params['max_clusters']

        # Convertendo os dados de entrada para uma lista de dados
        cls.input = Tools.format_data(_params['input'])

        # Formatando os dados dos pesos gerados
        result = Tools.format_data(_params['weight'])
        cls.weights = result['weights']
        cls.show_weight_matrix()

        try:
            for item in cls.input.items():

                # Definindo a chave e os valores de cada item
                key = item[0]
                values = item[1]

                # Zerando a lista de distancias
                distance = []

                # Calculando a distância de cada neoronio de saída (número de cluster)
                for col in range(cls.max_clusters):
                    result = 0
                    # print("\n--------------------------------------------------------")
                    for row in range(len(values)):
                        # print("Valor do item na posição [{}] = [{}]".format(row, values[row]))
                        # print("Valor do peso de [{}][{}] = [{}]".format(row, col, cls.weigths[row][col]))
                        result += round((cls.weights[row][col] - float(values[row])) ** 2, 2)

                    distance.append(round(result, 2))

                # Verificando qual foi o neurônio vencedor após a aplicação da distância euclidiana
                # print("\nValor das distancias: {}".format(distance))
                winner_neuron = distance.index(min(distance))
                # print("Neurônio vencedor: [{}] \n".format(distance[winner_neuron]))

                # Definindo os grupos com seus items correspondentes
                if clusters.get(winner_neuron) is not None:
                    clusters[winner_neuron].append({key: values})
                else:
                    clusters[winner_neuron] = [{key: values}]

        except (ValueError, TypeError, Exception) as e:
            print('Ocorreu um erro ao processar a interação. [{}] (ts-01) '.format(e))
            return False

        print(clusters)
        return True

    @classmethod
    def set_weights(cls):
        """
        Método responsável por definir a matriz de pesos
        Exemplo: Sorteia um valor entre o valor minimo e maximo encontrado na lista de dados
        :return:
        """

        if cls.weights is None or len(cls.weights) <= 0:

            print("Quantidade de itens dos dados de entrada [{}]".format(len(cls.input.values())))
            cls.weights = []
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
                min_input = (float(min(items)) + 0.1) if float(min(items)) >= 0 else (float(min(items)) - 0.1)
                max_input = (float(max(items)) - 0.1) if float(max(items)) > 0 else (float(max(items)) + 0.1)

                print("Valor minimo: [{}] | Valor maximo: [{}]".format(min_input, max_input))

                # Número de linhas é igual ao tamanho do maior item
                # Número de colunas é igual ao número de clusters

                # Laço pelo número máximo de grupos
                for col in range(cls.max_clusters):

                    # Laço pelo número máximo de items
                    for row in range(item_size):

                        # Verificando se já existe a linha na matriz
                        if cls.check_key_exists(row) is False:
                            cls.weights.append([])

                        # Defininfo mais um item para a coluna
                        cls.weights[row].append(round(random.uniform(min_input, max_input), 2))

            except (ValueError, TypeError, Exception) as e:
                print('Ocorreu um erro ao identificar os dados de cada item. [{}] (sw-01) '.format(e))
                return False

        return True

    @classmethod
    def update_weights(cls, _item, _wn):
        """
        Método responsável por atualizar a tabela (matriz) de pesos
        :param list _item:          Lista de dados
        :param int _wn:             Neurônio vencedor
        :return: boolean
        """

        # cls.show_weight_matrix('Matriz de pesos antiga')
        try:

            # Laço por cada posição do item informado
            for pos in range(len(_item)):

                # Verificando se foi informado o raio (vizinhanca)
                if cls.neighborhood is not None and cls.neighborhood > 0:

                    # Verificando toda a vizinhanca
                    for nh in range(1, cls.neighborhood + 1):

                        # Verificando se o indice saiu da faixa permitida [0...] e se existe a posição na matriz de pesos
                        if (_wn - nh) > -1 and cls.check_key_exists(pos, _wn - nh):

                            # print("Vou atualizar o antecessor [{}]".format(cls.weigths[y][_wn - n]))
                            cls.weights[pos][_wn - nh] = round(
                                cls.weights[pos][_wn - nh] + cls.learning_rate * (float(_item[pos]) - cls.weights[pos][_wn - nh]), 2)

                        # Verificando se o indice saiu da faixa permitida [max_clusters]
                        # e se existe a posição na matriz de pesos
                        if (_wn - nh) < cls.max_clusters and cls.check_key_exists(pos, _wn + nh):

                            # print("Vou atualizar o predecessor [{}]".format(cls.weigths[y][_wn + n]))
                            cls.weights[pos][_wn + nh] = round(
                                cls.weights[pos][_wn + nh] + cls.learning_rate * (float(_item[pos]) - cls.weights[pos][_wn + nh]), 2)

                # Atualizando os pesos do neuronio vencedor
                cls.weights[pos][_wn] = round(cls.weights[pos][_wn] + cls.learning_rate * (float(_item[pos]) - cls.weights[pos][_wn]), 2)

        except (ValueError, TypeError, Exception) as e:
            print('Ocorreu um erro ao atualizar os pesos. [{}] (uw-01) '.format(e))

        # cls.show_weight_matrix('Matriz de pesos atualizada')
        return True

    @classmethod
    def check_key_exists(cls, _row, _col=None):
        """
        Método responsável por verificar se uma posição existe em uma lista unidimensional ou multidimensional
        :param int _row:        Valor do índice correspondente a linha
        :param int _col:        Valor do índice correspondente a coluna
        :return:
        """
        try:
            cls.weights[_row] if _col is None else cls.weights[_row][_col]
        except IndexError:
            return False
        return True

    @classmethod
    def write_output(cls, _clusters):
        """
        Método responsável por escrever os dados gerados pelo algoritmo em um arquivo
        :param dict _clusters:      Dicionário de grupos
        :return: boolean
        """

        # Definindo o nome do diretório do arquivo de saída
        dirname = os.path.dirname(cls.output)

        try:
            # Verificando se o diretório existe, senão cria o mesmo
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            # Escrevendo os dados dentro do arquivo de saída
            f = open(cls.output, 'w')

            result = {
                'weights': cls.weights,
                'clusters': _clusters
            }

            f.write(json.dumps(result, ensure_ascii=False) + "\n")
            f.close()

        except (OSError, Exception) as e:
            print("Ocorreu um erro ao criar o diretório do arquivo de saída. [{}] (wo-01)".format(e))
            return False
        return True

    @classmethod
    def show_weight_matrix(cls, _title='Matriz de pesos'):
        """
        Método responsável por imprimir na tela a matriz de pesos
        :param string _title:      Título da impressão
        :return: boolean
        """

        print("\n{}".format(_title))
        print("--------------------------------------------------------")
        for weight in cls.weights:
            print(weight)
        print("--------------------------------------------------------\n")
        return True

