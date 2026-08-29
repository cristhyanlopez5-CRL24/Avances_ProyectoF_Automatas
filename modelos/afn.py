from modelos.automata import Automata


class AFN(Automata):
    """
    Representa un Autómata Finito No Determinista (AFN).

    En un AFN:
    - Un estado puede tener varios destinos
      para el mismo símbolo.
    - Puede haber transiciones epsilon (ε).
    - Puede haber combinaciones estado-símbolo
      sin transición.
    """

    def __init__(
        self,
        nombre,
        estados,
        alfabeto,
        estado_inicial,
        estados_finales
    ):
        super().__init__(
            nombre,
            estados,
            alfabeto,
            estado_inicial,
            estados_finales
        )

    def agregar_transicion(
        self,
        origen,
        simbolo,
        destino
    ):
        """
        Agrega una transición al AFN.
        """

        if origen not in self.estados:
            raise ValueError(
                f"El estado de origen '{origen}' no existe."
            )

        if destino not in self.estados:
            raise ValueError(
                f"El estado de destino '{destino}' no existe."
            )

        if (
            simbolo not in self.alfabeto
            and simbolo != self.EPSILON
        ):
            raise ValueError(
                f"El símbolo '{simbolo}' no pertenece "
                f"al alfabeto y tampoco es ε."
            )

        clave = (origen, simbolo)

        if clave not in self.transiciones:
            self.transiciones[clave] = set()

        self.transiciones[clave].add(destino)

    def eliminar_transicion(
        self,
        origen,
        simbolo,
        destino=None
    ):
        """
        Elimina una transición específica o todas
        las transiciones de una combinación
        estado-símbolo.
        """

        clave = (origen, simbolo)

        if clave not in self.transiciones:
            raise ValueError(
                f"No existen transiciones desde "
                f"'{origen}' con el símbolo '{simbolo}'."
            )

        if destino is None:
            del self.transiciones[clave]
            return

        if destino not in self.transiciones[clave]:
            raise ValueError(
                f"No existe la transición "
                f"{origen} --{simbolo}--> {destino}."
            )

        self.transiciones[clave].remove(destino)

        if not self.transiciones[clave]:
            del self.transiciones[clave]

    def obtener_destinos(
        self,
        estado,
        simbolo
    ):
        """
        Devuelve todos los destinos existentes
        desde un estado con determinado símbolo.
        """

        return self.obtener_transiciones(
            estado,
            simbolo
        ).copy()

    def tiene_transiciones_epsilon(self):
        """
        Indica si existe al menos una transición ε.
        """

        for estado, simbolo in self.transiciones:

            if simbolo == self.EPSILON:
                return True

        return False

    def obtener_transiciones_epsilon(self):
        """
        Devuelve todas las transiciones ε.
        """

        resultado = []

        for (
            origen,
            simbolo
        ), destinos in self.transiciones.items():

            if simbolo == self.EPSILON:

                for destino in destinos:

                    resultado.append(
                        (origen, destino)
                    )

        return resultado

    def validar_cadena(self, cadena):
        """
        Comprueba que todos los símbolos
        pertenezcan al alfabeto.
        """

        for simbolo in cadena:

            if simbolo not in self.alfabeto:

                raise ValueError(
                    f"El símbolo '{simbolo}' de la cadena "
                    f"no pertenece al alfabeto."
                )

        return True

    def es_determinista(self):
        """
        Indica si el AFN cumple accidentalmente
        las reglas de un AFD.
        """

        for (
            estado,
            simbolo
        ), destinos in self.transiciones.items():

            if simbolo == self.EPSILON:
                return False

            if len(destinos) > 1:
                return False

        return True

    def mostrar_transiciones(self):
        """
        Devuelve las transiciones en formato legible.
        """

        resultado = []

        for (
            origen,
            simbolo
        ), destinos in sorted(
            self.transiciones.items()
        ):

            destinos_ordenados = sorted(destinos)

            destinos_texto = ", ".join(
                destinos_ordenados
            )

            resultado.append(
                f"δ({origen}, {simbolo}) = "
                f"{{{destinos_texto}}}"
            )

        return resultado

    def simular(self, cadena):
        """
        Simula una cadena considerando:
        - múltiples estados posibles;
        - transiciones ε.

        Devuelve:
            True  -> cadena aceptada
            False -> cadena rechazada
        """

        from algoritmos.epsilon import (
            epsilon_cerradura,
            mover
        )

        self.validar_cadena(cadena)

        # Antes de leer cualquier símbolo debemos
        # considerar todos los estados alcanzables
        # mediante ε.
        estados_actuales = epsilon_cerradura(
            self,
            {self.estado_inicial}
        )

        # Procesamos la cadena símbolo por símbolo.
        for simbolo in cadena:

            nuevos_estados = mover(
                self,
                estados_actuales,
                simbolo
            )

            estados_actuales = epsilon_cerradura(
                self,
                nuevos_estados
            )

            # Si ya no existe ningún camino posible,
            # podemos rechazar inmediatamente.
            if not estados_actuales:
                return False

        # La cadena es aceptada si al menos uno de
        # los estados posibles es un estado final.
        return bool(
            estados_actuales
            & self.estados_finales
        )

    def simular_con_recorrido(self, cadena):
        """
        Simula una cadena y conserva los conjuntos
        de estados alcanzados en cada paso.
        """

        from algoritmos.epsilon import (
            epsilon_cerradura,
            mover
        )

        self.validar_cadena(cadena)

        estados_actuales = epsilon_cerradura(
            self,
            {self.estado_inicial}
        )

        recorrido = []

        recorrido.append({
            "paso": 0,
            "simbolo": "ε",
            "estados": set(estados_actuales)
        })

        for numero_paso, simbolo in enumerate(
            cadena,
            start=1
        ):

            estados_antes = set(
                estados_actuales
            )

            alcanzados = mover(
                self,
                estados_actuales,
                simbolo
            )

            estados_actuales = epsilon_cerradura(
                self,
                alcanzados
            )

            recorrido.append({
                "paso": numero_paso,
                "simbolo": simbolo,
                "estados_antes": estados_antes,
                "estados": set(estados_actuales)
            })

            if not estados_actuales:
                return False, recorrido

        aceptada = bool(
            estados_actuales
            & self.estados_finales
        )

        return aceptada, recorrido