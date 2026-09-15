# FUENTE

## Origen de los textos

Los textos que conforman el corpus corresponden a novelas en español
obtenidas de Wikisource.
url	| Cant-Tokens |	Titulo de la página	| Autoría de la página | Fecha de publicación de la página | Año de publicación de la Obra | Licencia |	Medio
https://es.wikisource.org/wiki/Caramur%C3%BA	48766	Caramurú - Wikisource	Alejandro Magariños Cervantes	14/03/2007	1865	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/Do%C3%B1a_Luz	59381	Doña Luz - Wikisource	Juan Valera	27/03/2007	1879	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/A_flor_de_piel	60849	A flor de piel - Wikisource	Antonio de Hoyos y Vinent	25/01/2008	1907	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/Don_Segundo_Sombra 61274	Don Segundo Sombra - Wikisource	AutorRicardo Güiraldes	05/05/2008	1927	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/A_fuego_lento	64006	A fuego lento - Wikisource	Emilio Bobadilla	17/06/2008	1903	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/Dulce_due%C3%B1o_(Pardo_Baz%C3%A1n)	66584	Dulce dueño (Pardo Bazán) - Wikisource	Emilia Pardo Bazán	29/03/2007	1911	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/Cr%C3%B3nica_del_reinado_de_Carlos_IX	66868  Crónica del reinado de Carlos IX - Wikisource	AutorProsper Mérimée	20/02/2008	1920	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/Do%C3%B1a_Milagros	67790	Doña Milagros - Wikisource	Emilia Pardo Bazán	29/03/2007	1894	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/De_Cartago_a_Sagunto	68103	De Cartago a Sagunto - Wikisource	Benito Pérez Galdós	01/02/2006	1911	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/Aurora_roja	69763	Aurora roja - Wikisource	Pío Baroja	03/02/2007	1904	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/Carlos_VI_en_la_R%C3%A1pita	70053	Carlos VI en la Rápita - Wikisource	Benito Pérez Galdós	21/02/2007	1905	CC BY-SA 4.0	wikisource.org
https://es.wikisource.org/wiki/Ca%C3%B1as_y_barro	74953  Cañas y barro - Wikisource	AutorVicente Blasco Ibáñez	07/12/2006	1916	CC BY-SA 4.0	wikisource.org


## Recolección

Los documentos fueron obtenidos mediante scraping utilizando Python,
Requests, BeautifulSoup y Trafilatura.

En las obras divididas en capítulos se recorrieron las distintas páginas
y posteriormente se unificaron sus textos en un único documento.

## Transformaciones de limpieza

Los textos extraídos fueron normalizados mediante:

- Reemplazo de espacios duros (\xa0) por espacios normales.
- Reducción de espacios y tabulaciones consecutivas.
- Reducción de tres o más saltos de línea consecutivos a dos.
- Revisión de restos de HTML y JavaScript.
- Revisión de posibles artefactos de digitalización.

No se eliminaron palabras ni signos lingüísticos necesarios para el
posterior análisis POS.

## Criterios de exclusión

Se excluyeron documentos que:

- Presentaban una longitud muy diferente respecto del resto del corpus.
- No podían extraerse correctamente.
- No disponían de información suficiente sobre su fuente.