from modelos.afd import AFD

from algoritmos.minimizacion import (
    minimizar_afd,
    obtener_estados_alcanzables,
    formatear_minimizacion
)


def crear_afd_redundante():
    """
    AFD con estados equivalentes.

    q1 y q2 tienen exactamente el mismo
    comportamiento y pueden fusionarse.

    q4 es inalcanzable.
    """

    afd = AFD(
        nombre="AFD redundante",
        estados={
            "q0",
            "q1",
            "q2",
            "q3",
            "q4"
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

    # q0
    afd.agregar_transicion(
        "q0",
        "0",
        "q1"
    )

    afd.agregar_transicion(
        "q0",
        "1",
        "q2"
    )

    # q1
    afd.agregar_transicion(
        "q1",
        "0",
        "q1"
    )

    afd.agregar_transicion(
        "q1",
        "1",
        "q3"
    )

    # q2
    afd.agregar_transicion(
        "q2",
        "0",
        "q1"
    )

    afd.agregar_transicion(
        "q2",
        "1",
        "q3"
    )

    # q3
    afd.agregar_transicion(
        "q3",
        "0",
        "q3"
    )

    afd.agregar_transicion(
        "q3",
        "1",
        "q3"
    )

    # q4 es inalcanzable
    afd.agregar_transicion(
        "q4",
        "0",
        "q4"
    )

    afd.agregar_transicion(
        "q4",
        "1",
        "q4"
    )

    return afd


def test_estados_alcanzables():

    afd = crear_afd_redundante()

    alcanzables = (
        obtener_estados_alcanzables(
            afd
        )
    )

    assert alcanzables == {
        "q0",
        "q1",
        "q2",
        "q3"
    }


def test_elimina_inalcanzables():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    assert "q4" not in minimo.estados

    assert (
        "q4"
        in minimo.estados_inalcanzables
    )


def test_detecta_equivalentes():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    assert (
        "{q1,q2}"
        in minimo.estados
    )


def test_cantidad_estados():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    assert len(
        minimo.estados
    ) == 3


def test_estado_inicial():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    assert (
        minimo.estado_inicial
        == "q0"
    )


def test_estado_final():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    assert (
        minimo.estados_finales
        == {"q3"}
    )


def test_transiciones_minimas():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    assert (
        minimo.obtener_destino(
            "q0",
            "0"
        )
        == "{q1,q2}"
    )

    assert (
        minimo.obtener_destino(
            "q0",
            "1"
        )
        == "{q1,q2}"
    )

    assert (
        minimo.obtener_destino(
            "{q1,q2}",
            "1"
        )
        == "q3"
    )


def test_equivalencia_lenguaje():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    cadenas = [
        "",
        "0",
        "1",
        "00",
        "01",
        "10",
        "11",
        "000",
        "001",
        "010",
        "101",
        "111"
    ]

    for cadena in cadenas:

        assert (
            afd.simular(cadena)
            ==
            minimo.simular(cadena)
        )


def test_afd_minimo_completo():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    assert (
        minimo.es_completo()
        is True
    )


def test_formato_minimizacion():

    afd = crear_afd_redundante()

    minimo = minimizar_afd(
        afd
    )

    texto = formatear_minimizacion(
        minimo
    )

    assert "AFD redundante" in texto

    assert "{q1,q2}" in texto

    assert "q4" in texto