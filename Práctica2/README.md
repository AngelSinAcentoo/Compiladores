# Practica 2 - Parser LL
## Escobar Hernández Angel Emiliano
## Compiladores
## Grupo 06

En esta práctica implementé un analizador sintáctico descendente con tabla LL. El programa recibe una cadena de tokens, la guarda en un arreglo y la revisa con la pila del algoritmo LL. En cada paso imprime la pila, lo que falta de la entrada y la producción que aplicó o el terminal que coincidió. Al final dice si la cadena es válida o muestra el error sintáctico.

## Requisitos e instalación

Se necesita Python 3; yo lo probé con Python 3.13.2. El código solo usa módulos incluidos con Python, así que no hay paquetes que instalar. Basta con abrir una terminal dentro de la carpeta del proyecto.

## Cómo funciona

Las tablas LL de la consigna están en `TABLA_1` y `TABLA_2` como diccionarios. La primera llave es el no terminal, la segunda es el token que llega y el valor es el lado derecho de la producción. `ε` se guarda en la constante `EPSILON`. `TABLA_1` es la del ejemplo 1 y `TABLA_2` la de los ejemplos 2, 3 y 4.

`main()` recibe el número de tabla y la entrada, separa la entrada por espacios y le pasa esa lista a `analizar()` de la clase `Parser`. Si la lista no termina en `$`, el método lo agrega, ya que los ejemplos 3 y 4 vienen sin él. La pila empieza como `['$', 'E']` y su tope es el último elemento de la lista.

En cada vuelta se compara el tope de la pila con el token actual. Si el tope es terminal y coincide con el token, se saca de la pila y se avanza en la entrada (`Match`); si no coincide, se lanza `ErrorSintactico`. Si el tope es no terminal, se busca la casilla `tabla[tope][token]`. Cuando está vacía también hay error; si tiene producción, se saca el no terminal y se meten los símbolos del lado derecho en orden inverso (`Aplicar`). Con una producción `ε` solo se saca el no terminal.

`es_terminal()` toma como terminal todo lo que no es llave de la tabla, por eso `$` también cuenta como terminal. El análisis termina cuando la pila queda vacía. Si después del `$` todavía quedan tokens, se marca error.

## Cómo ejecutarlo

Desde la carpeta del proyecto se escribe `python parser.py`, el número de tabla y la entrada entre comillas con los tokens separados por espacios:

```bash
python parser.py 1 "num + num $"
python parser.py 2 "num + num * num $"
python parser.py 2 "num + * num"
python parser.py 2 "( ( num + num ) *"
```

Si la cadena es válida el programa termina con código `0`. Si hay un error sintáctico termina con `1`. Si falta un argumento o la tabla no es 1 o 2, `argparse` muestra el uso y termina con `2`.

## Pruebas realizadas

Con la tabla 1 y la entrada `num + num $` obtuve la misma secuencia que pide la consigna:

```text
Pila: ['$', 'E'], Entrada: ['num', '+', 'num', '$']
Aplicar: E → ['T', "E'"]


Pila: ['$', "E'", 'T'], Entrada: ['num', '+', 'num', '$']
Aplicar: T → ['num']


Pila: ['$', "E'", 'num'], Entrada: ['num', '+', 'num', '$']
Match: num
Pila: ['$', "E'"], Entrada: ['+', 'num', '$']
Aplicar: E' → ['+', 'T', "E'"]


Pila: ['$', "E'", 'T', '+'], Entrada: ['+', 'num', '$']
Match: +
Pila: ['$', "E'", 'T'], Entrada: ['num', '$']
Aplicar: T → ['num']


Pila: ['$', "E'", 'num'], Entrada: ['num', '$']
Match: num
Pila: ['$', "E'"], Entrada: ['$']
Aplicar: E' → ['ε']


Pila: ['$'], Entrada: ['$']
Match: $
Cadena valida
```

Con la tabla 2, `num + num * num $` también terminó con `Cadena valida` y código `0`. En `num + * num`, después del `+` queda `T` en la pila y llega `*`; esa casilla está vacía, así que la salida termina con:

```text
Error sintactico: no hay produccion para tabla[T, *]
```

En `( ( num + num ) *` se cierra solo uno de los paréntesis. Después del `*` la pila espera una `F` y la entrada ya está en `$`:

```text
Error sintactico: no hay produccion para tabla[F, $]
```

Además probé dos cadenas con la tabla 2. `( num + num ) * num $` fue válida. `num + num ) $` tiene un paréntesis de más; la pila llega a `['$']` con `)` en la entrada y la salida es `Error sintactico: se esperaba '$' y llego ')'`. Las salidas completas están en el reporte.
