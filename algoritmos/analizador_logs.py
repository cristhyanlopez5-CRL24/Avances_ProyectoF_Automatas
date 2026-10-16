import re

from datetime import datetime

from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

EXTENSIONES_PERMITIDAS = {
    ".log",
    ".txt"
}


NIVELES_PERMITIDOS = {
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL"
}


# Formato utilizado por utilidades/registro_logs.py:
#
# 2026-10-15 22:30:00 | ERROR    | REGEX        | Mensaje
#
PATRON_LOG_APLICACION = re.compile(
    r"^"
    r"(?P<fecha>\d{4}-\d{2}-\d{2})"
    r"\s+"
    r"(?P<hora>\d{2}:\d{2}:\d{2})"
    r"\s*\|\s*"
    r"(?P<nivel>[A-Za-z]+)"
    r"\s*\|\s*"
    r"(?P<modulo>[^|]+)"
    r"\s*\|\s*"
    r"(?P<mensaje>.*)"
    r"$"
)


# ============================================================
# FUNCIONES ANTERIORES DE BÚSQUEDA POR REGEX
# ============================================================
#
# Se conservan porque ya forman parte del proyecto
# y tienen pruebas existentes.
# ============================================================

def compilar_patron(
    patron,
    ignorar_mayusculas=False
):
    """
    Comprueba que el patrón ingresado
    sea una expresión regular válida.
    """

    if patron is None:

        raise ValueError(
            "El patrón de búsqueda "
            "no puede ser nulo."
        )

    patron = str(
        patron
    ).strip()

    if not patron:

        raise ValueError(
            "Debe ingresar una expresión "
            "regular para analizar los logs."
        )

    banderas = 0

    if ignorar_mayusculas:

        banderas = re.IGNORECASE

    try:

        return re.compile(
            patron,
            banderas
        )

    except re.error as error:

        raise ValueError(
            "La expresión regular para "
            f"logs no es válida: {error}"
        ) from error


def analizar_texto_log(
    texto,
    patron,
    ignorar_mayusculas=False
):
    """
    Analiza un bloque de texto línea por línea
    utilizando una expresión regular.

    Devuelve únicamente las líneas que
    coinciden con el patrón indicado.
    """

    if texto is None:

        raise ValueError(
            "El contenido del log "
            "no puede ser nulo."
        )

    regex = compilar_patron(
        patron,
        ignorar_mayusculas
    )

    lineas = str(
        texto
    ).splitlines()

    coincidencias = []

    for numero, linea in enumerate(
        lineas,
        start=1
    ):

        resultado = regex.search(
            linea
        )

        if resultado is None:

            continue

        coincidencias.append({
            "numero_linea": numero,
            "contenido": linea,
            "coincidencia": (
                resultado.group(0)
            ),
            "inicio": resultado.start(),
            "fin": resultado.end()
        })

    return {
        "patron": patron,
        "ignorar_mayusculas": (
            ignorar_mayusculas
        ),
        "total_lineas": len(
            lineas
        ),
        "cantidad_coincidencias": len(
            coincidencias
        ),
        "coincidencias": coincidencias
    }


def analizar_archivo_log(
    ruta,
    patron,
    ignorar_mayusculas=False
):
    """
    Lee un archivo .log o .txt y analiza
    su contenido mediante una expresión regular.
    """

    ruta = validar_archivo_log(
        ruta
    )

    try:

        texto = ruta.read_text(
            encoding="utf-8",
            errors="replace"
        )

    except OSError as error:

        raise ValueError(
            "No fue posible leer "
            "el archivo seleccionado."
        ) from error

    resultado = analizar_texto_log(
        texto,
        patron,
        ignorar_mayusculas
    )

    resultado[
        "archivo"
    ] = str(
        ruta
    )

    resultado[
        "nombre_archivo"
    ] = ruta.name

    return resultado


# ============================================================
# VALIDAR ARCHIVO
# ============================================================

def validar_archivo_log(
    ruta
):
    """
    Comprueba que la ruta corresponda
    a un archivo de log permitido.
    """

    if ruta is None:

        raise ValueError(
            "Debe seleccionar un archivo "
            "de logs."
        )

    ruta = Path(
        ruta
    )

    if not ruta.exists():

        raise ValueError(
            "El archivo seleccionado "
            "no existe."
        )

    if not ruta.is_file():

        raise ValueError(
            "La ruta seleccionada "
            "no corresponde a un archivo."
        )

    if (
        ruta.suffix.lower()
        not in EXTENSIONES_PERMITIDAS
    ):

        raise ValueError(
            "Solo se permiten archivos "
            ".log y .txt."
        )

    return ruta


# ============================================================
# VALIDAR UNA LÍNEA DEL LOG DE LA APLICACIÓN
# ============================================================

