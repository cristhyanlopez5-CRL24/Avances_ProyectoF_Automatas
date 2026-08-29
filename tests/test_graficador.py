import os

import pytest

from modelos.afd import AFD
from modelos.afn import AFN

from utilidades.graficador import (
    construir_grafo,
    generar_diagrama,
    obtener_codigo_dot
)


def crear_afd_grafico():

    afd = AFD(
        nombre="AFD gráfico",
        estados={
            "q0",
            "q1",
            "q2"
        },
        alfabeto={
            "0",
            "1"
        },
        estado_inicial="q0",
        estados_finales={
            "q2"
        }
    )

    afd.agregar_transicion(
        "q0",
        "0",
        "q1"
    )

    afd.agregar_transicion(
        "q0",
        "1",
        "q0"
    )

    afd.agregar_transicion(
        "q1",
        "0",
        "q1"
    )

    afd.agregar_transicion(
        "q1",
        "1",
        "q2"
    )

    afd.agregar_transicion(
        "q2",
        "0",
        "q1"
    )

    afd.agregar_transicion(
        "q2",
        "1",
        "q0"
    )

    return afd


def crear_afn_grafico():

    afn = AFN(
        nombre="AFN gráfico",
        estados={
            "q0",
            "q1",
            "q2"
        },
        alfabeto={
            "0",
            "1"
        },
        estado_inicial="q0",
        estados_finales={
            "q2"
        }
    )

    afn.agregar_transicion(
        "q0",
        "ε",
        "q1"
    )

    afn.agregar_transicion(
        "q0",
        "0",
        "q0"
    )

    afn.agregar_transicion(
        "q0",
        "0",
        "q1"
    )

    afn.agregar_transicion(
        "q1",
        "1",
        "q2"
    )

    return afn


def test_construir_grafo_afd():

    afd = crear_afd_grafico()

    grafo = construir_grafo(
        afd
    )

    assert grafo is not None


def test_codigo_dot_contiene_estados():

    afd = crear_afd_grafico()

    codigo = obtener_codigo_dot(
        afd
    )

    assert "q0" in codigo
    assert "q1" in codigo
    assert "q2" in codigo


def test_codigo_dot_estado_final():

    afd = crear_afd_grafico()

    codigo = obtener_codigo_dot(
        afd
    )

    assert "doublecircle" in codigo


def test_codigo_dot_estado_inicial():

    afd = crear_afd_grafico()

    codigo = obtener_codigo_dot(
        afd
    )

    assert "__inicio_automata__" in codigo


def test_grafo_afn():

    afn = crear_afn_grafico()

    codigo = obtener_codigo_dot(
        afn
    )

    assert "ε" in codigo


def test_grafo_afn_varios_destinos():

    afn = crear_afn_grafico()

    codigo = obtener_codigo_dot(
        afn
    )

    assert "q0" in codigo
    assert "q1" in codigo


def test_formato_invalido():

    afd = crear_afd_grafico()

    with pytest.raises(ValueError):

        generar_diagrama(
            afd,
            "recursos/diagramas/prueba",
            formato="jpg"
        )


def test_generar_png(tmp_path):

    afd = crear_afd_grafico()

    ruta_base = str(
        tmp_path / "afd_prueba"
    )

    ruta_generada = generar_diagrama(
        afd,
        ruta_base,
        formato="png"
    )

    assert os.path.exists(
        ruta_generada
    )

    assert ruta_generada.endswith(
        ".png"
    )