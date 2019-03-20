#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections
import csv
import json
import os

import time
import sys

from Kohonen import Kohonen

if __name__ == "__main__":

    inputs = [{"E1": [0, 0, 0, 0, 0]},
              {"E2": [0, 0, 0, 0, 1]},
              {"E3": [0, 0, 0, 1, 1]},
              {"E4": [0, 0, 1, 1, 1]},
              {"E5": [0, 1, 1, 1, 1]},
              {"E6": [1, 1, 1, 1, 1]},
              {"E7": [1, 0, 0, 0, 0]},
              {"E8": [1, 1, 0, 0, 0]},
              {"E9": [1, 1, 1, 0, 0]},
              {"E10": [1, 1, 1, 1, 0]}
              ]

    if len(sys.argv) > 1 and sys.argv[1] in ('-tr', '--training'):

        porcent = 1

        print(sys.argv)

        if 4 < len(sys.argv) and sys.argv[4] in ('-p', '--porcent'):
            if 5 < len(sys.argv):
                porcent = float(sys.argv[5])

        # TREINAMENTO ##################################################################################################
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        clusters = Kohonen.training(inputs, _max_clusters=3, _max_interactions=10, _neighborhood=1,
                                    _learning_rate=0.98, _decrease=True, _output="KEYS")
        print(time.strftime("%Y-%m-%d %H:%M:%S"))

        sys.exit(0)

    elif len(sys.argv) > 1 and sys.argv[1] in ('-ts', '--test'):

        inputs = weigth = None

        # TESTE ########################################################################################################

        if sys.argv[4] in ('-w', '--weigth'):
            weigth = str(sys.argv[5])

        if inputs is not None:

            print(time.strftime("%Y-%m-%d %H:%M:%S"))
            clusters = Kohonen.test(inputs, weigth, _max_clusters=3, _output="KEYS")
            print(time.strftime("%Y-%m-%d %H:%M:%S\n"))

            print("Grupo da entrada: [{}]\n".format(list(clusters.keys())[0] + 1))

        else:
            print("Não possível identificar a entrada de teste")
            exit(0)
