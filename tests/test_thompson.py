from modelos.afn import AFN

from algoritmos.thompson import (
    construir_afn_thompson
)


def test_thompson_simbolo_simple():

    afn = construir_afn_thompson(
        "a"
    )

    assert isinstance(
        afn,
        AFN
    )

    assert len(
        afn.estados
    ) == 2

    assert afn.simular(
        "a"
    ) is True

    assert afn.simular(
        ""
    ) is False


def test_thompson_union():

    afn = construir_afn_thompson(
        "a|b"
    )

    assert afn.simular(
        "a"
    ) is True

    assert afn.simular(
        "b"
    ) is True

    assert afn.simular(
        "ab"
    ) is False


def test_thompson_concatenacion():

    afn = construir_afn_thompson(
        "ab"
    )

    assert afn.simular(
        "ab"
    ) is True

    assert afn.simular(
        "a"
    ) is False

    assert afn.simular(
        "b"
    ) is False


def test_thompson_estrella():

    afn = construir_afn_thompson(
        "a*"
    )

    assert afn.simular(
        ""
    ) is True

    assert afn.simular(
        "a"
    ) is True

    assert afn.simular(
        "aaaa"
    ) is True


def test_thompson_operador_mas():

    afn = construir_afn_thompson(
        "a+"
    )

    assert afn.simular(
        ""
    ) is False

    assert afn.simular(
        "a"
    ) is True

    assert afn.simular(
        "aaaa"
    ) is True


def test_thompson_opcional():

    afn = construir_afn_thompson(
        "a?"
    )

    assert afn.simular(
        ""
    ) is True

    assert afn.simular(
        "a"
    ) is True

    assert afn.simular(
        "aa"
    ) is False


def test_thompson_regex_completa():

    afn = construir_afn_thompson(
        "(0|1)*01"
    )

    assert afn.simular(
        "01"
    ) is True

    assert afn.simular(
        "101"
    ) is True

    assert afn.simular(
        "1101"
    ) is True

    assert afn.simular(
        ""
    ) is False

    assert afn.simular(
        "0"
    ) is False

    assert afn.simular(
        "10"
    ) is False


def test_thompson_con_epsilon():

    afn = construir_afn_thompson(
        "a|ε"
    )

    assert afn.simular(
        ""
    ) is True

    assert afn.simular(
        "a"
    ) is True


def test_thompson_genera_transiciones_epsilon():

    afn = construir_afn_thompson(
        "a|b"
    )

    assert (
        afn.tiene_transiciones_epsilon()
        is True
    )


def test_thompson_guarda_informacion():

    afn = construir_afn_thompson(
        "(a|b)*c",
        nombre="Regex de prueba"
    )

    assert afn.nombre == (
        "Regex de prueba"
    )

    assert afn.expresion_regular == (
        "(a|b)*c"
    )

    assert afn.expresion_postfija == (
        "ab|*c·"
    )

    assert afn.metodo_generacion == (
        "Construcción de Thompson"
    )