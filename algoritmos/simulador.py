from algoritmos.epsilon import (
    epsilon_cerradura,
    mover
)


# =========================================================
# SIMULACIÓN DETALLADA DE AFD
# =========================================================

def simular_afd_detallado(afd, cadena):
    """
    Simula una cadena en un AFD y devuelve información
    detallada de cada transición realizada.
    """

    afd.validar_cadena(cadena)

    estado_actual = afd.estado_inicial
    pasos = []

    for numero_paso, simbolo in enumerate(cadena, start=1):

        origen = estado_actual

        destino = afd.obtener_destino(
            origen,
            simbolo
        )

        if destino is None:

            return {
                "cadena": cadena,
                "aceptada": False,
                "estado_inicial": afd.estado_inicial,
                "estado_final": origen,
                "pasos": pasos,
                "mensaje": (
                    f"No existe transición desde "
                    f"'{origen}' con el símbolo '{simbolo}'."
                )
            }

        pasos.append({
            "paso": numero_paso,
            "origen": origen,
            "simbolo": simbolo,
            "destino": destino
        })

        estado_actual = destino

    aceptada = estado_actual in afd.estados_finales

    if aceptada:
        mensaje = "Cadena aceptada."
    else:
        mensaje = "Cadena rechazada."

    return {
        "cadena": cadena,
        "aceptada": aceptada,
        "estado_inicial": afd.estado_inicial,
        "estado_final": estado_actual,
        "pasos": pasos,
        "mensaje": mensaje
    }


def formatear_resultado_afd(resultado):
    """
    Convierte el resultado detallado de un AFD
    en texto fácil de leer.
    """

    lineas = []

    cadena = resultado["cadena"]

    if cadena == "":
        cadena_mostrada = "ε"
    else:
        cadena_mostrada = cadena

    lineas.append(
        f"Cadena: {cadena_mostrada}"
    )

    lineas.append(
        f"Estado inicial: {resultado['estado_inicial']}"
    )

    lineas.append("")

    if resultado["pasos"]:

        for paso in resultado["pasos"]:

            lineas.append(
                f"Paso {paso['paso']}: "
                f"{paso['origen']} "
                f"--{paso['simbolo']}--> "
                f"{paso['destino']}"
            )

    else:
        lineas.append(
            "No se consumieron símbolos."
        )

    lineas.append("")

    lineas.append(
        f"Estado final alcanzado: "
        f"{resultado['estado_final']}"
    )

    lineas.append("")

    if resultado["aceptada"]:
        lineas.append("CADENA ACEPTADA")
    else:
        lineas.append("CADENA RECHAZADA")

    lineas.append(
        f"Resultado: {resultado['mensaje']}"
    )

    return "\n".join(lineas)


# =========================================================
# FUNCIONES AUXILIARES PARA AFN
# =========================================================

def formatear_conjunto(estados):
    """
    Convierte un conjunto de estados a un formato
    fácil de leer.

    Ejemplo:
        {'q0', 'q1'} -> {q0, q1}
    """

    if not estados:
        return "∅"

    estados_ordenados = sorted(estados)

    return "{" + ", ".join(estados_ordenados) + "}"


# =========================================================
# SIMULACIÓN DETALLADA DE AFN
# =========================================================

