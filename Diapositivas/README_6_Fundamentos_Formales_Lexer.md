# Fundamentos formales del análisis léxico

**PDF de origen:** 6_Fundamentos_Formales_Lexer.pdf  
**Páginas:** 18

## Resumen

Introduce lenguajes regulares, expresiones regulares y autómatas finitos deterministas y no deterministas. Explica qué puede reconocer un lexer usando memoria finita y muestra patrones de identificadores y números.

## Temas principales

- Lenguaje regular: puede describirse con expresiones regulares, reconocerse con un autómata finito o generarse mediante una gramática regular.
- Operaciones de expresiones regulares: unión, concatenación y cerradura de Kleene.
- AFD: para cada estado y símbolo tiene una transición determinada.
- AFN: puede tener varias transiciones posibles para una entrada.
- Ejemplo de identificador: letra seguida de cero o más letras o dígitos.
- Ejemplo de número entero: uno o más dígitos.
- Ejemplos de palabras reservadas: if, while y return.

## Relación con Práctica 1

Los patrones de identificador y entero coinciden con las clases del lexer. Por solicitud del usuario, también se añadieron `if`, `while` y `return` como tokens reservados. Son una extensión léxica: la práctica original no define la gramática que les daría estructura.