def validar_linea_log(
    linea,
    numero_linea=None
):
    """
    Valida una línea utilizando el formato
    real generado por registro_logs.py.

    Devuelve un diccionario indicando
    si el registro es válido o inválido.
    """

    if linea is None:

        return {
            "numero_linea": numero_linea,
            "contenido": "",
            "valido": False,
            "error": (
                "La línea no puede ser nula."
            )
        }

    contenido = str(
        linea
    ).rstrip(
        "\r\n"
    )

    if not contenido.strip():

        return {
            "numero_linea": numero_linea,
            "contenido": contenido,
            "valido": False,
            "error": (
                "La línea está vacía."
            )
        }

    coincidencia = (
        PATRON_LOG_APLICACION.match(
            contenido
        )
    )

    if coincidencia is None:

        return {
            "numero_linea": numero_linea,
            "contenido": contenido,
            "valido": False,
            "error": (
                "El registro no cumple "
                "el formato esperado."
            )
        }

    fecha = (
        coincidencia
        .group(
            "fecha"
        )
        .strip()
    )

    hora = (
        coincidencia
        .group(
            "hora"
        )
        .strip()
    )

    nivel = (
        coincidencia
        .group(
            "nivel"
        )
        .strip()
        .upper()
    )

    modulo = (
        coincidencia
        .group(
            "modulo"
        )
        .strip()
    )

    mensaje = (
        coincidencia
        .group(
            "mensaje"
        )
        .strip()
    )

    # --------------------------------------------------------
    # VALIDAR FECHA Y HORA
    # --------------------------------------------------------

    try:

        datetime.strptime(
            f"{fecha} {hora}",
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:

        return {
            "numero_linea": numero_linea,
            "contenido": contenido,
            "valido": False,
            "error": (
                "La fecha u hora del registro "
                "no es válida."
            )
        }

    # --------------------------------------------------------
    # VALIDAR NIVEL
    # --------------------------------------------------------

    if nivel not in NIVELES_PERMITIDOS:

        return {
            "numero_linea": numero_linea,
            "contenido": contenido,
            "valido": False,
            "error": (
                f"Nivel de log no permitido: "
                f"{nivel}."
            )
        }

    # --------------------------------------------------------
    # VALIDAR MÓDULO
    # --------------------------------------------------------

    if not modulo:

        return {
            "numero_linea": numero_linea,
            "contenido": contenido,
            "valido": False,
            "error": (
                "El módulo del registro "
                "está vacío."
            )
        }

    # --------------------------------------------------------
    # VALIDAR MENSAJE
    # --------------------------------------------------------

    if not mensaje:

        return {
            "numero_linea": numero_linea,
            "contenido": contenido,
            "valido": False,
            "error": (
                "El mensaje del registro "
                "está vacío."
            )
        }

    # --------------------------------------------------------
    # REGISTRO VÁLIDO
    # --------------------------------------------------------

    return {
        "numero_linea": numero_linea,
        "contenido": contenido,
        "valido": True,
        "fecha": fecha,
        "hora": hora,
        "fecha_hora": (
            f"{fecha} {hora}"
        ),
        "nivel": nivel,
        "modulo": modulo,
        "mensaje": mensaje,
        "error": None
    }


# ============================================================
# ANALIZAR TEXTO COMPLETO DE LOGS
# ============================================================

def analizar_texto_logs(
    texto
):
    """
    Valida todas las líneas de un bloque
    de logs generado por la aplicación.

    Separa registros válidos e inválidos
    y genera un resumen por nivel.
    """

    if texto is None:

        raise ValueError(
            "El contenido del log "
            "no puede ser nulo."
        )

    lineas = str(
        texto
    ).splitlines()

    registros_validos = []

    registros_invalidos = []

    resumen_niveles = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0
    }

    for numero, linea in enumerate(
        lineas,
        start=1
    ):

        registro = validar_linea_log(
            linea,
            numero_linea=numero
        )

        if registro["valido"]:

            registros_validos.append(
                registro
            )

            resumen_niveles[
                registro["nivel"]
            ] += 1

        else:

            registros_invalidos.append(
                registro
            )

    return {
        "total_lineas": len(
            lineas
        ),
        "cantidad_validos": len(
            registros_validos
        ),
        "cantidad_invalidos": len(
            registros_invalidos
        ),
        "registros_validos": (
            registros_validos
        ),
        "registros_invalidos": (
            registros_invalidos
        ),
        "resumen_niveles": (
            resumen_niveles
        )
    }


# ============================================================
# ANALIZAR ARCHIVO REAL DE LOGS
# ============================================================

def analizar_archivo_logs(
    ruta
):
    """
    Lee y valida un archivo completo
    generado por el sistema de logs.
    """

    ruta = validar_archivo_log(
        ruta
    )

    try:

        texto = ruta.read_text(
            encoding="utf-8",
            errors="replace"
        )

    except OSError as error:

        raise ValueError(
            "No fue posible leer "
            "el archivo seleccionado."
        ) from error

    resultado = analizar_texto_logs(
        texto
    )

    resultado[
        "archivo"
    ] = str(
        ruta
    )

    resultado[
        "nombre_archivo"
    ] = ruta.name

    return resultado