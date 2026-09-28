# Especificación léxica y diseño del lenguaje base

**PDF de origen:** 7_Especificación_Léxica.pdf  
**Páginas:** 13

## Resumen

Explica cómo el lexer agrupa caracteres en lexemas y los clasifica como tokens. Distingue patrón, lexema y token, y muestra reglas para identificadores, números y operadores. También trata la resolución de ambigüedades, el alfabeto, los literales y las palabras reservadas.

## Temas principales

- El token puede representarse con tipo, atributo y posición.
- Ejemplos de patrones: NUMBER con uno o más dígitos e IDENTIFIER que empieza con una letra y continúa con letras o dígitos.
- Ejemplo de entrada: x = 10 + y, que produce identificador, asignación, número y suma.
- Clases léxicas comunes: identificadores, números, palabras reservadas, operadores y delimitadores.
- Mayor coincidencia: escoger el lexema válido más largo, por ejemplo >= antes que >.
- Prioridad de reglas: reconocer if como palabra reservada antes de dejarlo como identificador.
- Ejemplos generales de palabras clave: if, while, return y class.
- Ejemplos de operadores y delimitadores: +, -, *, /, =, <, >, <=, >=, ==, paréntesis, llaves y punto y coma.
- Ejemplos de literales: enteros, números decimales y el booleano true.

## Relación con Práctica 1

La práctica original pide identificadores, enteros, +, = y sus delimitadores. Por solicitud del usuario, el lexer también incorpora tokens de las diapositivas: palabras como `if`, `while`, `return` y `class`; literales decimales y `true`; y operadores como `-`, `*`, `/`, `<`, `>`, `<=`, `>=` y `==`. Esto amplía el análisis léxico, pero no define la gramática de esas construcciones.
