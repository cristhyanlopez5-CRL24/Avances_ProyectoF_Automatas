from modelos.afd import AFD


def obtener_estados_alcanzables(afd):
    """
    Devuelve todos los estados que pueden alcanzarse
    desde el estado inicial del AFD.
    """

    alcanzables = {afd.estado_inicial}
    pendientes = [afd.estado_inicial]

    while pendientes:

        estado_actual = pendientes.pop(0)

        for simbolo in afd.alfabeto:

            destino = afd.obtener_destino(
                estado_actual,
                simbolo
            )

            if (
                destino is not None
                and destino not in alcanzables
            ):
                alcanzables.add(destino)
                pendientes.append(destino)

    return alcanzables


def nombre_grupo(grupo):
    """
    Genera el nombre de un estado del AFD mínimo.

    Ejemplos:

        {'q0'} -> q0

        {'q1', 'q2'} -> {q1,q2}
    """

    estados = sorted(grupo)

    if len(estados) == 1:
        return estados[0]

    return (
        "{"
        + ",".join(estados)
        + "}"
    )


def minimizar_afd(afd, nombre=None):
    """
    Minimiza un AFD utilizando refinamiento
    de particiones.

    El algoritmo:

    1. Elimina estados inalcanzables.
    2. Completa el AFD si existen transiciones faltantes.
    3. Separa estados finales y no finales.
    4. Refina las particiones.
    5. Une estados equivalentes.
    6. Construye un nuevo AFD mínimo.
    """

    if nombre is None:
        nombre = f"AFD mínimo de {afd.nombre}"

    # =====================================================
    # 1. OBTENER ESTADOS ALCANZABLES
    # =====================================================

    alcanzables = obtener_estados_alcanzables(
        afd
    )

    inalcanzables = (
        afd.estados - alcanzables
    )

    estados_trabajo = set(
        alcanzables
    )

    # =====================================================
    # 2. COPIAR TRANSICIONES
    # =====================================================

    transiciones = {}

    necesita_trampa = False

    for estado in alcanzables:

        for simbolo in afd.alfabeto:

            destino = afd.obtener_destino(
                estado,
                simbolo
            )

            if destino is None:
                necesita_trampa = True
            else:
                transiciones[
                    (estado, simbolo)
                ] = destino

    # =====================================================
    # 3. CREAR ESTADO TRAMPA SI ES NECESARIO
    # =====================================================

    estado_trampa = "__TRAMPA__"

    if necesita_trampa:

        while estado_trampa in estados_trabajo:
            estado_trampa += "_"

        estados_trabajo.add(
            estado_trampa
        )

        for estado in list(estados_trabajo):

            for simbolo in afd.alfabeto:

                if (
                    estado,
                    simbolo
                ) not in transiciones:

                    transiciones[
                        (estado, simbolo)
                    ] = estado_trampa

        for simbolo in afd.alfabeto:

            transiciones[
                (estado_trampa, simbolo)
            ] = estado_trampa

    # =====================================================
    # 4. ESTADOS FINALES Y NO FINALES
    # =====================================================

    finales = (
        estados_trabajo
        & afd.estados_finales
    )

    no_finales = (
        estados_trabajo
        - finales
    )

    particiones = []

    if finales:
        particiones.append(
            set(finales)
        )

    if no_finales:
        particiones.append(
            set(no_finales)
        )

    # =====================================================
    # 5. REFINAMIENTO DE PARTICIONES
    # =====================================================

    cambio = True

    while cambio:

        cambio = False

        nuevas_particiones = []

        # Mapa:
        # estado -> número de partición
        indice_particion = {}

        for indice, grupo in enumerate(
            particiones
        ):

            for estado in grupo:

                indice_particion[
                    estado
                ] = indice

        for grupo in particiones:

            subgrupos = {}

            for estado in grupo:

                firma = []

                for simbolo in sorted(
                    afd.alfabeto
                ):

                    destino = transiciones[
                        (estado, simbolo)
                    ]

                    firma.append(
                        indice_particion[
                            destino
                        ]
                    )

                firma = tuple(firma)

                if firma not in subgrupos:
                    subgrupos[firma] = set()

                subgrupos[firma].add(
                    estado
                )

            nuevas_particiones.extend(
                subgrupos.values()
            )

            if len(subgrupos) > 1:
                cambio = True

        particiones = (
            nuevas_particiones
        )

    # =====================================================
    # 6. MAPEAR CADA ESTADO A SU GRUPO
    # =====================================================

    estado_a_grupo = {}

    for grupo in particiones:

        nombre_estado = nombre_grupo(
            grupo
        )

        for estado in grupo:

            estado_a_grupo[
                estado
            ] = nombre_estado

    # =====================================================
    # 7. ESTADOS DEL AFD MÍNIMO
    # =====================================================

    estados_minimos = {
        nombre_grupo(grupo)
        for grupo in particiones
    }

    # =====================================================
    # 8. ESTADO INICIAL
    # =====================================================

    estado_inicial_minimo = (
        estado_a_grupo[
            afd.estado_inicial
        ]
    )

    # =====================================================
    # 9. ESTADOS FINALES
    # =====================================================

    estados_finales_minimos = set()

    for grupo in particiones:

        if grupo & afd.estados_finales:

            estados_finales_minimos.add(
                nombre_grupo(
                    grupo
                )
            )

    # =====================================================
    # 10. CREAR AFD MÍNIMO
    # =====================================================

    afd_minimo = AFD(
        nombre=nombre,
        estados=estados_minimos,
        alfabeto=set(
            afd.alfabeto
        ),
        estado_inicial=estado_inicial_minimo,
        estados_finales=estados_finales_minimos
    )

    # =====================================================
    # 11. CREAR TRANSICIONES
    # =====================================================

    for grupo in particiones:

        representante = next(
            iter(grupo)
        )

        origen_minimo = nombre_grupo(
            grupo
        )

        for simbolo in sorted(
            afd.alfabeto
        ):

            destino_original = (
                transiciones[
                    (
                        representante,
                        simbolo
                    )
                ]
            )

            destino_minimo = (
                estado_a_grupo[
                    destino_original
                ]
            )

            afd_minimo.agregar_transicion(
                origen_minimo,
                simbolo,
                destino_minimo
            )

    # =====================================================
    # 12. INFORMACIÓN ADICIONAL
    # =====================================================

    afd_minimo.afd_origen = afd.nombre

    afd_minimo.estados_inalcanzables = set(
        inalcanzables
    )

    afd_minimo.estado_trampa_agregado = (
        estado_trampa
        if necesita_trampa
        else None
    )

    afd_minimo.grupos_equivalencia = {}

    for grupo in particiones:

        nombre_estado = nombre_grupo(
            grupo
        )

        afd_minimo.grupos_equivalencia[
            nombre_estado
        ] = set(grupo)

    return afd_minimo


