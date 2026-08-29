import pytest

from utilidades.validaciones import (
    separar_elementos,
    validar_nombre_automata,
    validar_estados,
    validar_alfabeto,
    validar_estado_inicial,
    validar_estados_finales,
    validar_tipo_automata,
    validar_transicion,
    validar_cadena,
    validar_datos_automata
)


def test_separar_elementos():

    resultado = separar_elementos(
        "q0, q1, q2"
    )

    assert resultado == [
        "q0",
        "q1",
        "q2"
    ]


def test_nombre_vacio():

    with pytest.raises(ValueError):

        validar_nombre_automata("")


def test_estados_correctos():

    estados = validar_estados(
        "q0,q1,q2"
    )

    assert estados == {
        "q0",
        "q1",
        "q2"
    }


def test_estados_repetidos():

    with pytest.raises(ValueError):

        validar_estados(
            "q0,q1,q1"
        )


def test_alfabeto_correcto():

    alfabeto = validar_alfabeto(
        "0,1"
    )

    assert alfabeto == {
        "0",
        "1"
    }


def test_alfabeto_con_epsilon():

    with pytest.raises(ValueError):

        validar_alfabeto(
            "0,1,ε"
        )


def test_estado_inicial_inexistente():

    with pytest.raises(ValueError):

        validar_estado_inicial(
            "q9",
            {"q0", "q1"}
        )


def test_estado_final_inexistente():

    with pytest.raises(ValueError):

        validar_estados_finales(
            "q2",
            {"q0", "q1"}
        )


def test_tipo_invalido():

    with pytest.raises(ValueError):

        validar_tipo_automata(
            "PDA"
        )


def test_epsilon_valido_en_afn():

    resultado = validar_transicion(
        origen="q0",
        simbolo="ε",
        destino="q1",
        estados={"q0", "q1"},
        alfabeto={"0", "1"},
        tipo="AFN"
    )

    assert resultado["simbolo"] == "ε"


def test_epsilon_invalido_en_afd():

    with pytest.raises(ValueError):

        validar_transicion(
            origen="q0",
            simbolo="ε",
            destino="q1",
            estados={"q0", "q1"},
            alfabeto={"0", "1"},
            tipo="AFD"
        )


def test_datos_completos():

    datos = validar_datos_automata(
        nombre="Prueba",
        tipo="AFD",
        texto_estados="q0,q1,q2",
        texto_alfabeto="0,1",
        estado_inicial="q0",
        texto_estados_finales="q2"
    )

    assert datos["nombre"] == "Prueba"

    assert datos["tipo"] == "AFD"

    assert datos["estados"] == {
        "q0",
        "q1",
        "q2"
    }

    assert datos["alfabeto"] == {
        "0",
        "1"
    }

    assert datos[
        "estado_inicial"
    ] == "q0"

    assert datos[
        "estados_finales"
    ] == {"q2"}