import logging

from datetime import datetime

from pathlib import Path


CARPETA_LOGS = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    / "logs"
)

NOMBRE_LOGGER = (
    "simulador_automatas"
)

_logger = logging.getLogger(
    NOMBRE_LOGGER
)

_logger.setLevel(
    logging.DEBUG
)

_logger.propagate = False

_ruta_configurada = None


def obtener_ruta_log(
    fecha=None
):
    """
    Devuelve la ruta del archivo de log
    correspondiente a la fecha indicada.

    Ejemplo:
    logs/logs_2026-10-13.txt
    """

    if fecha is None:

        fecha = datetime.now()

    CARPETA_LOGS.mkdir(
        parents=True,
        exist_ok=True
    )

    nombre = (
        "logs_"
        + fecha.strftime(
            "%Y-%m-%d"
        )
        + ".txt"
    )

    return (
        CARPETA_LOGS
        / nombre
    )


def cerrar_logging():
    """
    Cierra correctamente los manejadores
    del sistema de logs.
    """

    global _ruta_configurada

    for handler in list(
        _logger.handlers
    ):

        handler.flush()

        handler.close()

        _logger.removeHandler(
            handler
        )

    _ruta_configurada = None


def configurar_logging(
    ruta=None
):
    """
    Configura el archivo donde se guardarán
    los eventos del simulador.
    """

    global _ruta_configurada

    if ruta is None:

        ruta = obtener_ruta_log()

    else:

        ruta = Path(
            ruta
        )

        ruta.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    ruta = ruta.resolve()

    if (
        _ruta_configurada == ruta
        and _logger.handlers
    ):

        return _logger

    cerrar_logging()

    handler = logging.FileHandler(
        ruta,
        mode="a",
        encoding="utf-8"
    )

    formato = logging.Formatter(
        (
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(modulo)-12s | "
            "%(message)s"
        ),
        datefmt=(
            "%Y-%m-%d "
            "%H:%M:%S"
        )
    )

    handler.setFormatter(
        formato
    )

    handler.setLevel(
        logging.DEBUG
    )

    _logger.addHandler(
        handler
    )

    _ruta_configurada = ruta

    return _logger


def registrar_evento(
    nivel,
    modulo,
    mensaje
):
    """
    Registra un evento del sistema.

    Niveles disponibles:

    INFO
    WARNING
    ERROR
    CRITICAL
    """

    if nivel is None:

        raise ValueError(
            "Debe indicar el nivel "
            "del evento."
        )

    nivel = (
        str(nivel)
        .strip()
        .upper()
    )

    niveles = {
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    if nivel not in niveles:

        raise ValueError(
            "Nivel de log no válido."
        )

    modulo = (
        str(modulo)
        .strip()
        .upper()
        if modulo is not None
        else "SISTEMA"
    )

    if not modulo:

        modulo = "SISTEMA"

    if mensaje is None:

        raise ValueError(
            "El mensaje del log "
            "no puede ser nulo."
        )

    mensaje = str(
        mensaje
    ).strip()

    if not mensaje:

        raise ValueError(
            "El mensaje del log "
            "no puede estar vacío."
        )

    logger = configurar_logging()

    logger.log(
        niveles[nivel],
        mensaje,
        extra={
            "modulo": modulo
        }
    )

    # Fuerza la escritura inmediata.
    for handler in (
        logger.handlers
    ):

        handler.flush()

    return _ruta_configurada


def registrar_info(
    modulo,
    mensaje
):

    return registrar_evento(
        "INFO",
        modulo,
        mensaje
    )


def registrar_warning(
    modulo,
    mensaje
):

    return registrar_evento(
        "WARNING",
        modulo,
        mensaje
    )


def registrar_error(
    modulo,
    mensaje
):

    return registrar_evento(
        "ERROR",
        modulo,
        mensaje
    )


def registrar_critical(
    modulo,
    mensaje
):

    return registrar_evento(
        "CRITICAL",
        modulo,
        mensaje
    )