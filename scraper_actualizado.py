import requests
import time
import trafilatura
import json
import re
import csv
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser
from pathlib import Path
from bs4 import BeautifulSoup


class Scraper:
    def __init__(
        self,
        url,
        timeout=20,
        headers=None,
        carpeta_destino="datos",
        nombre_archivo=None,
        **kwargs
    ):
        """Inicializa el scraper con URL, timeout, headers y carpeta de destino."""
        self.url = url
        self.timeout = timeout
        self.headers = headers if headers else {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            )
        }

        self.carpeta_destino = Path(carpeta_destino)
        self.nombre_archivo = (
            nombre_archivo if nombre_archivo else self.url.split("/")[-1]
        )
        self.carpeta_destino.mkdir(parents=True, exist_ok=True)

        self.pagina_temporal = None
        self.kwargs = kwargs
        self.ruta_archivo = self.carpeta_destino / self.nombre_archivo

    def obtener_pagina(self):
        """Obtiene una página y la almacena en pagina_temporal."""
        pausa = 1.0

        try:
            response = requests.get(
                self.url,
                timeout=self.timeout,
                headers=self.headers
            )
            response.raise_for_status()

            self.pagina_temporal = response.text
            time.sleep(pausa)

            return True

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return False

    def permite_scrapeo(self):
        """Lee robots.txt y verifica si el scraping está permitido."""
        try:
            robots_url = urljoin(self.url, "/robots.txt")

            response = requests.get(
                robots_url,
                timeout=self.timeout,
                headers=self.headers
            )
            response.raise_for_status()

            reglas = RobotFileParser()
            reglas.set_url(robots_url)
            reglas.parse(response.text.splitlines())

            user_agent = self.headers.get("User-Agent", "*")

            return reglas.can_fetch(user_agent, self.url)

        except requests.exceptions.RequestException as e:
            print(f"Error al consultar robots.txt: {e}")
            return False

    def guardar_pagina(self):
        """Guarda el HTML de la página principal en un archivo local."""
        print(
            f"Guardando página en carpeta "
            f"{self.carpeta_destino.resolve()}\\{self.nombre_archivo}"
        )

        archivo_destino = self.carpeta_destino / self.nombre_archivo

        if archivo_destino.exists():
            print(
                f"El archivo {self.nombre_archivo} ya existe. "
                "¿Desea sobrescribirlo? (s/n): "
            )
            respuesta = input().lower()

            if respuesta != "s":
                print("No se sobrescribió el archivo.")
                return

        archivo_destino.write_text(
            self.pagina_temporal,
            encoding="utf-8"
        )

        print(f"Página guardada en {archivo_destino.resolve()}")

    def contar_palabra(self, palabra):
        """Cuenta cuántas veces aparece una palabra en el HTML cargado."""
        sopa = BeautifulSoup(self.pagina_temporal, "html.parser")
        texto = sopa.get_text()

        contador = texto.lower().count(palabra.lower())

        return contador

    def obtener_datos_corpus(self):
        """
        Extrae texto y metadatos de la página principal utilizando Trafilatura.
        Se usa para páginas simples y también para recuperar los metadatos de
        una obra multipágina.
        """
        dato_crudo = trafilatura.extract(
            self.pagina_temporal,
            url=self.url,
            output_format="json",
            with_metadata=True
        )

        dato = json.loads(dato_crudo) if dato_crudo else {}

        return dato

    def obtener_enlaces_capitulos(self):
        """
        Obtiene los enlaces internos que cuelgan de la URL principal.

        Ejemplo:
        https://es.wikisource.org/wiki/Cel%C3%ADn
        https://es.wikisource.org/wiki/Cel%C3%ADn/I
        https://es.wikisource.org/wiki/Cel%C3%ADn/II

        La decisión de usar este método sigue siendo explícita desde URLS.
        """
        if not self.pagina_temporal:
            return []

        sopa = BeautifulSoup(self.pagina_temporal, "html.parser")

        base = self.url.rstrip("/")
        parsed_base = urlparse(base)
        prefijo_path = parsed_base.path.rstrip("/") + "/"

        enlaces = []

        for link in sopa.find_all("a", href=True):
            href = link["href"]

            # Elimina fragmentos (#...) antes de comparar.
            url_completa = urljoin(self.url, href)
            url_completa, _ = urldefrag(url_completa)

            parsed = urlparse(url_completa)

            # Solo mismo dominio.
            if parsed.netloc != parsed_base.netloc:
                continue

            # Solo URLs que están debajo de la ruta de la obra.
            if not parsed.path.startswith(prefijo_path):
                continue

            # Evita parámetros de consulta.
            url_limpia = parsed._replace(query="", fragment="").geturl()

            if url_limpia not in enlaces:
                enlaces.append(url_limpia)

        return enlaces

    def obtener_texto_multipagina(self):
        """
        Recorre los capítulos enlazados desde la página principal,
        extrae el texto de cada capítulo con Trafilatura y devuelve
        todo unido como un único documento.
        """
        enlaces = self.obtener_enlaces_capitulos()

        if not enlaces:
            print("No se encontraron capítulos para recorrer.")
            return ""

        print(f"Se encontraron {len(enlaces)} páginas/capítulos.")

        textos = []

        for numero, url_capitulo in enumerate(enlaces, start=1):
            print(
                f"Procesando capítulo {numero}/{len(enlaces)}: "
                f"{url_capitulo}"
            )

            try:
                response = requests.get(
                    url_capitulo,
                    timeout=self.timeout,
                    headers=self.headers
                )
                response.raise_for_status()

                dato_crudo = trafilatura.extract(
                    response.text,
                    url=url_capitulo,
                    output_format="json",
                    with_metadata=True
                )

                dato = json.loads(dato_crudo) if dato_crudo else {}
                texto = dato.get("text", "")

                if texto:
                    textos.append(texto)

                time.sleep(1.0)

            except requests.exceptions.RequestException as e:
                print(
                    f"Error al obtener el capítulo "
                    f"{url_capitulo}: {e}"
                )

        return "\n\n".join(textos).strip()

    def normalizar(self, texto):
        """Limpieza de captura: ordena espacios. No borra información."""
        texto = texto.replace("\xa0", " ")
        texto = re.sub(r"[ \t]+", " ", texto)
        texto = re.sub(r"\n{3,}", "\n\n", texto)

        return texto.strip()

    def guardar_datos_corpus(
        self,
        texto,
        tipo_dato="texto",
        tipo_archivo="normalizado"
    ):
        """Guarda los datos del corpus como TXT o JSON."""
        if tipo_dato == "texto":
            archivo_destino = self.carpeta_destino / (
                f"{self.nombre_archivo}_{tipo_archivo}_datos_corpus.txt"
            )

            with open(archivo_destino, "w", encoding="utf-8") as f:
                f.write(texto)

            print(
                f"Datos del corpus guardados en "
                f"{archivo_destino.resolve()}"
            )

        elif tipo_dato == "json":
            archivo_destino = self.carpeta_destino / (
                f"{self.nombre_archivo}_{tipo_archivo}_datos_corpus.json"
            )

            with open(archivo_destino, "w", encoding="utf-8") as f:
                json.dump(
                    texto,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            print(
                f"Datos del corpus guardados en "
                f"{archivo_destino.resolve()}"
            )

    def palabras_significativas(self, texto, stopwords):
        """
        Preprocesamiento de análisis: destructivo.
        El resultado NO se guarda como corpus original.
        """
        stopwords = set(stopwords)

        texto = texto.lower()
        texto = re.sub(r"[^\w\s]", " ", texto)

        return [
            palabra
            for palabra in texto.split()
            if palabra not in stopwords and len(palabra) > 2
        ]

    def actualizo_csv(
        self,
        url,
        columna,
        valor,
        nombre_archivo_csv="control_corpus.csv"
    ):
        archivo_destino = (
            self.carpeta_destino / nombre_archivo_csv
        )

        columnas = [
            "url",
            "ruta",
            "multipagina",
            "robots",
            "extraccion",
            "normalizacion",
            "Cant-Tokens",
            "guardado",
            "Titulo de la página",
            "Autoría de la página",
            "Fecha de publicación de la página",
            "Año de publicación de la Obra",
            "Licencia",
            "Medio"
        ]

        filas = []

        if archivo_destino.exists():
            with open(
                archivo_destino,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as f:
                reader = csv.DictReader(f)
                filas = list(reader)

        encontrado = False

        for fila in filas:
            if fila["url"] == url:
                fila[columna] = valor
                encontrado = True
                break

        if not encontrado:
            nueva_fila = {col: "" for col in columnas}
            nueva_fila["url"] = url
            nueva_fila[columna] = valor
            filas.append(nueva_fila)

        with open(
            archivo_destino,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=columnas,
                extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(filas)

    # Guardamos, para cada documento, su lista de tokens.
    def tokenizar_documentos(self, documentos):
        documentos_en_tokens = []
        for documento in documentos:
            en_minusculas = documento.lower()
            tokens = en_minusculas.split()
            documentos_en_tokens.append(tokens)

        """ numero = 0
        for tokens in documentos_en_tokens:
            numero = numero + 1
            print("Documento", numero, ":", tokens) """
            
        return len(documentos_en_tokens[0]) if documentos_en_tokens else 0
    
    def obtener_fecha_publicacion_obra(self):
        if not self.pagina_temporal:
            return None

        sopa = BeautifulSoup(self.pagina_temporal, "html.parser")
               
        for enlace in sopa.find_all("a"):
            texto = enlace.get_text(strip=True)

            coincidencia = re.fullmatch(r"P(\d{4})", texto)

            if coincidencia:
                return coincidencia.group(1)
        return None
    
    def generar_corpus_jsonl(self, nombre_csv="control_corpus_2.csv", nombre_salida="corpus.jsonl"):
        """
            Genera corpus.jsonl a partir del CSV de control y de los
            archivos *_normalizado_datos_corpus.txt.
    
            Cada línea del archivo contiene un documento con:
            id, titulo, autor, fecha, fuente_url, categoria y texto.
            """
    
        ruta_csv = self.carpeta_destino / nombre_csv
        ruta_salida = self.carpeta_destino / nombre_salida
    
        if not ruta_csv.exists():
            print(f"No se encontró el CSV: {ruta_csv}")
            return
    
        documentos_guardados = 0
    
        with open(
            ruta_csv,
            "r",
            newline="",
            encoding="utf-8-sig"
            ) as csv_file, open(
            ruta_salida,
            "w",
            encoding="utf-8"
            ) as jsonl_file:
    
            reader = csv.DictReader(csv_file, delimiter=";")
    
            for fila in reader:
    
                ruta_html = fila.get("ruta", "").strip()
    
                if not ruta_html:
                    print(
                        f"Sin ruta para: {fila.get('url', '')}"
                    )
                    continue
    
                # De una ruta como:
                # C:\...\datos\pagina_24.html
                # obtenemos:
                # pagina_24.html
                nombre_html = Path(ruta_html).name
    
                nombre_normalizado = (
                    f"{nombre_html}_normalizado_datos_corpus.txt"
                )
    
                ruta_normalizado = (
                    self.carpeta_destino / nombre_normalizado
                )
    
                if not ruta_normalizado.exists():
                    print(
                        f"No se encontró el normalizado: "
                        f"{ruta_normalizado}"
                    )
                    continue
    
                # Leer el texto ya normalizado
                with open(
                    ruta_normalizado,
                    "r",
                    encoding="utf-8"
                ) as archivo_texto:
    
                    texto = archivo_texto.read().strip()
    
                if not texto:
                    print(
                        f"Texto vacío: {ruta_normalizado}"
                    )
                    continue
    
                documentos_guardados += 1
    
                documento = {
                    "id": f"doc_{documentos_guardados:02d}",
                    "titulo": fila.get(
                        "Titulo de la página",
                        ""
                    ),
                    "autor": fila.get(
                        "Autoría de la página",
                        ""
                    ),
                    "fecha": fila.get(
                        "Año de publicación de la Obra",
                        ""
                    ),
                    "fuente_url": fila.get(
                        "url",
                        ""
                    ),
                    "categoria": "Novela",
                    "texto": texto
                }
    
                jsonl_file.write(
                    json.dumps(
                        documento,
                        ensure_ascii=False
                    )
                    + "\n"
                )
    
        print(
            f"Corpus generado en: {ruta_salida.resolve()}"
        )
    
        print(
            f"Documentos guardados: "
            f"{documentos_guardados}"
        )
        