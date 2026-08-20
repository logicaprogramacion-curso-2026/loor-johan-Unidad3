"""
gestor.py

Módulo encargado de leer bancos de preguntas desde archivos en formato
JSON, CSV o TXT, validarlos/normalizarlos e insertarlos en la base de
datos a través del DAO (Capa 1: Datos).

Formatos soportados
--------------------
Se soporta tanto el esquema "externo" (el que usan los archivos reales
del proyecto: preguntas.json, preguntas.csv, preguntas.txt) como el
esquema "interno" de la clase Pregunta, por compatibilidad.

JSON (externo): lista de objetos con los campos
    ID, Pregunta, OpcionA, OpcionB, OpcionC, OpcionD,
    RespuestaCorrecta, Dificultad, Tema.
JSON (interno): lista de objetos con los campos de Pregunta
    (id, tipo, enunciado, opciones, respuesta_correcta, puntaje,
    retroalimentacion).

CSV: delimitador ',' o ';' (detectado automáticamente), con o sin
     cabecera. Si tiene cabecera, se detecta si es del esquema externo
     o interno según los nombres de columna.

TXT: un bloque por pregunta, separado por línea en blanco:
     1. Enunciado
        A) opción 1
        B) opción 2
        C) opción 3
        D) opción 4
        Respuesta correcta: B
        Dificultad: Fácil | Tema: Nombre del tema

Solo se usan librerías estándar: json, csv, os.
"""

import json
import csv
import os

from pregunta import Pregunta

CAMPOS_ESPERADOS = [
    "id", "tipo", "enunciado", "opciones",
    "respuesta_correcta", "puntaje", "retroalimentacion",
]

# Esquema "externo": el que realmente usan preguntas.json / .csv / .txt
# (ID, Pregunta, OpcionA..D, RespuestaCorrecta, Dificultad, Tema).
CAMPOS_EXTERNOS = [
    "id", "pregunta", "opciona", "opcionb", "opcionc", "opciond",
    "respuestacorrecta", "dificultad", "tema",
]


def _fila_externa_a_diccionario(id_, pregunta, opcion_a, opcion_b, opcion_c,
                                 opcion_d, respuesta_correcta, dificultad,
                                 tema):
    """Traduce una fila con el esquema externo (Pregunta/OpcionA..D/...)
    al diccionario interno que espera Pregunta, y lo valida."""
    opciones = [opcion_a, opcion_b, opcion_c, opcion_d]
    partes_retro = []
    if tema and str(tema).strip():
        partes_retro.append(f"Tema: {str(tema).strip()}")
    if dificultad and str(dificultad).strip():
        partes_retro.append(f"Dificultad: {str(dificultad).strip()}")
    retroalimentacion = " | ".join(partes_retro)

    return _construir_diccionario(
        id_, "multiple", pregunta, opciones,
        respuesta_correcta, 1, retroalimentacion,
    )


# ---------------------------------------------------------------------------
# Utilidades internas de validación / normalización
# ---------------------------------------------------------------------------

def _normalizar_opciones(valor):
    """Convierte 'opciones' a lista, sin importar si viene como lista,
    cadena separada por comas o por punto y coma."""
    if valor is None:
        return []
    if isinstance(valor, list):
        return [str(o).strip() for o in valor if str(o).strip() != ""]

    texto = str(valor).strip()
    if texto == "":
        return []

    separador = ";" if ";" in texto and "," not in texto else ","
    return [o.strip() for o in texto.split(separador) if o.strip() != ""]


def _validar_puntaje(valor):
    """Convierte el puntaje a número y valida que sea >= 0.
    Lanza ValueError si no es válido."""
    try:
        puntaje = float(valor)
    except (TypeError, ValueError):
        raise ValueError(f"puntaje no es numérico: {valor!r}")
    if puntaje < 0:
        raise ValueError(f"puntaje no puede ser negativo: {puntaje}")
    if puntaje.is_integer():
        puntaje = int(puntaje)
    return puntaje


def _construir_diccionario(id_, tipo, enunciado, opciones,
                            respuesta_correcta, puntaje, retroalimentacion):
    """Valida y arma un diccionario homogéneo con los 7 campos de una
    pregunta. Lanza ValueError describiendo el primer problema encontrado."""
    if tipo is None or str(tipo).strip() == "":
        raise ValueError("falta campo tipo")
    if enunciado is None or str(enunciado).strip() == "":
        raise ValueError("falta campo enunciado")
    if respuesta_correcta is None or str(respuesta_correcta).strip() == "":
        raise ValueError("falta campo respuesta_correcta")
    if puntaje is None or str(puntaje).strip() == "":
        raise ValueError("falta campo puntaje")

    id_normalizado = None
    if id_ not in (None, "", "None"):
        try:
            id_normalizado = int(id_)
        except (TypeError, ValueError):
            raise ValueError(f"id no es válido: {id_!r}")

    return {
        "id": id_normalizado,
        "tipo": str(tipo).strip(),
        "enunciado": str(enunciado).strip(),
        "opciones": _normalizar_opciones(opciones),
        "respuesta_correcta": str(respuesta_correcta).strip(),
        "puntaje": _validar_puntaje(puntaje),
        "retroalimentacion": str(retroalimentacion).strip() if retroalimentacion else "",
    }


