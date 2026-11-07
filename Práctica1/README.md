# Practica 1 - Lexer de MiniLang
## Escobar Hernández Angel Emiliano
## Compiladores
## Grupo 06

En esta práctica implementé un analizador léxico manual para MiniLang. El programa lee un archivo `.mini` carácter por carácter y muestra los tokens en el orden en que aparecen. No ejecuta las instrucciones ni comprueba si la estructura del programa es válida.

## Requisitos e instalación

Se necesita Python 3. El código solo usa módulos incluidos con Python, por lo que no hay paquetes adicionales que instalar. Basta con copiar la carpeta del proyecto, abrir una terminal dentro de ella y comprobar que Python esté disponible con `python --version`.

## Cómo funciona

Primero, `main()` recibe la ruta del archivo y lee su contenido como UTF-8. Después llama a `tokenizar()`, que crea un objeto `Lexer`. El método `analizar()` recorre el texto, ignora espacios y comentarios de bloque `/* ... */`, y va formando la lista de tokens. `Token` guarda el tipo, el lexema y su posición; al imprimirlo se muestra como `(TIPO, lexema)`.

El lexer reconoce las palabras `program`, `int`, `print`, `float`, `bool`, `if`, `while`, `for`, `return` y `class`; también distingue `true` y `false` como `BOOL_LITERAL`. Los identificadores comienzan con una letra ASCII y pueden continuar con letras o dígitos. Los enteros se clasifican como `NUM` y los decimales con dígitos a ambos lados del punto como `FLOAT_NUM`.

Los símbolos simples que reconoce son `=`, `+`, `-`, `*`, `/`, `%`, `<`, `>`, `!`, `;`, `(`, `)`, `{` y `}`. También reconoce `<=`, `>=`, `==`, `!=`, `&&` y `||`. Primero revisa los operadores de dos caracteres para que, por ejemplo, `==` no se separe en dos signos `=`. Si aparece un símbolo desconocido o un comentario sin cierre, `ErrorLexico` indica la línea y la columna.

## Cómo ejecutarlo

Desde la carpeta del proyecto se escribe `python lexer.py` seguido del archivo que se quiere analizar. Por ejemplo:

```bash
python lexer.py ejemplo1p1.mini
python lexer.py ejemplo2p1.mini
```

El primer archivo termina con código de salida `0`. Si hay un error léxico, como en el segundo archivo, termina con `1`. Si no puede abrir el archivo, termina con `2`.

## Pruebas realizadas

En `ejemplo1p1.mini` declaré `x`, le asigné `5+3` y escribí `print(x)`. Al ejecutar el lexer obtuve estos tokens:

```text
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

En `ejemplo2p1.mini` escribí `x=5@3;` en la línea 4. Como `@` no está definido, la salida fue:

```text
Error lexico en linea 4, columna 8: simbolo '@' no reconocido
```

También ejecuté `ejemplo3p1.mini`, `ejemplo4p1.mini` y `ejemplo5p1.mini`. El tercero muestra números decimales, el cuarto booleanos y operadores compuestos, y el quinto un comentario de bloque y un ciclo `while`. Los tres terminaron con código `0`. En el reporte Word están las capturas del código y de la salida de cada ejemplo.
