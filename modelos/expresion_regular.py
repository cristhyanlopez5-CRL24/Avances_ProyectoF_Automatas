class ExpresionRegular:
    """
    Representa una expresión regular dentro del sistema.

    En esta primera versión solamente almacena:
    - Nombre
    - Expresión original
    - Alfabeto detectado

    La validación sintáctica y la conversión a autómata
    se implementarán en pasos posteriores.
    """

    OPERADORES = {
        "|",
        "*",
        "+",
        "?",
        "(",
        ")"
    }

    EPSILON = "ε"

    def __init__(
        self,
        nombre,
        expresion
    ):
        self.nombre = nombre.strip()
        self.expresion = expresion.strip()

        self._validar_datos_basicos()

        self.alfabeto = (
            self._obtener_alfabeto()
        )

    def _validar_datos_basicos(self):
        """
        Comprueba únicamente los datos mínimos
        necesarios para crear una expresión regular.
        """

        if not self.nombre:

            raise ValueError(
                "La expresión regular debe tener un nombre."
            )

        if not self.expresion:

            raise ValueError(
                "La expresión regular no puede estar vacía."
            )

    def _obtener_alfabeto(self):
        """
        Obtiene los símbolos utilizados por la expresión
        ignorando operadores, paréntesis y epsilon.

        Ejemplo:

        (0|1)*01
        -> {"0", "1"}
        """

        alfabeto = set()

        for simbolo in self.expresion:

            if simbolo.isspace():

                continue

            if simbolo in self.OPERADORES:

                continue

            if simbolo == self.EPSILON:

                continue

            alfabeto.add(
                simbolo
            )

        return alfabeto

    def obtener_alfabeto(self):
        """
        Devuelve una copia del alfabeto detectado.
        """

        return set(
            self.alfabeto
        )

    def __str__(self):
        """
        Devuelve información básica de la expresión.
        """

        return (
            f"Nombre: {self.nombre}\n"
            f"Expresión: {self.expresion}\n"
            f"Alfabeto: {sorted(self.alfabeto)}"
        )