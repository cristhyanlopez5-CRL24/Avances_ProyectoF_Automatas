import os

from graphviz import Digraph


FORMATOS_PERMITIDOS = {
    "png",
    "svg",
    "pdf"
}


def _agrupar_transiciones(automata):
    """
    Agrupa símbolos cuando varias transiciones
    tienen el mismo estado de origen y destino.

    Ejemplo:

        q0 --0--> q1
        q0 --1--> q1

    se dibujará como:

        q0 --0, 1--> q1

    También funciona con AFN y transiciones ε.
    """

    agrupadas = {}

    for (
        origen,
        simbolo
    ), destinos in automata.transiciones.items():

        for destino in destinos:

            clave = (
                origen,
                destino
            )

            if clave not in agrupadas:
                agrupadas[clave] = []

            agrupadas[clave].append(
                simbolo
            )

    return agrupadas


def construir_grafo(
    automata,
    titulo=None
):
    """
    Construye un objeto Digraph de Graphviz
    a partir de un AFD o AFN.

    No genera todavía ningún archivo.
    """

    if automata is None:
        raise ValueError(
            "Debe proporcionar un autómata."
        )

    if titulo is None:
        titulo = automata.nombre

    grafo = Digraph(
        name="Automata"
    )

    # -------------------------------------------------
    # CONFIGURACIÓN GENERAL
    # -------------------------------------------------

    grafo.attr(
        rankdir="LR",
        label=titulo,
        labelloc="t",
        fontsize="18",
        fontname="Segoe UI Symbol",
        nodesep="0.6",
        ranksep="0.8"
    )

    grafo.attr(
        "node",
        shape="circle",
        fontsize="11",
        fontname="Segoe UI Symbol",
        margin="0.08"
    )

    grafo.attr(
        "edge",
        fontsize="10",
        fontname="Segoe UI Symbol"
    )

    # -------------------------------------------------
    # NODO ESPECIAL DE INICIO
    # -------------------------------------------------
    #
    # Este nodo solamente sirve para mostrar
    # la flecha que apunta al estado inicial.
    # -------------------------------------------------

    nodo_inicio = "__inicio_automata__"

    grafo.node(
        nodo_inicio,
        label="",
        shape="point",
        width="0"
    )

    # -------------------------------------------------
    # ESTADOS
    # -------------------------------------------------

    for estado in sorted(
        automata.estados
    ):

        if estado in automata.estados_finales:

            grafo.node(
                estado,
                label=estado,
                shape="doublecircle"
            )

        else:

            grafo.node(
                estado,
                label=estado,
                shape="circle"
            )

    # -------------------------------------------------
    # FLECHA AL ESTADO INICIAL
    # -------------------------------------------------

    grafo.edge(
        nodo_inicio,
        automata.estado_inicial
    )

    # -------------------------------------------------
    # TRANSICIONES
    # -------------------------------------------------

    transiciones_agrupadas = (
        _agrupar_transiciones(
            automata
        )
    )

    for (
        origen,
        destino
    ), simbolos in sorted(
        transiciones_agrupadas.items()
    ):

        simbolos_ordenados = sorted(
            simbolos
        )

        etiqueta = ", ".join(
            simbolos_ordenados
        )

        grafo.edge(
            origen,
            destino,
            label=etiqueta
        )

    return grafo


def generar_diagrama(
    automata,
    ruta_salida,
    formato="png",
    abrir=False
):
    """
    Genera físicamente el diagrama del autómata.

    Ejemplo:

        generar_diagrama(
            afd,
            "recursos/diagramas/afd_ejemplo"
        )

    producirá:

        recursos/diagramas/afd_ejemplo.png
    """

    formato = formato.lower()

    if formato not in FORMATOS_PERMITIDOS:

        raise ValueError(
            "Formato no permitido. "
            "Utilice png, svg o pdf."
        )

    if not ruta_salida:

        raise ValueError(
            "Debe proporcionar una ruta de salida."
        )

    # -------------------------------------------------
    # EVITAR EXTENSIONES DUPLICADAS
    # -------------------------------------------------

    extension = f".{formato}"

    if ruta_salida.lower().endswith(
        extension
    ):
        ruta_salida = ruta_salida[
            :-len(extension)
        ]

    # -------------------------------------------------
    # CREAR CARPETA SI NO EXISTE
    # -------------------------------------------------

    carpeta = os.path.dirname(
        ruta_salida
    )

    if carpeta:

        os.makedirs(
            carpeta,
            exist_ok=True
        )

    # -------------------------------------------------
    # CONSTRUIR GRAFO
    # -------------------------------------------------

    grafo = construir_grafo(
        automata
    )

    # -------------------------------------------------
    # RENDERIZAR
    # -------------------------------------------------

    ruta_generada = grafo.render(
        filename=ruta_salida,
        format=formato,
        cleanup=True,
        view=abrir
    )

    return ruta_generada


def obtener_codigo_dot(
    automata
):
    """
    Devuelve el código DOT generado por Graphviz.

    Resulta útil para pruebas y depuración.
    """

    grafo = construir_grafo(
        automata
    )

    return grafo.source