from algoritmos.integracion_regex import (
    generar_afn_desde_regex,
    generar_afd_desde_regex
)

from algoritmos.simulador import (
    simular_afn_detallado,
    simular_afd_detallado
)

from algoritmos.minimizacion import (
    minimizar_afd
)


REGEX = "(0|1)*01"


def test_regex_genera_afn_funcional():

    afn = generar_afn_desde_regex(
        REGEX,
        nombre="AFN prueba integración"
    )

    aceptada = simular_afn_detallado(
        afn,
        "1101"
    )

    rechazada = simular_afn_detallado(
        afn,
        "1110"
    )

    assert aceptada["aceptada"] is True

    assert rechazada["aceptada"] is False


def test_regex_genera_afd_funcional():

    afd = generar_afd_desde_regex(
        REGEX,
        nombre_afd="AFD prueba integración"
    )

    aceptada = simular_afd_detallado(
        afd,
        "0001"
    )

    rechazada = simular_afd_detallado(
        afd,
        "1010"
    )

    assert aceptada["aceptada"] is True

    assert rechazada["aceptada"] is False


def test_afn_y_afd_aceptan_mismas_cadenas():

    afn = generar_afn_desde_regex(
        REGEX
    )

    afd = generar_afd_desde_regex(
        REGEX
    )

    cadenas = [
        "",
        "01",
        "101",
        "0001",
        "1111",
        "10",
        "1110"
    ]

    for cadena in cadenas:

        resultado_afn = simular_afn_detallado(
            afn,
            cadena
        )

        resultado_afd = simular_afd_detallado(
            afd,
            cadena
        )

        assert (
            resultado_afn["aceptada"]
            == resultado_afd["aceptada"]
        )


def test_minimizacion_conserva_lenguaje():

    afd = generar_afd_desde_regex(
        REGEX
    )

    afd_minimo = minimizar_afd(
        afd
    )

    cadenas = [
        "",
        "01",
        "101",
        "0001",
        "1111",
        "10",
        "1110"
    ]

    for cadena in cadenas:

        original = simular_afd_detallado(
            afd,
            cadena
        )

        minimo = simular_afd_detallado(
            afd_minimo,
            cadena
        )

        assert (
            original["aceptada"]
            == minimo["aceptada"]
        )