# ---------------------------------------------------------------------------
# Cargadores por formato
# ---------------------------------------------------------------------------

def cargar_json(ruta):
    """Lee un archivo JSON con una lista de preguntas.

    Devuelve (preguntas, errores):
        preguntas: lista de diccionarios normalizados y válidos.
        errores: lista de mensajes de error (elementos inválidos que se
                 saltaron).

    Lanza FileNotFoundError si el archivo no existe, o ValueError si el
    contenido no es JSON válido o no es una lista.
    """
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    with open(ruta, "r", encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)
        except json.JSONDecodeError as error:
            raise ValueError(f"JSON inválido en '{ruta}': {error}")

    if not isinstance(datos, list):
        raise ValueError("El archivo JSON debe contener una lista de preguntas")

    preguntas = []
    errores = []
    for indice, item in enumerate(datos, start=1):
        try:
            if not isinstance(item, dict):
                raise ValueError("el elemento no es un objeto válido")

            claves = {clave.lower() for clave in item.keys()}
            es_formato_interno = "tipo" in claves and "enunciado" in claves

            if es_formato_interno:
                preguntas.append(_construir_diccionario(
                    item.get("id"),
                    item.get("tipo"),
                    item.get("enunciado"),
                    item.get("opciones"),
                    item.get("respuesta_correcta"),
                    item.get("puntaje"),
                    item.get("retroalimentacion"),
                ))
            else:
                preguntas.append(_fila_externa_a_diccionario(
                    item.get("ID") or item.get("id"),
                    item.get("Pregunta") or item.get("pregunta"),
                    item.get("OpcionA") or item.get("opciona"),
                    item.get("OpcionB") or item.get("opcionb"),
                    item.get("OpcionC") or item.get("opcionc"),
                    item.get("OpcionD") or item.get("opciond"),
                    item.get("RespuestaCorrecta") or item.get("respuestacorrecta"),
                    item.get("Dificultad") or item.get("dificultad"),
                    item.get("Tema") or item.get("tema"),
                ))
        except ValueError as error:
            errores.append(f"Elemento {indice}: {error}")

    return preguntas, errores


def cargar_csv(ruta):
    """Lee un archivo CSV (delimitador ',' o ';', detectado
    automáticamente), con o sin cabecera.

    Devuelve (preguntas, errores). Lanza FileNotFoundError si el archivo
    no existe.
    """
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        contenido = archivo.read()

    if not contenido.strip():
        return [], []

    primera_linea = contenido.splitlines()[0]
    delimitador = ";" if primera_linea.count(";") > primera_linea.count(",") else ","

    lector = csv.reader(contenido.splitlines(), delimiter=delimitador,
                         quoting=csv.QUOTE_MINIMAL)
    filas = [fila for fila in lector]

    if not filas:
        return [], []

    primera_fila_normalizada = [c.strip().lower() for c in filas[0]]
    es_cabecera_interna = all(
        campo in CAMPOS_ESPERADOS for campo in primera_fila_normalizada if campo
    ) and "enunciado" in primera_fila_normalizada
    es_cabecera_externa = all(
        campo in CAMPOS_EXTERNOS for campo in primera_fila_normalizada if campo
    ) and "pregunta" in primera_fila_normalizada

    if es_cabecera_interna:
        cabecera = primera_fila_normalizada
        filas_datos = filas[1:]
        offset_linea = 2  # la fila 1 es la cabecera
        formato = "interno"
    elif es_cabecera_externa:
        cabecera = primera_fila_normalizada
        filas_datos = filas[1:]
        offset_linea = 2
        formato = "externo"
    else:
        # Sin cabecera reconocible: asumimos el formato externo, que es
        # el que usan los archivos reales del proyecto.
        cabecera = list(CAMPOS_EXTERNOS)
        filas_datos = filas
        offset_linea = 1
        formato = "externo"

    preguntas = []
    errores = []
    for indice, fila in enumerate(filas_datos):
        numero_linea = indice + offset_linea

        if not fila or all(campo.strip() == "" for campo in fila):
            continue  # línea en blanco: se ignora sin reportar error

        # Toleramos que falte solo el último campo opcional
        if len(fila) < len(cabecera) - 1:
            errores.append(
                f"Línea {numero_linea}: formato incorrecto, se esperaban "
                f"{len(cabecera)} campos y se recibieron {len(fila)}"
            )
            continue

        fila = list(fila)
        while len(fila) < len(cabecera):
            fila.append("")

        datos_fila = dict(zip(cabecera, fila))
        try:
            if formato == "interno":
                preguntas.append(_construir_diccionario(
                    datos_fila.get("id"),
                    datos_fila.get("tipo"),
                    datos_fila.get("enunciado"),
                    datos_fila.get("opciones"),
                    datos_fila.get("respuesta_correcta"),
                    datos_fila.get("puntaje"),
                    datos_fila.get("retroalimentacion"),
                ))
            else:
                preguntas.append(_fila_externa_a_diccionario(
                    datos_fila.get("id"),
                    datos_fila.get("pregunta"),
                    datos_fila.get("opciona"),
                    datos_fila.get("opcionb"),
                    datos_fila.get("opcionc"),
                    datos_fila.get("opciond"),
                    datos_fila.get("respuestacorrecta"),
                    datos_fila.get("dificultad"),
                    datos_fila.get("tema"),
                ))
        except ValueError as error:
            errores.append(f"Línea {numero_linea}: {error}")

    return preguntas, errores


