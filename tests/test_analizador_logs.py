import pytest

from algoritmos.analizador_logs import (
    compilar_patron,
    analizar_texto_log,
    analizar_archivo_log,
    validar_linea_log,
    analizar_texto_logs,
    analizar_archivo_logs
)


# ============================================================
# LOG DE EJEMPLO DEL ANALIZADOR ANTERIOR
# ============================================================

LOG_EJEMPLO = """192.168.1.10 GET /index 200
192.168.1.20 POST /login 401
192.168.1.20 POST /login 401
192.168.1.30 GET /admin 403
192.168.1.40 GET /error 500"""


# ============================================================
# LOG REAL GENERADO POR NUESTRA APLICACIÓN
# ============================================================

LOG_APLICACION = """2026-10-15 20:10:00 | INFO     | SISTEMA      | Aplicación iniciada correctamente.
2026-10-15 20:11:00 | WARNING  | REGEX        | Expresión regular inválida.
2026-10-15 20:12:00 | ERROR    | ARCHIVO      | No fue posible abrir el autómata.
2026-10-15 20:13:00 | CRITICAL | SISTEMA      | Error crítico de prueba.
esta linea no pertenece al formato"""


# ============================================================
# PRUEBAS DEL ANALIZADOR ANTERIOR
# ============================================================

def test_compilar_patron_valido():

    patron = compilar_patron(
        r"POST.*401"
    )

    assert patron is not None


def test_patron_vacio():

    with pytest.raises(
        ValueError
    ):

        compilar_patron(
            ""
        )


def test_patron_invalido():

    with pytest.raises(
        ValueError
    ):

        compilar_patron(
            r"[0-9"
        )


def test_analizar_texto_encuentra_coincidencias():

    resultado = analizar_texto_log(
        LOG_EJEMPLO,
        r"POST.*401"
    )

    assert (
        resultado[
            "total_lineas"
        ]
        == 5
    )

    assert (
        resultado[
            "cantidad_coincidencias"
        ]
        == 2
    )


def test_numeros_de_linea_correctos():

    resultado = analizar_texto_log(
        LOG_EJEMPLO,
        r"POST.*401"
    )

    numeros = [
        registro[
            "numero_linea"
        ]
        for registro
        in resultado[
            "coincidencias"
        ]
    ]

    assert numeros == [
        2,
        3
    ]


def test_buscar_error_500():

    resultado = analizar_texto_log(
        LOG_EJEMPLO,
        r"500$"
    )

    assert (
        resultado[
            "cantidad_coincidencias"
        ]
        == 1
    )

    assert (
        resultado[
            "coincidencias"
        ][0][
            "numero_linea"
        ]
        == 5
    )


def test_sin_coincidencias():

    resultado = analizar_texto_log(
        LOG_EJEMPLO,
        r"DELETE"
    )

    assert (
        resultado[
            "cantidad_coincidencias"
        ]
        == 0
    )

    assert (
        resultado[
            "coincidencias"
        ]
        == []
    )


def test_ignorar_mayusculas():

    resultado = analizar_texto_log(
        LOG_EJEMPLO,
        r"post.*401",
        ignorar_mayusculas=True
    )

    assert (
        resultado[
            "cantidad_coincidencias"
        ]
        == 2
    )


def test_analizar_archivo_log(
    tmp_path
):

    archivo = (
        tmp_path
        / "servidor.log"
    )

    archivo.write_text(
        LOG_EJEMPLO,
        encoding="utf-8"
    )

    resultado = analizar_archivo_log(
        archivo,
        r"GET.*403"
    )

    assert (
        resultado[
            "nombre_archivo"
        ]
        == "servidor.log"
    )

    assert (
        resultado[
            "cantidad_coincidencias"
        ]
        == 1
    )


def test_rechazar_extension_no_permitida(
    tmp_path
):

    archivo = (
        tmp_path
        / "datos.csv"
    )

    archivo.write_text(
        LOG_EJEMPLO,
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError
    ):

        analizar_archivo_log(
            archivo,
            r"401"
        )


# ============================================================
# PRUEBAS DE VALIDACIÓN DEL FORMATO REAL
# ============================================================

