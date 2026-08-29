def limpiar_texto(texto):
    """
    Elimina espacios innecesarios al inicio
    y al final de un texto.
    """

    if texto is None:
        return ""

    return str(texto).strip()


def separar_elementos(texto):
    """
    Convierte un texto separado por comas
    en una lista limpia.

    Ejemplo:

        "q0, q1, q2"

    devuelve:

        ["q0", "q1", "q2"]
    """

    texto = limpiar_texto(texto)

    if not texto:
        return []

    elementos = texto.split(",")

    resultado = []

    for elemento in elementos:

        elemento = elemento.strip()

        if elemento:
            resultado.append(elemento)

    return resultado


def validar_nombre_automata(nombre):
    """
    Comprueba que el autómata tenga nombre.
    """

    nombre = limpiar_texto(nombre)

    if not nombre:
        raise ValueError(
            "Debe ingresar un nombre para el autómata."
        )

    return nombre


def validar_estados(texto_estados):
    """
    Valida y convierte los estados ingresados
    por el usuario.

    Ejemplo:

        q0,q1,q2

    devuelve:

        {"q0", "q1", "q2"}
    """

    estados_lista = separar_elementos(
        texto_estados
    )

    if not estados_lista:
        raise ValueError(
            "Debe ingresar al menos un estado."
        )

    # Detectar estados repetidos antes
    # de convertir a conjunto.
    if len(estados_lista) != len(
        set(estados_lista)
    ):
        raise ValueError(
            "No se permiten estados repetidos."
        )

    for estado in estados_lista:

        if " " in estado:
            raise ValueError(
                f"El estado '{estado}' contiene espacios."
            )

        if estado == "ε":
            raise ValueError(
                "ε no puede utilizarse como nombre de estado."
            )

        if estado == "∅":
            raise ValueError(
                "∅ está reservado para uso interno del programa."
            )

    return set(estados_lista)


def validar_alfabeto(texto_alfabeto):
    """
    Valida el alfabeto ingresado.

    Para esta primera versión cada símbolo
    debe ser de un solo carácter.

    Ejemplo:

        0,1

    devuelve:

        {"0", "1"}
    """

    simbolos = separar_elementos(
        texto_alfabeto
    )

    if not simbolos:
        raise ValueError(
            "Debe ingresar al menos un símbolo en el alfabeto."
        )

    if len(simbolos) != len(
        set(simbolos)
    ):
        raise ValueError(
            "No se permiten símbolos repetidos en el alfabeto."
        )

    for simbolo in simbolos:

        if simbolo == "ε":
            raise ValueError(
                "ε no debe incluirse dentro del alfabeto."
            )

        if simbolo == "∅":
            raise ValueError(
                "∅ no puede utilizarse como símbolo del alfabeto."
            )

        if len(simbolo) != 1:
            raise ValueError(
                f"El símbolo '{simbolo}' debe contener "
                f"un solo carácter."
            )

    return set(simbolos)


def validar_estado_inicial(
    estado_inicial,
    estados
):
    """
    Verifica que el estado inicial exista.
    """

    estado_inicial = limpiar_texto(
        estado_inicial
    )

    if not estado_inicial:
        raise ValueError(
            "Debe seleccionar un estado inicial."
        )

    if estado_inicial not in estados:
        raise ValueError(
            f"El estado inicial '{estado_inicial}' "
            f"no pertenece al conjunto de estados."
        )

    return estado_inicial


def validar_estados_finales(
    texto_estados_finales,
    estados
):
    """
    Comprueba que todos los estados finales
    pertenezcan al autómata.
    """

    finales_lista = separar_elementos(
        texto_estados_finales
    )

    if len(finales_lista) != len(
        set(finales_lista)
    ):
        raise ValueError(
            "No se permiten estados finales repetidos."
        )

    finales = set(finales_lista)

    inexistentes = (
        finales - estados
    )

    if inexistentes:

        texto_inexistentes = ", ".join(
            sorted(inexistentes)
        )

        raise ValueError(
            "Los siguientes estados finales "
            f"no existen: {texto_inexistentes}."
        )

    return finales


def validar_tipo_automata(tipo):
    """
    Valida que el tipo sea AFD o AFN.
    """

    tipo = limpiar_texto(
        tipo
    ).upper()

    if tipo not in {
        "AFD",
        "AFN"
    }:
        raise ValueError(
            "El tipo de autómata debe ser AFD o AFN."
        )

    return tipo


def validar_transicion(
    origen,
    simbolo,
    destino,
    estados,
    alfabeto,
    tipo
):
    """
    Valida una transición antes de agregarla
    al autómata.

    Para AFN se permite ε.

    Para AFD no se permite ε.
    """

    origen = limpiar_texto(
        origen
    )

    simbolo = limpiar_texto(
        simbolo
    )

    destino = limpiar_texto(
        destino
    )

    tipo = validar_tipo_automata(
        tipo
    )

    if not origen:
        raise ValueError(
            "Debe seleccionar un estado de origen."
        )

    if origen not in estados:
        raise ValueError(
            f"El estado de origen '{origen}' no existe."
        )

    if not destino:
        raise ValueError(
            "Debe seleccionar un estado de destino."
        )

    if destino not in estados:
        raise ValueError(
            f"El estado de destino '{destino}' no existe."
        )

    if not simbolo:
        raise ValueError(
            "Debe seleccionar un símbolo."
        )

    if simbolo == "ε":

        if tipo == "AFD":
            raise ValueError(
                "Un AFD no puede tener transiciones ε."
            )

    elif simbolo not in alfabeto:

        raise ValueError(
            f"El símbolo '{simbolo}' "
            f"no pertenece al alfabeto."
        )

    return {
        "origen": origen,
        "simbolo": simbolo,
        "destino": destino
    }


def validar_cadena(
    cadena,
    alfabeto
):
    """
    Comprueba que todos los símbolos de una cadena
    pertenezcan al alfabeto.

    La cadena vacía se permite porque representa ε.
    """

    if cadena is None:
        cadena = ""

    cadena = str(cadena)

    for simbolo in cadena:

        if simbolo not in alfabeto:

            raise ValueError(
                f"El símbolo '{simbolo}' "
                f"no pertenece al alfabeto."
            )

    return cadena


def validar_datos_automata(
    nombre,
    tipo,
    texto_estados,
    texto_alfabeto,
    estado_inicial,
    texto_estados_finales
):
    """
    Valida de una sola vez la información
    principal ingresada por el usuario.

    Devuelve los datos ya preparados para
    crear un objeto AFD o AFN.
    """

    nombre = validar_nombre_automata(
        nombre
    )

    tipo = validar_tipo_automata(
        tipo
    )

    estados = validar_estados(
        texto_estados
    )

    alfabeto = validar_alfabeto(
        texto_alfabeto
    )

    estado_inicial = validar_estado_inicial(
        estado_inicial,
        estados
    )

    estados_finales = validar_estados_finales(
        texto_estados_finales,
        estados
    )

    return {
        "nombre": nombre,
        "tipo": tipo,
        "estados": estados,
        "alfabeto": alfabeto,
        "estado_inicial": estado_inicial,
        "estados_finales": estados_finales
    }