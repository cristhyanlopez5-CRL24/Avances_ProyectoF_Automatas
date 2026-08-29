import pytest

from modelos.afn import AFN

from algoritmos.epsilon import (
    epsilon_cerradura,
    mover,
    mover_con_epsilon
)

from algoritmos.simulador import (
    simular_afn_detallado,
    formatear_resultado_afn
)


def crear_afn_prueba():
    """
    AFN de prueba:

    q0 --ε--> q1
    q1 --ε--> q2
    q2 --0--> q2
    q2 --1--> q3

    q3 es final.

    Acepta cadenas formadas por cero o más 0
    seguidos de un 1.
    """

    afn = AFN(
        nombre="AFN con epsilon",
        estados={
            "q0",
            "q1",
            "q2",
            "q3"
        },
        alfabeto={
            "0",
            "1"
        },
        estado_inicial="q0",
        estados_finales={
            "q3"
        }
    )

    afn.agregar_transicion(
        "q0",
        "ε",
        "q1"
    )

    afn.agregar_transicion(
        "q1",
        "ε",
        "q2"
    )

    afn.agregar_transicion(
        "q2",
        "0",
        "q2"
    )

    afn.agregar_transicion(
        "q2",
        "1",
        "q3"
    )

    return afn


def test_epsilon_cerradura():

    afn = crear_afn_prueba()

    resultado = epsilon_cerradura(
        afn,
        "q0"
    )

    assert resultado == {
        "q0",
        "q1",
        "q2"
    }


def test_epsilon_cerradura_q1():

    afn = crear_afn_prueba()

    resultado = epsilon_cerradura(
        afn,
        "q1"
    )

    assert resultado == {
        "q1",
        "q2"
    }


def test_epsilon_cerradura_sin_epsilon():

    afn = crear_afn_prueba()

    resultado = epsilon_cerradura(
        afn,
        "q3"
    )

    assert resultado == {
        "q3"
    }


def test_mover():

    afn = crear_afn_prueba()

    resultado = mover(
        afn,
        {"q0", "q1", "q2"},
        "0"
    )

    assert resultado == {
        "q2"
    }


def test_mover_con_epsilon():

    afn = crear_afn_prueba()

    resultado = mover_con_epsilon(
        afn,
        {"q0"},
        "0"
    )

    assert resultado == {
        "q2"
    }


def test_cadena_uno():

    afn = crear_afn_prueba()

    assert afn.simular("1") is True


def test_cadena_ceros_y_uno():

    afn = crear_afn_prueba()

    assert afn.simular("01") is True
    assert afn.simular("001") is True
    assert afn.simular("00001") is True


def test_cadenas_rechazadas():

    afn = crear_afn_prueba()

    assert afn.simular("") is False
    assert afn.simular("0") is False
    assert afn.simular("00") is False
    assert afn.simular("10") is False
    assert afn.simular("11") is False


def test_simbolo_invalido():

    afn = crear_afn_prueba()

    with pytest.raises(ValueError):

        afn.simular("0021")


def test_recorrido():

    afn = crear_afn_prueba()

    aceptada, recorrido = (
        afn.simular_con_recorrido("001")
    )

    assert aceptada is True

    assert recorrido[0]["estados"] == {
        "q0",
        "q1",
        "q2"
    }

    assert recorrido[-1]["estados"] == {
        "q3"
    }


def test_tiene_epsilon():

    afn = crear_afn_prueba()

    assert (
        afn.tiene_transiciones_epsilon()
        is True
    )


def test_no_es_determinista():

    afn = crear_afn_prueba()

    assert afn.es_determinista() is False

def test_simulacion_detallada_afn():

    afn = crear_afn_prueba()

    resultado = simular_afn_detallado(
        afn,
        "001"
    )

    assert resultado["aceptada"] is True

    assert resultado["cerradura_inicial"] == {
        "q0",
        "q1",
        "q2"
    }

    assert len(
        resultado["pasos"]
    ) == 3

    assert resultado[
        "estados_finales_posibles"
    ] == {
        "q3"
    }

    assert resultado[
        "estados_finales_alcanzados"
    ] == {
        "q3"
    }


def test_simulacion_detallada_rechazada():

    afn = crear_afn_prueba()

    resultado = simular_afn_detallado(
        afn,
        "00"
    )

    assert resultado["aceptada"] is False

    assert resultado[
        "estados_finales_posibles"
    ] == {
        "q2"
    }


def test_formatear_afn():

    afn = crear_afn_prueba()

    resultado = simular_afn_detallado(
        afn,
        "001"
    )

    texto = formatear_resultado_afn(
        resultado
    )

    assert "CADENA ACEPTADA" in texto

    assert (
        "ε-cerradura inicial"
        in texto
    )

    assert (
        "{q0, q1, q2}"
        in texto
    )

    assert (
        "{q3}"
        in texto
    )