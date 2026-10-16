from algoritmos.procesador_regex import (
    insertar_concatenacion_explicita,
    convertir_a_postfija,
    procesar_expresion_regular
)


def test_concatenacion_simple():

    resultado = (
        insertar_concatenacion_explicita(
            "ab"
        )
    )

    assert resultado == "a·b"


def test_concatenacion_antes_parentesis():

    resultado = (
        insertar_concatenacion_explicita(
            "a(b|c)"
        )
    )

    assert resultado == "a·(b|c)"


def test_concatenacion_despues_parentesis():

    resultado = (
        insertar_concatenacion_explicita(
            "(a|b)c"
        )
    )

    assert resultado == "(a|b)·c"


def test_concatenacion_despues_estrella():

    resultado = (
        insertar_concatenacion_explicita(
            "(a|b)*c"
        )
    )

    assert resultado == "(a|b)*·c"


def test_union_no_agrega_concatenacion():

    resultado = (
        insertar_concatenacion_explicita(
            "a|b"
        )
    )

    assert resultado == "a|b"


def test_concatenacion_con_epsilon():

    resultado = (
        insertar_concatenacion_explicita(
            "aε"
        )
    )

    assert resultado == "a·ε"


def test_postfija_union():

    resultado = (
        convertir_a_postfija(
            "a|b"
        )
    )

    assert resultado == "ab|"


def test_postfija_concatenacion():

    resultado = (
        convertir_a_postfija(
            "ab"
        )
    )

    assert resultado == "ab·"


def test_postfija_precedencia():

    resultado = (
        convertir_a_postfija(
            "a|bc"
        )
    )

    assert resultado == "abc·|"


def test_postfija_con_parentesis():

    resultado = (
        convertir_a_postfija(
            "a(b|c)"
        )
    )

    assert resultado == "abc|·"


def test_postfija_regex_completa():

    resultado = (
        convertir_a_postfija(
            "(0|1)*01"
        )
    )

    assert resultado == (
        "01|*0·1·"
    )


def test_postfija_mas_y_opcional():

    resultado = (
        convertir_a_postfija(
            "a+b?"
        )
    )

    assert resultado == "a+b?·"


def test_procesar_expresion_regular():

    resultado = (
        procesar_expresion_regular(
            " ( a | b ) * c "
        )
    )

    assert resultado[
        "normalizada"
    ] == "(a|b)*c"

    assert resultado[
        "explicita"
    ] == "(a|b)*·c"

    assert resultado[
        "postfija"
    ] == "ab|*c·"