import pytest

from utilidades.validador_regex import (
    validar_expresion_regular
)

from modelos.expresion_regular import (
    ExpresionRegular
)


def test_regex_simbolo_simple():

    resultado = (
        validar_expresion_regular(
            "a"
        )
    )

    assert resultado == "a"


def test_regex_union():

    resultado = (
        validar_expresion_regular(
            "a|b"
        )
    )

    assert resultado == "a|b"


def test_regex_concatenacion():

    resultado = (
        validar_expresion_regular(
            "abc"
        )
    )

    assert resultado == "abc"


def test_regex_parentesis_y_estrella():

    resultado = (
        validar_expresion_regular(
            "(0|1)*01"
        )
    )

    assert resultado == "(0|1)*01"


def test_regex_operador_mas():

    resultado = (
        validar_expresion_regular(
            "a+"
        )
    )

    assert resultado == "a+"


def test_regex_operador_opcional():

    resultado = (
        validar_expresion_regular(
            "a?"
        )
    )

    assert resultado == "a?"


def test_regex_epsilon():

    resultado = (
        validar_expresion_regular(
            "a|ε"
        )
    )

    assert resultado == "a|ε"


def test_regex_elimina_espacios():

    resultado = (
        validar_expresion_regular(
            "( a | b ) *"
        )
    )

    assert resultado == "(a|b)*"


def test_parentesis_sin_cerrar():

    with pytest.raises(
        ValueError
    ):

        validar_expresion_regular(
            "(a|b"
        )


def test_parentesis_cierre_sin_apertura():

    with pytest.raises(
        ValueError
    ):

        validar_expresion_regular(
            "a)"
        )


def test_parentesis_vacios():

    with pytest.raises(
        ValueError
    ):

        validar_expresion_regular(
            "()"
        )


def test_union_al_inicio():

    with pytest.raises(
        ValueError
    ):

        validar_expresion_regular(
            "|a"
        )


def test_union_al_final():

    with pytest.raises(
        ValueError
    ):

        validar_expresion_regular(
            "a|"
        )


def test_union_doble():

    with pytest.raises(
        ValueError
    ):

        validar_expresion_regular(
            "a||b"
        )


def test_operador_unario_al_inicio():

    with pytest.raises(
        ValueError
    ):

        validar_expresion_regular(
            "*a"
        )