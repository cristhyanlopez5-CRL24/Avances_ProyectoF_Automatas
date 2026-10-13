import pytest

from algoritmos.analizador_logs import (
    compilar_patron,
    analizar_texto_log,
    analizar_archivo_log
)


LOG_EJEMPLO = """192.168.1.10 GET /index 200
192.168.1.20 POST /login 401
192.168.1.20 POST /login 401
192.168.1.30 GET /admin 403
192.168.1.40 GET /error 500"""


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