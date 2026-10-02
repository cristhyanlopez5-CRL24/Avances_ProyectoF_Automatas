from algoritmos.thompson import (
    construir_afn_thompson
)

from algoritmos.conversion import (
    convertir_afn_a_afd
)

from algoritmos.simulador import (
    simular_afn_detallado
)


def generar_afn_desde_regex(
    expresion,
    nombre=None
):
    """
    Genera un AFN-ε a partir de una
    expresión regular utilizando Thompson.
    """

    if nombre is None:
        nombre = (
            f"AFN de regex: {expresion}"
        )

    return construir_afn_thompson(
        expresion,
        nombre=nombre
    )


def generar_afd_desde_regex(
    expresion,
    nombre_afn=None,
    nombre_afd=None
):
    """
    Genera primero el AFN-ε mediante
    Thompson y posteriormente lo convierte
    a un AFD utilizando la construcción
    de subconjuntos de la Fase 1.
    """

    afn = generar_afn_desde_regex(
        expresion,
        nombre=nombre_afn
    )

    if nombre_afd is None:
        nombre_afd = (
            f"AFD de regex: {afn.expresion_regular}"
        )

    afd = convertir_afn_a_afd(
        afn,
        nombre=nombre_afd
    )

    # Guardamos información de origen
    # para utilizarla posteriormente
    # desde la interfaz gráfica.
    afd.expresion_regular = (
        afn.expresion_regular
    )

    afd.expresion_postfija = (
        afn.expresion_postfija
    )

    afd.metodo_generacion = (
        "Thompson + construcción de subconjuntos"
    )

    return afd


def validar_cadena_con_regex(
    expresion,
    cadena
):
    """
    Valida una cadena utilizando directamente
    una expresión regular.

    Internamente:
    1. Convierte la regex a AFN-ε.
    2. Simula la cadena en el AFN.
    3. Devuelve un resultado detallado.
    """

    afn = generar_afn_desde_regex(
        expresion
    )

    detalle = simular_afn_detallado(
        afn,
        cadena
    )

    return {
        "expresion": (
            afn.expresion_regular
        ),
        "postfija": (
            afn.expresion_postfija
        ),
        "cadena": cadena,
        "alfabeto": set(
            afn.alfabeto
        ),
        "aceptada": detalle[
            "aceptada"
        ],
        "mensaje": detalle[
            "mensaje"
        ],
        "automata": afn,
        "detalle": detalle
    }


def validar_varias_cadenas(
    expresion,
    cadenas
):
    """
    Valida varias cadenas utilizando
    el mismo AFN generado desde una regex.

    Esta función también será útil
    posteriormente para los logs.
    """

    afn = generar_afn_desde_regex(
        expresion
    )

    resultados = []

    for cadena in cadenas:

        detalle = (
            simular_afn_detallado(
                afn,
                cadena
            )
        )

        resultados.append({
            "cadena": cadena,
            "aceptada": detalle[
                "aceptada"
            ],
            "mensaje": detalle[
                "mensaje"
            ]
        })

    return {
        "expresion": (
            afn.expresion_regular
        ),
        "alfabeto": set(
            afn.alfabeto
        ),
        "automata": afn,
        "resultados": resultados
    }