def epsilon_cerradura(afn, estados):
    """
    Calcula la ε-cerradura de uno o varios estados.

    La ε-cerradura contiene:
    - Los estados originales.
    - Todos los estados alcanzables utilizando
      únicamente transiciones ε.

    Ejemplo:

        q0 --ε--> q1
        q1 --ε--> q2

    Entonces:

        ε-cerradura(q0) = {q0, q1, q2}
    """

    # Si recibimos un único estado como texto,
    # lo convertimos en conjunto.
    if isinstance(estados, str):
        estados = {estados}
    else:
        estados = set(estados)

    # Validamos que todos los estados existan.
    for estado in estados:
        if estado not in afn.estados:
            raise ValueError(
                f"El estado '{estado}' no existe en el AFN."
            )

    # Inicialmente la cerradura contiene
    # los propios estados recibidos.
    cerradura = set(estados)

    # Usaremos una pila para recorrer
    # todas las transiciones ε posibles.
    pendientes = list(estados)

    while pendientes:

        estado_actual = pendientes.pop()

        destinos_epsilon = afn.obtener_destinos(
            estado_actual,
            afn.EPSILON
        )

        for destino in destinos_epsilon:

            # Si todavía no habíamos visitado
            # este estado, lo agregamos.
            if destino not in cerradura:

                cerradura.add(destino)

                pendientes.append(destino)

    return cerradura


def mover(afn, estados, simbolo):
    """
    Obtiene todos los estados alcanzables desde
    un conjunto de estados consumiendo un símbolo.

    NO sigue transiciones ε automáticamente.

    Ejemplo:

        estados = {q0, q1}
        símbolo = 0

        δ(q0, 0) = {q2}
        δ(q1, 0) = {q3, q4}

    Resultado:

        {q2, q3, q4}
    """

    if isinstance(estados, str):
        estados = {estados}
    else:
        estados = set(estados)

    if simbolo not in afn.alfabeto:
        raise ValueError(
            f"El símbolo '{simbolo}' no pertenece al alfabeto."
        )

    resultado = set()

    for estado in estados:

        if estado not in afn.estados:
            raise ValueError(
                f"El estado '{estado}' no existe en el AFN."
            )

        destinos = afn.obtener_destinos(
            estado,
            simbolo
        )

        resultado.update(destinos)

    return resultado


def mover_con_epsilon(afn, estados, simbolo):
    """
    Realiza un movimiento completo considerando ε.

    El procedimiento es:

    1. Calcular ε-cerradura de los estados actuales.
    2. Consumir el símbolo.
    3. Calcular nuevamente ε-cerradura.

    Esto será útil para la simulación del AFN.
    """

    cerradura_inicial = epsilon_cerradura(
        afn,
        estados
    )

    alcanzados = mover(
        afn,
        cerradura_inicial,
        simbolo
    )

    cerradura_final = epsilon_cerradura(
        afn,
        alcanzados
    )

    return cerradura_final