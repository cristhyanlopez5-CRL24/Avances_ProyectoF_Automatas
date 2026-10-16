import pytest

from modelos.afn import AFN
from modelos.afd import AFD

from algoritmos.integracion_regex import (
    generar_afn_desde_regex,
    generar_afd_desde_regex,
    validar_cadena_con_regex,
    validar_varias_cadenas
)


def test_generar_afn_desde_regex():

    afn = generar_afn_desde_regex(
        "(0|1)*01"
    )

    assert isinstance(
        afn,
        AFN
    )

    assert afn.expresion_regular == (
        "(0|1)*01"
    )


def test_afn_generado_acepta_cadena():

    afn = generar_afn_desde_regex(
        "(0|1)*01"
    )

    assert afn.simular(
        "1101"
    ) is True


def test_afn_generado_rechaza_cadena():

    afn = generar_afn_desde_regex(
        "(0|1)*01"
    )

    assert afn.simular(
        "1110"
    ) is False


def test_generar_afd_desde_regex():

    afd = generar_afd_desde_regex(
        "a|b"
    )

    assert isinstance(
        afd,
        AFD
    )

    assert afd.expresion_regular == (
        "a|b"
    )


def test_afd_generado_es_equivalente():

    afd = generar_afd_desde_regex(
        "(0|1)*01"
    )

    assert afd.simular(
        "01"
    ) is True

    assert afd.simular(
        "101"
    ) is True

    assert afd.simular(
        "10"
    ) is False


def test_validar_cadena_aceptada():

    resultado = (
        validar_cadena_con_regex(
            "(0|1)*01",
            "1101"
        )
    )

    assert resultado[
        "aceptada"
    ] is True

    assert resultado[
        "cadena"
    ] == "1101"


def test_validar_cadena_rechazada():

    resultado = (
        validar_cadena_con_regex(
            "(0|1)*01",
            "1110"
        )
    )

    assert resultado[
        "aceptada"
    ] is False


def test_validar_cadena_vacia():

    resultado = (
        validar_cadena_con_regex(
            "a*",
            ""
        )
    )

    assert resultado[
        "aceptada"
    ] is True


def test_simbolo_fuera_del_alfabeto():

    with pytest.raises(
        ValueError
    ):

        validar_cadena_con_regex(
            "a|b",
            "ac"
        )


def test_validar_varias_cadenas():

    resultado = (
        validar_varias_cadenas(
            "a*b",
            [
                "b",
                "ab",
                "aaab",
                "a"
            ]
        )
    )

    respuestas = [
        elemento["aceptada"]
        for elemento
        in resultado["resultados"]
    ]

    assert respuestas == [
        True,
        True,
        True,
        False
    ]