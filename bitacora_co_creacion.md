# Bitácora de Co-creación

## Fase 1 — Generación del abanico

### Prompt utilizado
«Somos estudiantes universitarios de la materia Laboratorio de Tecnologías de Procesamiento del Lenguaje Natural. Se nos pidió conformar un corpus de 12 textos en español de [Ficción / No Ficción], con el fin de realizar un análisis de estilo cuantitativo mediante minería de textos (frecuencias, Bag of Words y TF-IDF).

Necesitamos que actúes como consultor experto en lingüística computacional y nos propongas 5 posibles preguntas guía de investigación o hipótesis lingüísticas que sean metodológica y matemáticamente viables de responder analizando un corpus tan pequeño de solo 12 documentos de este género. Enfocá las hipótesis en rasgos formales medibles cuantitativamente: distribución gramatical de categorías de palabras, densidad léxica, polaridad o patrones de adjetivación.»


### Respuesta de la IA
1.	¿Qué categorías gramaticales predominan en los textos del corpus y cómo varía su distribución entre documentos?
Pueden medir la proporción de sustantivos, verbos, adjetivos y adverbios respecto del total de palabras de cada texto. Por ejemplo: adjetivos / total de tokens. Esto permite comparar si algunos documentos presentan un estilo más descriptivo —mayor presencia de sustantivos y adjetivos— o más orientado a acciones —mayor proporción de verbos—. Requiere etiquetado POS, por ejemplo con spaCy. 

2.	¿Existen diferencias de densidad léxica entre los 12 textos?
Una opción sencilla es medir qué proporción del texto corresponde a palabras de contenido: sustantivos + verbos + adjetivos + adverbios / total de palabras. Una mayor densidad indicaría mayor concentración de contenido léxico frente a palabras funcionales. También pueden complementar esto con diversidad léxica, por ejemplo palabras únicas / total de palabras, aunque conviene distinguir conceptualmente densidad de diversidad. 

3.	¿Qué documentos presentan mayor grado de adjetivación y qué adjetivos caracterizan a cada uno?
Primero pueden calcular cantidad de adjetivos / cantidad de sustantivos o adjetivos / total de palabras. Después, mediante TF-IDF, identificar qué adjetivos tienen mayor peso distintivo en cada documento. Esto combina muy bien análisis gramatical con las técnicas que les pide la materia. 
Contrastable: podemos medir la proporción de adjetivos respecto del total de palabras de cada documento y comparar el grado de adjetivación entre los 12 textos. Además, mediante TF-IDF podemos identificar qué adjetivos son más característicos de cada documento.

4.	¿La polaridad léxica de los textos es predominantemente positiva, negativa o neutra, y existen diferencias entre documentos?
Pueden asignar puntuaciones de sentimiento a palabras o segmentos y calcular por documento indicadores como proporción de términos positivos y negativos o una puntuación media de polaridad. Después pueden contrastar esos resultados con las palabras de mayor TF-IDF. La precaución aquí es importante: polaridad léxica no equivale necesariamente al tono real del texto, especialmente en ficción, donde aparecen ironía, diálogos o negaciones. 

5.	¿Qué vocabulario permite diferenciar cuantitativamente el estilo de cada documento dentro del corpus?
Esta es especialmente apropiada para Bag of Words y TF-IDF. Bag of Words les permite observar las palabras más frecuentes y compartidas, mientras que TF-IDF permite detectar términos que tienen un peso relativamente alto en determinados documentos y bajo en los demás. 

### Decisión del equipo
Las propuestas fueron clasificadas en los grupos A, B y C...
1. Contrastable: podemos medir cuantitativamente la proporción de sustantivos, verbos, adjetivos y adverbios respecto del total de palabras de cada texto y comparar su distribución entre los 12 documentos.
2. Contrastable: se puede calcular la densidad léxica mediante la proporción de sustantivos, verbos, adjetivos y adverbios respecto del total de palabras, y comparar el resultado entre los 12 documentos.
3. Contrastable: podemos medir la proporción de adjetivos respecto del total de palabras de cada documento y comparar el grado de adjetivación entre los 12 textos. Además, mediante TF-IDF podemos identificar qué adjetivos son más característicos de cada documento
4. Nombra algo real, pero todavía no medible: la polaridad léxica es un fenómeno que puede analizarse cuantitativamente, pero la hipótesis todavía no establece una magnitud concreta ni el criterio con el que se asignarán valores positivos, negativos o neutros a las palabras. Sería necesario definir previamente una métrica o método de análisis de sentimiento.
5. Contrastable: podemos medir la frecuencia de las palabras mediante Bag of Words y utilizar TF-IDF para identificar los términos con mayor peso en cada documento, comparándolos con los demás textos del corpus.

## Operacionalización

### Hipótesis seleccionada inicialmente
4.	¿La polaridad léxica de los textos es predominantemente positiva, negativa o neutra, y existen diferencias entre documentos?

### Decisión del equipo
Se seleccionó esta propuesta del grupo B para realizar el proceso
de operacionalización.

