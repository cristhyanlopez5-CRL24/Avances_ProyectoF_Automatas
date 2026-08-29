import os

from modelos.afd import AFD
from modelos.afn import AFN

from utilidades.persistencia import (
    guardar_automata,
    cargar_automata
)


def crear_afd_prueba():

    afd = AFD(
        nombre="AFD guardado",
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
        "q0", "0", "q1"
    )

    afd.agregar_transicion(
        "q0", "1", "q0"
    )

    afd.agregar_transicion(
        "q1", "0", "q1"
    )

    afd.agregar_transicion(
        "q1", "1", "q2"
    )

    afd.agregar_transicion(
        "q2", "0", "q1"
    )

    afd.agregar_transicion(
        "q2", "1", "q0"
    )

    return afd


def crear_afn_prueba():

    afn = AFN(
        nombre="AFN guardado",
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
        "q0", "ε", "q1"
    )

    afn.agregar_transicion(
        "q1", "0", "q1"
    )

    afn.agregar_transicion(
        "q1", "1", "q2"
    )

    return afn


def test_guardar_afd(tmp_path):

    afd = crear_afd_prueba()

    ruta = str(
        tmp_path / "afd"
    )

    ruta_final = guardar_automata(
        afd,
        "AFD",
        ruta
    )

    assert os.path.exists(
        ruta_final
    )

    assert ruta_final.endswith(
        ".json"
    )


def test_cargar_afd(tmp_path):

    afd = crear_afd_prueba()

    ruta = guardar_automata(
        afd,
        "AFD",
        str(
            tmp_path / "afd.json"
        )
    )

    cargado, tipo = cargar_automata(
        ruta
    )

    assert tipo == "AFD"

    assert cargado.nombre == (
        "AFD guardado"
    )

    assert cargado.estados == {
        "q0",
        "q1",
        "q2"
    }

    assert cargado.estado_inicial == "q0"

    assert cargado.estados_finales == {
        "q2"
    }


def test_transiciones_afd(tmp_path):

    afd = crear_afd_prueba()

    ruta = guardar_automata(
        afd,
        "AFD",
        str(
            tmp_path / "afd.json"
        )
    )

    cargado, tipo = cargar_automata(
        ruta
    )

    assert (
        cargado.obtener_destino(
            "q0",
            "0"
        )
        == "q1"
    )

    assert (
        cargado.obtener_destino(
            "q1",
            "1"
        )
        == "q2"
    )


def test_equivalencia_afd(tmp_path):

    afd = crear_afd_prueba()

    ruta = guardar_automata(
        afd,
        "AFD",
        str(
            tmp_path / "afd.json"
        )
    )

    cargado, tipo = cargar_automata(
        ruta
    )

    cadenas = [
        "",
        "01",
        "101",
        "100",
        "111",
        "0001"
    ]

    for cadena in cadenas:

        assert (
            afd.simular(cadena)
            ==
            cargado.simular(cadena)
        )


def test_cargar_afn_epsilon(tmp_path):

    afn = crear_afn_prueba()

    ruta = guardar_automata(
        afn,
        "AFN",
        str(
            tmp_path / "afn.json"
        )
    )

    cargado, tipo = cargar_automata(
        ruta
    )

    assert tipo == "AFN"

    assert (
        cargado.obtener_destinos(
            "q0",
            "ε"
        )
        == {"q1"}
    )


def test_equivalencia_afn(tmp_path):

    afn = crear_afn_prueba()

    ruta = guardar_automata(
        afn,
        "AFN",
        str(
            tmp_path / "afn.json"
        )
    )

    cargado, tipo = cargar_automata(
        ruta
    )

    cadenas = [
        "",
        "1",
        "01",
        "001",
        "0",
        "11"
    ]

    for cadena in cadenas:

        assert (
            afn.simular(cadena)
            ==
            cargado.simular(cadena)
        )