def cargar_txt(ruta):
    """Lee un archivo TXT donde cada pregunta es un bloque de líneas
    separado por una línea en blanco, con este formato:

        1. Enunciado de la pregunta
           A) opción 1
           B) opción 2
           C) opción 3
           D) opción 4
           Respuesta correcta: B
           Dificultad: Fácil | Tema: Nombre del tema

    La línea de Dificultad/Tema es opcional.

    Devuelve (preguntas, errores). Lanza FileNotFoundError si el archivo
    no existe.
    """
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    bloques = [b for b in contenido.replace("\r\n", "\n").split("\n\n") if b.strip()]

    preguntas = []
    errores = []
    for numero_bloque, bloque in enumerate(bloques, start=1):
        lineas = [linea.strip() for linea in bloque.splitlines() if linea.strip()]
        try:
            if len(lineas) < 6:
                raise ValueError(
                    "formato incorrecto, se esperaba al menos: enunciado, "
                    f"4 opciones y respuesta correcta (se recibieron {len(lineas)} líneas)"
                )

            primera_linea = lineas[0]
            if ". " in primera_linea:
                id_texto, enunciado = primera_linea.split(". ", 1)
            else:
                id_texto, enunciado = "", primera_linea

            opciones = []
            for linea_opcion in lineas[1:5]:
                if ")" in linea_opcion:
                    opciones.append(linea_opcion.split(")", 1)[1].strip())
                else:
                    opciones.append(linea_opcion.strip())

            linea_respuesta = lineas[5]
            respuesta_correcta = (
                linea_respuesta.split(":", 1)[1].strip()
                if ":" in linea_respuesta else linea_respuesta
            )

            dificultad, tema = "", ""
            if len(lineas) >= 7:
                for parte in lineas[6].split("|"):
                    parte = parte.strip()
                    clave, _, valor = parte.partition(":")
                    if clave.strip().lower() == "dificultad":
                        dificultad = valor.strip()
                    elif clave.strip().lower() == "tema":
                        tema = valor.strip()

            preguntas.append(_fila_externa_a_diccionario(
                id_texto.strip(), enunciado, opciones[0], opciones[1],
                opciones[2], opciones[3], respuesta_correcta, dificultad, tema,
            ))
        except ValueError as error:
            errores.append(f"Bloque {numero_bloque}: {error}")

    return preguntas, errores


# ---------------------------------------------------------------------------
# Función principal de importación
# ---------------------------------------------------------------------------

def importar_preguntas(ruta, dao):
    """Detecta el formato del archivo por su extensión (.json, .csv,
    .txt), lo procesa e inserta cada pregunta válida usando
    dao.insertar(pregunta).

    Devuelve un diccionario:
        {
            "insertadas": int,   # inserciones exitosas
            "omitidas": int,     # duplicadas (dao.insertar devolvió False)
            "errores": int,      # líneas/elementos con formato inválido
            "mensajes": [str, ...]  # detalle de cada error
        }

    Lanza ValueError si la extensión no es soportada, o FileNotFoundError
    si el archivo no existe.
    """
    extension = os.path.splitext(ruta)[1].lower()

    if extension == ".json":
        datos, errores_carga = cargar_json(ruta)
    elif extension == ".csv":
        datos, errores_carga = cargar_csv(ruta)
    elif extension == ".txt":
        datos, errores_carga = cargar_txt(ruta)
    else:
        raise ValueError(
            f"Formato de archivo no soportado: '{extension}'. "
            "Se esperaba .json, .csv o .txt"
        )

    resultado = {
        "insertadas": 0,
        "omitidas": 0,
        "errores": len(errores_carga),
        "mensajes": list(errores_carga),
    }

    for datos_pregunta in datos:
        pregunta = Pregunta(**datos_pregunta)
        try:
            if dao.insertar(pregunta):
                resultado["insertadas"] += 1
            else:
                resultado["omitidas"] += 1
        except Exception as error:
            resultado["errores"] += 1
            resultado["mensajes"].append(
                f"Error al insertar pregunta '{pregunta.enunciado[:30]}...': {error}"
            )

    return resultado
