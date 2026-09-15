# Auditoría de stopwords

## 1) Alcance
Se revisó la lista de stopwords usada por el proyecto en `stopwords_es.txt` y la lógica de filtrado en `scraper_actualizado.py`, en particular `palabras_significativas()`.

La regla aplicada por el código es:

- normaliza a minúsculas
- elimina signos de puntuación
- devuelve solo tokens con longitud > 2
- elimina cualquier palabra que aparezca en la lista de stopwords

Esto implica que la auditoría no es solo una revisión nominal de la lista, sino una revisión de su efecto real sobre el corpus.

## 2) Evidencia objetiva
Se verificó la lista con un script de control. Resultado:

```text
total_stopwords= 260
encontradas= ['yo', 'tu', 'el', 'ella', 'ellos', 'nos', 'me', 'te', 'se', 'no', 'ni', 'sin', 'nada', 'porque', 'como', 'cual', 'quien', 'muy', 'tanto', 'algunos', 'otra', 'otros']
pronombres_y_negaciones= 12
```

Ese resultado confirma que la lista actual sí elimina pronombres y negaciones, además de otros términos funcionales.

## 3) Qué quitó la lista
La revisión detectó que la lista elimina, entre otros, estos tipos de palabras:

### Pronombres y clíticos
- yo, tu, el, ella, ellos, nos, me, te, se
- mi, ti, su, sus, lo, la, le, les
- nosotros, vosotros, ellas, etc.

### Negaciones y operadores de oposición
- no, ni, sin, nada
- términos asociados a negación o restricción semántica, aunque en menor frecuencia

### Conectores y palabras funcionales
- porque, como, cual, quien, cuando, donde, entre, sobre, para, por, que
- muy, tanto, mucho, poco, más, menos

## 4) ¿Eso afecta la tesis?
### Evaluación para la hipótesis actual
La hipótesis del trabajo se centra en la frecuencia relativa de adjetivos frente a adverbios. En ese contexto, esta lista es razonablemente apropiada porque:

- elimina palabras funcionales que no aportan contenido léxico
- reduce ruido para el conteo de categorías gramaticales
- ayuda a aislar sustantivos, verbos, adjetivos y adverbios

### Riesgo importante
El principal riesgo aparece si la tesis o un análisis posterior intenta estudiar:

- polaridad léxica
- negación semántica
- valor argumentativo del texto
- concordancias de elementos de negación

En esos casos, quitar `no`, `ni`, `sin` y `nada` puede distorsionar el significado, porque la negación cambia radicalmente la interpretación de un enunciado.

## 5) Ajuste recomendado
Para la tesis actual, no es necesario reemplazar la lista base, porque el filtrado funciona para un análisis de estilo basado en contenido léxico y categorías gramaticales.

Sin embargo, se recomienda mantener una regla explícita de control:

- usar la lista actual para análisis de densidad léxica y POS
- conservar una lista secundaria para análisis de negación o polaridad, donde no se eliminen términos como `no`, `ni`, `sin`, `nada`, `nunca`, `jamás`

## 6) Decisión final
La lista de stopwords actual no es un error metodológico para la hipótesis elegida, pero sí es una decisión que tiene un costo semántico si después se reutiliza para análisis de sentimiento, negación o interpretación pragmática.

Por eso, el registro recomendado es:

- “Sí se eliminan pronombres y conectores funcionales”
- “Sí se eliminan negaciones en análisis de frecuencia léxica”
- “No es recomendable para estudios de polaridad o negación sin una lista especial”

## 7) Registro de decisión
- Archivo auditado: `stopwords_es.txt`
- Total de entradas: 260
- Pronombres / negaciones detectados en la lista: 12 ejemplos relevantes
- Resultado: compatible con la tesis actual, pero no con estudios de negación o polaridad sin un ajuste específico
