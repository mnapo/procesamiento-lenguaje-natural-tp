# Trabajo Práctico - Procesamiento de Lenguaje Natural

## Título-tesis

**¿Existe una diferencia en la frecuencia relativa de adjetivos y adverbios entre las obras del corpus?**

## Informe

El trabajo analiza un corpus de novelas en español para estudiar la frecuencia relativa de **adjetivos (ADJ)** y **adverbios (ADV)**. Para el procesamiento lingüístico se utilizó **spaCy**, con el modelo `es_core_news_lg`, aplicando `nlp.pipe()` sobre el corpus. Se analizaron principalmente las categorías gramaticales (POS), los lemas y la información morfológica.

El análisis permitió observar que la presencia de adjetivos y adverbios no es uniforme entre las obras: existen diferencias en sus frecuencias relativas, lo que muestra que las elecciones léxicas y estilísticas varían según el texto. Sin embargo, las diferencias observadas **no permiten afirmar por sí solas que exista una separación clara y general entre las obras únicamente a partir de estas dos categorías gramaticales**.

Lo que desmiente una interpretación demasiado fuerte de la hipótesis es que las diferencias de frecuencia no necesariamente implican una diferencia estilística global. La frecuencia de ADJ y ADV puede estar condicionada por el tema, el género, la narración y las características particulares de cada obra. Por eso, no alcanza con observar una mayor o menor frecuencia para establecer una relación causal o una clasificación definitiva.

A partir de estos resultados surgen nuevas preguntas: **¿qué ocurre si se incorporan otras categorías gramaticales?, ¿las diferencias se mantienen al controlar por autor, época o extensión de las obras?, ¿qué lemas concretos explican las diferencias de ADJ y ADV?, y ¿es posible distinguir las obras mediante un conjunto más amplio de rasgos lingüísticos?**

## Integrantes

- Amendolia Cerino Camila
- Arribas Yamil
- Cané Germán
- Escobar Sergio
- Firme Fernando
- Montaña Leandro
- Nápoli Matías
- Traviezo González Joselyn
