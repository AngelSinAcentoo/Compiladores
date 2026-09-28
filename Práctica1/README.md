# Practica 1 - Lexer de MiniLang

Este es mi lexer para la Practica 1 de Compiladores. Esta hecho a mano, sin usar
lex/flex ni nada parecido: el programa lee el codigo fuente caracter por
caracter y va armando la lista de tokens el mismo.

## Como funciona

`lexer.py` tiene una clase `Lexer` que guarda tres cosas: el codigo fuente
completo, la posicion donde vamos leyendo y la linea/columna actual (esto
ultimo es solo para que los mensajes de error sean mas utiles).

El metodo `analizar()` es el corazon del programa: en cada vuelta del ciclo
mira el caracter actual y decide que hacer:

- Si es un espacio, tab o salto de linea, se ignora.
- Si empieza un comentario `/* ... */`, se salta hasta encontrar el cierre.
- Si es una letra, se lee el identificador completo (letras + digitos). Luego
  se clasifica como palabra reservada (`program`, `int`, `print`, `float`,
  `bool`, `if`, `while`, `for`, `return` o `class`), como literal booleano
  (`true`) o como `ID`.
- Si empieza con un digito, se lee un entero como `NUM` o un decimal como
  `FLOAT_NUM` (por ejemplo, `3.141592`).
- Los operadores de dos caracteres (`<=`, `>=`, `==`) se revisan antes que los
  de un caracter para aplicar la regla de mayor coincidencia. Tambien reconoce
  `= + - * / < > ; ( ) { }`.
- Si no calza con nada de lo anterior, se lanza un `ErrorLexico` indicando el
  simbolo y en donde aparecio.

Cada token se imprime con el formato `(TIPO, lexema)`, que es el mismo formato
que pide el enunciado.

## Como ejecutarlo

Se necesita Python 3. El programa recibe la ruta de un archivo con codigo
MiniLang:

```bash
python lexer.py ejemplo.mini
```

Tambien se puede importar y usar la funcion `tokenizar(codigo)` desde otro
script, que recibe un string y devuelve la lista de tokens.

## Pruebas que hice

### Prueba 1: el ejemplo del enunciado

Archivo de entrada:

```
program ejemplo {
  int x;
  x = 5 + 3;
  print(x);
}
```

Salida del lexer:

```
(PROGRAM, program)
(ID, ejemplo)
(LBRACE, {)
(INT, int)
(ID, x)
(SEMICOLON, ;)
(ID, x)
(ASSIGN, =)
(NUM, 5)
(PLUS, +)
(NUM, 3)
(SEMICOLON, ;)
(PRINT, print)
(LPAREN, ()
(ID, x)
(RPAREN, ))
(SEMICOLON, ;)
(RBRACE, })
```

Coincide exactamente con lo que pide el PDF de la practica.

### Prueba 2: variables con nombres distintos y un comentario

Quise probar con otros nombres de variable y ademas meter un comentario de
bloque en medio, para revisar que se ignora bien:

```
program suma {
  /* este programa suma dos numeros */
  int total;
  total = 12 + 8;
  print(total);
}
```

Salida:

```
(PROGRAM, program)
(ID, suma)
(LBRACE, {)
(INT, int)
(ID, total)
(SEMICOLON, ;)
(ID, total)
(ASSIGN, =)
(NUM, 12)
(PLUS, +)
(NUM, 8)
(SEMICOLON, ;)
(PRINT, print)
(LPAREN, ()
(ID, total)
(RPAREN, ))
(SEMICOLON, ;)
(RBRACE, })
```

El comentario no aparece en ningun lado de la salida, que es justo lo que
tiene que pasar.

### Prueba 3: simbolo invalido

Con la entrada del enunciado:

```
x = 5 @ 3;
```

el lexer se detiene y muestra:

```
Error lexico en linea 1, columna 7: simbolo '@' no reconocido
```

Ademas probe dejando un comentario de bloque sin cerrar (`/* algo` sin el
`*/`) y tambien lanza un error lexico avisando que falta el cierre.

## Extension con tokens de las diapositivas

Ademas de los tokens de la practica, el lexer reconoce los ejemplos de
palabras y operadores que aparecen en las diapositivas:

- Palabras reservadas: `if`, `while`, `for`, `return`, `class`, `float` y
  `bool`.
- Literales booleanos: `true` y `false`, ambos con tipo `BOOL_LITERAL`.
- Literal decimal, con tipo `FLOAT_NUM`.
- Operadores: `-`, `*`, `/`, `%`, `<`, `>`, `!`, `<=`, `>=`, `==`, `!=`, `&&` y
  `||`.

Se conservan los tipos de la practica (`ID`, `NUM`, `INT`, `PRINT`, `ASSIGN`,
`PLUS` y los delimitadores) para que sus ejemplos sigan generando la misma
salida. La práctica original no define la gramática de `if`, `for`, clases ni
tipos booleanos; el lexer solo reconoce sus tokens, no valida esas estructuras.

Ejemplo de entrada:

```
if (x <= 3.5) { return x - 1; }
```

Salida esperada:

```
(IF, if)
(LPAREN, ()
(ID, x)
(LE, <=)
(FLOAT_NUM, 3.5)
(RPAREN, ))
(LBRACE, {)
(RETURN, return)
(ID, x)
(MINUS, -)
(NUM, 1)
(SEMICOLON, ;)
(RBRACE, })
```