def formatear_minimizacion(afd_minimo):
    """
    Devuelve un texto fácil de leer con la
    información obtenida durante la minimización.
    """

    lineas = []

    lineas.append(
        f"AFD original: {afd_minimo.afd_origen}"
    )

    lineas.append(
        f"AFD mínimo: {afd_minimo.nombre}"
    )

    lineas.append("")

    lineas.append(
        f"Estado inicial: "
        f"{afd_minimo.estado_inicial}"
    )

    lineas.append(
        "Estados finales: "
        + ", ".join(
            sorted(
                afd_minimo.estados_finales
            )
        )
    )

    lineas.append("")

    lineas.append(
        f"Cantidad de estados mínimos: "
        f"{len(afd_minimo.estados)}"
    )

    lineas.append("")

    lineas.append(
        "Grupos de equivalencia:"
    )

    for nombre_estado in sorted(
        afd_minimo.grupos_equivalencia
    ):

        grupo = (
            afd_minimo.grupos_equivalencia[
                nombre_estado
            ]
        )

        contenido = (
            "{"
            + ", ".join(
                sorted(grupo)
            )
            + "}"
        )

        lineas.append(
            f"{nombre_estado} = {contenido}"
        )

    if (
        afd_minimo.estados_inalcanzables
    ):

        lineas.append("")

        lineas.append(
            "Estados inalcanzables eliminados:"
        )

        lineas.append(
            "{"
            + ", ".join(
                sorted(
                    afd_minimo.estados_inalcanzables
                )
            )
            + "}"
        )

    lineas.append("")

    lineas.append(
        "Transiciones del AFD mínimo:"
    )

    for transicion in (
        afd_minimo.mostrar_transiciones()
    ):

        lineas.append(
            transicion
        )

    return "\n".join(lineas)