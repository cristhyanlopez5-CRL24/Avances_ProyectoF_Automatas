from abc import ABC, abstractmethod


class Automata(ABC):
    """
    Clase base para representar un autómata finito.

    Esta clase contiene los elementos comunes de un AFD y un AFN:
    - Estados
    - Alfabeto
    - Estado inicial
    - Estados finales
    - Transiciones
    """

    EPSILON = "ε"

    def __init__(self, nombre, estados, alfabeto, estado_inicial, estados_finales):
        self.nombre = nombre

        self.estados = set(estados)
        self.alfabeto = set(alfabeto)

        self.estado_inicial = estado_inicial
        self.estados_finales = set(estados_finales)

        # Estructura:
        # (estado, simbolo) -> conjunto de estados destino
        self.transiciones = {}

        self._validar_automata()

    def _validar_automata(self):
        """
        Comprueba que la información básica del autómata sea válida.
        """

        if not self.nombre.strip():
            raise ValueError("El autómata debe tener un nombre.")

        if not self.estados:
            raise ValueError("El autómata debe tener al menos un estado.")

        if not self.alfabeto:
            raise ValueError("El alfabeto no puede estar vacío.")

        if self.EPSILON in self.alfabeto:
            raise ValueError(
                "El símbolo ε no debe incluirse dentro del alfabeto."
            )

        if self.estado_inicial not in self.estados:
            raise ValueError(
                f"El estado inicial '{self.estado_inicial}' no existe."
            )

        if not self.estados_finales.issubset(self.estados):
            raise ValueError(
                "Todos los estados finales deben pertenecer al conjunto de estados."
            )

    def existe_estado(self, estado):
        """
        Indica si un estado pertenece al autómata.
        """
        return estado in self.estados

    def existe_simbolo(self, simbolo):
        """
        Indica si un símbolo pertenece al alfabeto.
        """
        return simbolo in self.alfabeto

    def agregar_estado(self, estado):
        """
        Agrega un nuevo estado al autómata.
        """

        if not estado:
            raise ValueError("El nombre del estado no puede estar vacío.")

        if estado in self.estados:
            raise ValueError(
                f"El estado '{estado}' ya existe."
            )

        self.estados.add(estado)

    def agregar_simbolo(self, simbolo):
        """
        Agrega un símbolo al alfabeto.
        """

        if not simbolo:
            raise ValueError("El símbolo no puede estar vacío.")

        if simbolo == self.EPSILON:
            raise ValueError(
                "ε no debe agregarse al alfabeto."
            )

        if simbolo in self.alfabeto:
            raise ValueError(
                f"El símbolo '{simbolo}' ya existe."
            )

        self.alfabeto.add(simbolo)

    def cambiar_estado_inicial(self, estado):
        """
        Cambia el estado inicial del autómata.
        """

        if estado not in self.estados:
            raise ValueError(
                f"El estado '{estado}' no existe."
            )

        self.estado_inicial = estado

    def agregar_estado_final(self, estado):
        """
        Convierte un estado existente en estado final.
        """

        if estado not in self.estados:
            raise ValueError(
                f"El estado '{estado}' no existe."
            )

        self.estados_finales.add(estado)

    def quitar_estado_final(self, estado):
        """
        Quita un estado del conjunto de estados finales.
        """

        if estado not in self.estados_finales:
            raise ValueError(
                f"El estado '{estado}' no es un estado final."
            )

        self.estados_finales.remove(estado)

    def obtener_transiciones(self, estado, simbolo):
        """
        Devuelve los estados destino correspondientes
        a una transición.

        Si no existe la transición, devuelve un conjunto vacío.
        """

        return self.transiciones.get(
            (estado, simbolo),
            set()
        )

    @abstractmethod
    def agregar_transicion(self, origen, simbolo, destino):
        """
        Cada tipo de autómata implementará sus propias reglas
        para agregar transiciones.

        AFD:
            un solo destino por símbolo.

        AFN:
            puede tener varios destinos y transiciones ε.
        """
        pass

    @abstractmethod
    def simular(self, cadena):
        """
        Cada autómata deberá implementar su propio
        algoritmo para simular cadenas.
        """
        pass

    def __str__(self):
        """
        Devuelve información básica del autómata.
        """

        return (
            f"Nombre: {self.nombre}\n"
            f"Estados: {sorted(self.estados)}\n"
            f"Alfabeto: {sorted(self.alfabeto)}\n"
            f"Estado inicial: {self.estado_inicial}\n"
            f"Estados finales: {sorted(self.estados_finales)}"
        )