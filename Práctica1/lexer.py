# Practica 1 - Analizador lexico de MiniLang
# Compiladores, 2026
#
# La idea es recorrer el codigo caracter por caracter (nada de lex/flex) y
# armar la lista de tokens nosotros mismos. Si aparece algo raro que no
# sabemos reconocer, se reporta como error lexico.

import argparse
import sys
from pathlib import Path

# palabras reservadas, si el identificador coincide se cambia el tipo en vez de ID
PALABRAS_RESERVADAS = {
    "program": "PROGRAM",
    "int": "INT",
    "print": "PRINT",
    "float": "FLOAT_TYPE",
    "bool": "BOOL_TYPE",
    "if": "IF",
    "while": "WHILE",
    "for": "FOR",
    "return": "RETURN",
    "class": "CLASS",
}
# literales booleanos
LITERALES_BOOLEANOS = {
    "true": "BOOL_LITERAL",
    "false": "BOOL_LITERAL",
}
# operadores de dos caracteres, se revisan antes que los de uno solo (mayor coincidencia)
SIMBOLOS_COMPUESTOS = {
    "<=": "LE",
    ">=": "GE",
    "==": "EQ",
    "!=": "NEQ",
    "&&": "AND",
    "||": "OR",
}
# simbolos de un solo caracter -> tipo de token
SIMBOLOS_SIMPLES = {
    "=": "ASSIGN",
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "%": "PERCENT",
    "<": "LT",
    ">": "GT",
    "!": "NOT",
    ";": "SEMICOLON",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
}


class Token:
    # guarda tipo, lexema y donde aparecio (para los mensajes de error)
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return "({}, {})".format(self.tipo, self.lexema)  # formato que pide el enunciado


class ErrorLexico(Exception):
    # se lanza con un simbolo desconocido o un comentario de bloque que nunca cierra
    def __init__(self, mensaje, linea, columna):
        self.linea = linea
        self.columna = columna
        texto = "Error lexico en linea {}, columna {}: {}".format(linea, columna, mensaje)
        super().__init__(texto)


class Lexer:
    def __init__(self, codigo_fuente):
        self.codigo = codigo_fuente
        self.pos = 0
        self.linea = 1
        self.columna = 1

    def fin_de_entrada(self):
        return self.pos >= len(self.codigo)

    def ver(self, adelanto=0):
        # mira el caracter actual (o uno mas adelante) sin consumirlo
        i = self.pos + adelanto
        if i >= len(self.codigo):
            return ""
        return self.codigo[i]

    def avanzar(self):
        # consume el caracter actual y actualiza linea/columna
        c = self.codigo[self.pos]
        self.pos += 1
        if c == "\n":
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        return c

    @staticmethod
    def es_letra(c):
        return ("a" <= c <= "z") or ("A" <= c <= "Z")

    @staticmethod
    def es_digito(c):
        return "0" <= c <= "9"

    def leer_identificador(self):
        inicio = self.pos
        while not self.fin_de_entrada() and (self.es_letra(self.ver()) or self.es_digito(self.ver())):
            self.avanzar()
        return self.codigo[inicio:self.pos]

    def leer_numero(self):
        inicio = self.pos
        while not self.fin_de_entrada() and self.es_digito(self.ver()):
            self.avanzar()
        # si hay punto seguido de digito es decimal, si no se deja como NUM y
        # el punto se reporta como simbolo raro en la siguiente vuelta
        tipo = "NUM"
        if self.ver() == "." and self.es_digito(self.ver(1)):
            tipo = "FLOAT_NUM"
            self.avanzar()
            while not self.fin_de_entrada() and self.es_digito(self.ver()):
                self.avanzar()
        return self.codigo[inicio:self.pos], tipo

    def saltar_comentario_bloque(self):
        # ya sabemos que estamos parados justo en "/*"
        linea_inicio = self.linea
        columna_inicio = self.columna
        self.avanzar()
        self.avanzar()
        while not self.fin_de_entrada():
            if self.ver() == "*" and self.ver(1) == "/":
                self.avanzar()
                self.avanzar()
                return
            self.avanzar()
        # se acabo el archivo y nunca cerro el comentario
        raise ErrorLexico("comentario de bloque sin cerrar (falta '*/')", linea_inicio, columna_inicio)

    def analizar(self):
        # recorre todo el codigo y devuelve la lista de tokens en orden
        tokens = []
        while not self.fin_de_entrada():
            c = self.ver()
            if c in (" ", "\t", "\r", "\n"):  # espacios y saltos se ignoran
                self.avanzar()
                continue
            if c == "/" and self.ver(1) == "*":  # comentario /* ... */
                self.saltar_comentario_bloque()
                continue
            linea_tok = self.linea
            columna_tok = self.columna
            if self.es_letra(c):
                lexema = self.leer_identificador()
                tipo = PALABRAS_RESERVADAS.get(lexema)
                if tipo is None:
                    tipo = LITERALES_BOOLEANOS.get(lexema, "ID")
                tokens.append(Token(tipo, lexema, linea_tok, columna_tok))
                continue
            if self.es_digito(c):
                lexema, tipo = self.leer_numero()
                tokens.append(Token(tipo, lexema, linea_tok, columna_tok))
                continue
            operador_doble = c + self.ver(1)
            if operador_doble in SIMBOLOS_COMPUESTOS:
                self.avanzar()
                self.avanzar()
                tokens.append(Token(SIMBOLOS_COMPUESTOS[operador_doble], operador_doble, linea_tok, columna_tok))
                continue
            if c in SIMBOLOS_SIMPLES:
                self.avanzar()
                tokens.append(Token(SIMBOLOS_SIMPLES[c], c, linea_tok, columna_tok))
                continue
            # no calzo con nada de lo anterior, simbolo desconocido
            raise ErrorLexico("simbolo '{}' no reconocido".format(c), linea_tok, columna_tok)
        return tokens


def tokenizar(codigo_fuente):
    # atajo para no instanciar Lexer a mano desde afuera
    lexer = Lexer(codigo_fuente)
    return lexer.analizar()


def main():
    parser = argparse.ArgumentParser(description="Lexer de MiniLang - Practica 1 de Compiladores")
    parser.add_argument("archivo", help="ruta al archivo con codigo MiniLang")
    args = parser.parse_args()
    ruta = Path(args.archivo)
    try:
        codigo = ruta.read_text(encoding="utf-8")
    except OSError as e:
        print("No se pudo abrir el archivo {}: {}".format(ruta, e), file=sys.stderr)
        return 2
    try:
        tokens = tokenizar(codigo)
    except ErrorLexico as e:
        print(e)
        return 1
    for t in tokens:
        print(t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
