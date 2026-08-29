import json
import os

from modelos.afd import AFD
from modelos.afn import AFN


def automata_a_diccionario(
    automata,
    tipo
):
    """
    Convierte un AFD o AFN en un diccionario
    que posteriormente puede guardarse como JSON.
    """

    if automata is None:
        raise ValueError(
            "No existe ningún autómata para guardar."
        )

    tipo = str(tipo).upper()

    if tipo not in {"AFD", "AFN"}:
        raise ValueError(
            "El tipo de autómata debe ser AFD o AFN."
        )

    transiciones = []

    for (
        origen,
        simbolo
    ), destinos in sorted(
        automata.transiciones.items()
    ):

        transiciones.append({
            "origen": origen,
            "simbolo": simbolo,
            "destinos": sorted(destinos)
        })

    return {
        "version": 1,
        "tipo": tipo,
        "nombre": automata.nombre,
        "estados": sorted(
            automata.estados
        ),
        "alfabeto": sorted(
            automata.alfabeto
        ),
        "estado_inicial":
            automata.estado_inicial,
        "estados_finales": sorted(
            automata.estados_finales
        ),
        "transiciones": transiciones
    }


def guardar_automata(
    automata,
    tipo,
    ruta
):
    """
    Guarda un autómata en un archivo JSON.
    """

    if not ruta:
        raise ValueError(
            "Debe proporcionar una ruta de guardado."
        )

    # Agregar extensión automáticamente
    if not ruta.lower().endswith(
        ".json"
    ):
        ruta += ".json"

    carpeta = os.path.dirname(
        ruta
    )

    if carpeta:

        os.makedirs(
            carpeta,
            exist_ok=True
        )

    datos = automata_a_diccionario(
        automata,
        tipo
    )

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    return ruta


def validar_datos_archivo(datos):
    """
    Comprueba que el archivo tenga la
    estructura mínima necesaria.
    """

    if not isinstance(
        datos,
        dict
    ):
        raise ValueError(
            "El archivo no contiene un autómata válido."
        )

    campos = {
        "tipo",
        "nombre",
        "estados",
        "alfabeto",
        "estado_inicial",
        "estados_finales",
        "transiciones"
    }

    faltantes = (
        campos - set(datos.keys())
    )

    if faltantes:

        raise ValueError(
            "El archivo está incompleto. "
            "Faltan los campos: "
            + ", ".join(
                sorted(faltantes)
            )
        )

    tipo = str(
        datos["tipo"]
    ).upper()

    if tipo not in {
        "AFD",
        "AFN"
    }:
        raise ValueError(
            "El archivo contiene un tipo "
            "de autómata desconocido."
        )

    if not isinstance(
        datos["transiciones"],
        list
    ):
        raise ValueError(
            "Las transiciones del archivo "
            "no tienen un formato válido."
        )

    return tipo


def cargar_automata(ruta):
    """
    Carga un AFD o AFN desde un archivo JSON.

    Retorna:

        automata, tipo
    """

    if not ruta:
        raise ValueError(
            "Debe proporcionar un archivo."
        )

    if not os.path.exists(
        ruta
    ):
        raise ValueError(
            "El archivo seleccionado no existe."
        )

    try:

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(
                archivo
            )

    except json.JSONDecodeError:

        raise ValueError(
            "El archivo seleccionado no contiene "
            "un JSON válido."
        )

    tipo = validar_datos_archivo(
        datos
    )

    # =========================================
    # CREAR OBJETO
    # =========================================

    if tipo == "AFD":

        automata = AFD(
            nombre=datos["nombre"],
            estados=set(
                datos["estados"]
            ),
            alfabeto=set(
                datos["alfabeto"]
            ),
            estado_inicial=(
                datos["estado_inicial"]
            ),
            estados_finales=set(
                datos["estados_finales"]
            )
        )

    else:

        automata = AFN(
            nombre=datos["nombre"],
            estados=set(
                datos["estados"]
            ),
            alfabeto=set(
                datos["alfabeto"]
            ),
            estado_inicial=(
                datos["estado_inicial"]
            ),
            estados_finales=set(
                datos["estados_finales"]
            )
        )

    # =========================================
    # RESTAURAR TRANSICIONES
    # =========================================

    for transicion in (
        datos["transiciones"]
    ):

        if not isinstance(
            transicion,
            dict
        ):

            raise ValueError(
                "Existe una transición "
                "con formato inválido."
            )

        if not {
            "origen",
            "simbolo",
            "destinos"
        }.issubset(
            transicion.keys()
        ):

            raise ValueError(
                "Existe una transición incompleta."
            )

        origen = transicion[
            "origen"
        ]

        simbolo = transicion[
            "simbolo"
        ]

        destinos = transicion[
            "destinos"
        ]

        if not isinstance(
            destinos,
            list
        ):

            raise ValueError(
                "Los destinos de una transición "
                "deben estar almacenados como lista."
            )

        # Un AFD solamente puede tener
        # un destino por transición.
        if (
            tipo == "AFD"
            and len(destinos) > 1
        ):

            raise ValueError(
                "El archivo intenta cargar un AFD "
                "con múltiples destinos."
            )

        for destino in destinos:

            automata.agregar_transicion(
                origen,
                simbolo,
                destino
            )

    return automata, tipo