def test_validar_linea_info():

    resultado = validar_linea_log(
        (
            "2026-10-15 20:10:00 | "
            "INFO     | SISTEMA      | "
            "Aplicación iniciada correctamente."
        )
    )

    assert resultado["valido"] is True

    assert resultado["nivel"] == "INFO"

    assert resultado["modulo"] == "SISTEMA"

    assert (
        resultado["fecha"]
        == "2026-10-15"
    )

    assert (
        resultado["hora"]
        == "20:10:00"
    )


def test_validar_linea_warning():

    resultado = validar_linea_log(
        (
            "2026-10-15 20:11:00 | "
            "WARNING | REGEX | "
            "Expresión regular inválida."
        )
    )

    assert resultado["valido"] is True

    assert (
        resultado["nivel"]
        == "WARNING"
    )

    assert (
        resultado["modulo"]
        == "REGEX"
    )


def test_validar_linea_error():

    resultado = validar_linea_log(
        (
            "2026-10-15 20:12:00 | "
            "ERROR | ARCHIVO | "
            "No fue posible abrir el autómata."
        )
    )

    assert resultado["valido"] is True

    assert (
        resultado["nivel"]
        == "ERROR"
    )


def test_validar_linea_critical():

    resultado = validar_linea_log(
        (
            "2026-10-15 20:13:00 | "
            "CRITICAL | SISTEMA | "
            "Error crítico de prueba."
        )
    )

    assert resultado["valido"] is True

    assert (
        resultado["nivel"]
        == "CRITICAL"
    )


def test_rechazar_fecha_invalida():

    resultado = validar_linea_log(
        (
            "2026-15-40 25:80:90 | "
            "ERROR | SISTEMA | "
            "Fecha incorrecta."
        )
    )

    assert resultado["valido"] is False

    assert (
        "fecha"
        in resultado["error"].lower()
        or "hora"
        in resultado["error"].lower()
    )


def test_rechazar_nivel_invalido():

    resultado = validar_linea_log(
        (
            "2026-10-15 20:15:00 | "
            "PELIGRO | SISTEMA | "
            "Nivel inexistente."
        )
    )

    assert resultado["valido"] is False

    assert (
        "nivel"
        in resultado["error"].lower()
    )


def test_rechazar_mensaje_vacio():

    resultado = validar_linea_log(
        (
            "2026-10-15 20:16:00 | "
            "INFO | SISTEMA | "
        )
    )

    assert resultado["valido"] is False

    assert (
        "mensaje"
        in resultado["error"].lower()
    )


def test_rechazar_linea_sin_formato():

    resultado = validar_linea_log(
        (
            "esto no es un registro "
            "válido de la aplicación"
        )
    )

    assert resultado["valido"] is False

    assert (
        "formato"
        in resultado["error"].lower()
    )


def test_analizar_texto_logs_generar_resumen():

    resultado = analizar_texto_logs(
        LOG_APLICACION
    )

    assert (
        resultado["total_lineas"]
        == 5
    )

    assert (
        resultado["cantidad_validos"]
        == 4
    )

    assert (
        resultado["cantidad_invalidos"]
        == 1
    )

    assert (
        resultado["resumen_niveles"]
        ["INFO"]
        == 1
    )

    assert (
        resultado["resumen_niveles"]
        ["WARNING"]
        == 1
    )

    assert (
        resultado["resumen_niveles"]
        ["ERROR"]
        == 1
    )

    assert (
        resultado["resumen_niveles"]
        ["CRITICAL"]
        == 1
    )


def test_analizar_archivo_logs_aplicacion(
    tmp_path
):

    archivo = (
        tmp_path
        / "logs_2026-10-15.txt"
    )

    archivo.write_text(
        LOG_APLICACION,
        encoding="utf-8"
    )

    resultado = analizar_archivo_logs(
        archivo
    )

    assert (
        resultado["nombre_archivo"]
        == "logs_2026-10-15.txt"
    )

    assert (
        resultado["cantidad_validos"]
        == 4
    )

    assert (
        resultado["cantidad_invalidos"]
        == 1
    )

    assert (
        len(
            resultado[
                "registros_validos"
            ]
        )
        == 4
    )

    assert (
        len(
            resultado[
                "registros_invalidos"
            ]
        )
        == 1
    )