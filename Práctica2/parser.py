# Practica 2 - Analizador sintactico descendente (parser LL)
#Angel Emiliano Escobar Hernández
# Compiladores Grupo 06

import argparse
import sys

EPSILON = "ε"
FIN = "$"
# tabla LL del ejemplo 1: no terminal -> token que llega -> lado derecho de la produccion
TABLA_1 = {
    "E": {
        "num": ["T", "E'"],
    },
    "E'": {
        "+": ["+", "T", "E'"],
        "$": [EPSILON],
    },
    "T": {
        "num": ["num"],
    },
}
# tabla LL del ejemplo 2, se usa tambien para los ejemplos 3 y 4
TABLA_2 = {
    "E": {
        "num": ["T", "E'"],
        "(": ["T", "E'"],
    },
    "E'": {
        "+": ["+", "T", "E'"],
        ")": [EPSILON],
        "$": [EPSILON],
    },
    "T": {
        "num": ["F", "T'"],
        "(": ["F", "T'"],
    },
    "T'": {
        "*": ["*", "F", "T'"],
        "+": [EPSILON],
        ")": [EPSILON],
        "$": [EPSILON],
    },
    "F": {
        "num": ["num"],
        "(": ["(", "E", ")"],
    },
}
TABLAS = {
    "1": TABLA_1,
    "2": TABLA_2,
}


class ErrorSintactico(Exception):
    # se lanza si el terminal no coincide con el token o si la casilla de la tabla esta vacia
    def __init__(self, mensaje):
        super().__init__("Error sintactico: {}".format(mensaje))


class Parser:
    # guarda la tabla y el simbolo inicial, la pila se arma de nuevo en cada analisis
    def __init__(self, tabla, simbolo_inicial="E"):
        self.tabla = tabla
        self.simbolo_inicial = simbolo_inicial

    def es_terminal(self, simbolo):
        # los no terminales son las llaves de la tabla, lo demas (incluido $) es terminal
        return simbolo not in self.tabla

    def analizar(self, tokens):
        # algoritmo LL con tabla, el tope de la pila es el ultimo elemento de la lista
        entrada = list(tokens)
        if not entrada or entrada[-1] != FIN:
            entrada.append(FIN)  # los ejemplos 3 y 4 vienen sin $
        pila = [FIN, self.simbolo_inicial]
        i = 0
        while pila:
            tope = pila[-1]
            actual = entrada[i]
            print("Pila: {}, Entrada: {}".format(pila, entrada[i:]))
            if self.es_terminal(tope):
                if tope != actual:
                    raise ErrorSintactico("se esperaba '{}' y llego '{}'".format(tope, actual))
                pila.pop()
                i += 1
                print("Match: {}".format(actual))
                continue
            produccion = self.tabla[tope].get(actual)
            if produccion is None:
                raise ErrorSintactico("no hay produccion para tabla[{}, {}]".format(tope, actual))
            print("Aplicar: {} → {}".format(tope, produccion))
            print("\n")
            pila.pop()
            if produccion != [EPSILON]:  # con epsilon solo se quita el no terminal
                pila.extend(reversed(produccion))
        # la pila ya se vacio pero pudieron quedar tokens despues del $
        if i < len(entrada):
            raise ErrorSintactico("sobran tokens despues de '$': {}".format(entrada[i:]))
        return True


def main():
    # recibe el numero de tabla y la cadena de tokens separados por espacios
    argumentos = argparse.ArgumentParser(description="Parser LL - Practica 2 de Compiladores")
    argumentos.add_argument("tabla", choices=sorted(TABLAS), help="1 para la gramatica del ejemplo 1, 2 para la del ejemplo 2")
    argumentos.add_argument("entrada", help="tokens separados por espacios, por ejemplo \"num + num $\"")
    args = argumentos.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # sin esto windows truena con → y ε al redirigir la salida
    tokens = args.entrada.split()
    try:
        Parser(TABLAS[args.tabla]).analizar(tokens)
    except ErrorSintactico as e:
        print(e)
        return 1
    print("Cadena valida")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # 0 si la cadena es valida, 1 si hay error sintactico
