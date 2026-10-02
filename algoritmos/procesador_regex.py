from utilidades.validador_regex import (
    validar_expresion_regular
)


OPERADORES_UNARIOS = {
    "*",
    "+",
    "?"
}

OPERADORES_BINARIOS = {
    "|",
    "·"
}

PRECEDENCIA = {
    "|": 1,
    "·": 2
}

EPSILON = "ε"


def _es_operando(simbolo):
    """
    Indica si un símbolo representa
    un elemento normal del alfabeto
    o epsilon.
    """

    if simbolo is None:
        return False

    return (
        simbolo not in {
            "|",
            "*",
            "+",
            "?",
            "(",
            ")",
            "·"
        }
    )


def _puede_terminar_termino(simbolo):
    """
    Determina si un símbolo puede estar
    a la izquierda de una concatenación.
    """

    if simbolo is None:
        return False

    return (
        _es_operando(simbolo)
        or simbolo == ")"
        or simbolo in OPERADORES_UNARIOS
    )


def _puede_iniciar_termino(simbolo):
    """
    Determina si un símbolo puede estar
    a la derecha de una concatenación.
    """

    if simbolo is None:
        return False

    return (
        _es_operando(simbolo)
        or simbolo == "("
    )


def insertar_concatenacion_explicita(
    expresion
):
    """
    Inserta el operador interno '·'
    donde exista concatenación implícita.

    Ejemplos:

    ab
    -> a·b

    a(b|c)
    -> a·(b|c)

    (a|b)*c
    -> (a|b)*·c
    """

    expresion = validar_expresion_regular(
        expresion
    )

    resultado = []

    for indice, simbolo in enumerate(
        expresion
    ):

        resultado.append(
            simbolo
        )

        if indice == len(expresion) - 1:
            continue

        actual = simbolo

        siguiente = expresion[
            indice + 1
        ]

        if (
            _puede_terminar_termino(
                actual
            )
            and _puede_iniciar_termino(
                siguiente
            )
        ):

            resultado.append(
                "·"
            )

    return "".join(
        resultado
    )


def convertir_a_postfija(
    expresion
):
    """
    Convierte una expresión regular válida
    a notación postfija.

    Se utiliza una variante del algoritmo
    Shunting Yard.

    Precedencia:

    * + ?   mayor precedencia
    ·       concatenación
    |       unión
    """

    expresion = (
        insertar_concatenacion_explicita(
            expresion
        )
    )

    salida = []

    pila = []

    for simbolo in expresion:

        # =====================================================
        # OPERANDO
        # =====================================================

        if _es_operando(
            simbolo
        ):

            salida.append(
                simbolo
            )

            continue

        # =====================================================
        # OPERADORES UNARIOS
        # =====================================================

        if simbolo in OPERADORES_UNARIOS:

            salida.append(
                simbolo
            )

            continue

        # =====================================================
        # PARÉNTESIS DE APERTURA
        # =====================================================

        if simbolo == "(":

            pila.append(
                simbolo
            )

            continue

        # =====================================================
        # PARÉNTESIS DE CIERRE
        # =====================================================

        if simbolo == ")":

            while (
                pila
                and pila[-1] != "("
            ):

                salida.append(
                    pila.pop()
                )

            if pila:

                pila.pop()

            continue

        # =====================================================
        # OPERADORES BINARIOS
        # =====================================================

        if simbolo in OPERADORES_BINARIOS:

            while (
                pila
                and pila[-1] != "("
                and (
                    PRECEDENCIA[
                        pila[-1]
                    ]
                    >= PRECEDENCIA[
                        simbolo
                    ]
                )
            ):

                salida.append(
                    pila.pop()
                )

            pila.append(
                simbolo
            )

    # =========================================================
    # VACIAR PILA
    # =========================================================

    while pila:

        salida.append(
            pila.pop()
        )

    return "".join(
        salida
    )


def procesar_expresion_regular(
    expresion
):
    """
    Procesa completamente la expresión
    y devuelve sus representaciones.

    Este resultado se utilizará después
    por el algoritmo de Thompson.
    """

    normalizada = (
        validar_expresion_regular(
            expresion
        )
    )

    explicita = (
        insertar_concatenacion_explicita(
            normalizada
        )
    )

    postfija = (
        convertir_a_postfija(
            normalizada
        )
    )

    return {
        "original": expresion,
        "normalizada": normalizada,
        "explicita": explicita,
        "postfija": postfija
    }