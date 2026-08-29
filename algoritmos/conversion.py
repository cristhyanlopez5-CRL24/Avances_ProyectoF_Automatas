from modelos.afd import AFD

from algoritmos.epsilon import (
    epsilon_cerradura,
    mover
)


def nombre_subconjunto(estados):
    """
    Convierte un conjunto de estados del AFN
    en el nombre de un estado del AFD.

    Ejemplos:

        {'q0', 'q1'} -> {q0,q1}

        set() -> ∅
    """

    if not estados:
        return "∅"

    estados_ordenados = sorted(estados)

    return (
        "{"
        + ",".join(estados_ordenados)
        + "}"
    )


def convertir_afn_a_afd(afn, nombre=None):
    """
    Convierte un AFN en un AFD equivalente utilizando
    el método de construcción de subconjuntos.

    También considera transiciones ε.

    Retorna un objeto de tipo AFD.
    """

    # -------------------------------------------------
    # 1. Nombre del nuevo AFD
    # -------------------------------------------------

    if nombre is None:
        nombre = f"AFD equivalente de {afn.nombre}"

    # -------------------------------------------------
    # 2. Estado inicial del AFD
    # -------------------------------------------------
    #
    # El primer estado del AFD es la ε-cerradura
    # del estado inicial del AFN.
    # -------------------------------------------------

    subconjunto_inicial = frozenset(
        epsilon_cerradura(
            afn,
            {afn.estado_inicial}
        )
    )

    # -------------------------------------------------
    # 3. Estructuras para construir el AFD
    # -------------------------------------------------

    subconjuntos_descubiertos = {
        subconjunto_inicial
    }

    pendientes = [
        subconjunto_inicial
    ]

    transiciones_afd = {}

    # -------------------------------------------------
    # 4. Construcción de subconjuntos
    # -------------------------------------------------

    while pendientes:

        subconjunto_actual = pendientes.pop(0)

        for simbolo in sorted(afn.alfabeto):

            # -----------------------------------------
            # Consumimos el símbolo
            # -----------------------------------------

            movimiento = mover(
                afn,
                subconjunto_actual,
                simbolo
            )

            # -----------------------------------------
            # Calculamos ε-cerradura del resultado
            # -----------------------------------------

            destino = frozenset(
                epsilon_cerradura(
                    afn,
                    movimiento
                )
            )

            # Guardamos la transición
            transiciones_afd[
                (
                    subconjunto_actual,
                    simbolo
                )
            ] = destino

            # -----------------------------------------
            # Si encontramos un nuevo subconjunto,
            # debemos procesarlo posteriormente.
            # -----------------------------------------

            if destino not in subconjuntos_descubiertos:

                subconjuntos_descubiertos.add(
                    destino
                )

                pendientes.append(
                    destino
                )

    # -------------------------------------------------
    # 5. Convertir subconjuntos en nombres
    # -------------------------------------------------

    mapa_nombres = {}

    for subconjunto in subconjuntos_descubiertos:

        mapa_nombres[subconjunto] = (
            nombre_subconjunto(
                subconjunto
            )
        )

    # -------------------------------------------------
    # 6. Estados del AFD
    # -------------------------------------------------

    estados_afd = {
        mapa_nombres[subconjunto]
        for subconjunto
        in subconjuntos_descubiertos
    }

    # -------------------------------------------------
    # 7. Estado inicial del AFD
    # -------------------------------------------------

    estado_inicial_afd = (
        mapa_nombres[
            subconjunto_inicial
        ]
    )

    # -------------------------------------------------
    # 8. Estados finales del AFD
    # -------------------------------------------------
    #
    # Un subconjunto es final si contiene al menos
    # un estado final del AFN.
    # -------------------------------------------------

    estados_finales_afd = set()

    for subconjunto in subconjuntos_descubiertos:

        if (
            set(subconjunto)
            & afn.estados_finales
        ):

            estados_finales_afd.add(
                mapa_nombres[
                    subconjunto
                ]
            )

    # -------------------------------------------------
    # 9. Crear el AFD
    # -------------------------------------------------

    afd = AFD(
        nombre=nombre,
        estados=estados_afd,
        alfabeto=set(afn.alfabeto),
        estado_inicial=estado_inicial_afd,
        estados_finales=estados_finales_afd
    )

    # -------------------------------------------------
    # 10. Agregar las transiciones
    # -------------------------------------------------

    for (
        subconjunto_origen,
        simbolo
    ), subconjunto_destino in transiciones_afd.items():

        origen = mapa_nombres[
            subconjunto_origen
        ]

        destino = mapa_nombres[
            subconjunto_destino
        ]

        afd.agregar_transicion(
            origen,
            simbolo,
            destino
        )

    # -------------------------------------------------
    # 11. Guardar información de la conversión
    # -------------------------------------------------
    #
    # Esto será útil posteriormente para la GUI.
    # Nos permitirá saber qué estados del AFN
    # representa cada estado del AFD.
    # -------------------------------------------------

    afd.subconjuntos_origen = {}

    for subconjunto, nombre_estado in mapa_nombres.items():

        afd.subconjuntos_origen[
            nombre_estado
        ] = set(subconjunto)

    afd.afn_origen = afn.nombre

    return afd


def obtener_tabla_conversion(afd):
    """
    Devuelve las transiciones del AFD generado
    en formato de tabla.

    Retorna una lista de diccionarios.
    """

    tabla = []

    for estado in sorted(afd.estados):

        fila = {
            "estado": estado
        }

        for simbolo in sorted(afd.alfabeto):

            destino = afd.obtener_destino(
                estado,
                simbolo
            )

            fila[simbolo] = destino

        tabla.append(fila)

    return tabla


def formatear_conversion(afd):
    """
    Genera un texto que explica el resultado
    de la conversión AFN -> AFD.
    """

    lineas = []

    lineas.append(
        f"AFN original: {afd.afn_origen}"
    )

    lineas.append(
        f"AFD generado: {afd.nombre}"
    )

    lineas.append("")

    lineas.append(
        f"Estado inicial: {afd.estado_inicial}"
    )

    lineas.append(
        "Estados finales: "
        + ", ".join(
            sorted(
                afd.estados_finales
            )
        )
    )

    lineas.append("")

    lineas.append(
        "Subconjuntos generados:"
    )

    for estado in sorted(
        afd.subconjuntos_origen
    ):

        conjunto = (
            afd.subconjuntos_origen[
                estado
            ]
        )

        if conjunto:

            contenido = (
                "{"
                + ", ".join(
                    sorted(conjunto)
                )
                + "}"
            )

        else:
            contenido = "∅"

        lineas.append(
            f"{estado} = {contenido}"
        )

    lineas.append("")

    lineas.append(
        "Transiciones del AFD:"
    )

    for transicion in (
        afd.mostrar_transiciones()
    ):

        lineas.append(
            transicion
        )

    return "\n".join(lineas)