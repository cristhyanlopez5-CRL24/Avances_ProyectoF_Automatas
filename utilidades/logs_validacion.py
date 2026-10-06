from datetime import datetime
from pathlib import Path
import json


ARCHIVO_LOGS = (
    Path(__file__).resolve().parent.parent
    / "datos"
    / "logs_validacion.json"
)


def _asegurar_archivo():
    """
    Crea la carpeta y el archivo de logs
    si todavía no existen.
    """

    ARCHIVO_LOGS.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not ARCHIVO_LOGS.exists():

        ARCHIVO_LOGS.write_text(
            "[]",
            encoding="utf-8"
        )


def cargar_logs():
    """
    Devuelve todos los registros guardados.
    """

    _asegurar_archivo()

    try:

        contenido = ARCHIVO_LOGS.read_text(
            encoding="utf-8"
        )

        datos = json.loads(
            contenido
        )

        if not isinstance(
            datos,
            list
        ):
            return []

        return datos

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def registrar_validacion(
    expresion,
    cadena,
    aceptada
):
    """
    Guarda una validación realizada
    desde una expresión regular.
    """

    logs = cargar_logs()

    registro = {
        "fecha_hora": (
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ),
        "expresion": expresion,
        "cadena": (
            cadena
            if cadena != ""
            else "ε"
        ),
        "resultado": (
            "Aceptada"
            if aceptada
            else "Rechazada"
        )
    }

    logs.append(
        registro
    )

    ARCHIVO_LOGS.write_text(
        json.dumps(
            logs,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return registro


def limpiar_logs():
    """
    Elimina el historial completo.
    """

    _asegurar_archivo()

    ARCHIVO_LOGS.write_text(
        "[]",
        encoding="utf-8"
    )