### Operacionalización

01. Qué se cuenta...
Se cuenta la cantidad de palabras positivas, negativas y neutras presentes en cada documento.
02. Contra qué se compara...
Se van a comparar entre ellas dentro de un mismo documento y también entre todos los documentos. Por ejemplo, qué porcentaje de palabras negativas hay en un documento y cómo se compara ese porcentaje con el de los demás documentos.
Hipótesis operacionalizada: En los textos del corpus, la proporción de palabras positivas es mayor que la proporción de palabras negativas y neutras.”
03. Qué resultado la refutaría...
Que la proporción de palabras positivas no sea mayor que la proporción de palabras negativas y neutras.

## Consulta de viabilidad

### Prompt utilizado
«Esta es nuestra hipótesis de trabajo: "En los textos del corpus predominan las palabras de polaridad positivas sobre las negativas y neutras". Vamos a contrastarla sobre un corpus de 12 textos en español usando exclusivamente estas técnicas: Bag of Words, frecuencias relativas, TF-IDF, spaCy NER, análisis POS, lematización, morfología verbal con token.morph y concordancias.

Indicá qué variable textual habría que contrastar, con cuál de esas técnicas se obtiene, y qué operación de comparación permitiría confirmar o refutar la afirmación. Si alguna parte de la hipótesis no es contrastable con este repertorio, señalalo explícitamente.»

### Respuesta de la IAG
La variable textual que habría que contrastar es la polaridad léxica, clasificando las palabras como positivas, negativas o neutras. Una vez realizada esa clasificación, las frecuencias relativas permitirían calcular y comparar la proporción de cada categoría en los documentos.
Sin embargo, con las técnicas permitidas podemos contar palabras, calcular frecuencias, identificar categorías gramaticales, lematizar, obtener TF-IDF, etc., pero ninguna de ellas asigna por sí misma una polaridad positiva, negativa o neutra a una palabra. Por lo tanto, la hipótesis no puede contrastarse completamente con el repertorio de técnicas disponible.

### Decisión del equipo
Se aceptó la observación y se decidió reformular la hipótesis.

### Hipótesis final
**En los textos del corpus, los adjetivos presentan una frecuencia relativa mayor que los adverbios, lo que indíca un predominio de una narrativa descriptiva por sobre una narrativa orientada a la acción**


## Curaduría del corpus

### Prompt utilizado
«Como especialista en curaduría de datos textuales, sugerime una rúbrica de 5 criterios de control para conformar un corpus balanceado de 12 textos en español orientados a contrastar la hipótesis: "[ En los textos del corpus, los adjetivos presentan una frecuencia relativa mayor que los adverbios]". Necesitamos controlar: dispersión de longitud (tokens), estabilidad del registro lingüístico, balance temporal o de autoría, trazabilidad ética de las fuentes y formato de almacenamiento estructurado.»

### Respuesta de la IA
| Criterio | Qué controlar | Regla práctica para los 12 textos |
|---|---|---|
| **1. Dispersión de longitud** | Evitar diferencias excesivas en la cantidad de tokens entre documentos. | Seleccionar textos de extensión similar o establecer un rango de tokens. Como se utilizarán frecuencias relativas, las diferencias moderadas de longitud son aceptables, pero deben registrarse. |
| **2. Estabilidad del registro lingüístico** | Evitar mezclar registros muy diferentes que puedan afectar artificialmente el uso de adjetivos y adverbios. | Mantener el mismo macrogénero y un registro comparable entre los 12 textos. Registrar género, subgénero y tipo de texto. |
| **3. Balance temporal y de autoría** | Evitar que un período histórico o un único autor domine el corpus. | Distribuir los textos entre distintos autores y, si abarcan diferentes épocas, procurar una representación equilibrada de los períodos seleccionados. |
| **4. Trazabilidad ética de las fuentes** | Poder determinar exactamente de dónde proviene cada documento y si puede utilizarse. | Registrar para cada texto autor, título, fecha, fuente y condiciones de acceso/uso. Priorizar textos de dominio público o fuentes que permitan su utilización académica. |
| **5. Almacenamiento estructurado** | Garantizar que todos los documentos puedan procesarse bajo las mismas condiciones. | Guardar los 12 textos con la misma codificación —por ejemplo UTF-8— y una estructura uniforme. Mantener metadatos como ID, autor, título, año, fuente y cantidad de tokens. |

Como criterio adicional específico para la hipótesis planteada, se propuso controlar que los textos sean adecuados para el análisis de categorías gramaticales mediante POS, sin seleccionarlos en función de que presenten previamente una mayor frecuencia de adjetivos que de adverbios.

### Decisión del equipo
El equipo decidió aplicar los cinco criterios propuestos para seleccionar y controlar los documentos del corpus. Además, se incorporó como criterio específico que los textos fueran novelas en español aptas para el análisis POS de adjetivos y adverbios. La selección de los documentos se realizó sin conocer previamente el resultado de esa comparación, para evitar condicionar la hipótesis.