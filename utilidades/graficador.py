import os

from graphviz import Digraph


FORMATOS_PERMITIDOS = {
    "png",
    "svg",
    "pdf"
}

ORIENTACIONES_PERMITIDAS = {
    "LR",
    "RL",
    "TB",
    "BT"
}


def _agrupar_transiciones(automata):
    """
    Agrupa símbolos cuando varias transiciones
    tienen el mismo estado de origen y destino.
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
    titulo=None,
    etiquetas_estados=None,
    rankdir="LR"
):
    """
    Construye un objeto Digraph de Graphviz.

    etiquetas_estados permite mostrar alias
    como A, B, C sin modificar los nombres
    reales del autómata.
    """

    if automata is None:

        raise ValueError(
            "Debe proporcionar un autómata."
        )

    if titulo is None:

        titulo = automata.nombre

    if etiquetas_estados is None:

        etiquetas_estados = {}

    rankdir = str(
        rankdir
    ).upper()

    if rankdir not in ORIENTACIONES_PERMITIDAS:

        rankdir = "LR"

    grafo = Digraph(
        name="Automata"
    )

    grafo.attr(
        rankdir=rankdir,
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

    # Nodo invisible que marca el inicio
    nodo_inicio = "__inicio_automata__"

    grafo.node(
        nodo_inicio,
        label="",
        shape="point",
        width="0"
    )

    # Estados
    for estado in sorted(
        automata.estados
    ):

        etiqueta = etiquetas_estados.get(
            estado,
            estado
        )

        if estado in automata.estados_finales:

            grafo.node(
                estado,
                label=etiqueta,
                shape="doublecircle"
            )

        else:

            grafo.node(
                estado,
                label=etiqueta,
                shape="circle"
            )

    # Flecha hacia estado inicial
    grafo.edge(
        nodo_inicio,
        automata.estado_inicial
    )

    # Transiciones
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
    abrir=False,
    etiquetas_estados=None,
    rankdir="LR"
):
    """
    Genera físicamente el diagrama.
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

    extension = f".{formato}"

    if ruta_salida.lower().endswith(
        extension
    ):

        ruta_salida = ruta_salida[
            :-len(extension)
        ]

    carpeta = os.path.dirname(
        ruta_salida
    )

    if carpeta:

        os.makedirs(
            carpeta,
            exist_ok=True
        )

    grafo = construir_grafo(
        automata,
        etiquetas_estados=etiquetas_estados,
        rankdir=rankdir
    )

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
    """

    grafo = construir_grafo(
        automata
    )

    return grafo.source