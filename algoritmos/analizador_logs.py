import re

from pathlib import Path


EXTENSIONES_PERMITIDAS = {
    ".log",
    ".txt"
}


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