from modelos.afn import AFN

from algoritmos.conversion import (
    convertir_afn_a_afd,
    obtener_tabla_conversion,
    formatear_conversion
)


def crear_afn_conversion():
    """
    AFN:

    q0 --ε--> q1
    q1 --ε--> q2

    q2 --0--> q2
    q2 --1--> q3

    q3 es final.

    Acepta:
    1
    01
    001
    0001
    ...
    """

    afn = AFN(
        nombre="AFN para conversión",
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


def test_conversion_crea_afd():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    assert afd is not None

    assert afd.es_completo() is True


def test_estado_inicial_conversion():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    assert (
        afd.estado_inicial
        == "{q0,q1,q2}"
    )


def test_estados_generados():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    assert "{q0,q1,q2}" in afd.estados

    assert "{q2}" in afd.estados

    assert "{q3}" in afd.estados

    assert "∅" in afd.estados


def test_estado_final_conversion():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    assert "{q3}" in afd.estados_finales


def test_equivalencia_cadenas():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    cadenas = [
        "",
        "0",
        "1",
        "00",
        "01",
        "001",
        "0001",
        "10",
        "11",
        "101",
        "111"
    ]

    for cadena in cadenas:

        resultado_afn = afn.simular(
            cadena
        )

        resultado_afd = afd.simular(
            cadena
        )

        assert (
            resultado_afn
            == resultado_afd
        )


def test_transiciones_conversion():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    assert (
        afd.obtener_destino(
            "{q0,q1,q2}",
            "0"
        )
        == "{q2}"
    )

    assert (
        afd.obtener_destino(
            "{q0,q1,q2}",
            "1"
        )
        == "{q3}"
    )

    assert (
        afd.obtener_destino(
            "{q3}",
            "0"
        )
        == "∅"
    )


def test_estado_vacio():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    assert (
        afd.obtener_destino(
            "∅",
            "0"
        )
        == "∅"
    )

    assert (
        afd.obtener_destino(
            "∅",
            "1"
        )
        == "∅"
    )


def test_tabla_conversion():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    tabla = obtener_tabla_conversion(
        afd
    )

    assert len(tabla) == 4


def test_formato_conversion():

    afn = crear_afn_conversion()

    afd = convertir_afn_a_afd(
        afn
    )

    texto = formatear_conversion(
        afd
    )

    assert "AFN para conversión" in texto

    assert "{q0,q1,q2}" in texto

    assert "{q3}" in texto

    assert "∅" in texto