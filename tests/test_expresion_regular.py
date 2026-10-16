import pytest

from modelos.expresion_regular import (
    ExpresionRegular
)


def test_crear_expresion_regular():

    expresion = ExpresionRegular(
        nombre="Termina en 01",
        expresion="(0|1)*01"
    )

    assert expresion.nombre == (
        "Termina en 01"
    )

    assert expresion.expresion == (
        "(0|1)*01"
    )

    assert expresion.alfabeto == {
        "0",
        "1"
    }


def test_nombre_vacio():

    with pytest.raises(
        ValueError
    ):

        ExpresionRegular(
            nombre="",
            expresion="0|1"
        )


def test_expresion_vacia():

    with pytest.raises(
        ValueError
    ):

        ExpresionRegular(
            nombre="Prueba",
            expresion=""
        )


def test_ignorar_operadores():

    expresion = ExpresionRegular(
        nombre="Prueba operadores",
        expresion="(a|b)*"
    )

    assert expresion.alfabeto == {
        "a",
        "b"
    }


def test_ignorar_epsilon():

    expresion = ExpresionRegular(
        nombre="Prueba epsilon",
        expresion="a|ε"
    )

    assert expresion.alfabeto == {
        "a"
    }


def test_obtener_alfabeto_devuelve_copia():

    expresion = ExpresionRegular(
        nombre="Prueba",
        expresion="a|b"
    )

    alfabeto = (
        expresion.obtener_alfabeto()
    )

    alfabeto.add(
        "x"
    )

    assert expresion.alfabeto == {
        "a",
        "b"
    }