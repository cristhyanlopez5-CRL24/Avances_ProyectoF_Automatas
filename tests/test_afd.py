from modelos.afd import AFD
from algoritmos.simulador import (
    simular_afd_detallado,
    formatear_resultado_afd
)


def crear_afd_prueba():
    """
    Crea un AFD que acepta cadenas binarias
    que terminan en 01.
    """

    afd = AFD(
        nombre="Termina en 01",
        estados={"q0", "q1", "q2"},
        alfabeto={"0", "1"},
        estado_inicial="q0",
        estados_finales={"q2"}
    )

    # q0
    afd.agregar_transicion("q0", "0", "q1")
    afd.agregar_transicion("q0", "1", "q0")

    # q1
    afd.agregar_transicion("q1", "0", "q1")
    afd.agregar_transicion("q1", "1", "q2")

    # q2
    afd.agregar_transicion("q2", "0", "q1")
    afd.agregar_transicion("q2", "1", "q0")

    return afd


def test_cadenas_aceptadas():

    afd = crear_afd_prueba()

    assert afd.simular("01") is True
    assert afd.simular("101") is True
    assert afd.simular("0001") is True
    assert afd.simular("1101") is True


def test_cadenas_rechazadas():

    afd = crear_afd_prueba()

    assert afd.simular("10") is False
    assert afd.simular("111") is False
    assert afd.simular("00") is False
    assert afd.simular("") is False


def test_afd_completo():

    afd = crear_afd_prueba()

    assert afd.es_completo() is True

    assert afd.obtener_transiciones_faltantes() == []


def test_simulacion_detallada():

    afd = crear_afd_prueba()

    resultado = simular_afd_detallado(
        afd,
        "101"
    )

    assert resultado["aceptada"] is True

    assert resultado["estado_inicial"] == "q0"

    assert resultado["estado_final"] == "q2"

    assert len(resultado["pasos"]) == 3


def test_cadena_con_simbolo_invalido():

    afd = crear_afd_prueba()

    try:

        afd.simular("102")

        assert False

    except ValueError:

        assert True


def test_resultado_formateado():

    afd = crear_afd_prueba()

    resultado = simular_afd_detallado(
        afd,
        "101"
    )

    texto = formatear_resultado_afd(
        resultado
    )

    assert "CADENA ACEPTADA" in texto
    assert "q0 --1--> q0" in texto
    assert "q1 --1--> q2" in texto