def simular_afn_detallado(afn, cadena):
    """
    Simula una cadena en un AFN considerando:
    - múltiples estados posibles;
    - transiciones ε;
    - ε-cerradura.

    Devuelve toda la información necesaria
    para mostrar posteriormente el proceso
    en consola o en la interfaz gráfica.
    """

    afn.validar_cadena(cadena)

    # -----------------------------------------------------
    # 1. Estado inicial
    # -----------------------------------------------------

    estado_inicial = afn.estado_inicial

    # -----------------------------------------------------
    # 2. ε-cerradura inicial
    # -----------------------------------------------------

    cerradura_inicial = epsilon_cerradura(
        afn,
        {estado_inicial}
    )

    estados_actuales = set(
        cerradura_inicial
    )

    pasos = []

    # -----------------------------------------------------
    # 3. Procesar cada símbolo
    # -----------------------------------------------------

    for numero_paso, simbolo in enumerate(
        cadena,
        start=1
    ):

        estados_antes = set(
            estados_actuales
        )

        # Primero consumimos el símbolo
        movimiento = mover(
            afn,
            estados_actuales,
            simbolo
        )

        # Después calculamos nuevamente
        # la ε-cerradura
        cerradura_despues = epsilon_cerradura(
            afn,
            movimiento
        )

        pasos.append({
            "paso": numero_paso,
            "simbolo": simbolo,
            "estados_antes": estados_antes,
            "movimiento": set(movimiento),
            "estados_despues": set(cerradura_despues)
        })

        estados_actuales = set(
            cerradura_despues
        )

        # Si no quedan caminos posibles,
        # no es necesario continuar.
        if not estados_actuales:
            break

    # -----------------------------------------------------
    # 4. Comprobar aceptación
    # -----------------------------------------------------

    estados_finales_alcanzados = (
        estados_actuales
        & afn.estados_finales
    )

    aceptada = bool(
        estados_finales_alcanzados
    )

    if aceptada:

        mensaje = (
            "La cadena es aceptada porque al menos "
            "uno de los estados alcanzados es final."
        )

    elif not estados_actuales:

        mensaje = (
            "La cadena es rechazada porque "
            "no quedan caminos posibles."
        )

    else:

        mensaje = (
            "La cadena es rechazada porque ninguno "
            "de los estados alcanzados es final."
        )

    # -----------------------------------------------------
    # 5. Resultado completo
    # -----------------------------------------------------

    return {
        "cadena": cadena,
        "aceptada": aceptada,
        "estado_inicial": estado_inicial,
        "cerradura_inicial": cerradura_inicial,
        "pasos": pasos,
        "estados_finales_posibles": estados_actuales,
        "estados_finales_alcanzados":
            estados_finales_alcanzados,
        "mensaje": mensaje
    }


def formatear_resultado_afn(resultado):
    """
    Convierte el resultado de una simulación AFN
    a un texto fácil de mostrar.
    """

    lineas = []

    cadena = resultado["cadena"]

    if cadena == "":
        cadena_mostrada = "ε"
    else:
        cadena_mostrada = cadena

    # -----------------------------------------------------
    # Información inicial
    # -----------------------------------------------------

    lineas.append(
        f"Cadena: {cadena_mostrada}"
    )

    lineas.append(
        f"Estado inicial: "
        f"{resultado['estado_inicial']}"
    )

    lineas.append("")

    lineas.append(
        "ε-cerradura inicial:"
    )

    lineas.append(
        formatear_conjunto(
            resultado["cerradura_inicial"]
        )
    )

    # -----------------------------------------------------
    # Mostrar cada paso
    # -----------------------------------------------------

    for paso in resultado["pasos"]:

        lineas.append("")

        lineas.append(
            f"Paso {paso['paso']}"
        )

        lineas.append(
            f"Símbolo leído: "
            f"{paso['simbolo']}"
        )

        lineas.append(
            "Estados antes: "
            + formatear_conjunto(
                paso["estados_antes"]
            )
        )

        lineas.append(
            "Movimiento: "
            + formatear_conjunto(
                paso["movimiento"]
            )
        )

        lineas.append(
            "Después de ε-cerradura: "
            + formatear_conjunto(
                paso["estados_despues"]
            )
        )

    # -----------------------------------------------------
    # Resultado
    # -----------------------------------------------------

    lineas.append("")

    lineas.append(
        "Estados posibles al finalizar:"
    )

    lineas.append(
        formatear_conjunto(
            resultado["estados_finales_posibles"]
        )
    )

    if resultado["estados_finales_alcanzados"]:

        lineas.append("")

        lineas.append(
            "Estados finales alcanzados:"
        )

        lineas.append(
            formatear_conjunto(
                resultado[
                    "estados_finales_alcanzados"
                ]
            )
        )

    lineas.append("")

    if resultado["aceptada"]:

        lineas.append(
            "CADENA ACEPTADA"
        )

    else:

        lineas.append(
            "CADENA RECHAZADA"
        )

    lineas.append("")

    lineas.append(
        f"Resultado: {resultado['mensaje']}"
    )

    return "\n".join(lineas)