from modelos.automata import Automata


class AFD(Automata):
    """
    Representa un Autómata Finito Determinista (AFD).

    En un AFD:
    - No existen transiciones epsilon.
    - Para cada estado y símbolo solamente puede existir
      un estado destino.
    """

    def __init__(self, nombre, estados, alfabeto, estado_inicial, estados_finales):
        super().__init__(
            nombre,
            estados,
            alfabeto,
            estado_inicial,
            estados_finales
        )

    def agregar_transicion(self, origen, simbolo, destino):
        """
        Agrega una transición al AFD.

        Ejemplo:
            q0 --0--> q1
        """

        # Verificar estado de origen
        if origen not in self.estados:
            raise ValueError(
                f"El estado de origen '{origen}' no existe."
            )

        # Verificar estado de destino
        if destino not in self.estados:
            raise ValueError(
                f"El estado de destino '{destino}' no existe."
            )

        # En un AFD no se permiten transiciones epsilon
        if simbolo == self.EPSILON:
            raise ValueError(
                "Un AFD no puede tener transiciones ε."
            )

        # Verificar que el símbolo pertenezca al alfabeto
        if simbolo not in self.alfabeto:
            raise ValueError(
                f"El símbolo '{simbolo}' no pertenece al alfabeto."
            )

        clave = (origen, simbolo)

        # Un AFD solamente puede tener un destino
        # para cada combinación estado-símbolo
        if clave in self.transiciones:
            destino_actual = next(iter(self.transiciones[clave]))

            raise ValueError(
                f"Ya existe la transición "
                f"δ({origen}, {simbolo}) = {destino_actual}."
            )

        self.transiciones[clave] = {destino}

    def eliminar_transicion(self, origen, simbolo):
        """
        Elimina una transición existente.
        """

        clave = (origen, simbolo)

        if clave not in self.transiciones:
            raise ValueError(
                f"No existe una transición desde '{origen}' "
                f"con el símbolo '{simbolo}'."
            )

        del self.transiciones[clave]

    def obtener_destino(self, estado, simbolo):
        """
        Obtiene el único estado destino para una transición.

        Si la transición no existe devuelve None.
        """

        destinos = self.obtener_transiciones(
            estado,
            simbolo
        )

        if not destinos:
            return None

        return next(iter(destinos))

    def validar_cadena(self, cadena):
        """
        Comprueba que todos los símbolos de la cadena
        pertenezcan al alfabeto.
        """

        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                raise ValueError(
                    f"El símbolo '{simbolo}' de la cadena "
                    f"no pertenece al alfabeto."
                )

        return True

    def simular(self, cadena):
        """
        Simula una cadena en el AFD.

        Devuelve:
            True  -> cadena aceptada
            False -> cadena rechazada
        """

        self.validar_cadena(cadena)

        estado_actual = self.estado_inicial

        for simbolo in cadena:
            destino = self.obtener_destino(
                estado_actual,
                simbolo
            )

            # Si no existe transición, la cadena se rechaza
            if destino is None:
                return False

            estado_actual = destino

        # La cadena se acepta únicamente si terminamos
        # en un estado final
        return estado_actual in self.estados_finales

    def simular_con_recorrido(self, cadena):
        """
        Simula una cadena y también devuelve
        el recorrido realizado por el autómata.

        Ejemplo:

        q0 --1--> q1 --0--> q2
        """

        self.validar_cadena(cadena)

        estado_actual = self.estado_inicial

        recorrido = [estado_actual]

        for simbolo in cadena:
            destino = self.obtener_destino(
                estado_actual,
                simbolo
            )

            if destino is None:
                return False, recorrido

            recorrido.append(
                f"--{simbolo}--> {destino}"
            )

            estado_actual = destino

        aceptada = estado_actual in self.estados_finales

        return aceptada, recorrido

    def es_completo(self):
        """
        Comprueba si el AFD tiene una transición definida
        para cada estado y cada símbolo del alfabeto.
        """

        for estado in self.estados:
            for simbolo in self.alfabeto:
                if (estado, simbolo) not in self.transiciones:
                    return False

        return True

    def obtener_transiciones_faltantes(self):
        """
        Devuelve las transiciones que faltan para
        que el AFD sea completo.
        """

        faltantes = []

        for estado in sorted(self.estados):
            for simbolo in sorted(self.alfabeto):
                if (estado, simbolo) not in self.transiciones:
                    faltantes.append(
                        (estado, simbolo)
                    )

        return faltantes

    def mostrar_transiciones(self):
        """
        Devuelve las transiciones del AFD
        en un formato fácil de leer.
        """

        resultado = []

        for (origen, simbolo), destinos in sorted(
            self.transiciones.items()
        ):
            destino = next(iter(destinos))

            resultado.append(
                f"δ({origen}, {simbolo}) = {destino}"
            )

        return resultado